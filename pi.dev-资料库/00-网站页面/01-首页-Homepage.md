# Pi 编码代理（Pi Coding Agent）
> 📄 来源 Source: https://pi.dev/
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译。

# There are many agent harnesses but this one is yours
# 世上有许多代理框架（agent harness），但这一个属于你

Pi is a minimal agent harness. Adapt Pi to your workflows, not the other way around.
Pi 是一个极简的代理框架。让 Pi 适应你的工作流，而不是反过来。

Install commands (tabs: curl / PowerShell / npm / pnpm / npm / bun):
安装命令（标签页：curl / PowerShell / npm / pnpm / npm / bun）：

```
curl -fsSL https://pi.dev/install.sh | sh
powershell -c "irm https://pi.dev/install.ps1 | iex"
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
pnpm add -g --ignore-scripts @earendil-works/pi-coding-agent
bun add -g --ignore-scripts @earendil-works/pi-coding-agent
```

$ scroll to continue
$ 向下滚动继续

Pi - Make it yours
Pi - 让它成为你的

Crooked mode: ON
歪斜模式：开启

Revert
还原

## Why Pi?
## 为什么选择 Pi？

Pi - manipulate the website
Pi - 操纵本网站

Pi is a minimal agent harness. Adapt Pi to your workflows, not the other way around. Customize Pi with extensions, skills, prompt templates, and themes. Bundle them as Pi packages and share via npm or git.
Pi 是一个极简的代理框架。让 Pi 适应你的工作流，而不是反过来。通过扩展、技能、提示词模板和主题定制 Pi。把它们打包为 Pi 包，通过 npm 或 git 分享。

Pi ships with powerful defaults but skips features like sub-agents and plan mode. Ask Pi to build what you want, or install a package that does it your way.
Pi 自带强大的默认配置，但刻意省略了子代理（sub-agents）和计划模式之类的功能。让 Pi 构建你想要的东西，或安装一个按你的方式做事的包。

Four modes: interactive, print/JSON, RPC, and SDK. See OpenClaw for a real-world integration.
四种模式：交互式、打印/JSON、RPC 和 SDK。真实集成示例参见 OpenClaw。

Read the documentation
阅读文档

## Change the harness, not your workflow
## 改变框架，而不是你的工作流

Pi - Build a custom workflow extension
Pi - 构建自定义工作流扩展

Pi isn't a sealed product. If you need a command, tool, provider, workflow, or UI tweak, just ask Pi to build it. It will customize itself on the fly.
Pi 不是一个封闭的产品。如果你需要某个命令、工具、提供商、工作流或 UI 调整，直接让 Pi 去构建。它会即时完成自我定制。

Have Pi manipulate itself in place, hit `/reload`, and keep going. If you think others will find what you built useful, share it!
让 Pi 原地修改自身，按下 `/reload`，然后继续。如果你觉得你构建的东西对他人有用，分享出来吧！

## 15+ providers, hundreds of models
## 15+ 提供商，数百个模型

Pi - Switch models mid-session
Pi - 会话中途切换模型

Anthropic, OpenAI, Google, Azure, Bedrock, Mistral, Groq, Cerebras, xAI, Hugging Face, Kimi For Coding, MiniMax, NVIDIA, OpenRouter, Ollama, and more. Authenticate via API keys or OAuth.
Anthropic、OpenAI、Google、Azure、Bedrock、Mistral、Groq、Cerebras、xAI、Hugging Face、Kimi For Coding、MiniMax、NVIDIA、OpenRouter、Ollama 等。通过 API 密钥或 OAuth 认证。

Switch models mid-session with `/model` or `Ctrl+L`. Cycle through your favorites with `Ctrl+P`.
用 `/model` 或 `Ctrl+L` 在会话中途切换模型。用 `Ctrl+P` 在你收藏的模型之间循环切换。

Add custom providers and models via models.json or extensions.
通过 models.json 或扩展添加自定义提供商和模型。
## Tree-structured, shareable history
## 树状结构、可分享的历史

Pi - Branch and share a session tree
Pi - 分支并分享会话树

Sessions are stored as trees. Use `/tree` to navigate to any previous point and continue from there. All branches live in a single file. Filter by message type, label entries as bookmarks.
会话以树的形式存储。使用 `/tree` 导航到之前任意一点并从那里继续。所有分支都在同一个文件中。按消息类型过滤，把条目标记为书签。

Export to HTML with `/export`, or upload to a GitHub gist with `/share` and get a shareable URL that renders it. Example session.
用 `/export` 导出为 HTML，或用 `/share` 上传到 GitHub gist 并获得可渲染它的分享链接。示例会话。

## Context engineering
## 上下文工程

Pi - Load project skills and instructions
Pi - 加载项目技能与指令

Pi's minimal system prompt and extensibility let you do actual context engineering. Control what goes into the context window and how it's managed.
Pi 的极简系统提示词和可扩展性让你能做真正的上下文工程。控制什么进入上下文窗口，以及如何管理它。

AGENTS.md: Project instructions loaded at startup from `~/.pi/agent/`, parent directories, and the current directory.
AGENTS.md：项目指令，启动时从 `~/.pi/agent/`、父目录和当前目录加载。

SYSTEM.md: Replace or append to the default system prompt per-project.
SYSTEM.md：按项目替换或追加默认系统提示词。

Compaction: Auto-summarizes older messages when approaching the context limit. Fully customizable via extensions: implement topic-based compaction, code-aware summaries, or use different summarization models.
压缩（Compaction）：接近上下文上限时自动摘要较旧的消息。可通过扩展完全自定义：实现基于主题的压缩、代码感知摘要，或使用不同的摘要模型。

Skills: Capability packages with instructions and tools, loaded on-demand. Progressive disclosure without busting the prompt cache. See skills.
技能（Skills）：带指令和工具的能力包，按需加载。在不破坏提示词缓存的前提下实现渐进式披露。参见技能文档。

Prompt templates: Reusable prompts as Markdown files. Type `/name` to expand. See prompt templates.
提示词模板：以 Markdown 文件形式存在的可复用提示词。输入 `/name` 展开。参见提示词模板文档。

Dynamic context: Extensions can inject messages before each turn, filter the message history, implement RAG, or build long-term memory.
动态上下文：扩展可以在每轮之前注入消息、过滤消息历史、实现 RAG，或构建长期记忆。

## Steer or follow up
## 转向（Steer）或跟进（Follow up）

Pi - Steer a running agent
Pi - 转向一个正在运行的代理

Submit messages while the agent works. `Enter` sends a steering message (delivered after current tool, interrupts remaining tools). `Alt+Enter` sends a follow-up (waits until the agent finishes).
在代理工作时提交消息。`Enter` 发送转向消息（在当前工具完成后送达，中断其余工具）。`Alt+Enter` 发送跟进消息（等待代理完成后再送达）。

## Four modes
## 四种模式

Pi - Generate a shell script in print mode
Pi - 在打印模式下生成 shell 脚本

Interactive: The full TUI experience.
交互式（Interactive）：完整的 TUI 体验。

Print/JSON: `pi -p "query"` for scripts, `--mode json` for event streams.
打印/JSON：脚本用 `pi -p "query"`，事件流用 `--mode json`。

RPC: JSON protocol over stdin/stdout for non-Node integrations. See docs/rpc.md.
RPC：通过 stdin/stdout 的 JSON 协议，用于非 Node 集成。参见 docs/rpc.md。

SDK: Embed Pi in your apps. See OpenClaw for a real-world example.
SDK：把 Pi 嵌入你的应用。真实示例参见 OpenClaw。

## Primitives, not features
## 提供原语，而非堆砌功能

Pi - Install a third-party extension
Pi - 安装第三方扩展

Features that other agents bake in, you can build yourself. Extensions are TypeScript modules with access to tools, commands, keyboard shortcuts, events, and the full TUI.
其他代理内置的功能，你可以自己构建。扩展是 TypeScript 模块，可以访问工具、命令、键盘快捷键、事件和完整的 TUI。

Sub-agents, plan mode, permission gates, path protection, SSH execution, sandboxing, MCP integration, custom editors, status bars, overlays.
子代理、计划模式、权限门、路径保护、SSH 执行、沙箱、MCP 集成、自定义编辑器、状态栏、浮层。

Don't want to build it? Ask Pi to build it for you. Or install a package that does it your way. See the 50+ examples.
不想自己构建？让 Pi 替你构建。或者安装一个按你的方式做事的包。参见 50 多个示例。

## Intentionally minimal
## 有意保持极简

There is no built-in MCP, no sub-agents, no permission popups, no plan mode, no to-do lists.
没有内置的 MCP，没有子代理，没有权限弹窗，没有计划模式，没有待办清单。

### No built-in MCP
### 没有内置 MCP

Install pi-mcp-adapter, or build MCP integration with full visibility into tool calls and responses.
安装 pi-mcp-adapter，或自行构建 MCP 集成，并完整掌控工具调用与响应。

### No sub-agents
### 没有子代理

Install pi-subagents, or build your own orchestration on the SDK.
安装 pi-subagents，或在 SDK 上构建你自己的编排。

### No plan mode
### 没有计划模式

Write plans to files, or build it with extensions, or install a package.
把计划写入文件，或用扩展构建，或安装一个包。

### No built-in to-dos
### 没有内置待办

Use a TODO.md file, or build your own with extensions.
使用 TODO.md 文件，或用扩展构建你自己的。

### No background bash
### 没有后台 bash

Use tmux. Full observability, direct interaction.
使用 tmux。完全可观察，可直接交互。

## Get involved with Pi
## 参与到 Pi 中

### Issues
### 问题（Issues）

GitHub for bugs and features.
GitHub 用于提交 bug 和功能请求。

### Discord
### Discord

Community server for discussion and sharing.
用于讨论和分享的社区服务器。

### Documentation
### 文档

Read the documentation or browse the source on GitHub.
阅读文档，或在 GitHub 上浏览源码。