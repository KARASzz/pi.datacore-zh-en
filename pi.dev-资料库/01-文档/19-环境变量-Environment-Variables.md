> 📄 来源 Source: https://pi.dev/docs/latest/environment-variables
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Environment Variables
# 环境变量

Pi uses environment variables in three ways:
Pi 以三种方式使用环境变量：

- Variables such as `PI_OFFLINE` configure the Pi process.
- 诸如 `PI_OFFLINE` 之类的变量用于配置 Pi 进程。
- Pi sets process markers so child processes can identify Pi as the launching agent.
- Pi 设置进程标记，让子进程能识别出 Pi 是启动它的代理。
- Commands run by the LLM-callable shell tools receive `PI_*` variables describing the current session.
- LLM 可调用的 shell 工具所运行的命令会收到描述当前会话的 `PI_*` 变量。

Provider API-key variables are documented separately in [Providers](providers.md#environment-variables-or-auth-file).
提供商 API 密钥变量在[提供商](providers.md#environment-variables-or-auth-file)中单独说明。

## Process Marker
## 进程标记

The CLI and RPC entry points set two process markers:
CLI 和 RPC 入口会设置两个进程标记：

- `AI_AGENT=pi` is a generic marker that lets tooling identify Pi as the agent that launched the process.
- `AI_AGENT=pi` 是一个通用标记，让工具链能把 Pi 识别为启动该进程的代理。
- `PI_CODING_AGENT=true` is Pi-specific and lets child processes detect that they run inside Pi.
- `PI_CODING_AGENT=true` 是 Pi 专属的标记，让子进程能检测到自己运行在 Pi 内部。

Child processes inherit both markers. They are not session-specific and are not set automatically when Pi is embedded through the SDK.
子进程会继承这两个标记。它们与会话无关，并且在 Pi 通过 SDK 嵌入时不会自动设置。

## Shell Tool Session Environment
## Shell 工具会话环境

Commands run by the `bash` and `powershell` tools receive the current Pi session state:
`bash` 和 `powershell` 工具运行的命令会收到当前的 Pi 会话状态：

| Variable | Description |
|----------|-------------|
| `PI_SESSION_ID` | Current session ID |
| `PI_SESSION_FILE` | Absolute path to the current session JSONL file; unset for ephemeral sessions |
| `PI_PROVIDER` | Currently selected model provider |
| `PI_MODEL` | Currently selected model ID |
| `PI_REASONING_LEVEL` | Current effective reasoning level: `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, or `max` |

| 变量 | 描述 |
|----------|-------------|
| `PI_SESSION_ID` | 当前会话 ID |
| `PI_SESSION_FILE` | 当前会话 JSONL 文件的绝对路径；临时（ephemeral）会话不设置 |
| `PI_PROVIDER` | 当前选择的模型提供商 |
| `PI_MODEL` | 当前选择的模型 ID |
| `PI_REASONING_LEVEL` | 当前的有效推理等级：`off`、`minimal`、`low`、`medium`、`high`、`xhigh` 或 `max` |


The values are resolved when each command starts. Switching models or changing the reasoning level therefore affects the next shell command without restarting Pi. `PI_PROVIDER` and `PI_MODEL` identify the selected Pi model, not a different upstream model that a router may choose internally.
这些值在每条命令启动时解析。因此切换模型或更改推理等级会影响下一条 shell 命令，而无需重启 Pi。`PI_PROVIDER` 和 `PI_MODEL` 标识的是所选的 Pi 模型，而不是路由器内部可能选择的其他上游模型。

When asked which model or provider is running, inspect these variables instead of inferring the answer from the system prompt:
当被问到正在运行哪个模型或提供商时，请检查这些变量，而不是从系统提示词中推断答案：

```bash
printf '%s/%s\n' "$PI_PROVIDER" "$PI_MODEL"
printf 'reasoning=%s session=%s\n' "$PI_REASONING_LEVEL" "$PI_SESSION_ID"
```

The session file can be inspected directly when the session is persistent:
会话为持久化时，可以直接检查会话文件：

```bash
if [ -n "$PI_SESSION_FILE" ]; then
  tail -n 1 "$PI_SESSION_FILE"
fi
```

These variables are injected into the LLM-callable `bash` and `powershell` tools. They are not injected into user-entered `!` or `!!` commands.
这些变量会被注入到 LLM 可调用的 `bash` 和 `powershell` 工具中。它们不会注入到用户输入的 `!` 或 `!!` 命令中。

### Custom Shell Tools
### 自定义 Shell 工具

Tools created with `createBashTool()` or `createPowerShellTool()` expose the session environment by default when registered with Pi. Injection happens before `spawnHook`, so a hook receives the variables in `ctx.env`:
用 `createBashTool()` 或 `createPowerShellTool()` 创建的工具在向 Pi 注册时默认会暴露会话环境。注入发生在 `spawnHook` 之前，因此钩子会在 `ctx.env` 中收到这些变量：

```typescript
const bashTool = createBashTool(cwd, {
  spawnHook: (ctx) => ({
    ...ctx,
    env: { ...ctx.env, CI: "1" },
  }),
});
```

Disable session metadata independently of the spawn hook:
独立于 spawn 钩子禁用会话元数据：

```typescript
const powershellTool = createPowerShellTool(cwd, {
  exposeSessionEnvironment: false,
  spawnHook: (ctx) => ctx,
});
```

When disabled, Pi removes inherited values for these variables so nested Pi processes do not expose stale parent-session metadata.
禁用后，Pi 会移除这些变量的继承值，这样嵌套的 Pi 进程就不会暴露过期的父会话元数据。

## Pi Process Configuration
## Pi 进程配置

These variables are read by Pi itself:
这些变量由 Pi 自身读取：

| Variable | Description |
|----------|-------------|
| `PI_CODING_AGENT_DIR` | Override the config directory; default is `~/.pi/agent` |
| `PI_CODING_AGENT_SESSION_DIR` | Override session storage; overridden by `--session-dir` |
| `PI_PACKAGE_DIR` | Override the package directory, useful for Nix/Guix store paths |
| `PI_OFFLINE` | Disable startup network operations, including update checks, package updates, and install/update telemetry |
| `PI_SKIP_VERSION_CHECK` | Disable the `pi.dev` latest-version request |
| `PI_TELEMETRY` | Override install/update telemetry and provider attribution headers: `1`/`true`/`yes` or `0`/`false`/`no` |
| `PI_CACHE_RETENTION` | Set to `long` for extended provider prompt caching where supported |
| `PI_SHARE_VIEWER_URL` | Override the base URL used by `/share` |
| `PI_HARDWARE_CURSOR` | Set to `1` to show the hardware cursor; see [Terminal setup](terminal-setup.md) |
| `PI_HYPERLINKS` | Override OSC 8 hyperlink detection with `1`, `0`, or `auto` |
| `PI_IMAGE_PROTOCOL` | Override inline image detection with `kitty`, `iterm2`, `none`, or `auto` |
| `PI_TRUE_COLOR` | Override truecolor detection with `1`, `0`, or `auto` |
| `PI_TUI_ESC_TIMEOUT` | How long to wait after a lone ESC before treating it as Escape, in milliseconds; defaults to `100` over SSH and `10` otherwise. Increase if Alt-key input is misread as Escape |
| `VISUAL`, `EDITOR` | External editor fallback when `externalEditor` is unset |
| `HTTP_PROXY`, `HTTPS_PROXY` | Proxy outbound HTTP requests |

| 变量 | 描述 |
|----------|-------------|
| `PI_CODING_AGENT_DIR` | 覆盖配置目录；默认为 `~/.pi/agent` |
| `PI_CODING_AGENT_SESSION_DIR` | 覆盖会话存储；会被 `--session-dir` 覆盖 |
| `PI_PACKAGE_DIR` | 覆盖包目录，对 Nix/Guix store 路径很有用 |
| `PI_OFFLINE` | 禁用启动时的网络操作，包括更新检查、包更新和安装/更新遥测 |
| `PI_SKIP_VERSION_CHECK` | 禁用对 `pi.dev` 最新版本的请求 |
| `PI_TELEMETRY` | 覆盖安装/更新遥测和提供商归因标头：`1`/`true`/`yes` 或 `0`/`false`/`no` |
| `PI_CACHE_RETENTION` | 在受支持时设为 `long` 以使用扩展的提供商提示词缓存 |
| `PI_SHARE_VIEWER_URL` | 覆盖 `/share` 使用的基础 URL |
| `PI_HARDWARE_CURSOR` | 设为 `1` 以显示硬件光标；参见[终端设置](terminal-setup.md) |
| `PI_HYPERLINKS` | 用 `1`、`0` 或 `auto` 覆盖 OSC 8 超链接检测 |
| `PI_IMAGE_PROTOCOL` | 用 `kitty`、`iterm2`、`none` 或 `auto` 覆盖内联图像检测 |
| `PI_TRUE_COLOR` | 用 `1`、`0` 或 `auto` 覆盖真彩色检测 |
| `PI_TUI_ESC_TIMEOUT` | 单独的 ESC 之后等待多久才视作 Escape，单位毫秒；SSH 下默认 `100`，其他情况为 `10`。如果 Alt 键输入被误读为 Escape，请调大该值 |
| `VISUAL`, `EDITOR` | `externalEditor` 未设置时的外部编辑器后备 |
| `HTTP_PROXY`, `HTTPS_PROXY` | 为出站 HTTP 请求设置代理 |


Provider credentials such as `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, and cloud-provider configuration are listed in [Providers](providers.md#environment-variables-or-auth-file).
诸如 `ANTHROPIC_API_KEY`、`OPENAI_API_KEY` 之类的提供商凭据和云提供商配置在[提供商](providers.md#environment-variables-or-auth-file)中列出。
