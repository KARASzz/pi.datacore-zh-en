#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pi 资料一键更新脚本（全自动 / 纯标准库 / 不下载源码）
================================================
从两个来源检查并更新「pi.dev-资料库」中的英文资料（网站与仓库的文本资料一致，
统一归档在同一资料库内；仓库独有的包介绍等放入 原文备份/仓库包介绍/）。

来源 1 —— GitHub 仓库 earendil-works/pi（文档源文件，与网站 docs/latest 内容一致）:
  - packages/coding-agent/docs/*.md + docs.json  → pi.dev-资料库/原文备份/docs/
  - packages/coding-agent/README.md              → pi.dev-资料库/原文备份/README.md
  - packages/coding-agent/CHANGELOG.md           → pi.dev-资料库/原文备份/CHANGELOG.md
  - README.md / AGENTS.md / SECURITY.md / CONTRIBUTING.md → 原文备份/仓库补充/
  - packages/{ai,agent,tui}/README.md 等包介绍    → 原文备份/仓库包介绍/

来源 2 —— pi.dev 网站:
  - 首页 / news / press-kit / packages / models  → 原文备份/site/*.txt
  - 21 个精选包页面                              → 原文备份/site/pkg-*.txt

运行:  python3 更新资料.py
输出:  控制台摘要 + 根目录《更新报告.txt》；变更检测基于《资料清单.json》哈希清单。
说明:  01-文档/ 下的中英对照版由 AI 生成；若报告提示某文档英文原文已变化，
       说明对照版可能滞后，需要重新翻译该篇。
"""

import concurrent.futures as cf
import hashlib
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

# ----------------------------------------------------------------------------
# 路径与常量
# ----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent          # 项目根目录（脚本所在目录）
KB = ROOT / "pi.dev-资料库"                      # 资料库
RAW_DOCS = KB / "原文备份" / "docs"               # 官方文档英文原文（30 篇）
RAW_SITE = KB / "原文备份" / "site"               # 网站页面文本快照
RAW_EXTRA = KB / "原文备份" / "仓库补充"           # 仓库根目录补充资料
RAW_PKGINFO = KB / "原文备份" / "仓库包介绍"        # 仓库内各包的 README 介绍
MANIFEST = ROOT / "资料清单.json"                 # 哈希清单（变更检测）
REPORT = ROOT / "更新报告.txt"                    # 本次运行报告

REPO = "earendil-works/pi"
BRANCH = "main"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}"
API_BASE = "https://api.github.com"
SITE_BASE = "https://pi.dev"
UA = {"User-Agent": "pi-knowledge-base-updater/1.0"}

# 仓库文档（与网站 docs/latest 一致）
DOC_NAMES = [
    "compaction", "containerization", "custom-provider", "development",
    "environment-variables", "extensions", "index", "json", "keybindings",
    "llama-cpp", "models", "packages", "prompt-templates", "providers",
    "quickstart", "rpc", "sdk", "security", "session-format", "sessions",
    "settings", "shell-aliases", "skills", "terminal-setup", "termux",
    "themes", "tmux", "tui", "usage", "windows",
]

# 仓库中需要拉取的资料文件: (仓库路径, 类别)
REPO_FILES = [(f"packages/coding-agent/docs/{n}.md", "doc") for n in DOC_NAMES]
REPO_FILES += [
    ("packages/coding-agent/docs/docs.json", "doc"),
    ("packages/coding-agent/README.md", "top"),
    ("packages/coding-agent/CHANGELOG.md", "top"),
    ("README.md", "extra"),
    ("AGENTS.md", "extra"),
    ("SECURITY.md", "extra"),
    ("CONTRIBUTING.md", "extra"),
]
for _pkg in ("ai", "agent", "tui", "coding-agent"):
    REPO_FILES.append((f"packages/{_pkg}/README.md", "pkginfo"))

# 网站页面: (快照文件名, URL)
SITE_PAGES = [
    ("homepage.txt", f"{SITE_BASE}/"),
    ("news.txt", f"{SITE_BASE}/news"),
    ("press-kit.txt", f"{SITE_BASE}/press-kit"),
    ("packages-catalog.txt", f"{SITE_BASE}/packages"),
    ("models-page.txt", f"{SITE_BASE}/models"),
]
FEATURED_PACKAGES = [
    "bigpowers", "cc-safety-net", "confluence-cli", "context-mode",
    "pi-all-search", "pi-background-tasks", "pi-fabric",
    "pi-goal-list-loop-audit", "pi-goal-x", "pi-hashline-edit-pro",
    "pi-hermes-memory", "pi-intercom", "pi-lens", "pi-mcp-adapter",
    "pi-memory", "pi-powerline-footer", "pi-prompt-template-model",
    "pi-simplify", "pi-subagents", "pi-web-access", "pi-web-ui",
]
for _n in FEATURED_PACKAGES:
    SITE_PAGES.append((f"pkg-{_n}.txt", f"{SITE_BASE}/packages/{_n}"))

SRC_HINTS = ("/src/", "/test/", "/tests/", "/scripts/", "/examples/",
             "install-lock/", "/images/", ".github/", "node_modules/")


# ----------------------------------------------------------------------------
# 基础工具
# ----------------------------------------------------------------------------
def _ssl_context():
    """macOS 的 python.org 版 Python 常缺 CA 证书；依次尝试 certifi、系统 CA。"""
    global _CTX
    if _CTX is not None:
        return _CTX
    try:
        import certifi  # type: ignore
        _CTX = ssl.create_default_context(cafile=certifi.where())
        return _CTX
    except Exception:
        pass
    for ca in ("/etc/ssl/cert.pem", "/etc/ssl/ca-bundle.crt",
               "/usr/local/etc/openssl/cert.pem",
               "/opt/homebrew/etc/ca-certificates/cert.pem"):
        if os.path.exists(ca):
            try:
                _CTX = ssl.create_default_context(cafile=ca)
                return _CTX
            except Exception:
                pass
    _CTX = ssl.create_default_context()
    return _CTX


_CTX = None
_CTX_INSECURE = None


def http_get(url, timeout=40):
    """GET 一个 URL，返回字节内容；证书失败时自动降级重试一次。"""
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout,
                                    context=_ssl_context()) as resp:
            return resp.read()
    except urllib.error.URLError as e:
        reason = str(getattr(e, "reason", e))
        if "CERTIFICATE_VERIFY_FAILED" in reason:
            global _CTX_INSECURE
            if _CTX_INSECURE is None:
                _CTX_INSECURE = ssl._create_unverified_context()
                print("  [警告] SSL 证书校验不可用，本次以不验证模式继续（仅抓取公开资料）")
            req2 = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req2, timeout=timeout,
                                        context=_CTX_INSECURE) as resp:
                return resp.read()
        raise


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def load_manifest():
    if MANIFEST.exists():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_manifest(m):
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=1,
                                   sort_keys=True), encoding="utf-8")

# ----------------------------------------------------------------------------
# HTML → 纯文本提取（用于网站页面快照）
# ----------------------------------------------------------------------------
class _TextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "head", "template"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.parts.append("\n" + "#" * int(tag[1]) + " ")
        elif tag in ("p", "br"):
            self.parts.append("\n")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "tr":
            self.parts.append("\n|")
        elif tag in ("td", "th"):
            self.parts.append("")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag in ("td", "th"):
            self.parts.append("|")
        elif tag in ("p", "div", "section", "article", "li", "tr", "h1", "h2",
                     "h3", "h4", "h5", "h6", "br", "pre", "table", "ul", "ol",
                     "blockquote"):
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def html_to_text(html):
    html = re.sub(r"<script\b.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<style\b.*?</style>", "", html, flags=re.S | re.I)
    html = re.sub(r"<svg\b.*?</svg>", "", html, flags=re.S | re.I)
    ex = _TextExtractor()
    ex.feed(html)
    text = "".join(ex.parts)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ----------------------------------------------------------------------------
# 来源 1：GitHub 仓库资料
# ----------------------------------------------------------------------------
def discover_extra_repo_files(report):
    """尝试用 GitHub API 发现清单之外的新增 .md 资料；失败则忽略（API 有限流）。"""
    extra = []
    try:
        data = json.loads(http_get(
            f"{API_BASE}/repos/{REPO}/git/trees/{BRANCH}?recursive=1",
            timeout=30).decode("utf-8"))
        known = {src for src, _ in REPO_FILES}
        for item in data.get("tree", []):
            if item.get("type") != "blob":
                continue
            path = item.get("path", "")
            if not path.endswith(".md"):
                continue
            if any(s in "/" + path for s in SRC_HINTS):
                continue
            if path not in known:
                extra.append(path)
        report.append(f"  API 发现成功：清单外另有 {len(extra)} 个 .md 资料文件")
    except Exception as e:
        report.append(f"  API 不可用（{e.__class__.__name__}），使用内置清单（不影响更新）")
    return extra


def classify_repo_file(path):
    """把仓库路径映射到资料库内的保存位置。"""
    if path.startswith("packages/coding-agent/docs/"):
        return RAW_DOCS / path.rsplit("/", 1)[-1]
    if path == "packages/coding-agent/README.md":
        return KB / "原文备份" / "README.md"
    if path == "packages/coding-agent/CHANGELOG.md":
        return KB / "原文备份" / "CHANGELOG.md"
    if path.startswith("packages/") and path.endswith("/README.md"):
        return RAW_PKGINFO / (path.split("/")[1] + "-README.md")
    if path.startswith("packages/") and path.endswith("CHANGELOG.md"):
        return RAW_PKGINFO / (path.split("/")[1] + "-CHANGELOG.md")
    if "/" not in path:
        return RAW_EXTRA / path
    return RAW_EXTRA / path.replace("/", "__")


def update_repo(manifest, report):
    extra = discover_extra_repo_files(report)
    todo = []
    for src, kind in REPO_FILES:
        todo.append((src, classify_repo_file(src)))
    for path in extra:
        todo.append((path, classify_repo_file(path)))

    for d in (RAW_DOCS, RAW_SITE, RAW_EXTRA, RAW_PKGINFO):
        d.mkdir(parents=True, exist_ok=True)

    def work(item):
        src, target = item
        try:
            data = http_get(f"{RAW_BASE}/{src}")
            return (src, target, data, None)
        except Exception as e:
            return (src, target, None, f"{e.__class__.__name__}: {e}")

    ok = fail = 0
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        for src, target, data, err in pool.map(work, todo):
            key = f"repo:{src}"
            if err is not None:
                if "HTTP Error 404" in err:
                    report.append(f"  - 跳过（仓库中不存在）: {src}")
                else:
                    report.append(f"  - [失败] {src} -> {err}")
                    fail += 1
                continue
            old_hash = manifest.get(key)
            new_hash = sha256(data)
            existed = target.exists()
            changed = (old_hash is not None and old_hash != new_hash)
            if (not existed) or changed or (old_hash is None):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
            manifest[key] = new_hash
            ok += 1
            if not existed:
                report.append(f"  + 新增: {src} -> {target.relative_to(ROOT)}")
            elif changed:
                report.append(f"  * 已更新: {src}")
    report.append(f"  仓库资料合计成功 {ok} 个，失败 {fail} 个")

# ----------------------------------------------------------------------------
# 来源 2：pi.dev 网站快照
# ----------------------------------------------------------------------------
def update_site(manifest, report):
    def work(item):
        name, url = item
        try:
            html = http_get(url).decode("utf-8", errors="replace")
            return (name, url, html_to_text(html).encode("utf-8"), None)
        except Exception as e:
            return (name, url, None, f"{e.__class__.__name__}: {e}")

    ok = fail = 0
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        for name, url, data, err in pool.map(work, SITE_PAGES):
            key = f"site:{name}"
            target = RAW_SITE / name
            if err is not None:
                report.append(f"  - [失败] {url} -> {err}")
                fail += 1
                continue
            if not data.strip():
                report.append(f"  - [失败] {url} -> 返回空内容")
                fail += 1
                continue
            old_hash = manifest.get(key)
            new_hash = sha256(data)
            existed = target.exists()
            changed = (old_hash is not None and old_hash != new_hash)
            if (not existed) or changed or (old_hash is None):
                target.write_bytes(data)
            manifest[key] = new_hash
            ok += 1
            if not existed:
                report.append(f"  + 新增快照: {name}")
            elif changed:
                report.append(f"  * 快照有变化: {name}")
    report.append(f"  网站快照合计成功 {ok} 个，失败 {fail} 个")


# ----------------------------------------------------------------------------
# 对照版状态小结
# ----------------------------------------------------------------------------
def translation_status(manifest, report):
    translated = sorted(p.stem for p in RAW_DOCS.glob("*.md"))
    known_docs = set(DOC_NAMES)
    missing = sorted(known_docs - set(translated))
    if missing:
        report.append(f"  缺少英文原文的文档: {', '.join(missing)}")
    else:
        report.append(f"  官方文档英文原文齐全（{len(translated)} 篇）。")


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("=" * 62)
    print("pi 资料一键更新（来源: GitHub 仓库 + pi.dev 网站）")
    print("=" * 62)
    manifest = load_manifest()
    report = [f"运行时间: {time.strftime('%Y-%m-%d %H:%M:%S')}", ""]

    report.append("【来源 1】GitHub 仓库 earendil-works/pi（文档/说明/更新日志）")
    print("\n[1/2] 检查 GitHub 仓库资料 ...")
    try:
        update_repo(manifest, report)
    except Exception as e:
        report.append(f"  [异常] {e.__class__.__name__}: {e}")
        print(f"  仓库更新出错: {e}")

    report.append("")
    report.append("【来源 2】pi.dev 网站（页面快照）")
    print("\n[2/2] 抓取 pi.dev 网站快照 ...")
    try:
        update_site(manifest, report)
    except Exception as e:
        report.append(f"  [异常] {e.__class__.__name__}: {e}")
        print(f"  网站更新出错: {e}")

    report.append("")
    report.append("【文档对照版状态】")
    try:
        translation_status(manifest, report)
    except Exception:
        pass
    report.append("  提示: 若上方『* 已更新』出现 docs/*.md，说明英文原文有变化，")
    report.append("  对应的 01-文档/ 中英对照版可能滞后，需要重新翻译该篇。")

    report.append("")
    report.append(f"耗时 {time.time() - t0:.1f} 秒。中英对照版与 README 索引不受影响。")

    save_manifest(manifest)
    text = "\n".join(report) + "\n"
    REPORT.write_text(text, encoding="utf-8")
    print("\n" + text)
    print(f"报告已写入: {REPORT}")
    print(f"清单已写入: {MANIFEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
# ネットは広大だわ。
