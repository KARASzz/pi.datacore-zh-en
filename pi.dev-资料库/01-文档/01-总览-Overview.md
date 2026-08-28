> 📄 来源 Source: https://pi.dev/docs/latest
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Pi Documentation
# Pi 文档

Pi is a minimal terminal coding harness. It is designed to stay small at the core while being extended through TypeScript extensions, skills, prompt templates, themes, and pi packages.
Pi 是一个极简的终端编码框架（harness）。它的核心设计保持精简，同时可通过 TypeScript 扩展、技能（skills）、提示词模板、主题和 pi 包进行扩展。

## Quick start
## 快速开始

Install Pi with npm:
使用 npm 安装 Pi：

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

`--ignore-scripts` disables dependency lifecycle scripts during install. Pi does not require install scripts for normal npm installs.
`--ignore-scripts` 会在安装期间禁用依赖的生命周期脚本。对于正常的 npm 安装，Pi 并不需要安装脚本。

On Linux or macOS, you can also use the installer:
在 Linux 或 macOS 上，你也可以使用安装脚本：

```bash
curl -fsSL https://pi.dev/install.sh | sh
```

To uninstall pi itself, use npm for curl and npm installs:
要卸载 pi 本体，curl 和 npm 安装的版本请使用 npm 卸载：

```bash
npm uninstall -g @earendil-works/pi-coding-agent
```

For pnpm, Yarn, or Bun installs, use the matching global remove command: `pnpm remove -g @earendil-works/pi-coding-agent`, `yarn global remove @earendil-works/pi-coding-agent`, or `bun uninstall -g @earendil-works/pi-coding-agent`.
对于 pnpm、Yarn 或 Bun 安装，请使用对应的全局移除命令：`pnpm remove -g @earendil-works/pi-coding-agent`、`yarn global remove @earendil-works/pi-coding-agent` 或 `bun uninstall -g @earendil-works/pi-coding-agent`。

Then run it in a project directory:
然后在项目目录中运行它：

```bash
pi
```

Authenticate with `/login` for subscription providers, or set an API key such as `ANTHROPIC_API_KEY` before starting pi.
使用 `/login` 登录订阅制提供商，或在启动 pi 之前设置诸如 `ANTHROPIC_API_KEY` 之类的 API 密钥。

For the full first-run flow, see [Quickstart](quickstart.md).
完整的首次运行流程参见[快速开始](quickstart.md)。

## Start here
## 从这里开始

- [Quickstart](quickstart.md) - install, authenticate, and run a first session.
- [快速开始](quickstart.md) - 安装、认证并运行第一个会话。
- [Using Pi](usage.md) - interactive mode, slash commands, context files, and CLI reference.
- [使用 Pi](usage.md) - 交互模式、斜杠命令、上下文文件与 CLI 参考。
- [Providers](providers.md) - subscription and API-key setup for built-in providers.
- [提供商](providers.md) - 内置提供商的订阅与 API 密钥配置。
- [llama.cpp](llama-cpp.md) - run a local router and manage models with `/llama`.
- [llama.cpp](llama-cpp.md) - 运行本地路由并用 `/llama` 管理模型。
- [Security](security.md) - project trust, sandbox boundaries, and vulnerability reporting.
- [安全](security.md) - 项目信任、沙箱边界与漏洞报告。
- [Containerization](containerization.md) - sandbox pi with Gondolin, Docker, or OpenShell.
- [容器化](containerization.md) - 使用 Gondolin、Docker 或 OpenShell 对 pi 进行沙箱隔离。
- [Settings](settings.md) - global and project settings.
- [设置](settings.md) - 全局与项目设置。
- [Keybindings](keybindings.md) - default shortcuts and custom keybindings.
- [快捷键](keybindings.md) - 默认快捷键与自定义键位。
- [Sessions](sessions.md) - session management, branching, and tree navigation.
- [会话](sessions.md) - 会话管理、分支与树状导航。
- [Compaction](compaction.md) - context compaction and branch summarization.
- [压缩](compaction.md) - 上下文压缩与分支摘要。

## Customization
## 定制

- [Extensions](extensions.md) - TypeScript modules for tools, commands, events, and custom UI.
- [扩展](extensions.md) - 用于工具、命令、事件与自定义 UI 的 TypeScript 模块。
- [Skills](skills.md) - Agent Skills for reusable on-demand capabilities.
- [技能](skills.md) - 用于可复用、按需能力的 Agent Skills。
- [Prompt templates](prompt-templates.md) - reusable prompts that expand from slash commands.
- [提示词模板](prompt-templates.md) - 通过斜杠命令展开的可复用提示词。
- [Themes](themes.md) - built-in and custom terminal themes.
- [主题](themes.md) - 内置与自定义终端主题。
- [Pi packages](packages.md) - bundle and share extensions, skills, prompts, and themes.
- [Pi 包](packages.md) - 打包并分享扩展、技能、提示词与主题。
- [Custom models](models.md) - add model entries for supported provider APIs.
- [自定义模型](models.md) - 为受支持的提供商 API 添加模型条目。
- [Custom providers](custom-provider.md) - implement custom APIs and OAuth flows.
- [自定义提供商](custom-provider.md) - 实现自定义 API 与 OAuth 流程。

## Programmatic usage
## 编程方式使用

- [SDK](sdk.md) - embed pi in Node.js applications.
- [SDK](sdk.md) - 将 pi 嵌入 Node.js 应用。
- [RPC mode](rpc.md) - integrate over stdin/stdout JSONL.
- [RPC 模式](rpc.md) - 通过 stdin/stdout 的 JSONL 进行集成。
- [JSON event stream mode](json.md) - print mode with structured events.
- [JSON 事件流模式](json.md) - 带结构化事件的打印（print）模式。
- [TUI components](tui.md) - build custom terminal UI for extensions.
- [TUI 组件](tui.md) - 为扩展构建自定义终端 UI。

## Reference
## 参考

- [Environment variables](environment-variables.md) - Pi process configuration and session metadata available to bash tools.
- [环境变量](environment-variables.md) - 可供 bash 工具使用的 Pi 进程配置与会话元数据。
- [Session format](session-format.md) - JSONL session file format, entry types, and SessionManager API.
- [会话格式](session-format.md) - JSONL 会话文件格式、条目类型与 SessionManager API。

## Platform setup
## 平台设置

- [Windows](windows.md)
- [Windows](windows.md)
- [Termux on Android](termux.md)
- [Android 上的 Termux](termux.md)
- [tmux](tmux.md)
- [tmux](tmux.md)
- [Terminal setup](terminal-setup.md)
- [终端设置](terminal-setup.md)
- [Shell aliases](shell-aliases.md)
- [Shell 别名](shell-aliases.md)

## Development
## 开发

- [Development](development.md) - local setup, project structure, and debugging.
- [开发](development.md) - 本地搭建、项目结构与调试。
