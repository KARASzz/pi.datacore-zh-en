# 新闻（News）
> 📄 来源 Source: https://pi.dev/news
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译。
> ℹ️ 更早的发布（0.83.0 及以前）见文末「英文参考」附录、`原文备份/site/news.txt` 与 `原文备份/CHANGELOG.md`。

# News
# 新闻

Release notes, project updates, and announcements from the Pi team.
来自 Pi 团队的发布说明、项目动态和公告。

Changelog / RSS Feed
更新日志 / RSS 订阅

Release notes · Aug 24, 2026
发布说明 · 2026 年 8 月 24 日

## Pi 0.84.3
## Pi 0.84.3

New version of pi. Download from npm or view release on GitHub.
pi 的新版本。从 npm 下载或在 GitHub 上查看发布。

### New Features
### 新功能

- PowerShell tool — Use optional native PowerShell command execution on Windows. See PowerShell Tool.
- PowerShell 工具 — 在 Windows 上使用可选的原生 PowerShell 命令执行。参见 PowerShell 工具。

- Safer managed updates — Stage, verify, and atomically activate updates for installer-managed installations. See Install and Manage.
- 更安全的托管更新 — 对安装器托管的安装进行暂存、验证并原子化激活更新。参见安装与管理。

- Model and thinking controls — Select thinking levels with `/thinking`, search defaults, keep selections session-scoped, and persist them explicitly with Ctrl+S. See Models and Thinking.
- 模型与思考控制 — 用 `/thinking` 选择思考等级、搜索默认值、保持选择限定在会话内，并用 Ctrl+S 显式持久化。参见模型与思考。

### Breaking Changes
### 破坏性变更

- Renamed the inherited `GoogleThinkingLevel` type to `GoogleApiThinkingLevel` and added `ResolvedGoogleThinkingLevel` for normalized adapter levels.
- 把继承的 `GoogleThinkingLevel` 类型重命名为 `GoogleApiThinkingLevel`，并添加用于规范化适配器等级的 `ResolvedGoogleThinkingLevel`。

### Added
### 新增

- Added an optional `powershell` tool for Windows, configurable through `defaultTools` and the SDK. See PowerShell Tool.
- 为 Windows 添加了可选的 `powershell` 工具，可通过 `defaultTools` 和 SDK 配置。参见 PowerShell 工具。

- Added a `/thinking` selector and searchable default choices to the model and thinking selectors; Ctrl+S saves the selected model as the global default. See Models and Thinking.
- 在模型与思考选择器中添加了 `/thinking` 选择器和可搜索的默认选项；Ctrl+S 将所选模型保存为全局默认值。参见模型与思考。

- Added optional routing session IDs to exported compaction summary helpers so callers can preserve provider routing without enabling prompt cache writes.
- 为导出的压缩摘要辅助函数添加了可选的路由会话 ID，使调用方能在不启用提示词缓存写入的情况下保留提供商路由。

- Added usage notices for compaction and branch summaries when cache miss notices are enabled.
- 在启用缓存未命中通知时，为压缩和分支摘要添加了用量通知。

- Added `session_compact_failed` extension events so compaction failures and aborts expose their reason, retry state, source, and error message to handlers (#8175).
- 添加了 `session_compact_failed` 扩展事件，让压缩失败和中止能向处理程序暴露原因、重试状态、来源和错误消息（#8175）。

- Added inherited provider-neutral `toolChoice` support to simple stream requests.
- 为简单流请求添加了继承的、与提供商无关的 `toolChoice` 支持。

- Added inherited automatic Anthropic server-side refusal fallback for supported first-party models, including returned-model usage pricing (#8017).
- 为受支持的第一方模型添加了继承的 Anthropic 服务端拒绝自动后备，包括按返回模型计费的用量定价（#8017）。

- Added inherited configurable OpenAI-compatible thinking-token budget fields for vLLM, Qwen/SGLang, and llama.cpp servers. See OpenAI Compatibility (#8275 by @bnsd55).
- 为 vLLM、Qwen/SGLang 和 llama.cpp 服务器添加了继承的、可配置的 OpenAI 兼容思考 token 预算字段。参见 OpenAI 兼容性（#8275，由 @bnsd55 贡献）。

- Added inherited China-specific ZAI Coding Plan models, including GLM-4.6V vision support and API-equivalent usage cost estimates (#8220).
- 添加了继承的中国区 ZAI Coding Plan 模型，包括 GLM-4.6V 视觉支持和与 API 等效的用量成本估算（#8220）。

- Added inherited `deepseek-v4-pro-0813` support to the Qwen Token Plan Individual catalog (#8194).
- 在 Qwen Token Plan 个人版目录中添加了继承的 `deepseek-v4-pro-0813` 支持（#8194）。
### Changed
### 变更

- Changed experimental installer-managed installations so `pi update` stages, verifies, and atomically activates the selected release in place. See Install and Manage.
- 更改了实验性的安装器托管安装，使 `pi update` 可以原地暂存、验证并原子化激活所选版本。参见安装与管理。

- Changed inherited built-in xAI models to use the Responses API with encrypted reasoning replay and made Grok 4.6 the default xAI model (#8124 by @Jaaneek).
- 更改了继承的内置 xAI 模型以使用带加密推理重放的 Responses API，并把 Grok 4.6 设为默认 xAI 模型（#8124，由 @Jaaneek 贡献）。

- Changed inherited Anthropic, Azure OpenAI, Google, Mistral, and OpenAI adapters to send Pi's default `User-Agent` unless overridden (#8305).
- 更改了继承的 Anthropic、Azure OpenAI、Google、Mistral 和 OpenAI 适配器，除非被覆盖，否则发送 Pi 的默认 `User-Agent`（#8305）。

- Changed Windows and WSL keybinding defaults to avoid terminal-reserved shortcuts for image paste, model cycling, editor undo, fullscreen transcript navigation and search, and message queueing (#8372).
- 更改了 Windows 和 WSL 的默认快捷键，避免使用终端保留的快捷方式（用于图片粘贴、模型循环切换、编辑器撤销、全屏对话记录导航与搜索，以及消息排队）（#8372）。

- Changed Bun release archives to ship the native clipboard binary only inside the wrapper package, removing a duplicate platform package from each archive.
- 更改了 Bun 发布归档，原生剪贴板二进制只在包装包内提供，从每个归档中移除了重复的平台包。

- Changed package resource glob expansion to use Node.js's built-in implementation with deterministic visible-path matching, reducing the installed runtime dependency tree.
- 更改了包资源 glob 展开，改用 Node.js 内置实现和确定性的可见路径匹配，减少了安装时的运行时依赖树。

- Changed the bundled Node.js runtime to load jiti only when importing an extension and Babel only when uncached source needs transformation, reducing CLI startup time and bundle size.
- 更改了内置 Node.js 运行时：仅在导入扩展时加载 jiti，仅在未缓存的源码需要转换时加载 Babel，降低了 CLI 启动时间和包体积。

- Changed syntax highlighting to initialize only twenty common languages eagerly and defer the remaining grammars until after the initial TUI render, reducing CLI startup time.
- 更改了语法高亮：仅急切初始化 20 种常用语言，其余语法推迟到首次 TUI 渲染之后，降低了 CLI 启动时间。

- Changed the Node.js CLI and RPC entrypoints to load a bundled runtime, reducing startup filesystem reads while keeping the public library and legacy module paths on the modular runtime for normal dependency identity.
- 更改了 Node.js CLI 和 RPC 入口以加载内置运行时，减少了启动时的文件系统读取，同时让公共库和旧版模块路径保持在模块化运行时上以维持正常的依赖标识。

- Changed session sharing to render clickable terminal links, display only the canonical Radius artifact URL, and include the current system prompt and active tool definitions in Radius session shares.
- 更改了会话分享：渲染可点击的终端链接、仅显示规范的 Radius 产物 URL，并在 Radius 会话分享中包含当前系统提示词和活动工具定义。

---

以下为 0.84.2 与 0.84.1 的中英对照（0.84.0 及更早版本请参见文末英文参考）。
The following are bilingual sections for 0.84.2 and 0.84.1 (for 0.84.0 and earlier, see the English reference appendix at the end).
Release notes · Aug 14, 2026
发布说明 · 2026 年 8 月 14 日

## Pi 0.84.2
## Pi 0.84.2

New version of pi. Download from npm or view release on GitHub.
pi 的新版本。从 npm 下载或在 GitHub 上查看发布。

### New Features
### 新功能

- Fullscreen transcript search — Search and navigate matches in fullscreen mode. See TUI Fullscreen Viewport.
- 全屏对话记录搜索 — 在全屏模式中搜索并导航匹配项。参见 TUI 全屏视口。

- Configurable default tools — Choose startup built-in tools globally or per project. See Tools.
- 可配置的默认工具 — 全局或按项目选择启动时的内置工具。参见工具。

- Configurable fullscreen exit output — Print the transcript or only a resume hint on exit. See Interactive Mode.
- 可配置的全屏退出输出 — 退出时打印对话记录或只打印恢复提示。参见交互模式。

### Added
### 新增

- Added fullscreen transcript search with `Ctrl+Shift+F`, incremental match highlighting, configurable search match theme colors, and next/previous navigation with `Enter`/`Ctrl+G` and `Shift+Enter`/`Ctrl+Shift+G`.
- 添加了全屏对话记录搜索，带 `Ctrl+Shift+F`、增量匹配高亮、可配置的搜索匹配主题颜色，以及用 `Enter`/`Ctrl+G` 和 `Shift+Enter`/`Ctrl+Shift+G` 进行下一个/上一个导航。

- Added experimental strict JSON-schema constrained sampling for the default `read`, `bash`, `edit`, and `write` tools under `PI_EXPERIMENTAL=1`.
- 在 `PI_EXPERIMENTAL=1` 下为默认的 `read`、`bash`、`edit` 和 `write` 工具添加了实验性的严格 JSON-schema 约束采样。

- Added a fullscreen exit output setting to choose between printing the final transcript and only a session resume hint.
- 添加了全屏退出输出设置，可选择打印最终对话记录或只打印会话恢复提示。

- Added the `defaultTools` setting for configuring the initial built-in tool selection globally or per project.
- 添加了 `defaultTools` 设置，用于全局或按项目配置初始内置工具选择。

- Added `--use-theme <name[/name]>` to choose an initial per-run interactive theme without changing saved settings (#7722 by @rwachtler).
- 添加了 `--use-theme <name[/name]>`，在不更改已保存设置的情况下为单次运行选择初始交互主题（#7722，由 @rwachtler 贡献）。

- Added `expandPromptTemplates` to extension `pi.sendUserMessage()` options for explicitly dispatching commands and expanding skills and prompt templates. See `pi.sendUserMessage()` (#7857 by @mrexodia).
- 在扩展的 `pi.sendUserMessage()` 选项中添加了 `expandPromptTemplates`，用于显式分发命令并展开技能与提示词模板。参见 `pi.sendUserMessage()`（#7857，由 @mrexodia 贡献）。

- Added inherited `createGatewayBindingFetch()` for routing Cloudflare AI Gateway requests through a Workers AI binding without an API token (#7901 by @Maximo-Guk).
- 添加了继承的 `createGatewayBindingFetch()`，无需 API 令牌即可通过 Workers AI 绑定路由 Cloudflare AI Gateway 请求（#7901，由 @Maximo-Guk 贡献）。

- Added inherited `AssistantMessage.endTurn` to preserve OpenAI Codex's terminal `end_turn` signal for diagnostics (#7766).
- 添加了继承的 `AssistantMessage.endTurn`，以保留 OpenAI Codex 的终止 `end_turn` 信号用于诊断（#7766）。

- Added inherited unbound single-line transcript scrolling actions for fullscreen mode. See TUI Fullscreen Viewport (#7903 by @midastruth).
- 为全屏模式添加了继承的、默认无绑定的单行对话记录滚动动作。参见 TUI 全屏视口（#7903，由 @midastruth 贡献）。

### Changed
### 变更

- Changed inherited Kimi Coding requests to use pi's runtime `User-Agent` header.
- 更改了继承的 Kimi Coding 请求，使用 pi 运行时的 `User-Agent` 头。

- Replaced the inherited Mistral SDK transport with a native Chat Completions HTTP stream, eliminating its generated client and schema runtime overhead.
- 用原生 Chat Completions HTTP 流替换了继承的 Mistral SDK 传输，消除了其生成客户端和模式（schema）的运行时开销。

- Documented the generic `AI_AGENT=pi` process marker and how it differs from `PI_CODING_AGENT=true` (#7747).
- 记录了通用的 `AI_AGENT=pi` 进程标记，以及它与 `PI_CODING_AGENT=true` 的区别（#7747）。

- Changed inherited OpenAI Responses deferred tool loading to prefer message-anchored `additional_tools` where supported while retaining tool-search and top-level fallbacks (#7709).
- 更改了继承的 OpenAI Responses 延迟工具加载，在受支持时优先使用消息锚定的 `additional_tools`，同时保留工具搜索和顶层后备（#7709）。

- Reduced inherited fullscreen rendering allocation churn by painting full-width layout rows directly instead of recompositing them on every frame.
- 通过直接绘制全宽布局行而不是每帧重新合成，减少了继承的全屏渲染分配抖动。
Release notes · Aug 7, 2026
发布说明 · 2026 年 8 月 7 日

## Pi 0.84.1
## Pi 0.84.1

New version of pi. Download from npm or view release on GitHub.
pi 的新版本。从 npm 下载或在 GitHub 上查看发布。

### New Features
### 新功能

- Qwen Token Plan Individual — Use the built-in provider for models documented for Individual subscriptions. See API Keys.
- Qwen Token Plan 个人版 — 对个人订阅所记录的模型使用内置提供商。参见 API 密钥。

- Authentication readiness checks — Use `pi auth check` to verify provider or model credentials, optionally emitting the resolved credential.
- 认证就绪检查 — 使用 `pi auth check` 验证提供商或模型凭据，可选择输出解析后的凭据。

- Improved fullscreen interaction — Select words and paragraphs with multiple clicks and configure half-page transcript scrolling. See TUI Fullscreen Viewport.
- 改进的全屏交互 — 通过多次点击选择单词和段落，并配置半页对话记录滚动。参见 TUI 全屏视口。

- Terminating blocked tool calls — Extension `tool_call` handlers can stop all-terminating batches without another model call. See Tool Events.
- 终止被阻止的工具调用 — 扩展的 `tool_call` 处理程序可以让“全部终止”批次无需再进行一次模型调用。参见工具事件。

### Added
### 新增

- Added Qwen Token Plan Individual as a built-in provider with its documented subscription model catalog and the shared international `QWEN_TOKEN_PLAN_API_KEY`. See API Keys (#7659 by @arasovic).
- 添加了 Qwen Token Plan 个人版作为内置提供商，带其文档记录的订阅模型目录和共享的国际 `QWEN_TOKEN_PLAN_API_KEY`。参见 API 密钥（#7659，由 @arasovic 贡献）。

- Added `pi auth check` provider/model auth preflight with optional credential output (#7152).
- 添加了 `pi auth check` 提供商/模型认证预检，可选择输出凭据（#7152）。

- Added `terminate` support to blocked extension `tool_call` events so all-terminating batches can skip the automatic follow-up model call. See Tool Events (#7715 by @muyiyr).
- 为被阻止的扩展 `tool_call` 事件添加了 `terminate` 支持，让“全部终止”批次可以跳过自动的后续模型调用。参见工具事件（#7715，由 @muyiyr 贡献）。

- Added inherited double-click word and whitespace selection, granularity-aware drag selection, and triple-click paragraph selection in fullscreen mode (#7725, #7733 by @volsa).
- 在全屏模式中添加了继承的双击单词与空白选择、粒度感知的拖动选择，以及三击段落选择（#7725、#7733，由 @volsa 贡献）。

- Added inherited unbound half-page transcript scrolling actions for fullscreen mode. See TUI Fullscreen Viewport (#7735).
- 为全屏模式添加了继承的、默认无绑定的半页对话记录滚动动作。参见 TUI 全屏视口（#7735）。

### Changed
### 变更

- Softened the bash tool's `PI_*` environment guideline in an attempt to reduce unnecessary inspection commands (#7128).
- 软化了 bash 工具中关于 `PI_*` 环境变量的指引，以尝试减少不必要的检查命令（#7128）。

- Reduced worst-case automatic terminal theme detection delay from 200 ms to 100 ms by probing color-scheme and background support concurrently.
- 通过并发探测配色方案与背景支持，把最坏情况的自动终端主题检测延迟从 200 ms 降低到 100 ms。
---

## 英文参考：更早的发布（English Reference: Older Releases）
> 以下为网站上其余发布（0.84.0 → 0.79.10，第 1/14 页）的英文原文摘录；完整内容见 `原文备份/site/news.txt` 与 `原文备份/CHANGELOG.md`。
> English excerpt of the remaining releases (page 1 of 14). Full text: `原文备份/site/news.txt` and `原文备份/CHANGELOG.md`.

### Pi 0.84.0 (Aug 6, 2026)
- New Features: Fullscreen TUI mode; Mermaid and LaTeX rendering; Per-directory context overrides (`AGENTS.override.md`); Advanced custom model sampling (`samplingParams`, vLLM `thinking_token_budget`); Baseten provider.
- Breaking Changes: Renamed pi-ai `ModelsStreamTransforms` → `ModelsRequestTransforms`; JSON/RPC `message_update` events now emit only `assistantMessageEvent` deltas (#7290); `ModelRegistry.getApiKeyAndHeaders()` returns `ProviderHeaders` with `string | null` values; `ModelRegistry.refresh()` accepts `ModelsRefreshOptions` / returns `ModelsRefreshResult`; `ModelRuntime.setRuntimeApiKey()` accepts auth cancellation options; config-form extension OAuth `refreshToken(credentials, signal)` must honor abort signals; provider refresh context replaced by read-only `context.stored` + `context.publish()`; pi-agent-core v4 lane-based `Session`/`SessionStorage`/`SessionRepo` replace the harness session model; legacy JSONL/in-memory repo APIs removed; required `FileSystem.renameFile()`; durable `SessionMetadata` replaces remote-session list summaries.
- Added: Baseten provider (`BASETEN_API_KEY`, default `zai-org/GLM-5.2`); experimental remote-session client APIs (`PiClient`, CBOR protocol, Unix-socket transport, `RemoteSession`); `CredentialSynchronizationError`; `pi.registerMarkdownTransformer()`; fullscreen TUI mode (`--tui-mode fullscreen` / `/settings`); sticky editor/status/widget/footer dock; draggable scrollbar (`auto`/`always`/`hidden`); page scrolling & marked-message navigation; `scrollbarThumb` theme color; themed Mermaid Unicode rendering; opt-in `Ctrl+P`/`Ctrl+N` history navigation; `AGENTS.override.md` per-directory context files; `AI_AGENT=pi` marker; LaTeX Unicode rendering; stacked notifications; `samplingParams`; vLLM `thinking_token_budget`; `compat.supportsFinishReason`; deferred provider request contracts; vendor-neutral telemetry contracts; Bedrock failure diagnostics; `AgentOptions.shouldStopAfterTurn`; v4 `JsonlSessionRepo`; bounded recovery queries; compile-complete `AgentHarness` v2 scaffold.
- Changed: optional cancellation in `ModelsStore` reads/writes/deletes; fullscreen mouse wheel step reduced from three lines to one.

### Pi 0.83.0 (Jul 29, 2026)
- New Features: Credential export for external clients (`pi auth print-api-key`, `pi auth print-bearer-token`); headless OpenRouter sign-in (paste redirect URL or authorization code over SSH); Claude Opus 5 on GitHub Copilot (adaptive thinking, 1M context window).
- Breaking Changes: Bundled TypeBox aliases upgraded to 1.3.7 — removed `Type.Base`, `Type.Awaited`, `Type.Promise`, `Type.AsyncIterator`, `Type.Iterator`, `Type.Options`, and `Value.Mutate`; extensions using removed APIs must migrate to supported TypeBox APIs (#7243).
- Added: credential export commands with automatic OAuth refresh and minimum-validity enforcement (#7168); `ctx.scopedModels`; per-request `fetch` injection; the `"pending"` stop reason for partial streaming messages (#7151); raw provider stop reasons across Google, Anthropic, Bedrock, Mistral, and OpenAI streams (#7272); OpenRouter manual redirect-URL / authorization-code entry (#7114); Claude Opus 5 for GitHub Copilot (#7158).
- Changed: OAuth credentials refresh when less than five minutes of validity remain instead of waiting until expiration (#7168).
### Pi 0.82.1 (Jul 25, 2026)
- New Features: Claude Opus 5 — on Anthropic and Amazon Bedrock with adaptive thinking (including `xhigh`), inference profiles, and prompt caching; Anthropic gateway bearer auth — `ANTHROPIC_AUTH_TOKEN` for Anthropic-compatible gateways requiring `Authorization: Bearer`; Faster, more resilient model catalogs — pi.dev catalogs revalidate with `If-None-Match` (empty `304`), llama.cpp models stay listed across restarts.
- Added: `outputPad` exposed to custom message renderers (#7045); inherited `ANTHROPIC_AUTH_TOKEN` bearer authentication; deterministic, checksummed source archives on GitHub releases with documented standalone binary rebuild instructions (#6913).

### Pi 0.81.0 (Jul 21, 2026)
- New Features: Local llama.cpp model management (connect to a router, search/download Hugging Face models, load/unload with live progress); Full provider extensions (register complete pi-ai providers with authentication, model refresh, filtering, custom streaming); Qwen Token Plan providers (international & China, regional endpoints, API-key auth); Expanded usage accounting (tool, compaction, and branch-summary usage persisted and included in session totals).
- Added: Qwen Token Plan and Qwen Token Plan China built-in providers (#6858); `get_available_thinking_levels` RPC command and `RpcClient.getAvailableThinkingLevels()` (#6865); exported message/tool lifecycle event types (#6772); llama.cpp router support with `/login` and `/llama` Hugging Face search/downloads; extension registration for complete pi-ai providers; usage accounting in sessions, footer totals, and session statistics (#6671).

### Pi 0.80.10 (Jul 16, 2026)
- Kimi Coding thinking compatibility — Kimi Coding models use adaptive thinking correctly; K3 exposes its `max` level and replays empty-signature thinking blocks.

### Pi 0.80.9 (Jul 16, 2026)
- Kimi K3 and deferred tool loading — progressive extension tool activation via Kimi's native protocol; K3 across Kimi Coding, Moonshot AI, Moonshot AI China, OpenRouter, and Vercel AI Gateway; xAI login device-authorization link "Sign in with SuperGrok or X Premium", default xAI model Grok 4.5 (#6734); removed Grok 3, Grok 3 Fast, Grok 4.20 variants, and Grok Code Fast 1 from the built-in xAI catalog.

### Pi 0.80.8 (Jul 16, 2026)
- See full notes in the raw backup (`原文备份/site/news.txt`).

### Pi 0.80.2 (Jun 23, 2026)
- pi-ai `ApiKeyCredential` uses the `auth.json`-compatible discriminator `type: "api_key"` and provider-scoped `env` values; agent-core `ExecutionEnvExecOptions` renamed to `ShellExecOptions`.

### Pi 0.80.1 (Jun 23, 2026)
- Fixed Bedrock scoped `AWS_PROFILE` endpoint resolution; Fireworks Anthropic-compatible session-affinity and unsupported tool-field defaults; Together MiniMax M2.7 metadata to avoid unsupported Together reasoning toggles.

### Pi 0.80.0 (Jun 23, 2026)
- Added `Ctrl+J` as a default newline keybinding alongside `Shift+Enter`; renamed the `zai` provider label to ZAI Coding Plan (Global) (#5965); pi-ai's old global API moved to `@earendil-works/pi-ai/compat` (extensions unaffected at runtime); removed `@earendil-works/pi-ai/base` and `@earendil-works/pi-agent-core/base` entrypoints.

### Pi 0.79.10 (Jun 22, 2026)
- Extension compaction event context — `session_before_compact`/`session_compact` include `reason` and `willRetry` (manual `/compact` vs threshold vs overflow retry); Safer update flow — `pi update` installs the exact checked Pi version and update notices show the changelog URL; `reason`/`willRetry` metadata added (#5962).

← Previous · 1 2 3 … 14 · Next →
← 上一页 · 1 2 3 … 14 · 下一页 →

Earendil Inc. & Contributors · Press Kit · MIT License
Earendil Inc. 及贡献者 · 媒体资料包 · MIT 许可证

pi.dev domain graciously donated by exe.dev
pi.dev 域名由 exe.dev 慷慨捐赠