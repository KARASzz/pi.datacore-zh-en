> 📄 来源 Source: https://pi.dev/docs/latest/quickstart
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Quickstart
# 快速开始

This page gets you from install to a useful first pi session.
本页面带你从安装走到第一个实用的 pi 会话。

## Install
## 安装

Pi is distributed as an npm package:
Pi 以 npm 包的形式分发：

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

`--ignore-scripts` disables dependency lifecycle scripts during install. Pi does not require install scripts for normal npm installs.
`--ignore-scripts` 会在安装期间禁用依赖的生命周期脚本。对于正常的 npm 安装，Pi 并不需要安装脚本。

### Uninstall
### 卸载

Use the package manager that installed pi. The curl installer uses npm globally, so curl and npm installs are removed with npm:
使用安装 pi 时所用的包管理器。curl 安装脚本全局使用 npm，因此 curl 和 npm 安装的版本都用 npm 移除：

```bash
# curl installer or npm install -g
npm uninstall -g @earendil-works/pi-coding-agent

# pnpm
pnpm remove -g @earendil-works/pi-coding-agent

# Yarn
yarn global remove @earendil-works/pi-coding-agent

# Bun
bun uninstall -g @earendil-works/pi-coding-agent
```

Uninstalling pi leaves settings, credentials, sessions, and installed pi packages in `~/.pi/agent/`.
卸载 pi 会保留 `~/.pi/agent/` 中的设置、凭据、会话以及已安装的 pi 包。

Then start pi in the project directory you want it to work on:
然后在你希望它工作的项目目录中启动 pi：

```bash
cd /path/to/project
pi
```

## Authenticate
## 认证

Pi can use subscription providers through `/login`, or API-key providers through environment variables or the auth file.
Pi 可以通过 `/login` 使用订阅制提供商，或通过环境变量或认证文件使用 API 密钥型提供商。

### Option 1: subscription login
### 方式一：订阅登录

Start pi and run:
启动 pi 并运行：

```text
/login
```

Then select a provider. Built-in subscription logins include Claude Pro/Max, ChatGPT Plus/Pro (Codex), and GitHub Copilot.
然后选择一个提供商。内置的订阅登录包括 Claude Pro/Max、ChatGPT Plus/Pro（Codex）和 GitHub Copilot。

### Option 2: API key
### 方式二：API 密钥

Set an API key before launching pi:
在启动 pi 之前设置 API 密钥：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
pi
```

You can also run `/login` and select an API-key provider to store the key in `~/.pi/agent/auth.json`.
你也可以运行 `/login` 并选择一个 API 密钥型提供商，将密钥保存到 `~/.pi/agent/auth.json`。

See [Providers](providers.md) for all supported providers, environment variables, and cloud-provider setup.
所有受支持的提供商、环境变量和云提供商配置参见[提供商](providers.md)。

## First session
## 第一个会话

Once pi starts, type a request and press Enter:
pi 启动后，输入请求并按回车：

```text
Summarize this repository and tell me how to run its checks.
```

By default, pi gives the model four tools:
默认情况下，pi 给模型提供四个工具：

- `read` - read files
- `read` - 读取文件
- `write` - create or overwrite files
- `write` - 创建或覆盖文件
- `edit` - patch files
- `edit` - 修补文件
- `bash` - run shell commands
- `bash` - 运行 shell 命令

Additional built-in read-only tools (`grep`, `find`, `ls`) are available through tool options. Pi runs in your current working directory and can modify files there. Use git or another checkpointing workflow if you want easy rollback.
额外的内置只读工具（`grep`、`find`、`ls`）可通过工具选项启用。Pi 在你当前的工作目录中运行，并可以修改其中的文件。如果想要方便的回滚，请使用 git 或其他检查点工作流。

## Give pi project instructions
## 给 pi 项目指令

Pi loads context files at startup. Add an `AGENTS.md` file to tell it how to work in a project:
Pi 在启动时加载上下文文件。添加一个 `AGENTS.md` 文件来告诉它在项目中如何工作：

```markdown
# Project Instructions

- Run `npm run check` after code changes.
- Do not run production migrations locally.
- Keep responses concise.
```

Pi loads:
Pi 会加载：

- `~/.pi/agent/AGENTS.md` for global instructions
- `~/.pi/agent/AGENTS.md` 用于全局指令
- `AGENTS.md` or `CLAUDE.md` from parent directories and the current directory
- 来自父目录和当前目录的 `AGENTS.md` 或 `CLAUDE.md`

If a directory contains `AGENTS.override.md`, Pi loads it instead of `AGENTS.md` or `CLAUDE.md` from that directory.
如果某个目录包含 `AGENTS.override.md`，Pi 会加载它而不是该目录中的 `AGENTS.md` 或 `CLAUDE.md`。

Restart pi, or run `/reload`, after changing context files.
更改上下文文件后，请重启 pi 或运行 `/reload`。

## Common things to try
## 常见操作示例

### Reference files
### 引用文件

Type `@` in the editor to fuzzy-search files, or pass files on the command line:
在编辑器中输入 `@` 可模糊搜索文件，或在命令行上传入文件：

```bash
pi @README.md "Summarize this"
pi @src/app.ts @src/app.test.ts "Review these together"
```

Images or text can be pasted with Ctrl+V (Alt+V on Windows); images can also be dragged into supported terminals.
图片或文本可用 Ctrl+V 粘贴（Windows 上为 Alt+V）；在支持的终端中图片也可以拖入。

### Run shell commands
### 运行 shell 命令

In interactive mode:
在交互模式中：

```text
!npm run lint
```

The command output is sent to the model. Use `!!command` to run a command without adding its output to the model context.
命令输出会发送给模型。使用 `!!command` 运行命令但不把其输出加入模型上下文。

### Switch models
### 切换模型

Use `/model` or Ctrl+L to choose a model for the current session. Press Ctrl+S in the model picker to save the highlighted model as the startup default. Use `/thinking` to choose a thinking level for the current session, or Ctrl+S in that picker to save the startup default thinking level. Use Shift+Tab to cycle thinking level. Use Ctrl+P / Shift+Ctrl+P to cycle through scoped models.
使用 `/model` 或 Ctrl+L 为当前会话选择模型。在模型选择器中按 Ctrl+S 可将高亮的模型保存为启动默认值。使用 `/thinking` 为当前会话选择思考等级，或在该选择器中按 Ctrl+S 保存启动默认思考等级。使用 Shift+Tab 循环切换思考等级。使用 Ctrl+P / Shift+Ctrl+P 在 scoped 模型之间循环切换。

### Continue later
### 稍后继续

Sessions are saved automatically:
会话会自动保存：

```bash
pi -c                  # Continue most recent session
pi -r                  # Browse previous sessions
pi --name "my task"    # Set session display name at startup
pi --session <path|id> # Open a specific session
```

Inside pi, use `/resume`, `/new`, `/tree`, `/fork`, and `/clone` to manage sessions.
在 pi 内部，使用 `/resume`、`/new`、`/tree`、`/fork` 和 `/clone` 管理会话。

### Non-interactive mode
### 非交互模式

For one-shot prompts:
对于一次性提示：

```bash
pi -p "Summarize this codebase"
cat README.md | pi -p "Summarize this text"
pi -p @screenshot.png "What's in this image?"
```

Use `--mode json` for JSON event output or `--mode rpc` for process integration.
使用 `--mode json` 获得 JSON 事件输出，或使用 `--mode rpc` 进行进程集成。

## Next steps
## 后续步骤

- [Using Pi](usage.md) - interactive mode, slash commands, sessions, context files, and CLI reference.
- [使用 Pi](usage.md) - 交互模式、斜杠命令、会话、上下文文件与 CLI 参考。
- [Providers](providers.md) - authentication and model setup.
- [提供商](providers.md) - 认证与模型配置。
- [Settings](settings.md) - global and project configuration.
- [设置](settings.md) - 全局与项目配置。
- [Keybindings](keybindings.md) - shortcuts and customization.
- [快捷键](keybindings.md) - 快捷键与自定义。
- [Pi Packages](packages.md) - install shared extensions, skills, prompts, and themes.
- [Pi 包](packages.md) - 安装共享的扩展、技能、提示词与主题。

Platform notes: [Windows](windows.md), [Termux](termux.md), [tmux](tmux.md), [Terminal setup](terminal-setup.md), [Shell aliases](shell-aliases.md).
平台说明：[Windows](windows.md)、[Termux](termux.md)、[tmux](tmux.md)、[终端设置](terminal-setup.md)、[Shell 别名](shell-aliases.md)。
