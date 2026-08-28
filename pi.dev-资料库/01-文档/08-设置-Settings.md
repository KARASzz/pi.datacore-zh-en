> 📄 来源 Source: https://pi.dev/docs/latest/settings
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Settings
# 设置

Pi uses JSON settings files with project settings overriding global settings.
Pi 使用 JSON 设置文件，项目设置覆盖全局设置。

| Location | Scope |
|----------|-------|
| `~/.pi/agent/settings.json` | Global (all projects) |
| `.pi/settings.json` | Project (current directory) |

| 位置 | 作用范围 |
|----------|-------|
| `~/.pi/agent/settings.json` | 全局（所有项目） |
| `.pi/settings.json` | 项目（当前目录） |


Edit directly or use `/settings` for common options. To save startup model defaults interactively, use `/model` and press Ctrl+S on the desired model. To save the startup thinking level, use `/thinking` and press Ctrl+S.
可以直接编辑，或用 `/settings` 配置常用选项。要以交互方式保存启动模型默认值，使用 `/model` 并在目标模型上按 Ctrl+S。要保存启动思考等级，使用 `/thinking` 并按 Ctrl+S。

## Project Trust
## 项目信任

On interactive startup, pi asks before trusting a project folder that contains project-local settings, resources, or project `.agents/skills` and has no saved decision for the folder or a parent folder in `~/.pi/agent/trust.json`. Trusting a project allows pi to load `.pi/settings.json` and `.pi` resources, install missing project packages, and execute project extensions.
交互式启动时，如果一个项目文件夹包含项目本地设置、资源或项目 `.agents/skills`，且在 `~/.pi/agent/trust.json` 中没有针对该文件夹或父文件夹的已保存决定，pi 会在信任它之前询问。信任项目允许 pi 加载 `.pi/settings.json` 和 `.pi` 资源、安装缺失的项目包并执行项目扩展。

Non-interactive modes (`-p`, `--mode json`, and `--mode rpc`) do not show a trust prompt. Without an applicable saved trust decision, they use `defaultProjectTrust` from global settings: `ask` (default) and `never` ignore those project resources, while `always` trusts them. Pass `--approve`/`-a` or `--no-approve`/`-na` to override project trust for one run.
非交互模式（`-p`、`--mode json` 和 `--mode rpc`）不显示信任提示。在没有适用的已保存信任决定时，它们使用全局设置中的 `defaultProjectTrust`：`ask`（默认）和 `never` 忽略这些项目资源，而 `always` 信任它们。可传入 `--approve`/`-a` 或 `--no-approve`/`-na` 为单次运行覆盖项目信任。

If no extension or saved decision applies, `defaultProjectTrust` controls the fallback behavior. Set it to `"ask"`, `"always"`, or `"never"` in `~/.pi/agent/settings.json`, or change it with `/settings`.
如果没有扩展或已保存决定适用，`defaultProjectTrust` 控制回退行为。在 `~/.pi/agent/settings.json` 中将其设为 `"ask"`、`"always"` 或 `"never"`，或用 `/settings` 修改。

`pi config` and package commands use the same project trust flow, except `pi update` never prompts. Pass `--approve` to trust project-local settings for one command or `--no-approve` to ignore them.
`pi config` 和包命令使用相同的项目信任流程，但 `pi update` 从不提示。传入 `--approve` 为单条命令信任项目本地设置，或 `--no-approve` 忽略它们。

Use `/trust` in interactive mode to save a project trust decision for future sessions, including trust for the immediate parent folder. It writes `~/.pi/agent/trust.json` only; the current session is not reloaded, so restart pi for changes to take effect.
在交互模式中使用 `/trust` 保存项目信任决定供未来会话使用，包括对直接父文件夹的信任。它只写入 `~/.pi/agent/trust.json`；当前会话不会重新加载，因此请重启 pi 以使更改生效。

## All Settings
## 全部设置

### Model & Thinking
### 模型与思考

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `defaultProvider` | string | - | Startup provider (e.g., `"anthropic"`, `"openai"`; saved with Ctrl+S in `/model`, or edited manually) |
| `defaultModel` | string | - | Startup model ID (saved with Ctrl+S in `/model`, or edited manually) |
| `defaultThinkingLevel` | string | - | Startup thinking level (saved with Ctrl+S in `/thinking`, or edited manually): `"off"`, `"minimal"`, `"low"`, `"medium"`, `"high"`, `"xhigh"`, `"max"` |
| `modelThinkingLevels` | object | - | Per-model startup thinking levels keyed by `"provider/modelId"`; configure from `/settings` → Default thinking level per model or edit manually |
| `hideThinkingBlock` | boolean | `false` | Hide thinking blocks in output |
| `showCacheMissNotices` | boolean | `false` | Show transcript notices for significant prompt-cache misses and compaction or branch-summary usage |
| `thinkingBudgets` | object | - | Custom token budgets per thinking level. Anthropic, Google, and Bedrock use these natively. OpenAI-compatible models use them when `compat.thinkingTokenBudgetField` (or `supportsThinkingTokenBudget`) is set. |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `defaultProvider` | string | - | 启动时的提供商（如 `"anthropic"`、`"openai"`；在 `/model` 中用 Ctrl+S 保存，或手动编辑） |
| `defaultModel` | string | - | 启动时的模型 ID（在 `/model` 中用 Ctrl+S 保存，或手动编辑） |
| `defaultThinkingLevel` | string | - | 启动时的思考等级（在 `/thinking` 中用 Ctrl+S 保存，或手动编辑）：`"off"`、`"minimal"`、`"low"`、`"medium"`、`"high"`、`"xhigh"`、`"max"` |
| `modelThinkingLevels` | object | - | 按 `"provider/modelId"` 索引的每模型启动思考等级；从 `/settings` → Default thinking level per model 配置或手动编辑 |
| `hideThinkingBlock` | boolean | `false` | 在输出中隐藏思考块 |
| `showCacheMissNotices` | boolean | `false` | 为显著的提示词缓存未命中以及压缩或分支摘要用量显示记录通知 |
| `thinkingBudgets` | object | - | 每个思考等级的自定义 token 预算。Anthropic、Google 和 Bedrock 原生使用这些值。OpenAI 兼容模型在设置了 `compat.thinkingTokenBudgetField`（或 `supportsThinkingTokenBudget`）时使用它们。 |


#### thinkingBudgets
#### thinkingBudgets

```json
{
  "thinkingBudgets": {
    "minimal": 1024,
    "low": 4096,
    "medium": 10240,
    "high": 32768
  }
}
```

### UI & Display
### UI 与显示

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `theme` | string | `"dark"` | Theme name (`"dark"`, `"light"`, or custom) |
| `externalEditor` | string | `$VISUAL`, then `$EDITOR`, then Notepad on Windows or `nano` elsewhere | Command for Ctrl+G external editor; takes precedence over environment variables |
| `quietStartup` | boolean | `false` | Hide startup header |
| `defaultProjectTrust` | string | `"ask"` | Fallback project trust behavior: `"ask"`, `"always"`, or `"never"`. Global setting only |
| `collapseChangelog` | boolean | `false` | Show condensed changelog after updates |
| `enableInstallTelemetry` | boolean | `true` | Send an anonymous install/update version ping after first install or changelog-detected updates. This does not control update checks |
| `enableAnalytics` | boolean | `false` | Opt-in analytics data sharing. Currently only asked for during the experimental first-time setup (`PI_EXPERIMENTAL=1`) |
| `trackingId` | string | - | Analytics tracking identifier, generated when `enableAnalytics` is turned on |
| `doubleEscapeAction` | string | `"tree"` | Action for double-escape: `"tree"`, `"fork"`, or `"none"` |
| `treeFilterMode` | string | `"default"` | Default filter for `/tree`: `"default"`, `"no-tools"`, `"user-only"`, `"labeled-only"`, `"all"` |
| `editorPaddingX` | number | `0` | Horizontal padding for input editor (0-3) |
| `outputPad` | number | `1` | Horizontal padding for user messages, assistant messages, and thinking (0 or 1) |
| `autocompleteMaxVisible` | number | `5` | Max visible items in autocomplete dropdown (3-20) |
| `showHardwareCursor` | boolean | `false` | Show the terminal cursor while TUI positions it for IME support |
| `tuiMode` | string | `"regular"` | Interactive TUI mode: `"regular"` or experimental `"fullscreen"`. Changes from `/settings` apply immediately; `--tui-mode` overrides this setting at startup |
| `fullscreenExitOutput` | string | `"transcript"` | Fullscreen exit output: `"transcript"` prints the final transcript and resume hint, while `"resume-hint"` restores the previous screen and prints only the resume hint. Has no effect in regular TUI mode |
| `fullscreenScrollbar` | string | `"auto"` | Fullscreen transcript scrollbar: `"auto"` shows it temporarily while scrolling, `"always"` reserves the rightmost column and keeps it visible, and `"hidden"` hides it. Has no effect in regular TUI mode |
| `fullscreenCopyOnSelect` | boolean | `true` | Automatically copy selected text in fullscreen mode. When disabled, selections stay highlighted and `Ctrl+X` copies the active selection |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `theme` | string | `"dark"` | 主题名称（`"dark"`、`"light"` 或自定义） |
| `externalEditor` | string | `$VISUAL`，然后 `$EDITOR`，Windows 上为记事本，其他平台为 `nano` | Ctrl+G 外部编辑器的命令；优先于环境变量 |
| `quietStartup` | boolean | `false` | 隐藏启动头 |
| `defaultProjectTrust` | string | `"ask"` | 回退的项目信任行为：`"ask"`、`"always"` 或 `"never"`。仅限全局设置 |
| `collapseChangelog` | boolean | `false` | 更新后显示精简版更新日志 |
| `enableInstallTelemetry` | boolean | `true` | 在首次安装或通过更新日志检测到更新后，发送匿名的安装/更新版本 ping。这不控制更新检查 |
| `enableAnalytics` | boolean | `false` | 选择加入的分析数据共享。目前只在实验性的首次设置（`PI_EXPERIMENTAL=1`）期间询问 |
| `trackingId` | string | - | 分析跟踪标识符，在开启 `enableAnalytics` 时生成 |
| `doubleEscapeAction` | string | `"tree"` | 双击 Escape 的动作：`"tree"`、`"fork"` 或 `"none"` |
| `treeFilterMode` | string | `"default"` | `/tree` 的默认过滤器：`"default"`、`"no-tools"`、`"user-only"`、`"labeled-only"`、`"all"` |
| `editorPaddingX` | number | `0` | 输入编辑器的水平内边距（0-3） |
| `outputPad` | number | `1` | 用户消息、助手消息和思考的水平内边距（0 或 1） |
| `autocompleteMaxVisible` | number | `5` | 自动补全下拉框的最大可见项数（3-20） |
| `showHardwareCursor` | boolean | `false` | 在 TUI 为支持输入法而定位终端光标时显示该光标 |
| `tuiMode` | string | `"regular"` | 交互式 TUI 模式：`"regular"` 或实验性的 `"fullscreen"`。从 `/settings` 所做的更改立即生效；`--tui-mode` 在启动时覆盖此设置 |
| `fullscreenExitOutput` | string | `"transcript"` | 全屏退出输出：`"transcript"` 打印最终对话记录和恢复提示，而 `"resume-hint"` 恢复之前的屏幕并只打印恢复提示。在常规 TUI 模式下无效果 |
| `fullscreenScrollbar` | string | `"auto"` | 全屏对话记录滚动条：`"auto"` 在滚动时临时显示，`"always"` 保留最右侧一列并保持可见，`"hidden"` 隐藏。在常规 TUI 模式下无效果 |
| `fullscreenCopyOnSelect` | boolean | `true` | 在全屏模式下自动复制选中的文本。禁用时，选区保持高亮，`Ctrl+X` 复制活动选区 |


For VS Code, include `--wait` so pi resumes after the editor exits:
对于 VS Code，请包含 `--wait`，这样 pi 会在编辑器退出后恢复运行：

```json
{
  "externalEditor": "code --wait"
}
```

### Telemetry and update checks
### 遥测与更新检查

`enableInstallTelemetry` only controls the anonymous install/update ping to `https://pi.dev/api/report-install`. Opting out of telemetry does not disable update checks; Pi can still fetch `https://pi.dev/api/latest-version` to look for the latest version.
`enableInstallTelemetry` 只控制发送到 `https://pi.dev/api/report-install` 的匿名安装/更新 ping。选择退出遥测不会禁用更新检查；Pi 仍可以获取 `https://pi.dev/api/latest-version` 来查找最新版本。

Set `PI_SKIP_VERSION_CHECK=1` to disable the Pi version update check. Use `--offline` or `PI_OFFLINE=1` to disable all startup network operations described here, including update checks, package update checks, and install/update telemetry.
设置 `PI_SKIP_VERSION_CHECK=1` 可禁用 Pi 版本更新检查。使用 `--offline` 或 `PI_OFFLINE=1` 可禁用此处描述的所有启动网络操作，包括更新检查、包更新检查和安装/更新遥测。

### Network
### 网络

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `httpProxy` | string | - | HTTP proxy URL applied as `HTTP_PROXY` and `HTTPS_PROXY`. Global setting only. |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `httpProxy` | string | - | 作为 `HTTP_PROXY` 和 `HTTPS_PROXY` 应用的 HTTP 代理 URL。仅限全局设置。 |


```json
{
  "httpProxy": "http://127.0.0.1:7890"
}
```

### Warnings
### 警告

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `warnings.anthropicExtraUsage` | boolean | `true` | Show a warning when Anthropic subscription auth may use paid extra usage |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `warnings.anthropicExtraUsage` | boolean | `true` | 当 Anthropic 订阅认证可能使用付费的额外用量时显示警告 |


```json
{
  "warnings": {
    "anthropicExtraUsage": false
  }
}
```

### Compaction
### 压缩

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `compaction.enabled` | boolean | `true` | Enable auto-compaction |
| `compaction.reserveTokens` | number | `16384` | Tokens reserved for LLM response |
| `compaction.keepRecentTokens` | number | `20000` | Recent tokens to keep (not summarized) |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `compaction.enabled` | boolean | `true` | 启用自动压缩 |
| `compaction.reserveTokens` | number | `16384` | 为 LLM 响应保留的 token 数 |
| `compaction.keepRecentTokens` | number | `20000` | 保留（不摘要）的最近 token 数 |


```json
{
  "compaction": {
    "enabled": true,
    "reserveTokens": 16384,
    "keepRecentTokens": 20000
  }
}
```

### Branch Summary
### 分支摘要

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `branchSummary.reserveTokens` | number | `16384` | Tokens reserved for branch summarization |
| `branchSummary.skipPrompt` | boolean | `false` | Skip "Summarize branch?" prompt on `/tree` navigation (defaults to no summary) |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `branchSummary.reserveTokens` | number | `16384` | 为分支摘要保留的 token 数 |
| `branchSummary.skipPrompt` | boolean | `false` | 在 `/tree` 导航时跳过“是否摘要分支？”提示（默认不摘要） |


### Retry
### 重试

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `retry.enabled` | boolean | `true` | Enable automatic agent-level retry on transient errors |
| `retry.maxRetries` | number | `3` | Maximum agent-level retry attempts |
| `retry.baseDelayMs` | number | `2000` | Base delay for agent-level exponential backoff (2s, 4s, 8s) |
| `retry.provider.timeoutMs` | number | SDK default | Provider/SDK request timeout in milliseconds |
| `retry.provider.maxRetries` | number | `0` | Provider/SDK retry attempts |
| `retry.provider.maxRetryDelayMs` | number | `60000` | Max server-requested delay before failing (60s) |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `retry.enabled` | boolean | `true` | 在出现瞬时错误时启用代理级自动重试 |
| `retry.maxRetries` | number | `3` | 代理级最大重试次数 |
| `retry.baseDelayMs` | number | `2000` | 代理级指数退避的基础延迟（2s、4s、8s） |
| `retry.provider.timeoutMs` | number | SDK 默认 | 提供商/SDK 请求超时（毫秒） |
| `retry.provider.maxRetries` | number | `0` | 提供商/SDK 重试次数 |
| `retry.provider.maxRetryDelayMs` | number | `60000` | 失败前允许的最大服务器请求延迟（60s） |


When a provider requests a retry delay longer than `retry.provider.maxRetryDelayMs`, the request fails immediately with an informative error instead of waiting silently. Set it to `0` to disable the limit.
当提供商请求的重试延迟超过 `retry.provider.maxRetryDelayMs` 时，请求会立即失败并给出说明性错误，而不是默默等待。设为 `0` 可禁用该限制。

Keep `retry.provider.maxRetries` at `0` unless provider-level retries are explicitly needed. Setting it above `0` can make SDK/provider retries handle out-of-usage-limit errors before Pi sees them, which may block the agent until the provider quota resets in some circumstances.
除非明确需要提供商级重试，否则请保持 `retry.provider.maxRetries` 为 `0`。把它设为大于 0 可能让 SDK/提供商重试在 Pi 看到之前就处理超出用量限制的错误，这在某些情况下可能阻塞代理，直到提供商配额重置。

```json
{
  "retry": {
    "enabled": true,
    "maxRetries": 3,
    "baseDelayMs": 2000,
    "provider": {
      "timeoutMs": 3600000,
      "maxRetries": 0,
      "maxRetryDelayMs": 60000
    }
  }
}
```

### Message Delivery
### 消息送达

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `steeringMode` | string | `"one-at-a-time"` | How steering messages are sent: `"all"` or `"one-at-a-time"` |
| `followUpMode` | string | `"one-at-a-time"` | How follow-up messages are sent: `"all"` or `"one-at-a-time"` |
| `transport` | string | `"auto"` | Preferred transport for providers that support multiple transports: `"sse"`, `"websocket"`, `"websocket-cached"`, or `"auto"` |
| `httpIdleTimeoutMs` | number | `300000` | HTTP header/body idle timeout in milliseconds, also used by providers with explicit stream idle timeouts. Set to `0` to disable. |
| `websocketConnectTimeoutMs` | number | `15000` | WebSocket connect/open handshake timeout in milliseconds for providers that support WebSocket transports. Set to `0` to disable. |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `steeringMode` | string | `"one-at-a-time"` | steering 消息的发送方式：`"all"` 或 `"one-at-a-time"` |
| `followUpMode` | string | `"one-at-a-time"` | follow-up 消息的发送方式：`"all"` 或 `"one-at-a-time"` |
| `transport` | string | `"auto"` | 对支持多种传输方式的提供商所使用的首选传输：`"sse"`、`"websocket"`、`"websocket-cached"` 或 `"auto"` |
| `httpIdleTimeoutMs` | number | `300000` | HTTP 头/体空闲超时（毫秒），也被具有显式流空闲超时的提供商使用。设为 `0` 禁用。 |
| `websocketConnectTimeoutMs` | number | `15000` | 支持 WebSocket 传输的提供商的 WebSocket 连接/打开握手超时（毫秒）。设为 `0` 禁用。 |


### Terminal & Images
### 终端与图片

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `terminal.showImages` | boolean | `true` | Show images in terminal (if supported) |
| `terminal.imageWidthCells` | number | `60` | Preferred inline image width in terminal cells |
| `terminal.clearOnShrink` | boolean | `false` | Clear empty rows when content shrinks (can cause flicker) |
| `terminal.hyperlinks` | boolean or `"auto"` | `"auto"` | Override OSC 8 hyperlink support (advanced, JSON-only) |
| `terminal.images` | string or boolean | `"auto"` | Override image protocol support with `"kitty"`, `"iterm2"`, `false`, or `"auto"` (advanced, JSON-only) |
| `terminal.trueColor` | boolean or `"auto"` | `"auto"` | Override truecolor support (advanced, JSON-only) |
| `images.autoResize` | boolean | `true` | Resize images to 2000x2000 max. Applies to `@file` attachments, `read`, and images returned by tools |
| `images.blockImages` | boolean | `false` | Block all images from being sent to LLM |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `terminal.showImages` | boolean | `true` | 在终端中显示图片（如果受支持） |
| `terminal.imageWidthCells` | number | `60` | 终端中内联图片的首选宽度（单元格数） |
| `terminal.clearOnShrink` | boolean | `false` | 内容缩小时清除空行（可能导致闪烁） |
| `terminal.hyperlinks` | boolean or `"auto"` | `"auto"` | 覆盖 OSC 8 超链接支持（高级，仅 JSON） |
| `terminal.images` | string or boolean | `"auto"` | 用 `"kitty"`、`"iterm2"`、`false` 或 `"auto"` 覆盖图片协议支持（高级，仅 JSON） |
| `terminal.trueColor` | boolean or `"auto"` | `"auto"` | 覆盖真彩色支持（高级，仅 JSON） |
| `images.autoResize` | boolean | `true` | 把图片调整为最大 2000x2000。适用于 `@file` 附件、`read` 以及工具返回的图片 |
| `images.blockImages` | boolean | `false` | 阻止所有图片发送给 LLM |


### Shell
### Shell

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `shellPath` | string | - | Custom shell path (e.g., for Cygwin on Windows); supports a leading `~` for the home directory |
| `shellCommandPrefix` | string | - | Prefix for every bash command (e.g., `"shopt -s expand_aliases"`) |
| `npmCommand` | string[] | - | Command argv used for npm package lookup/install operations (e.g., `["mise", "exec", "node@20", "--", "npm"]`) |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `shellPath` | string | - | 自定义 shell 路径（例如 Windows 上的 Cygwin）；支持以 `~` 表示主目录 |
| `shellCommandPrefix` | string | - | 每条 bash 命令的前缀（例如 `"shopt -s expand_aliases"`） |
| `npmCommand` | string[] | - | 用于 npm 包查找/安装操作的命令 argv（例如 `["mise", "exec", "node@20", "--", "npm"]`） |


Windows paths in JSON must use forward slashes or escaped backslashes:
JSON 中的 Windows 路径必须使用正斜杠或转义的反斜杠：

```json
{
  "shellPath": "C:/Program Files/Git/bin/bash.exe"
}
```

```json
{
  "shellPath": "C:\\Program Files\\Git\\bin\\bash.exe"
}
```

```json
{
  "npmCommand": ["mise", "exec", "node@20", "--", "npm"]
}
```

`npmCommand` is used for all npm package-manager operations, including installs, uninstalls, and dependency installs inside git packages. User-scoped npm packages install under `~/.pi/agent/npm/`; project-scoped npm packages install under `.pi/npm/`. Use argv-style entries exactly as the process should be launched. When `npmCommand` is configured, git package dependency installs use plain `install` to avoid npm-specific flags in wrappers or alternate package managers.
`npmCommand` 用于所有 npm 包管理器操作，包括安装、卸载以及 git 包内部的依赖安装。用户级 npm 包安装在 `~/.pi/agent/npm/` 下；项目级 npm 包安装在 `.pi/npm/` 下。请完全按照进程应有的启动方式使用 argv 风格的条目。配置 `npmCommand` 后，git 包的依赖安装使用普通 `install`，以避免在包装器或替代包管理器中出现 npm 特有的标志。

### Tools
### 工具

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `defaultTools` | string[] | - | Built-in tools enabled initially. When omitted, Pi uses its standard defaults |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `defaultTools` | string[] | - | 初始启用的内置工具。省略时，Pi 使用其标准默认值 |


`defaultTools` selects the built-in tools enabled at startup. Extension and SDK custom tools remain enabled. Available built-ins are `read`, `bash`, `powershell`, `edit`, `write`, `grep`, `find`, and `ls`:
`defaultTools` 选择启动时启用的内置工具。扩展和 SDK 自定义工具保持启用。可用的内置工具为 `read`、`bash`、`powershell`、`edit`、`write`、`grep`、`find` 和 `ls`：

```json
{
  "defaultTools": ["bash", "edit", "write"]
}
```

On Windows, select `powershell` instead of `bash`, or include both:
在 Windows 上，选择 `powershell` 而不是 `bash`，或两者都包含：

```json
{
  "defaultTools": ["read", "powershell", "edit", "write"]
}
```

An empty array starts with no built-in tools while preserving extension and SDK custom tools. `--tools` replaces this behavior with a strict allowlist for all tools, `--no-tools` disables all tools, and `--no-builtin-tools` disables the built-in defaults. `--exclude-tools` filters the resulting list. A project `defaultTools` array replaces the global array.
空数组表示从没有任何内置工具开始，同时保留扩展和 SDK 自定义工具。`--tools` 用严格的允许列表替换此行为（作用于所有工具），`--no-tools` 禁用所有工具，`--no-builtin-tools` 禁用内置默认值。`--exclude-tools` 过滤结果列表。项目的 `defaultTools` 数组会替换全局数组。

### Sessions
### 会话

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `sessionDir` | string | - | Directory where session files are stored. Accepts absolute or relative paths, plus `~`. |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `sessionDir` | string | - | 存储会话文件的目录。接受绝对或相对路径，以及 `~`。 |


```json
{ "sessionDir": ".pi/sessions" }
```

When multiple sources specify a session directory, precedence is `--session-dir`, `PI_CODING_AGENT_SESSION_DIR`, then `sessionDir` in settings.json.
当多个来源指定会话目录时，优先级为 `--session-dir`、`PI_CODING_AGENT_SESSION_DIR`，然后是 settings.json 中的 `sessionDir`。

### Model Cycling
### 模型循环切换

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `enabledModels` | string[] | - | Model patterns for Ctrl+P cycling (same format as `--models` CLI flag) |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `enabledModels` | string[] | - | 用于 Ctrl+P 循环切换的模型模式（与 `--models` CLI 标志格式相同） |


```json
{
  "enabledModels": ["claude-*", "gpt-4o", "gemini-2*"]
}
```

### Markdown
### Markdown

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `markdown.codeBlockIndent` | string | `"  "` | Indentation for code blocks |
| `markdown.mermaid` | string | `"streaming"` | Mermaid rendering mode: `"off"`, `"final"`, or `"streaming"` |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `markdown.codeBlockIndent` | string | `"  "` | 代码块的缩进 |
| `markdown.mermaid` | string | `"streaming"` | Mermaid 渲染模式：`"off"`、`"final"` 或 `"streaming"` |


### Resources
### 资源

These settings define where to load extensions, skills, prompts, and themes from.
这些设置定义从哪里加载扩展、技能、提示词和主题。

Paths in `~/.pi/agent/settings.json` resolve relative to `~/.pi/agent`. Paths in `.pi/settings.json` resolve relative to `.pi`. Absolute paths and `~` are supported.
`~/.pi/agent/settings.json` 中的路径相对于 `~/.pi/agent` 解析。`.pi/settings.json` 中的路径相对于 `.pi` 解析。支持绝对路径和 `~`。

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `packages` | array | `[]` | npm/git packages to load resources from |
| `extensions` | string[] | `[]` | Local extension file paths or directories |
| `skills` | string[] | `[]` | Local skill file paths or directories |
| `prompts` | string[] | `[]` | Local prompt template paths or directories |
| `themes` | string[] | `[]` | Local theme file paths or directories |
| `enableSkillCommands` | boolean | `true` | Register skills as `/skill:name` commands |

| 设置 | 类型 | 默认值 | 描述 |
|---------|------|---------|-------------|
| `packages` | array | `[]` | 从中加载资源的 npm/git 包 |
| `extensions` | string[] | `[]` | 本地扩展文件路径或目录 |
| `skills` | string[] | `[]` | 本地技能文件路径或目录 |
| `prompts` | string[] | `[]` | 本地提示词模板路径或目录 |
| `themes` | string[] | `[]` | 本地主题文件路径或目录 |
| `enableSkillCommands` | boolean | `true` | 把技能注册为 `/skill:name` 命令 |


Arrays support glob patterns and exclusions. Use `!pattern` to exclude. Use `+path` to force-include an exact path and `-path` to force-exclude an exact path.
数组支持 glob 模式和排除。用 `!pattern` 排除。用 `+path` 强制包含精确路径，`-path` 强制排除精确路径。

#### packages
#### packages

String form loads all resources from a package:
字符串形式从包加载所有资源：

```json
{
  "packages": ["pi-skills", "@org/my-extension"]
}
```

Object form filters which resources to load:
对象形式过滤要加载的资源：

```json
{
  "packages": [
    {
      "source": "pi-skills",
      "skills": ["brave-search", "transcribe"],
      "extensions": []
    }
  ]
}
```

See [packages.md](packages.md) for package management details.
包管理详情参见 [packages.md](packages.md)。

## Example
## 示例

```json
{
  "defaultProvider": "anthropic",
  "defaultModel": "claude-sonnet-4-20250514",
  "defaultThinkingLevel": "medium",
  "modelThinkingLevels": {
    "anthropic/claude-sonnet-4-20250514": "high"
  },
  "theme": "dark",
  "compaction": {
    "enabled": true,
    "reserveTokens": 16384,
    "keepRecentTokens": 20000
  },
  "retry": {
    "enabled": true,
    "maxRetries": 3
  },
  "enabledModels": ["claude-*", "gpt-4o"],
  "warnings": {
    "anthropicExtraUsage": true
  },
  "packages": ["pi-skills"]
}
```

## Project Overrides
## 项目覆盖

Project settings (`.pi/settings.json`) override global settings. Nested objects are merged:
项目设置（`.pi/settings.json`）覆盖全局设置。嵌套对象会被合并：

```json
// ~/.pi/agent/settings.json (global)
{
  "theme": "dark",
  "compaction": { "enabled": true, "reserveTokens": 16384 }
}

// .pi/settings.json (project)
{
  "compaction": { "reserveTokens": 8192 }
}

// Result
{
  "theme": "dark",
  "compaction": { "enabled": true, "reserveTokens": 8192 }
}
```
