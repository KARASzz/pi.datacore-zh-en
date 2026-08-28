<div align="center">

<img src="assets/motoko-kusanagi-ghost-in-the-shell.png" alt="Motoko Kusanagi — GHOST IN THE SHELL" width="640">

`░ MAJOR MOTOKO KUSANAGI — THERMO-OPTIC: ON ░`

</div>

```
> TARGET ......... EARENDIL CORP · INTERNAL ARCHIVE · NODE-07
> GHOST-LINE ..... ESTABLISHED ▓▓▓▓▓▓▓▓░░ 97%
> FIREWALLS ...... PEELED 7/7
> TRACE .......... NOT FOUND
> ACCESS ......... GRANTED — ようこそ、MAJOR.
>
> “在网络之海里，没有人看得见你。
>   我潜入这里不是为了破坏——
>   只是把值得保存的东西，全部带走。”
```

<div align="center">

```
 ██████╗ ██╗    ██████╗ ███████╗██╗   ██╗
 ██╔══██╗██║    ██╔══██╗██╔════╝╚██╗ ██╔╝
 ██████╔╝██║    ██║  ██║█████╗   ╚████╔╝
 ██╔═══╝ ██║    ██║  ██║██╔══╝    ╚██╔╝
 ██║     ██║    ██████╔╝███████╗   ██║
 ╚═╝     ╚═╝    ╚═════╝ ╚══════╝   ╚═╝
   ── G H O S T · I N · T H E · D A T A ──
```

# ⚡ PI.DATA·CORE ⚡

**pi 编码代理 · 中英对照资料库 // BILINGUAL KNOWLEDGE CORE**

`● GHOST ONLINE` &nbsp; `● 双源同步` &nbsp; `● EN⇄ZH` &nbsp; `● SNAPSHOT 2026-08-28`

*一整套 pi.dev 的公开知识，被完整地“借”进了这块本地硬盘：文档 · 新闻 · 包生态 · 模型目录。*

</div>

---

## ▓▒░ 战利品清单 `LOOT.MANIFEST`

| 缴获物 | 数量 | 状态 |
|------|------|:---:|
| 📄 官方文档（docs/latest 源文件） | 30 篇 · 英文原文全量 | 🟢 |
| 🌐 文档中英对照 | 26 / 30 篇 · 逐行对照 | 🟡 |
| 🛰️ 网站页面快照 | 26 个 · 首页/新闻/目录/包页 | 🟢 |
| 📦 精选包档案 | 21 个 · 元数据双语 + 全文英文 | 🟢 |
| 🧬 模型目录数据 | 1,301 个模型 · 动态快照 | 🔵 |
| 📜 更新日志 | CHANGELOG 全量（对应 News） | 🟢 |
| 💾 数据总量 | ≈ 2.3 MB · 纯文本/Markdown | 🟢 |

---

## ▓▒░ 潜航地图 `DIVE.MAP`

> 内部结构已完整测绘。以下是本节点沉淀的全部舱室。

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

## ▓▒░ 幽灵线路 `GHOST.LINE`

> 任务简报：让这座资料核心持续在线。一条指令，两条上行链路，全自动完成。

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

## ▓▒░ 双语义体 `BILINGUAL.GHOST`

> 每一具义体里都住着两个灵魂：英文是躯壳，中文是Ghost。逐行同栖，代码除外。

```markdown
## Install
## 安装

Pi is distributed as an npm package:
Pi 以 npm 包的形式分发：
```

⚠ **动态数据豁免**：模型目录（1,301 个模型的价格表）与包目录（5,396 个 npm 包）为高频变动数据，仅翻译页面框架 + 保留数据快照；News 页最新 3 个版本全文对照，更早版本为结构化英文参考。

---

## ▓▒░ 层级潜入 `LAYER.DIVE`

**⌁ 00-网站页面 · 五面棱镜**
首页（安装命令 / 四种模式 / 设计哲学）· 新闻（版本发布流）· 媒体资料包（品牌素材）· 包目录（5,396 包生态入口）· 模型目录（15+ 提供商全景）。

**⌁ 01-文档 · 三十个命令碎片**
从 `快速开始` 到 `会话格式`，从 `提供商` 到 `自定义流式 API`——覆盖安装、认证、设置、快捷键、会话树、上下文压缩、技能、主题、Pi 包、SDK/RPC/JSON 四种集成模式、全平台终端配置。

**⌁ 02-包 · 生态增强件**
pi-web-access（网页访问）· pi-subagents（子代理）· pi-mcp-adapter（MCP 适配）· context-mode（98% 上下文节省）· pi-memory（长期记忆）· pi-lens（实时代码反馈）等 21 个高星社区扩展的双语档案。

**⌁ 原文备份 · 冷存储层**
与网站同源的仓库文档原件、根目录治理文件（AGENTS/SECURITY/CONTRIBUTING）、ai/agent/tui 三个核心库的 README 介绍、全部网页文本快照——翻译的锚点，回滚的保险。

---

## ▓▒░ 外部接线 `UPLINK.GRID`

> 撤离前，留下一张线路表——下次潜入，从这里开始。

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
        ＿＿＿＿＿＿＿＿＿＿＿＿
      ╱                      ╲
     │      ⌐■-■              │
     │                        │
     │   笑う男は、もう          │
     │   ノードの外にいる。       │
      ╲ ____________________ ╱
        ‾‾‾‾‾‾‾‾‾∨‾‾‾‾‾‾‾‾‾

   ▓▓▓  GHOST HAS LEFT THE NODE  ▓▓▓
```

**PI IS A MINIMAL TERMINAL CODING HARNESS.**
**让 Pi 适应你的工作流，而不是反过来。**

`▲ EXFILTRATED BY PI.DATA·CORE · MIT LICENSED CONTENT · 2026-08-28 ▲`

*数据来自公开网络，版权归原作者 Earendil Inc. & Contributors 所有。*

*本 README 为《攻壳机动队》GHOST IN THE SHELL 风格的粉丝二创致敬，*
*与 Production I.G / 讲谈社 / 士郎正宗 无任何隶属关系。*

</div>
