# pi.dev 资料库（中英对照版）
> 抓取时间 / Snapshot: 2026-08-28 · 来源 / Source: https://pi.dev/（含官方文档仓库 earendil-works/pi 的 markdown 源文件，与网站 docs/latest 内容一致）
>
> **格式说明 / Format**：除特别标注外，所有文件均为「中英对照」——每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译（翻译会破坏代码），表格以“原表 + 译文表”成对出现。
>
> **格式说明 / Format (EN)**: Unless noted otherwise, every file is bilingual — each English line is followed by its Chinese translation. Code blocks are kept verbatim; tables appear as original + translated pairs.

## 目录结构 / Structure

```
pi.dev-资料库/
├── README.md                          ← 本索引 / this index
├── 00-网站页面/                        网站自身页面 / site pages
│   ├── 01-首页-Homepage.md            ✅ 全文中英对照
│   ├── 02-新闻-News.md                ✅ 最新版本全文对照 + 更早版本英文参考
│   ├── 03-媒体资料包-Press-Kit.md      ✅ 全文中英对照
│   ├── 04-包目录-Package-Catalog.md   ✅ 页面框架对照 + 数据说明
│   └── 05-模型目录-Model-Catalog.md   ✅ 页面框架对照 + 数据说明（1301 个模型为动态数据）
├── 01-文档/                            官方文档 docs/latest（26/30 已对照翻译）
│   ├── 01-总览-Overview.md            ✅
│   ├── 02-快速开始-Quickstart.md       ✅
│   ├── 03-使用-Pi-Usage.md            ✅
│   ├── 04-提供商-Providers.md          ✅
│   ├── 05-llama-cpp.md                ✅
│   ├── 06-安全-Security.md            ✅
│   ├── 07-容器化-Containerization.md   ✅
│   ├── 08-设置-Settings.md            ✅
│   ├── 09-快捷键-Keybindings.md        ✅
│   ├── 10-会话-Sessions.md            ✅
│   ├── 11-压缩-Compaction.md          ✅
│   ├── 13-技能-Skills.md              ✅
│   ├── 14-提示词模板-Prompt-Templates.md ✅
│   ├── 15-主题-Themes.md              ✅
│   ├── 16-Pi包-Packages.md            ✅
│   ├── 17-自定义模型-Custom-Models.md   ✅
│   ├── 18-自定义提供商-Custom-Provider.md ✅
│   ├── 19-环境变量-Environment-Variables.md ✅
│   ├── 20-会话格式-Session-Format.md    ✅
│   ├── 23-JSON事件流-JSON.md           ✅
│   ├── 25-Windows.md                   ✅
│   ├── 26-Termux.md                    ✅
│   ├── 27-tmux.md                      ✅
│   ├── 28-终端设置-Terminal-Setup.md    ✅
│   ├── 29-Shell别名-Shell-Aliases.md   ✅
│   └── 30-开发-Development.md          ✅
│   └── ⏳ 未翻译（仅有英文原文备份）：12-扩展(extensions, 3021行)、21-SDK(sdk)、22-RPC(rpc)、24-TUI组件(tui)
├── 02-包/                              精选包 / featured packages
│   └── 00-精选包总览-Packages-Overview.md ✅ 21 个包元数据对照 + 完整英文 README 指引
└── 原文备份/                           英文原文完整备份 / full English backup
    ├── docs/                           30 个文档 markdown 原文
    ├── README.md                       coding-agent 包 README
    ├── CHANGELOG.md                    完整更新日志（对应网站 News）
    └── site/                           网站 HTML 提取文本（首页/新闻/目录/21 个包页面）
```

## 内容说明 / Notes

1. **文档 26/30 已中英对照**。剩余 4 篇为最长的开发者参考（extensions ≈3021 行、rpc ≈1619 行、sdk ≈1220 行、tui ≈943 行），其完整英文原文在 `原文备份/docs/` 中，可按需补充翻译。
2. **模型目录**（https://pi.dev/models）含 1,301 个模型的实时价格表，属动态数据，翻译无意义，故仅翻译页面框架并附数据快照。
3. **包目录**（https://pi.dev/packages）共 5,396 个 npm 包且分页动态加载；静态可抓取部分（最近发布 + 前 50 + 21 个精选包页）已全部抓取备份，精选包的元数据已译。
4. **News** 页在网站上分 14 页展示发布说明；本资料库完整翻译了最新三个版本（0.84.3 / 0.84.2 / 0.84.1），其余版本提供结构化英文参考，完整原文见 `原文备份/CHANGELOG.md`。

## 一键更新 / Update

在项目根目录运行（全自动，不下载源码，只更新资料）：

```bash
python3 更新资料.py
```

- **来源 1 · GitHub 仓库** `earendil-works/pi`：刷新 `原文备份/docs/`（30 篇文档 + docs.json）、`原文备份/README.md`、`原文备份/CHANGELOG.md`、`原文备份/仓库补充/`（根目录 README/AGENTS/SECURITY/CONTRIBUTING）、`原文备份/仓库包介绍/`（ai / agent / tui / coding-agent 各包 README）；并尝试通过 GitHub API 自动发现清单外新增的 .md 资料（API 限流时自动退回内置清单）。
- **来源 2 · pi.dev 网站**：刷新 `原文备份/site/` 全部页面快照（首页 / news / press-kit / 包目录 / 模型目录 / 21 个精选包页）。
- **变更检测**：基于根目录 `资料清单.json` 的 SHA-256 清单；输出根目录《更新报告.txt》。`../翻译状态.json` 绑定每篇原文哈希与译文基线，明确标记 `CURRENT`、`STALE`、`UNTRANSLATED` 或 `SOURCE_MISSING`。
- **首次建基线**：第一次生成 `翻译状态.json` 时，仓库里已有的 26 篇译文会记录为当前基线；之后上游哈希变化会标记为 `STALE`，人工复核后再显式更新基线。
- **安全策略**：默认严格校验 TLS；证书校验失败会停止对应请求。只有确认环境可信时才使用 `python3 更新资料.py --allow-insecure`，且报告会记录 `SECURITY WARNING`。
- **译文基线**：人工复核译文后使用 `python3 更新资料.py --mark-translations-current`，不要让自动同步覆盖人工翻译。
- **自动同步**：GitHub Actions 按周运行 `更新资料.py`，发现变化后创建待审核 PR；workflow 不自动合并，也不覆盖 `01-文档/` 中的人工译文。
- **关闭自动同步**：克隆仓库后，将根目录 `sync-config.json` 中的 `github_actions.enabled` 改为 `false` 并提交到自己的远端；workflow 会在抓取前跳过。只在本地写入不会影响云端 workflow。

首次启用自动 PR 前，请在仓库设置中允许 Actions 使用读写权限并创建 Pull Request。

## 官方链接 / Official Links

- 文档 / Docs: https://pi.dev/docs/latest
- 新闻 / News: https://pi.dev/news
- 包目录 / Packages: https://pi.dev/packages
- 模型目录 / Models: https://pi.dev/models
- GitHub: https://github.com/earendil-works/pi
- npm: https://www.npmjs.com/package/@earendil-works/pi-coding-agent
- Discord: https://discord.com/invite/3cU7Bz4UPx
- X: https://x.com/pidotdev
- 媒体联系 / Press: rfc@earendil.com

> Pi is a minimal terminal coding harness. Adapt Pi to your workflows, not the other way around.
> Pi 是一个极简的终端编码框架。让 Pi 适应你的工作流，而不是反过来。
