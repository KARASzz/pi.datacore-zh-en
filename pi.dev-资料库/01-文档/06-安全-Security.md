> 📄 来源 Source: https://pi.dev/docs/latest/security
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Security
# 安全

Pi is a local coding agent. It runs with the permissions of the user account that starts it, and it treats files writable by that user as inside the same local trust boundary.
Pi 是一个本地编码代理。它以启动它的用户账户的权限运行，并将该用户可写的文件视为处于同一本地信任边界之内。

## Project Trust
## 项目信任

Project trust controls whether pi loads project-local settings, resources, packages, and extensions. It is not a sandbox and it does not restrict what the model can ask tools to do after you start working in a directory.
项目信任控制 pi 是否加载项目本地的设置、资源、包和扩展。它不是沙箱，也不会在你于某个目录中开始工作后限制模型可以让工具去做什么。

Pi considers a project to have resources that require trust when it finds any of these from the current working directory:
当 pi 从当前工作目录发现以下任意一项时，即认为该项目拥有需要信任的资源：

- `.pi/settings.json`
- `.pi/settings.json`
- `.pi/extensions`, `.pi/skills`, `.pi/prompts`, or `.pi/themes`
- `.pi/extensions`、`.pi/skills`、`.pi/prompts` 或 `.pi/themes`
- `.pi/SYSTEM.md` or `.pi/APPEND_SYSTEM.md`
- `.pi/SYSTEM.md` 或 `.pi/APPEND_SYSTEM.md`
- project `.agents/skills` in the current directory or an ancestor directory
- 当前目录或祖先目录中项目的 `.agents/skills`

A bare `.pi` directory does not count as a project resource that requires trust.
仅有空目录 `.pi` 并不算作需要信任的项目资源。

When an interactive session starts in a project with resources that require trust and no saved decision for the current directory or a parent directory, pi follows `defaultProjectTrust` from global settings. The default value is `"ask"`, which asks whether to trust the project when UI is available. Saved decisions are stored by canonical directory in `~/.pi/agent/trust.json`, and the closest saved decision on the current or parent path applies before the global default.
当交互式会话在一个拥有需信任资源、且当前目录或父目录没有已保存决定的项目中启动时，pi 会遵循全局设置中的 `defaultProjectTrust`。默认值为 `"ask"`，即在 UI 可用时询问是否信任该项目。已保存的决定按规范化目录存储在 `~/.pi/agent/trust.json` 中，当前或父路径上最近保存的决定优先于全局默认值。

Trusting a project allows pi to load project resources that require trust, including:
信任一个项目会允许 pi 加载该项目中需要信任的资源，包括：

- `.pi/settings.json`
- `.pi/settings.json`
- `.pi` resources such as extensions, skills, prompt templates, themes, and system prompt files
- `.pi` 资源，例如扩展、技能、提示词模板、主题和系统提示词文件
- missing project packages configured through project settings
- 通过项目设置配置的缺失项目包
- project-local extensions and project package-managed extensions
- 项目本地扩展和由项目包管理的扩展

Declining trust skips protected resources. Context files such as `AGENTS.override.md`, `AGENTS.md`, and `CLAUDE.md` are loaded regardless of project trust unless context loading is disabled. Before trust is resolved, pi only loads context files, user/global extensions, and CLI `-e` extensions. User/global and CLI extensions can handle the `project_trust` event; the first extension that returns a yes/no decision owns the decision.
拒绝信任会跳过受保护的资源。诸如 `AGENTS.override.md`、`AGENTS.md` 和 `CLAUDE.md` 之类的上下文文件无论如何都会加载，除非禁用了上下文加载。在信任被解析之前，pi 只加载上下文文件、用户/全局扩展和 CLI `-e` 扩展。用户/全局扩展和 CLI 扩展可以处理 `project_trust` 事件；第一个返回是/否决定的扩展拥有该决定权。

Non-interactive modes (`-p`, `--mode json`, and `--mode rpc`) do not show a trust prompt. Without an applicable saved trust decision, `defaultProjectTrust: "ask"` and `"never"` ignore such resources, while `"always"` trusts them. Use `--approve`/`-a` or `--no-approve`/`-na` to override project trust for one run.
非交互模式（`-p`、`--mode json` 和 `--mode rpc`）不显示信任提示。在没有适用的已保存信任决定时，`defaultProjectTrust: "ask"` 和 `"never"` 会忽略这些资源，而 `"always"` 则信任它们。可使用 `--approve`/`-a` 或 `--no-approve`/`-na` 为单次运行覆盖项目信任。

## No Built-in Sandbox
## 无内置沙箱

Pi does not include a built-in sandbox. Built-in tools can read files, write files, edit files, and run shell commands with the permissions of the pi process. Extensions are TypeScript modules that run with the same permissions. Package installs, shell commands, language servers, test commands, and other developer tools behave as ordinary local processes.
Pi 不包含内置沙箱。内置工具可以以 pi 进程的权限读取文件、写入文件、编辑文件和运行 shell 命令。扩展是以相同权限运行的 TypeScript 模块。包安装、shell 命令、语言服务器、测试命令以及其他开发工具都表现为普通的本地进程。

This is intentional. Pi is designed to operate on local source trees, invoke project toolchains, and integrate with the user's existing development environment. A partial in-process sandbox would be easy to misunderstand as a security boundary while still depending on the host shell, filesystem, package managers, credentials, and extension code. Real isolation needs to come from the operating system or a virtualization/container boundary.
这是有意为之。Pi 的设计目标是在本地源码树上操作、调用项目工具链并与用户现有的开发环境集成。一个部分的进程内沙箱容易被误解为安全边界，而它仍然依赖宿主 shell、文件系统、包管理器、凭据和扩展代码。真正的隔离需要来自操作系统或虚拟化/容器边界。

Project trust is only an input-loading guard. It prevents a repository from silently changing pi's settings or extensions before you approve it. It does not make untrusted code, untrusted prompts, or untrusted model output safe. Prompt injection from repository files, comments, documentation, context files, or build output is expected local-agent risk and cannot be reliably prevented by pi.
项目信任只是一个输入加载守卫。它防止一个仓库在你批准之前悄悄更改 pi 的设置或扩展。它不会让不受信任的代码、不受信任的提示词或模型输出变得安全。来自仓库文件、注释、文档、上下文文件或构建输出的提示词注入是本地代理的预期风险，pi 无法可靠地阻止。

## Running Untrusted or Unmonitored Work
## 运行不受信任或无人监督的工作

For untrusted repositories, generated code you do not intend to monitor closely, or unattended automation, run pi in a contained environment. Use a container, VM, micro-VM, remote sandbox, or policy-controlled sandbox with only the files and credentials required for the task.
对于不受信任的仓库、你不打算密切监督的生成代码或无人值守的自动化，请在受控环境中运行 pi。使用容器、虚拟机、微型虚拟机（micro-VM）、远程沙箱或策略受控的沙箱，只提供任务所需的文件和凭据。

Common patterns are documented in [Containerization](containerization.md):
[容器化](containerization.md)文档中记录了常见模式：

- run the whole `pi` process inside a container/sandbox
- 在容器/沙箱内运行整个 `pi` 进程
- run host pi while routing built-in tool execution into a Gondolin micro-VM
- 运行宿主 pi，同时将内置工具的执行路由到 Gondolin 微型虚拟机中
- mount only the workspace paths the agent should access
- 只挂载代理应访问的工作区路径
- avoid mounting host `~/.pi/agent` unless the container should access host sessions, settings, and credentials
- 避免挂载宿主的 `~/.pi/agent`，除非容器需要访问宿主的会话、设置和凭据
- pass the minimum required API keys or use short-lived credentials
- 只传递所需最低限度的 API 密钥，或使用短期凭据
- restrict network access when the task does not need it
- 在任务不需要网络时限制网络访问
- review diffs and outputs before copying results back to trusted systems
- 在把结果复制回受信任系统之前审查差异与输出

If you bind-mount a host workspace read/write, writes from inside the container or VM can still modify host files. Use read-only mounts or copy files into and out of the sandbox when you need stronger protection from unintended writes.
如果你以读写方式绑定挂载宿主工作区，来自容器或虚拟机内部的写入仍然可以修改宿主文件。当你需要更强保护以防意外写入时，请使用只读挂载，或在沙箱中复制文件进出。

## Reporting Security Issues
## 报告安全问题

To report a security issue, follow the repository [Security Policy](https://github.com/earendil-works/pi-mono/blob/main/SECURITY.md). Do not open a public issue for security-sensitive reports.
要报告安全问题，请遵循仓库的[安全策略](https://github.com/earendil-works/pi-mono/blob/main/SECURITY.md)。请勿为安全敏感的报告公开开 issue。

Expected local-agent behavior, lack of a built-in sandbox, prompt injection from untrusted content, and behavior of user-installed extensions or skills are generally outside the security boundary unless the report demonstrates a real privilege-boundary bypass or shows how pi grants access that the local user did not already have.
预期的本地代理行为、缺少内置沙箱、来自不受信任内容的提示词注入以及用户安装的扩展或技能的行为，一般都在安全边界之外，除非报告演示了真实的特权边界绕过，或展示了 pi 如何授予本地用户原本没有的访问权限。
