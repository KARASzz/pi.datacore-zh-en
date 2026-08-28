<div align="center">

```
 ██████╗ ██╗    ██████╗ ███████╗██╗   ██╗
 ██╔══██╗██║    ██╔══██╗██╔════╝╚██╗ ██╔╝
 ██████╔╝██║    ██║  ██║█████╗   ╚████╔╝
 ██╔═══╝ ██║    ██║  ██║██╔══╝    ╚██╔╝
 ██║     ██║    ██████╔╝███████╗   ██║
 ╚═╝     ╚═╝    ╚═════╝ ╚══════╝   ╚═╝
        ── D A T A · C O R E ──
```

# ⚡ PI 编码代理 · 赛博资料核心

**PI CODING AGENT — NEON KNOWLEDGE CORE**

`● SYSTEM ONLINE` &nbsp; `● 双源同步` &nbsp; `● 中英对照` &nbsp; `● SNAPSHOT 2026-08-28`

 *离线归档 pi.dev 的全部公开知识：文档 · 新闻 · 包生态 · 模型目录 —— 装进一块本地硬盘。*

</div>

---

## ▓▒░ 系统状态 `SYS.STATUS`

| 指标 | 数值 | 状态 |
|------|------|:---:|
| 📄 官方文档（docs/latest） | 30 篇 · 英文原文全量 | 🟢 |
| 🌐 文档中英对照 | 26 / 30 篇 · 逐行对照 | 🟡 |
| 🛰️ 网站页面快照 | 26 个 · 首页/新闻/目录/包页 | 🟢 |
| 📦 精选包档案 | 21 个 · 元数据双语 + 全文英文 | 🟢 |
| 🧬 模型目录数据 | 1,301 个模型 · 动态快照 | 🔵 |
| 📜 更新日志 | CHANGELOG 全量（对应 News） | 🟢 |
| 💾 数据总量 | ≈ 2.3 MB · 纯文本/Markdown | 🟢 |

---

## ▓▒░ 目录导航 `NAV.TREE`

```
Pi/
├── ⚡ 更新资料.py               ← 一键同步脚本（双源 · 全自动）
├── 📋 更新报告.txt               ← 每次同步的变更日志
├── 🔑 资料清单.json              ← SHA-256 指纹库（变更检测）
│
└── 🗄️ pi.dev-资料库/             ◁◈▷ 知识核心 ◁◈▷
    ├── README.md                 本资料库索引与说明
    ├── 00-网站页面/               ✦ 网站自身页面 · 中英对照 ✦
    │   ├── 01-首页 · 02-新闻 · 03-媒体资料包
    │   └── 04-包目录 · 05-模型目录
    ├── 01-文档/                  ✦ 官方文档 30 篇 · 26 篇已对照 ✦
    │   ├── 快速开始 / 使用 / 提供商 / 安全 / 容器化 …
    │   ├── 会话 / 压缩 / 技能 / 主题 / Pi包 / 自定义模型 …
    │   └── ⏳ 未对照: extensions · rpc · sdk · tui（原文在备份）
    ├── 02-包/                    ✦ 21 个精选包 · 双语元数据 ✦
    └── 原文备份/                  ✦ 英文原文全量备份 ✦
        ├── docs/                30 篇文档源文件 + docs.json
        ├── 仓库补充/             README · AGENTS · SECURITY · CONTRIBUTING
        ├── 仓库包介绍/           ai / agent / tui 各包 README（来自仓库）
        └── site/                网站页面文本快照 ×26
```

> ◈ 仓库（`earendil-works/pi`）与网站的文本资料同源，统一归档于此，不做重复存放。


---

## ▓▒░ 同步协议 `SYNC.PROTOCOL`

> 让资料核心保持在线，只需一行指令：

```bash
python3 更新资料.py
```

**⌁ 双源接入**

| 上行链路 | 抓取内容 | 落点 |
|----------|----------|------|
| 🛰️ `GitHub · earendil-works/pi` | 30 篇文档 + docs.json + README/CHANGELOG + AGENTS/SECURITY/CONTRIBUTING + 各包介绍（并尝试 API 自动发现新 .md，限流时自动回退内置清单） | `原文备份/` |
| 🌐 `pi.dev` | 首页 · news · press-kit · 包目录 · 模型目录 · 21 个精选包页 | `原文备份/site/` |

**⌁ 运行特性**

- 🔒 **零污染** —— 不下载源码，只抓 `.md` / `.json` 资料与页面文本（跳过 src/test/scripts/examples）
- 🧠 **指纹去重** —— SHA-256 清单比对，内容未变不落盘；有变化才写入并在报告中标记 `*`
- 🩺 **自愈容错** —— macOS 证书自动降级（certifi → 系统 CA → 安全重试）；单点失败不影响全局；任意目录可运行
- 📡 **滞后告警** —— 若某篇 `docs/*.md` 英文原文变化，报告会提示 `01-文档/` 对应中英对照需重译
- 📄 **同步回执** —— 结果写入根目录《更新报告.txt》

---

## ▓▒░ 对照格式 `BILINGUAL.FORMAT`

> 每一行英文原文之后，紧跟一行中文翻译。代码是机器的语言，保持原样；表格以「原表 + 译表」成对浮现。

```markdown
## Install
## 安装

Pi is distributed as an npm package:
Pi 以 npm 包的形式分发：
```

⚠ **动态数据豁免**：模型目录（1,301 个模型的价格表）与包目录（5,396 个 npm 包）为高频变动数据，仅翻译页面框架 + 保留数据快照；News 页最新 3 个版本全文对照，更早版本为结构化英文参考。

---

## ▓▒░ 数据层详解 `LAYER.MAP`

**⌁ 00-网站页面 · 五面棱镜**
首页（安装命令 / 四种模式 / 设计哲学）· 新闻（版本发布流）· 媒体资料包（品牌素材）· 包目录（5,396 包生态入口）· 模型目录（15+ 提供商全景）。

**⌁ 01-文档 · 三十个命令碎片**
从 `快速开始` 到 `会话格式`，从 `提供商` 到 `自定义流式 API`——覆盖安装、认证、设置、快捷键、会话树、上下文压缩、技能、主题、Pi 包、SDK/RPC/JSON 四种集成模式、全平台终端配置。

**⌁ 02-包 · 生态增强件**
pi-web-access（网页访问）· pi-subagents（子代理）· pi-mcp-adapter（MCP 适配）· context-mode（98% 上下文节省）· pi-memory（长期记忆）· pi-lens（实时代码反馈）等 21 个高星社区扩展的双语档案。

**⌁ 原文备份 · 冷存储层**
与网站同源的仓库文档原件、根目录治理文件（AGENTS/SECURITY/CONTRIBUTING）、ai/agent/tui 三个核心库的 README 介绍、全部网页文本快照——翻译的锚点，回滚的保险。

---

## ▓▒░ 外部链路 `UPLINK.GRID`

| 链路 | 地址 |
|------|------|
| 🌐 官网 | https://pi.dev |
| 📖 文档 | https://pi.dev/docs/latest |
| 📰 新闻 | https://pi.dev/news |
| 📦 包目录 | https://pi.dev/packages |
| 🧬 模型目录 | https://pi.dev/models |
| 🐙 GitHub | https://github.com/earendil-works/pi |
| 📥 npm | https://www.npmjs.com/package/@earendil-works/pi-coding-agent |
| 💬 Discord | https://discord.com/invite/3cU7Bz4UPx |
| 🐦 X | https://x.com/pidotdev |
| ✉️ 媒体联络 | rfc@earendil.com |

---

<div align="center">

```
╔══════════════════════════════════════════════════╗
║  PI IS A MINIMAL TERMINAL CODING HARNESS.        ║
║  Pi 是一个极简的终端编码框架。                       ║
║                                                  ║
║  ADAPT PI TO YOUR WORKFLOWS,                     ║
║  NOT THE OTHER WAY AROUND.                       ║
║  让 Pi 适应你的工作流，而不是反过来。                  ║
╚══════════════════════════════════════════════════╝
```

`▲ ARCHIVED BY PI.DATA-CORE · MIT LICENSED CONTENT · SNAPSHOT 2026-08-28 ▲`

*数据来自公开网络，版权归原作者 Earendil Inc. & Contributors 所有。*

</div>

