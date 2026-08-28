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
选项:  --allow-insecure（证书失败时显式降级）或 --mark-translations-current（人工复核后更新译文基线）
输出:  控制台摘要 + 根目录《更新报告.txt》；变更检测基于《资料清单.json》哈希清单，
       中英对照绑定状态写入《翻译状态.json》。
说明:  01-文档/ 下的中英对照版由 AI 生成；若报告提示某文档英文原文已变化，
       说明对照版可能滞后，需要重新翻译该篇。
"""

import argparse
import concurrent.futures as cf
from datetime import datetime, timezone
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
TRANSLATION_ROOT = KB / "01-文档"                 # 中英对照版
TRANSLATION_STATUS = ROOT / "翻译状态.json"       # 原文与译文绑定状态
SYNC_CONFIG = ROOT / "sync-config.json"           # GitHub Actions 开关

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

# 已存在的中英对照版；未列出的文档暂时只有英文原文。
TRANSLATION_FILES = {
    "compaction": "11-压缩-Compaction.md",
    "containerization": "07-容器化-Containerization.md",
    "custom-provider": "18-自定义提供商-Custom-Provider.md",
    "development": "30-开发-Development.md",
    "environment-variables": "19-环境变量-Environment-Variables.md",
    "index": "01-总览-Overview.md",
    "json": "23-JSON事件流-JSON.md",
    "keybindings": "09-快捷键-Keybindings.md",
    "llama-cpp": "05-llama-cpp.md",
    "models": "17-自定义模型-Custom-Models.md",
    "packages": "16-Pi包-Packages.md",
    "prompt-templates": "14-提示词模板-Prompt-Templates.md",
    "providers": "04-提供商-Providers.md",
    "quickstart": "02-快速开始-Quickstart.md",
    "security": "06-安全-Security.md",
    "session-format": "20-会话格式-Session-Format.md",
    "sessions": "10-会话-Sessions.md",
    "settings": "08-设置-Settings.md",
    "shell-aliases": "29-Shell别名-Shell-Aliases.md",
    "skills": "13-技能-Skills.md",
    "terminal-setup": "28-终端设置-Terminal-Setup.md",
    "termux": "26-Termux.md",
    "themes": "15-主题-Themes.md",
    "tmux": "27-tmux.md",
    "usage": "03-使用-Pi-Usage.md",
    "windows": "25-Windows.md",
}

SRC_HINTS = ("/src/", "/test/", "/tests/", "/scripts/", "/examples/",
             "install-lock/", "/images/", ".github/", "node_modules/")

_ALLOW_INSECURE = False


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


def http_get(url, timeout=40, *, allow_insecure=None):
    """GET 一个 URL；默认严格校验 TLS，显式允许时才会降级。"""
    global _CTX_INSECURE
    if allow_insecure is None:
        allow_insecure = _ALLOW_INSECURE
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=timeout,
                                    context=_ssl_context()) as resp:
            return resp.read()
    except urllib.error.URLError as e:
        reason = str(getattr(e, "reason", e))
        if "CERTIFICATE_VERIFY_FAILED" in reason:
            if not allow_insecure:
                raise RuntimeError(
                    "SSL 证书校验失败；默认拒绝连接。确认网络环境后，"
                    "如仍要继续请显式使用 --allow-insecure"
                ) from e
            if _CTX_INSECURE is None:
                _CTX_INSECURE = ssl._create_unverified_context()
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


def load_sync_config():
    """读取同步配置；配置无效时拒绝运行，避免意外开启自动同步。"""
    if not SYNC_CONFIG.exists():
        return {"github_actions": {"enabled": True}}
    try:
        data = json.loads(SYNC_CONFIG.read_text(encoding="utf-8"))
    except Exception as e:
        raise ValueError(f"无法读取 {SYNC_CONFIG.name}: {e}") from e
    if not isinstance(data, dict):
        raise ValueError(f"{SYNC_CONFIG.name} 顶层必须是 JSON 对象")
    actions = data.get("github_actions", {})
    if not isinstance(actions, dict):
        raise ValueError("sync-config.json 的 github_actions 必须是对象")
    enabled = actions.get("enabled", True)
    if not isinstance(enabled, bool):
        raise ValueError("sync-config.json 的 github_actions.enabled 必须是布尔值")
    return data


def github_actions_enabled():
    return load_sync_config().get("github_actions", {}).get("enabled", True)


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
    changed_any = False
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
                changed_any = True
            manifest[key] = new_hash
            ok += 1
            if not existed:
                report.append(f"  + 新增: {src} -> {target.relative_to(ROOT)}")
            elif changed:
                report.append(f"  * 已更新: {src}")
    report.append(f"  仓库资料合计成功 {ok} 个，失败 {fail} 个")
    return changed_any, fail

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
    changed_any = False
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
                changed_any = True
            manifest[key] = new_hash
            ok += 1
            if not existed:
                report.append(f"  + 新增快照: {name}")
            elif changed:
                report.append(f"  * 快照有变化: {name}")
    report.append(f"  网站快照合计成功 {ok} 个，失败 {fail} 个")
    return changed_any, fail


# ----------------------------------------------------------------------------
# 对照版状态小结
# ----------------------------------------------------------------------------
def load_translation_status():
    if TRANSLATION_STATUS.exists():
        try:
            data = json.loads(TRANSLATION_STATUS.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {}


def save_translation_status(data):
    TRANSLATION_STATUS.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _source_hash(name, manifest):
    key = f"repo:packages/coding-agent/docs/{name}.md"
    if manifest.get(key):
        return manifest[key]
    source = RAW_DOCS / f"{name}.md"
    if source.exists():
        return sha256(source.read_bytes())
    return None


def _utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def translation_status(manifest, report, *, mark_current=False):
    """比较英文原文哈希与译文基线，返回状态文件是否发生变化。"""
    old_state = load_translation_status()
    old_documents = old_state.get("documents", {})
    state_exists = TRANSLATION_STATUS.exists()
    documents = {}
    by_status = {"CURRENT": [], "STALE": [], "UNTRANSLATED": [],
                 "SOURCE_MISSING": []}

    for name in DOC_NAMES:
        raw_hash = _source_hash(name, manifest)
        filename = TRANSLATION_FILES.get(name)
        translation_path = TRANSLATION_ROOT / filename if filename else None
        old_entry = old_documents.get(name, {})
        old_translation_hash = old_entry.get("translation_source_hash")
        updated_at = old_entry.get("translation_updated_at")

        if translation_path is None or not translation_path.exists():
            status = "UNTRANSLATED"
            translation_hash = None
            updated_at = None
        elif raw_hash is None:
            status = "SOURCE_MISSING"
            translation_hash = old_translation_hash
        elif mark_current:
            status = "CURRENT"
            translation_hash = raw_hash
            updated_at = _utc_now()
        elif name in old_documents:
            translation_hash = old_translation_hash
            status = "CURRENT" if translation_hash == raw_hash else "STALE"
        elif not state_exists:
            # 首次建立状态文件时，把仓库中已有译文作为当前基线；之后必须显式标记。
            status = "CURRENT"
            translation_hash = raw_hash
        else:
            status = "STALE"
            translation_hash = None

        relative_path = (translation_path.relative_to(ROOT).as_posix()
                         if translation_path else None)
        documents[name] = {
            "raw_source_hash": raw_hash,
            "translation_source_hash": translation_hash,
            "translation_updated_at": updated_at,
            "status": status,
            "translation_file": relative_path,
        }
        by_status.setdefault(status, []).append(name)

    new_state = {"version": 1, "documents": documents}
    changed = new_state != old_state
    if changed:
        save_translation_status(new_state)

    report.append(
        "  翻译状态："
        + " / ".join(f"{status} {len(names)}"
                     for status, names in by_status.items())
    )
    for status in ("STALE", "UNTRANSLATED", "SOURCE_MISSING"):
        if by_status[status]:
            report.append(f"  {status}: {', '.join(by_status[status])}")
    report.append(f"  详细状态已写入: {TRANSLATION_STATUS.relative_to(ROOT)}")
    if mark_current:
        report.append("  已按 --mark-translations-current 更新现有译文基线。")
    return changed


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------
def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="同步 pi.dev 与 earendil-works/pi 的公开资料快照"
    )
    parser.add_argument(
        "--allow-insecure",
        action="store_true",
        help="证书校验失败时允许降级为不验证模式，并在报告中告警",
    )
    parser.add_argument(
        "--mark-translations-current",
        action="store_true",
        help="将现有中英对照版绑定到当前英文原文哈希（人工复核后使用）",
    )
    return parser.parse_args(argv)


def _report_signature(text):
    """忽略易变的时间字段，避免定时任务制造无意义的 PR。"""
    return "\n".join(
        line for line in text.splitlines()
        if not line.startswith("运行时间:") and not line.startswith("耗时 ")
    )


def main(argv=None):
    args = parse_args(argv)
    global _ALLOW_INSECURE
    _ALLOW_INSECURE = args.allow_insecure
    t0 = time.time()
    print("=" * 62)
    print("pi 资料一键更新（来源: GitHub 仓库 + pi.dev 网站）")
    print("=" * 62)
    manifest = load_manifest()
    report = [f"运行时间: {time.strftime('%Y-%m-%d %H:%M:%S')}", ""]
    if args.allow_insecure:
        report.append(
            "[SECURITY WARNING] 已启用 --allow-insecure；仅在证书校验失败时"
            "使用不验证 TLS 的重试。"
        )
        report.append("")

    data_changed = False
    failures = 0

    report.append("【来源 1】GitHub 仓库 earendil-works/pi（文档/说明/更新日志）")
    print("\n[1/2] 检查 GitHub 仓库资料 ...")
    try:
        changed, failed = update_repo(manifest, report)
        data_changed = data_changed or changed
        failures += failed
    except Exception as e:
        report.append(f"  [异常] {e.__class__.__name__}: {e}")
        print(f"  仓库更新出错: {e}")
        failures += 1

    report.append("")
    report.append("【来源 2】pi.dev 网站（页面快照）")
    print("\n[2/2] 抓取 pi.dev 网站快照 ...")
    try:
        changed, failed = update_site(manifest, report)
        data_changed = data_changed or changed
        failures += failed
    except Exception as e:
        report.append(f"  [异常] {e.__class__.__name__}: {e}")
        print(f"  网站更新出错: {e}")
        failures += 1

    report.append("")
    report.append("【文档对照版状态】")
    translation_changed = False
    try:
        translation_changed = translation_status(
            manifest,
            report,
            mark_current=args.mark_translations_current,
        )
    except Exception as e:
        report.append(f"  [异常] {e.__class__.__name__}: {e}")
        failures += 1

    report.append("")
    report.append(f"耗时 {time.time() - t0:.1f} 秒。中英对照版与 README 索引不受影响。")

    save_manifest(manifest)
    text = "\n".join(report) + "\n"
    try:
        previous_report = REPORT.read_text(encoding="utf-8")
    except Exception:
        previous_report = ""
    report_content_changed = (
        _report_signature(previous_report) != _report_signature(text)
    )
    should_write_report = (
        data_changed
        or translation_changed
        or failures
        or args.allow_insecure
        or args.mark_translations_current
        or not REPORT.exists()
        or report_content_changed
    )
    if should_write_report:
        REPORT.write_text(text, encoding="utf-8")
    else:
        print("\n本次无资料或状态变化，保留上一份《更新报告.txt》。")
    print("\n" + text)
    if should_write_report:
        print(f"报告已写入: {REPORT}")
    print(f"清单已写入: {MANIFEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
# GHOST_FINAL_TRACE
# ネットは広大だわ。
