> 📄 来源 Source: https://pi.dev/docs/latest/usage
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Using Pi
# 使用 Pi

This page collects day-to-day usage details that do not fit on the quickstart page.
本页面收集不适合放在快速开始页面中的日常使用细节。

## Interactive Mode
## 交互模式

<p align="center"><img src="images/interactive-mode.png" alt="Interactive Mode" width="600"></p>
<p align="center"><img src="images/interactive-mode.png" alt="交互模式" width="600"></p>

The interface has four main areas:
界面有四个主要区域：

- **Startup header** - shortcuts, loaded context files, prompt templates, skills, and extensions
- **启动头** - 快捷键、已加载的上下文文件、提示词模板、技能和扩展
- **Messages** - user messages, assistant responses, tool calls, tool results, notifications, errors, and extension UI
- **消息** - 用户消息、助手响应、工具调用、工具结果、通知、错误和扩展 UI
- **Editor** - where you type; border color indicates the current thinking level
- **编辑器** - 你输入的地方；边框颜色表示当前的思考等级
- **Footer** - working directory, session name, token/cache usage, cost, context usage, and current model. Totals include assistant responses, usage reported by tools, and summary generation.
- **页脚** - 工作目录、会话名称、token/缓存用量、成本、上下文使用情况和当前模型。总计包括助手响应、工具报告的用量和摘要生成。

The editor can be replaced temporarily by built-in UI such as `/settings` or by custom extension UI.
编辑器可以被内置 UI（如 `/settings`）或自定义扩展 UI 临时替换。

### Editor Features
### 编辑器功能

| Feature | How |
|---------|-----|
| File reference | Type `@` to fuzzy-search project files |
| Path completion | Press Tab to complete paths |
| Multi-line input | Shift+Enter, or Ctrl+Enter on Windows Terminal |
| Copy response | Ctrl+X copies the selected message in `/tree`; otherwise it copies the last assistant message, or the active fullscreen text selection when `fullscreenCopyOnSelect` is disabled |
| Images | Paste with Ctrl+V, Alt+V on Windows, or drag into the terminal |
| Shell command | `!command` runs and sends output to the model |
| Hidden shell command | `!!command` runs without sending output to the model |
| External editor | Ctrl+G opens `externalEditor`, `$VISUAL`, `$EDITOR`, Notepad on Windows, or `nano` elsewhere |

| 功能 | 操作方式 |
|---------|-----|
| 文件引用 | 输入 `@` 模糊搜索项目文件 |
| 路径补全 | 按 Tab 补全路径 |
| 多行输入 | Shift+Enter，Windows Terminal 上为 Ctrl+Enter |
| 复制响应 | Ctrl+X 在 `/tree` 中复制选中的消息；否则复制最后一条助手消息，或在 `fullscreenCopyOnSelect` 禁用时复制活动的全屏文本选区 |
| 图片 | 用 Ctrl+V 粘贴（Windows 上为 Alt+V），或拖入终端 |
| Shell 命令 | `!command` 运行并把输出发送给模型 |
| 隐藏 shell 命令 | `!!command` 运行但不把输出发送给模型 |
| 外部编辑器 | Ctrl+G 打开 `externalEditor`、`$VISUAL`、`$EDITOR`、Windows 上的记事本或其他平台上的 `nano` |


See [Keybindings](keybindings.md) for all shortcuts and customization.
所有快捷键与自定义参见[快捷键](keybindings.md)。

## Slash Commands
## 斜杠命令

Type `/` in the editor to open command completion. Extensions can register custom commands, skills are available as `/skill:name`, and prompt templates expand via `/templatename`.
在编辑器中输入 `/` 打开命令补全。扩展可以注册自定义命令，技能以 `/skill:name` 形式可用，提示词模板通过 `/templatename` 展开。

| Command | Description |
|---------|-------------|
| `/login`, `/logout` | Manage OAuth or API-key credentials |
| [`/llama`](llama-cpp.md) | Download, load, and unload llama.cpp router models |
| `/model` | Switch models; Ctrl+S in the picker saves the startup default |
| `/thinking` | Switch thinking level; Ctrl+S in the picker saves the startup default |
| `/scoped-models` | Enable/disable models for Ctrl+P cycling |
| `/settings` | Theme, message delivery, transport, and other preferences |
| `/resume` | Pick from previous sessions |
| `/new` | Start a new session |
| `/name <name>` | Set session display name |
| `/session` | Show session file, ID, messages, tokens, and cost |
| `/tree` | Jump to any point in the session and continue from there |
| `/trust` | Save project trust decision for future sessions |
| `/fork` | Create a new session from a previous user message |
| `/clone` | Duplicate the current active branch into a new session |
| `/compact [prompt]` | Manually compact context, optionally with custom instructions |
| `/copy` | Copy last assistant message to clipboard |
| `/export [file]` | Export session to HTML or JSONL |
| `/import <file>` | Import and resume a session from a JSONL file |
| `/share` | Upload as private GitHub gist with shareable HTML link |
| `/reload` | Reload keybindings, extensions, skills, prompts, themes, and context files |
| `/hotkeys` | Show all keyboard shortcuts |
| `/changelog` | Display version history |
| `/quit` | Quit pi |

| 命令 | 描述 |
|---------|-------------|
| `/login`, `/logout` | 管理 OAuth 或 API 密钥凭据 |
| [`/llama`](llama-cpp.md) | 下载、加载和卸载 llama.cpp 路由器模型 |
| `/model` | 切换模型；在选择器中按 Ctrl+S 保存启动默认值 |
| `/thinking` | 切换思考等级；在选择器中按 Ctrl+S 保存启动默认值 |
| `/scoped-models` | 启用/禁用用于 Ctrl+P 循环切换的模型 |
| `/settings` | 主题、消息送达、传输方式及其他偏好设置 |
| `/resume` | 从以前的会话中选择 |
| `/new` | 开始新会话 |
| `/name <name>` | 设置会话显示名称 |
| `/session` | 显示会话文件、ID、消息数、token 数和成本 |
| `/tree` | 跳转到会话中的任意一点并从那里继续 |
| `/trust` | 保存项目信任决定供未来会话使用 |
| `/fork` | 从之前的用户消息创建新会话 |
| `/clone` | 将当前活动分支复制到新会话 |
| `/compact [prompt]` | 手动压缩上下文，可选自定义指令 |
| `/copy` | 把最后一条助手消息复制到剪贴板 |
| `/export [file]` | 将会话导出为 HTML 或 JSONL |
| `/import <file>` | 从 JSONL 文件导入并恢复会话 |
| `/share` | 上传为私有 GitHub gist 并附可分享的 HTML 链接 |
| `/reload` | 重新加载快捷键、扩展、技能、提示词、主题和上下文文件 |
| `/hotkeys` | 显示所有键盘快捷键 |
| `/changelog` | 显示版本历史 |
| `/quit` | 退出 pi |


## Message Queue
## 消息队列

You can submit messages while the agent is still working:
你可以在代理仍在工作时提交消息：

- **Enter** queues a steering message, delivered after the current assistant turn finishes executing its tool calls.
- **Enter** 将 steering 消息排队，在当前助手轮次完成其工具调用执行后送达。
- **Alt+Enter** queues a follow-up message, delivered after the agent finishes all work.
- **Alt+Enter** 将 follow-up 消息排队，在代理完成所有工作后送达。
- **Escape** aborts and restores queued messages to the editor.
- **Escape** 中止并把排队的消息恢复到编辑器。
- **Alt+Up** retrieves queued messages back to the editor.
- **Alt+Up** 把排队的消息取回到编辑器。

On Windows Terminal, Alt+Enter is fullscreen by default. Remap it as described in [Terminal setup](terminal-setup.md) if you want pi to receive the shortcut.
在 Windows Terminal 上，Alt+Enter 默认是全屏。如果你想让 pi 接收该快捷键，请按[终端设置](terminal-setup.md)中的说明重新映射。

Configure delivery in [Settings](settings.md) with `steeringMode` and `followUpMode`.
在[设置](settings.md)中用 `steeringMode` 和 `followUpMode` 配置送达方式。

## Sessions
## 会话

Sessions are saved automatically to `~/.pi/agent/sessions/`, organized by working directory.
会话自动保存到 `~/.pi/agent/sessions/`，按工作目录组织。

```bash
pi -c                  # Continue most recent session
pi -r                  # Browse and select a session
pi --no-session        # Ephemeral mode; do not save
pi --name "my task"    # Set session display name at startup
pi --session <path|id> # Use a specific session file or session ID
pi --fork <path|id>    # Fork a session into a new session file
```

Useful session commands:
实用的会话命令：

- `/session` shows the current session file and ID.
- `/session` 显示当前会话文件和 ID。
- `/tree` navigates the in-file session tree and can summarize abandoned branches.
- `/tree` 导航文件内的会话树，并可摘要被放弃的分支。
- `/fork` creates a new session from an earlier user message.
- `/fork` 从较早的用户消息创建新会话。
- `/clone` duplicates the current active branch into a new session file.
- `/clone` 把当前活动分支复制到新会话文件。
- `/compact` summarizes older messages to free context.
- `/compact` 摘要较旧的消息以释放上下文。

See [Sessions](sessions.md) and [Compaction](compaction.md) for details.
详情参见[会话](sessions.md)与[压缩](compaction.md)。

## Context Files
## 上下文文件

Pi loads `AGENTS.md` or `CLAUDE.md` at startup from:
Pi 在启动时从以下位置加载 `AGENTS.md` 或 `CLAUDE.md`：

- `~/.pi/agent/AGENTS.md` for global instructions
- `~/.pi/agent/AGENTS.md` 用于全局指令
- parent directories, walking up from the current working directory
- 父目录，从当前工作目录向上遍历
- the current directory
- 当前目录

If a directory contains `AGENTS.override.md`, Pi loads it instead of `AGENTS.md` or `CLAUDE.md` from that directory. Context files from other directories still layer normally.
如果某个目录包含 `AGENTS.override.md`，Pi 会加载它而不是该目录中的 `AGENTS.md` 或 `CLAUDE.md`。来自其他目录的上下文文件仍正常叠加。

Use context files for project conventions, commands, safety rules, and preferences. Disable loading with `--no-context-files` or `-nc`.
上下文文件用于项目约定、命令、安全规则和偏好。使用 `--no-context-files` 或 `-nc` 禁用加载。

### System Prompt Files
### 系统提示词文件

Replace the default system prompt with:
用以下文件替换默认系统提示词：

- `.pi/SYSTEM.md` for a project
- `.pi/SYSTEM.md` 用于项目
- `~/.pi/agent/SYSTEM.md` globally
- `~/.pi/agent/SYSTEM.md` 用于全局

Append to the default prompt without replacing it with `APPEND_SYSTEM.md` in either location.
在任一位置使用 `APPEND_SYSTEM.md` 可以追加到默认提示词而不替换它。

### Project Trust
### 项目信任

On interactive startup, pi asks before trusting a project folder that contains project-local settings, resources, or project `.agents/skills` and has no saved decision for the folder or a parent folder in `~/.pi/agent/trust.json`. Trusting a project allows pi to load `.pi/settings.json` and `.pi` resources, install missing project packages, and execute project extensions.
交互式启动时，如果一个项目文件夹包含项目本地设置、资源或项目 `.agents/skills`，且在 `~/.pi/agent/trust.json` 中没有针对该文件夹或父文件夹的已保存决定，pi 会在信任它之前询问。信任项目允许 pi 加载 `.pi/settings.json` 和 `.pi` 资源、安装缺失的项目包并执行项目扩展。

Before the trust decision, pi loads only context files, user/global extensions, and CLI `-e` extensions so they can handle the `project_trust` event. Project-local extensions, project package-managed extensions, and project settings are loaded only after the project is trusted. This split also applies when switching to a session from a different cwd whose trust has not been resolved in the current process.
在信任决定之前，pi 只加载上下文文件、用户/全局扩展和 CLI `-e` 扩展，以便它们能处理 `project_trust` 事件。项目本地扩展、项目包管理的扩展和项目设置只在项目被信任之后才加载。当切换到来自不同 cwd、且其信任尚未在当前进程中解析的会话时，这一划分同样适用。

Non-interactive modes (`-p`, `--mode json`, and `--mode rpc`) do not show a trust prompt. Without an applicable saved trust decision, they use `defaultProjectTrust` from global settings: `ask` (default) and `never` ignore those project resources, while `always` trusts them. Pass `--approve`/`-a` or `--no-approve`/`-na` to override project trust for one run.
非交互模式（`-p`、`--mode json` 和 `--mode rpc`）不显示信任提示。在没有适用的已保存信任决定时，它们使用全局设置中的 `defaultProjectTrust`：`ask`（默认）和 `never` 忽略这些项目资源，而 `always` 信任它们。可传入 `--approve`/`-a` 或 `--no-approve`/`-na` 为单次运行覆盖项目信任。

If no extension or saved decision applies, `defaultProjectTrust` controls the fallback behavior. Set it to `"ask"`, `"always"`, or `"never"` in `~/.pi/agent/settings.json`, or change it with `/settings`.
如果没有扩展或已保存决定适用，`defaultProjectTrust` 控制回退行为。在 `~/.pi/agent/settings.json` 中将其设为 `"ask"`、`"always"` 或 `"never"`，或用 `/settings` 修改。

`pi config` and package commands use the same project trust flow, except `pi update` never prompts. Pass `--approve` to trust project-local settings for one command or `--no-approve` to ignore them.
`pi config` 和包命令使用相同的项目信任流程，但 `pi update` 从不提示。传入 `--approve` 为单条命令信任项目本地设置，或 `--no-approve` 忽略它们。

Use `/trust` in interactive mode to save a project trust decision for future sessions, including trust for the immediate parent folder. It writes `~/.pi/agent/trust.json` only; the current session is not reloaded, so restart pi for changes to take effect.
在交互模式中使用 `/trust` 保存项目信任决定供未来会话使用，包括对直接父文件夹的信任。它只写入 `~/.pi/agent/trust.json`；当前会话不会重新加载，因此请重启 pi 以使更改生效。


## Exporting and Sharing Sessions
## 导出与分享会话

Use `/export [file]` to write a session to HTML.
使用 `/export [file]` 把会话写入 HTML。

Use `/share` to upload a private GitHub gist with a shareable HTML link.
使用 `/share` 上传私有 GitHub gist 并获得可分享的 HTML 链接。

If you use pi for open source work and want to publish sessions for model, prompt, tool, and evaluation research, see [`badlogic/pi-share-hf`](https://github.com/badlogic/pi-share-hf). It publishes sessions to Hugging Face datasets.
如果你用 pi 做开源工作，并想为模型、提示词、工具和评估研究发布会话，请参见 [`badlogic/pi-share-hf`](https://github.com/badlogic/pi-share-hf)。它把会话发布到 Hugging Face 数据集。

## CLI Reference
## CLI 参考

```bash
pi [options] [--] [@files...] [messages...]
```

### Package Commands
### 包命令

```bash
pi install <source> [-l]     # Install package, -l for project-local
pi remove <source> [-l]      # Remove package
pi uninstall <source> [-l]   # Alias for remove
pi update [source|self|pi]   # Update pi only, or one package source
pi update --all              # Update pi and packages; reconcile pinned git refs
pi update --extensions       # Update packages only; reconcile pinned git refs
pi update --models           # Refresh model catalogs only
pi update --self             # Update pi only
pi update --extension <src>  # Update one package
pi list                      # List installed packages
pi config                    # Enable/disable package resources
```

These commands manage pi packages and `pi update` can update the pi CLI installation. To uninstall pi itself, see [Quickstart](quickstart.md#uninstall). `pi config` and project package commands accept `--approve`/`--no-approve` to trust or ignore project-local settings for one command. `pi update` never prompts for project trust.
这些命令管理 pi 包，`pi update` 还可以更新 pi CLI 安装。要卸载 pi 本体，参见[快速开始](quickstart.md#uninstall)。`pi config` 和项目包命令接受 `--approve`/`--no-approve` 来为单条命令信任或忽略项目本地设置。`pi update` 从不为项目信任提示。

See [Pi Packages](packages.md) for package sources and security notes.
包来源与安全说明参见 [Pi 包](packages.md)。

### Modes
### 模式

| Flag | Description |
|------|-------------|
| default | Interactive mode |
| `-p`, `--print` | Print response and exit |
| `--mode json` | Output all events as JSON lines; see [JSON mode](json.md) |
| `--mode rpc` | RPC mode over stdin/stdout; see [RPC mode](rpc.md) |
| `--export <in> [out]` | Export a session to HTML |

| 标志 | 描述 |
|------|-------------|
| default | 交互模式 |
| `-p`, `--print` | 打印响应并退出 |
| `--mode json` | 把所有事件输出为 JSON 行；参见 [JSON 模式](json.md) |
| `--mode rpc` | 基于 stdin/stdout 的 RPC 模式；参见 [RPC 模式](rpc.md) |
| `--export <in> [out]` | 把会话导出为 HTML |


In print mode, pi also reads piped stdin and merges it into the initial prompt:
在打印模式下，pi 还会读取管道 stdin 并将其合并到初始提示中：

```bash
cat README.md | pi -p "Summarize this text"
```

### Model Options
### 模型选项

| Option | Description |
|--------|-------------|
| `--provider <name>` | Provider, such as `anthropic`, `openai`, or `google` |
| `--model <pattern>` | Model pattern or ID; supports `provider/id` and optional `:<thinking>` |
| `--api-key <key>` | API key, overriding environment variables |
| `--thinking <level>` | `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max` |
| `--models <patterns>` | Comma-separated patterns for Ctrl+P cycling |
| `--list-models [search]` | List available models |

| 选项 | 描述 |
|--------|-------------|
| `--provider <name>` | 提供商，如 `anthropic`、`openai` 或 `google` |
| `--model <pattern>` | 模型模式或 ID；支持 `provider/id` 和可选的 `:<thinking>` |
| `--api-key <key>` | API 密钥，覆盖环境变量 |
| `--thinking <level>` | `off`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max` |
| `--models <patterns>` | 用于 Ctrl+P 循环切换的逗号分隔模式 |
| `--list-models [search]` | 列出可用模型 |


### Session Options
### 会话选项

| Option | Description |
|--------|-------------|
| `-c`, `--continue` | Continue the most recent session |
| `-r`, `--resume` | Browse and select a session |
| `--session <path\|id>` | Use a specific session file or partial UUID |
| `--fork <path\|id>` | Fork a session file or partial UUID into a new session |
| `--session-dir <dir>` | Custom session storage directory |
| `--no-session` | Ephemeral mode; do not save |
| `--name <name>`, `-n <name>` | Set session display name at startup |

| 选项 | 描述 |
|--------|-------------|
| `-c`, `--continue` | 继续最近的会话 |
| `-r`, `--resume` | 浏览并选择会话 |
| `--session <path\|id>` | 使用特定的会话文件或部分 UUID |
| `--fork <path\|id>` | 把会话文件或部分 UUID 分叉为新会话 |
| `--session-dir <dir>` | 自定义会话存储目录 |
| `--no-session` | 临时模式；不保存 |
| `--name <name>`, `-n <name>` | 启动时设置会话显示名称 |


### Tool Options
### 工具选项

| Option | Description |
|--------|-------------|
| `--tools <list>`, `-t <list>` | Allowlist specific built-in, extension, and custom tools |
| `--exclude-tools <list>`, `-xt <list>` | Disable specific built-in, extension, and custom tools |
| `--no-builtin-tools`, `-nbt` | Disable built-in tools but keep extension/custom tools enabled |
| `--no-tools`, `-nt` | Disable all tools |

| 选项 | 描述 |
|--------|-------------|
| `--tools <list>`, `-t <list>` | 把特定的内置、扩展和自定义工具加入允许列表 |
| `--exclude-tools <list>`, `-xt <list>` | 禁用特定的内置、扩展和自定义工具 |
| `--no-builtin-tools`, `-nbt` | 禁用内置工具，但保持扩展/自定义工具启用 |
| `--no-tools`, `-nt` | 禁用所有工具 |


Built-in tools: `read`, `bash`, `powershell` (Windows), `edit`, `write`, `grep`, `find`, `ls`.
内置工具：`read`、`bash`、`powershell`（Windows）、`edit`、`write`、`grep`、`find`、`ls`。

### Resource Options
### 资源选项

| Option | Description |
|--------|-------------|
| `-e`, `--extension <source>` | Load an extension from path, npm, or git; repeatable |
| `--no-extensions` | Disable extension discovery |
| `--skill <path>` | Load a skill; repeatable |
| `--no-skills` | Disable skill discovery |
| `--prompt-template <path>` | Load a prompt template; repeatable |
| `--no-prompt-templates` | Disable prompt template discovery |
| `--theme <path>` | Load a theme; repeatable |
| `--no-themes` | Disable theme discovery |
| `--no-context-files`, `-nc` | Disable `AGENTS.md` and `CLAUDE.md` discovery |

| 选项 | 描述 |
|--------|-------------|
| `-e`, `--extension <source>` | 从路径、npm 或 git 加载扩展；可重复 |
| `--no-extensions` | 禁用扩展发现 |
| `--skill <path>` | 加载技能；可重复 |
| `--no-skills` | 禁用技能发现 |
| `--prompt-template <path>` | 加载提示词模板；可重复 |
| `--no-prompt-templates` | 禁用提示词模板发现 |
| `--theme <path>` | 加载主题；可重复 |
| `--no-themes` | 禁用主题发现 |
| `--no-context-files`, `-nc` | 禁用 `AGENTS.md` 和 `CLAUDE.md` 发现 |


Combine `--no-*` with explicit flags to load exactly what you need, ignoring settings. Example:
把 `--no-*` 与显式标志组合可以精确加载所需内容并忽略设置。示例：

```bash
pi --no-extensions -e ./my-extension.ts
```

### Other Options
### 其他选项

| Option | Description |
|--------|-------------|
| `--system-prompt <text>` | Replace default prompt; context files and skills are still appended |
| `--append-system-prompt <text>` | Append to system prompt |
| `--tui-mode <mode>` | TUI mode: `regular` (default) or experimental `fullscreen` |
| `--use-theme <name[/name]>` | Set the initial interactive theme for this run without changing settings |
| `--verbose` | Force verbose startup |
| `-a`, `--approve` | Trust project-local files for this run |
| `-na`, `--no-approve` | Ignore project-local files for this run |
| `--` | Stop option parsing; remaining arguments are prompts or `@file` inputs |
| `-h`, `--help` | Show help |
| `-v`, `--version` | Show version |

| 选项 | 描述 |
|--------|-------------|
| `--system-prompt <text>` | 替换默认提示词；上下文文件和技能仍会追加 |
| `--append-system-prompt <text>` | 追加到系统提示词 |
| `--tui-mode <mode>` | TUI 模式：`regular`（默认）或实验性的 `fullscreen` |
| `--use-theme <name[/name]>` | 为本次运行设置初始交互主题，而不更改设置 |
| `--verbose` | 强制详细启动输出 |
| `-a`, `--approve` | 为本次运行信任项目本地文件 |
| `-na`, `--no-approve` | 为本次运行忽略项目本地文件 |
| `--` | 停止选项解析；其余参数是提示词或 `@file` 输入 |
| `-h`, `--help` | 显示帮助 |
| `-v`, `--version` | 显示版本 |


In `fullscreen` mode, the transcript scrolls inside the terminal viewport while queued messages, working status, extension widgets, editor, and footer remain fixed at the bottom. Mouse/trackpad input scrolls the region under the pointer; keyboard viewport actions always remain available. Inline images work in terminals that support the Kitty graphics protocol, including Kitty and Ghostty. In iTerm2 they render as text placeholders because its inline-image protocol cannot delete or crop placements during application-owned scrolling. In `regular` mode, pi uses the main screen and terminal-owned scrollback, and iTerm2 inline images continue to render normally. See [Terminal setup](terminal-setup.md) for terminal-specific settings and workarounds.
在 `fullscreen` 模式下，对话记录在终端视口内滚动，而排队的消息、工作状态、扩展组件、编辑器和页脚固定在底部。鼠标/触控板输入滚动指针下的区域；键盘视口操作始终可用。内联图片在支持 Kitty 图形协议的终端中可用，包括 Kitty 和 Ghostty。在 iTerm2 中它们渲染为文本占位符，因为其内联图片协议无法在应用持有的滚动过程中删除或裁剪放置。在 `regular` 模式下，pi 使用主屏幕和终端自有的回滚缓冲区，iTerm2 内联图片继续正常渲染。终端特定的设置与变通方法参见[终端设置](terminal-setup.md)。

Set **TUI mode** in `/settings` to switch between `regular` and `fullscreen` immediately and choose the default for future sessions. **Fullscreen exit output** controls whether exiting fullscreen prints the final transcript or restores the previous screen and prints only the session resume hint.
在 `/settings` 中设置 **TUI mode** 可立即在 `regular` 和 `fullscreen` 之间切换，并选择未来会话的默认值。**Fullscreen exit output** 控制退出全屏时是打印最终对话记录，还是恢复之前的屏幕并只打印会话恢复提示。

### File Arguments
### 文件参数

Prefix files with `@` to include them in the message:
给文件加 `@` 前缀以将其包含在消息中：

```bash
pi @prompt.md "Answer this"
pi -p @screenshot.png "What's in this image?"
pi @code.ts @test.ts "Review these files"
```

### Examples
### 示例

```bash
# Interactive with initial prompt
pi "List all .ts files in src/"

# Non-interactive
pi -p "Summarize this codebase"

# Prompt beginning with a dash
pi -p -- "- Summarize these points"

# Non-interactive with piped stdin
cat README.md | pi -p "Summarize this text"

# Named one-shot session
pi --name "release audit" -p "Audit this repository"

# Different model
pi --provider openai --model gpt-4o "Help me refactor"

# Model with provider prefix
pi --model openai/gpt-4o "Help me refactor"

# Model with thinking level shorthand
pi --model sonnet:high "Solve this complex problem"

# Limit model cycling
pi --models "claude-*,gpt-4o"

# Read-only mode
pi --tools read,grep,find,ls -p "Review the code"

# Disable one extension or built-in tool while keeping the rest available
pi --exclude-tools ask_question
```

## Design Principles
## 设计原则

Pi keeps the core small and pushes workflow-specific behavior into extensions, skills, prompt templates, and packages.
Pi 保持核心精简，把工作流特定的行为推入扩展、技能、提示词模板和包中。

It intentionally does not include built-in MCP, sub-agents, permission popups, plan mode, to-dos, or background bash. You can build or install those workflows as extensions or packages, or use external tools such as containers and tmux.
它有意不包含内置的 MCP、子代理、权限弹窗、计划模式、待办事项或后台 bash。你可以把这些工作流构建或安装为扩展或包，或使用容器和 tmux 等外部工具。

For the full rationale, read the [blog post](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/).
完整的理念阐述请阅读[博客文章](https://mariozechner.at/posts/2025-11-30-pi-coding-agent/)。
