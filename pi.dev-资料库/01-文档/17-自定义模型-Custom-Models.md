> 📄 来源 Source: https://pi.dev/docs/latest/models
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Custom Models
# 自定义模型

Add custom providers and models (Ollama, vLLM, LM Studio, proxies) via `~/.pi/agent/models.json`.
通过 `~/.pi/agent/models.json` 添加自定义提供商和模型（Ollama、vLLM、LM Studio、代理）。

## Table of Contents
## 目录

- [Minimal Example](#minimal-example)
- [最小示例](#minimal-example)
- [Full Example](#full-example)
- [完整示例](#full-example)
- [Supported APIs](#supported-apis)
- [支持的 API](#supported-apis)
- [Provider Configuration](#provider-configuration)
- [提供商配置](#provider-configuration)
- [Model Configuration](#model-configuration)
- [模型配置](#model-configuration)
- [Overriding Built-in Providers](#overriding-built-in-providers)
- [覆盖内置提供商](#overriding-built-in-providers)
- [Per-model Overrides](#per-model-overrides)
- [每模型覆盖](#per-model-overrides)
- [Anthropic Messages Compatibility](#anthropic-messages-compatibility)
- [Anthropic Messages 兼容性](#anthropic-messages-compatibility)
- [OpenAI Compatibility](#openai-compatibility)
- [OpenAI 兼容性](#openai-compatibility)

## Minimal Example
## 最小示例

For local models (Ollama, LM Studio, vLLM), only `id` is required per model:
对于本地模型（Ollama、LM Studio、vLLM），每个模型只需要 `id`：

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [
        { "id": "llama3.1:8b" },
        { "id": "qwen2.5-coder:7b" }
      ]
    }
  }
}
```

The `apiKey` value is a placeholder because Ollama ignores it. pi still treats models as requiring auth before they appear in `/model`, so keyless local servers should keep a dummy value, save a key for that provider with `/login`, or pass `--api-key` when selecting the model.
`apiKey` 值是占位符，因为 Ollama 会忽略它。pi 仍然把模型视为需要认证后才会出现在 `/model` 中，因此无密钥的本地服务器应保留一个占位值、用 `/login` 为该提供商保存密钥，或在选择模型时传入 `--api-key`。

Some OpenAI-compatible servers do not understand the `developer` role used for reasoning-capable models. For those providers, set `compat.supportsDeveloperRole` to `false` so pi sends the system prompt as a `system` message instead. If the server also does not support `reasoning_effort`, set `compat.supportsReasoningEffort` to `false` too.
一些 OpenAI 兼容服务器不理解用于推理模型的 `developer` 角色。对于这些提供商，把 `compat.supportsDeveloperRole` 设为 `false`，这样 pi 会以 `system` 消息发送系统提示词。如果服务器也不支持 `reasoning_effort`，同时把 `compat.supportsReasoningEffort` 设为 `false`。

You can set `compat` at the provider level to apply to all models, or at the model level to override a specific model. This commonly applies to Ollama, vLLM, SGLang, and similar OpenAI-compatible servers.
你可以在提供商级别设置 `compat` 应用于所有模型，或在模型级别设置以覆盖特定模型。这常见于 Ollama、vLLM、SGLang 和类似的 OpenAI 兼容服务器。

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "compat": {
        "supportsDeveloperRole": false,
        "supportsReasoningEffort": false
      },
      "models": [
        {
          "id": "gpt-oss:20b",
          "reasoning": true
        }
      ]
    }
  }
}
```

## Full Example
## 完整示例

Override defaults when you need specific values:
需要特定值时覆盖默认值：

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434/v1",
      "api": "openai-completions",
      "apiKey": "ollama",
      "models": [
        {
          "id": "llama3.1:8b",
          "name": "Llama 3.1 8B (Local)",
          "reasoning": false,
          "input": ["text"],
          "contextWindow": 128000,
          "maxTokens": 32000,
          "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
        }
      ]
    }
  }
}
```

The file reloads each time you open `/model`. Edit during session; no restart needed.
每次打开 `/model` 时该文件都会重新加载。可在会话中编辑；无需重启。

## Google AI Studio Example
## Google AI Studio 示例

Use `google-generative-ai` with a `baseUrl` to add models from Google AI Studio, including custom Gemma 4 entries:
使用带 `baseUrl` 的 `google-generative-ai` 来添加来自 Google AI Studio 的模型，包括自定义 Gemma 4 条目：

```json
{
  "providers": {
    "my-google": {
      "baseUrl": "https://generativelanguage.googleapis.com/v1beta",
      "api": "google-generative-ai",
      "apiKey": "$GEMINI_API_KEY",
      "models": [
        {
          "id": "gemma-4-31b-it",
          "name": "Gemma 4 31B",
          "input": ["text", "image"],
          "contextWindow": 262144,
          "reasoning": true
        }
      ]
    }
  }
}
```

The `baseUrl` is required when adding custom models to the `google-generative-ai` API type.
为 `google-generative-ai` API 类型添加自定义模型时 `baseUrl` 是必需的。

## Supported APIs
## 支持的 API

| API | Description |
|-----|-------------|
| `openai-completions` | OpenAI Chat Completions (most compatible) |
| `openai-responses` | OpenAI Responses API |
| `anthropic-messages` | Anthropic Messages API |
| `google-generative-ai` | Google Generative AI |

| API | 描述 |
|-----|-------------|
| `openai-completions` | OpenAI Chat Completions（兼容性最好） |
| `openai-responses` | OpenAI Responses API |
| `anthropic-messages` | Anthropic Messages API |
| `google-generative-ai` | Google Generative AI |


Set `api` at provider level (default for all models) or model level (override per model).
在提供商级别设置 `api`（对所有模型默认）或在模型级别设置（按模型覆盖）。

## Provider Configuration
## 提供商配置

| Field | Description |
|-------|-------------|
| `baseUrl` | API endpoint URL |
| `api` | API type (see above) |
| `apiKey` | Optional API key config (see value resolution below). Omit it when auth is provided by `/login`/`auth.json` or CLI `--api-key`. |
| `oauth` | Dynamic OAuth provider type. Currently supports `"radius"`; requires the gateway `baseUrl`. |
| `headers` | Custom headers (see value resolution below) |
| `authHeader` | Set `true` to add `Authorization: Bearer <apiKey>` automatically |
| `models` | Array of model configurations |
| `modelOverrides` | Per-model overrides for built-in or extension-registered models on this provider |

| 字段 | 描述 |
|-------|-------------|
| `baseUrl` | API 端点 URL |
| `api` | API 类型（见上） |
| `apiKey` | 可选的 API 密钥配置（见下文的值解析）。当认证由 `/login`/`auth.json` 或 CLI `--api-key` 提供时省略。 |
| `oauth` | 动态 OAuth 提供商类型。目前支持 `"radius"`；需要网关 `baseUrl`。 |
| `headers` | 自定义请求头（见下文的值解析） |
| `authHeader` | 设为 `true` 可自动添加 `Authorization: Bearer <apiKey>` |
| `models` | 模型配置数组 |
| `modelOverrides` | 对该提供商上内置或扩展注册模型的每模型覆盖 |


For providers with `models`, non-built-in provider configs need `baseUrl` and an `api` value at either provider or model level. `apiKey` is not required to load the file: models become available when auth is configured through `/login`/`auth.json`, CLI `--api-key`, or provider `apiKey`. If no auth is configured, the models load but stay unavailable in `/model` and `--list-models`.
对于带 `models` 的提供商，非内置的提供商配置需要在提供商或模型级别有 `baseUrl` 和 `api` 值。`apiKey` 不是加载文件所必需的：当通过 `/login`/`auth.json`、CLI `--api-key` 或提供商 `apiKey` 配置认证后，模型变为可用。如果没有配置认证，模型会加载但在 `/model` 和 `--list-models` 中不可用。

### Value Resolution
### 值解析

The `apiKey` and `headers` fields support command execution, environment interpolation, and literals:
`apiKey` 和 `headers` 字段支持命令执行、环境变量插值和字面量：

- **Shell command:** `"!command"` at the start executes the whole value as a command and uses stdout
- **Shell 命令：** 开头的 `"!command"` 会把整个值作为命令执行并使用其 stdout
  ```json
  "apiKey": "!security find-generic-password -ws 'anthropic'"
  "apiKey": "!op read 'op://vault/item/credential'"
  ```
- **Environment interpolation:** `"$ENV_VAR"` or `"${ENV_VAR}"` uses the value of the named variable. Interpolation works inside larger literals.
- **环境变量插值：** `"$ENV_VAR"` 或 `"${ENV_VAR}"` 使用指定变量的值。插值可用于更大的字面量内部。
  ```json
  "apiKey": "$MY_API_KEY"
  "apiKey": "${KEY_PREFIX}_${KEY_SUFFIX}"
  ```
  `$FOO_BAR` is the variable `FOO_BAR`; use `${FOO}_BAR` when `BAR` is literal text. Missing environment variables make the value unresolved.
  `$FOO_BAR` 是变量 `FOO_BAR`；当 `BAR` 是字面文本时用 `${FOO}_BAR`。缺失的环境变量会使该值无法解析。
- **Escapes:** `"$$"` emits a literal `"$"`; `"$!"` emits a literal `"!"` without triggering command execution.
- **转义：** `"$$"` 输出字面量 `"$"`；`"$!"` 输出字面量 `"!"`，不触发命令执行。
  ```json
  "apiKey": "$$literal-dollar-prefix"
  "apiKey": "$!literal-bang-prefix"
  ```
- **Literal value:** Used directly. Plain uppercase strings such as `MY_API_KEY` are literals; use `$MY_API_KEY` for environment variables.
- **字面量值：** 直接使用。诸如 `MY_API_KEY` 的纯大写字符串是字面量；环境变量请用 `$MY_API_KEY`。
  ```json
  "apiKey": "sk-..."
  ```

For `models.json`, shell commands are resolved at request time. pi intentionally does not apply built-in TTL, stale reuse, or recovery logic for arbitrary commands. Different commands need different caching and failure strategies, and pi cannot infer the right one.
对于 `models.json`，shell 命令在请求时解析。pi 有意不为任意命令应用内置的 TTL、过期复用或恢复逻辑。不同命令需要不同的缓存和失败策略，pi 无法推断出正确的策略。

If your command is slow, expensive, rate-limited, or should keep using a previous value on transient failures, wrap it in your own script or command that implements the caching or TTL behavior you want.
如果你的命令缓慢、昂贵、有速率限制，或应在瞬时失败时继续使用上一次的值，请把它包装在你自己的脚本或命令中，以实现你想要的缓存或 TTL 行为。

`/model` availability checks use configured auth presence and do not execute shell commands.
`/model` 的可用性检查使用已配置认证的存在性，不会执行 shell 命令。

### Custom Headers
### 自定义请求头

```json
{
  "providers": {
    "custom-proxy": {
      "baseUrl": "https://proxy.example.com/v1",
      "apiKey": "$MY_API_KEY",
      "api": "anthropic-messages",
      "headers": {
        "x-portkey-api-key": "$PORTKEY_API_KEY",
        "x-secret": "!op read 'op://vault/item/secret'"
      },
      "models": [...]
    }
  }
}
```

## Model Configuration
## 模型配置

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `id` | Yes | — | Model identifier (passed to the API) |
| `name` | No | `id` | Human-readable model label. Used for matching (`--model` patterns) and shown as secondary model detail text. |
| `api` | No | provider's `api` | Override provider's API for this model |
| `reasoning` | No | `false` | Supports extended thinking |
| `thinkingLevelMap` | No | omitted | Maps pi thinking levels to provider values and marks unsupported levels (see below) |
| `input` | No | `["text"]` | Input types: `["text"]` or `["text", "image"]` |
| `contextWindow` | No | `128000` | Context window size in tokens |
| `maxTokens` | No | `16384` | Maximum output tokens |
| `samplingParams` | No | omitted | Sampling parameters merged verbatim into every request body (see below) |
| `cost` | No | all zeros | Per-million-token rates with optional request-wide input pricing tiers |
| `compat` | No | provider `compat` | Provider compatibility overrides. Merged with provider-level `compat` when both are set. |

| 字段 | 必需 | 默认值 | 描述 |
|-------|----------|---------|-------------|
| `id` | 是 | — | 模型标识符（传给 API） |
| `name` | 否 | `id` | 人类可读的模型标签。用于匹配（`--model` 模式）并显示为次要模型详情文本。 |
| `api` | 否 | 提供商的 `api` | 为该模型覆盖提供商的 API |
| `reasoning` | 否 | `false` | 支持扩展思考 |
| `thinkingLevelMap` | 否 | 省略 | 把 pi 思考等级映射到提供商的值，并标记不支持的等级（见下） |
| `input` | 否 | `["text"]` | 输入类型：`["text"]` 或 `["text", "image"]` |
| `contextWindow` | 否 | `128000` | 以 token 计的上下文窗口大小 |
| `maxTokens` | 否 | `16384` | 最大输出 token 数 |
| `samplingParams` | 否 | 省略 | 原样合并进每个请求体的采样参数（见下） |
| `cost` | 否 | 全零 | 每百万 token 的费率，可选按请求的输入定价层级 |
| `compat` | 否 | 提供商 `compat` | 提供商兼容性覆盖。两者都设置时与提供商级 `compat` 合并。 |


A cost tier supplies a complete alternate rate set and applies to the full request when total input usage (`input + cacheRead + cacheWrite`) exceeds `inputTokensAbove`. When multiple tiers match, the highest threshold wins.
成本层级提供一整套替代费率，当总输入用量（`input + cacheRead + cacheWrite`）超过 `inputTokensAbove` 时应用于整个请求。多个层级匹配时，取阈值最高的一个。

```json
{
  "cost": {
    "input": 5,
    "output": 30,
    "cacheRead": 0.5,
    "cacheWrite": 6.25,
    "tiers": [
      {
        "inputTokensAbove": 272000,
        "input": 10,
        "output": 45,
        "cacheRead": 1,
        "cacheWrite": 12.5
      }
    ]
  }
}
```

Current behavior:
当前行为：
- `/model`, `--list-models`, and the interactive footer display entries by model `id`.
- `/model`、`--list-models` 和交互式页脚按模型 `id` 显示条目。
- The configured `name` is used for model matching and secondary model detail text. It does not replace the footer/status-bar model id.
- 配置的 `name` 用于模型匹配和次要模型详情文本。它不会替换页脚/状态栏中的模型 id。

### Sampling Parameters
### 采样参数

`samplingParams` is a free-form object merged verbatim into every request body for the model, after the fields pi sets itself, so its keys win. Use it to send sampling parameters pi does not model — including server-specific ones like llama.cpp's `min_p` or vLLM's `top_k`:
`samplingParams` 是一个自由格式对象，在 pi 自身设置的字段之后原样合并进该模型的每个请求体，因此它的键获胜。用它来发送 pi 未建模的采样参数——包括服务器特定的参数，如 llama.cpp 的 `min_p` 或 vLLM 的 `top_k`：

```json
{
  "id": "deepseek-v4-flash",
  "samplingParams": {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 0,
    "min_p": 0.0
  }
}
```

Only OpenAI-compatible APIs apply it (`openai-completions`, `openai-responses`, `azure-openai-responses`); other APIs ignore it. Keys override pi's named request fields (for example a `temperature` key here beats the request-level temperature), so prefer it as the single source of sampling truth for a model. In `modelOverrides`, `samplingParams` merges per key with the base model's value.
只有 OpenAI 兼容 API 应用它（`openai-completions`、`openai-responses`、`azure-openai-responses`）；其他 API 忽略它。键会覆盖 pi 的具名请求字段（例如这里的 `temperature` 键胜过请求级 temperature），因此建议把它作为模型采样配置的唯一事实来源。在 `modelOverrides` 中，`samplingParams` 按键与基础模型的值合并。

A constant thinking-token cap can go here too, but it will not follow `thinkingBudgets` or leave room for the answer. Prefer `compat.thinkingTokenBudgetField` (or the `supportsThinkingTokenBudget` alias) for that.
固定的思考 token 上限也可以放在这里，但它不会跟随 `thinkingBudgets`，也不会为答案留出空间。为此请使用 `compat.thinkingTokenBudgetField`（或 `supportsThinkingTokenBudget` 别名）。

### Thinking Level Map
### 思考等级映射

Use `thinkingLevelMap` on a model to describe model-specific thinking controls. Keys are pi thinking levels: `off`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`. Maps may contain holes; for example, a model can expose `high` and `max` without exposing `xhigh`.
在模型上使用 `thinkingLevelMap` 来描述模型特定的思考控制。键是 pi 思考等级：`off`、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`。映射可以有空洞；例如，模型可以暴露 `high` 和 `max` 而不暴露 `xhigh`。

Values are tristate:
值是三态的：

| Value | Meaning |
|-------|---------|
| omitted | Standard levels through `high` use the provider's default mapping; extended `xhigh` and `max` levels are unsupported |
| string | Level is supported and this value is sent to the provider |
| `null` | Level is unsupported and hidden/skipped/clamped away |

| 值 | 含义 |
|-------|---------|
| 省略 | 到 `high` 为止的标准等级使用提供商的默认映射；扩展的 `xhigh` 和 `max` 等级不受支持 |
| 字符串 | 等级受支持，且该值会发送给提供商 |
| `null` | 等级不受支持，会被隐藏/跳过/钳制 |


Example for a model that only supports off, high, and max reasoning:
只支持 off、high 和 max 推理的模型示例：

```json
{
  "id": "deepseek-v4-pro",
  "reasoning": true,
  "thinkingLevelMap": {
    "minimal": null,
    "low": null,
    "medium": null,
    "high": "high",
    "xhigh": null,
    "max": "max"
  }
}
```

Example for a model where thinking cannot be disabled:
无法禁用思考的模型示例：

```json
{
  "id": "always-thinking-model",
  "reasoning": true,
  "thinkingLevelMap": {
    "off": null
  }
}
```

Migration: older configs that used `compat.reasoningEffortMap` should move that mapping to model-level `thinkingLevelMap`. Use `null` for levels that should not appear in the UI.
迁移：使用 `compat.reasoningEffortMap` 的旧配置应把该映射移到模型级 `thinkingLevelMap`。不应出现在 UI 中的等级使用 `null`。

## Overriding Built-in Providers
## 覆盖内置提供商

Route a built-in provider through a proxy without redefining models:
无需重新定义模型即可把内置提供商路由到代理：

```json
{
  "providers": {
    "anthropic": {
      "baseUrl": "https://my-proxy.example.com/v1"
    }
  }
}
```

All built-in Anthropic models remain available. Existing OAuth or API key auth continues to work.
所有内置 Anthropic 模型保持可用。现有的 OAuth 或 API 密钥认证继续有效。

To merge custom models into a built-in provider, include the `models` array:
要把自定义模型合并进内置提供商，请包含 `models` 数组：

```json
{
  "providers": {
    "anthropic": {
      "baseUrl": "https://my-proxy.example.com/v1",
      "apiKey": "$ANTHROPIC_API_KEY",
      "api": "anthropic-messages",
      "models": [...]
    }
  }
}
```

Merge semantics:
合并语义：
- Built-in models are kept.
- 内置模型保留。
- Custom models are upserted by `id` within the provider.
- 自定义模型在提供商内按 `id` 执行 upsert。
- If a custom model `id` matches a built-in model `id`, the custom model replaces that built-in model.
- 如果自定义模型 `id` 与内置模型 `id` 匹配，自定义模型替换该内置模型。
- If a custom model `id` is new, it is added alongside built-in models.
- 如果自定义模型 `id` 是新的，它与内置模型并列添加。

## Per-model Overrides
## 每模型覆盖

Use `modelOverrides` to customize built-in models and matching extension-registered models without replacing the provider's full model list.
使用 `modelOverrides` 自定义内置模型和匹配的扩展注册模型，而不替换提供商的完整模型列表。

```json
{
  "providers": {
    "openrouter": {
      "modelOverrides": {
        "anthropic/claude-sonnet-4": {
          "name": "Claude Sonnet 4 (Bedrock Route)",
          "compat": {
            "openRouterRouting": {
              "only": ["amazon-bedrock"]
            }
          }
        }
      }
    }
  }
}
```

`modelOverrides` supports these fields per model: `name`, `reasoning`, `thinkingLevelMap`, `input`, `cost` (partial), `contextWindow`, `maxTokens`, `samplingParams` (merged per key), `headers`, `compat`.
`modelOverrides` 支持每个模型的这些字段：`name`、`reasoning`、`thinkingLevelMap`、`input`、`cost`（部分）、`contextWindow`、`maxTokens`、`samplingParams`（按键合并）、`headers`、`compat`。

Direct OpenAI GPT-5.6 Sol, Terra, and Luna default to a `272000` context window so requests remain within OpenAI's short-context pricing tier. To opt into OpenAI's 1.05M context window, increase it for each model you use:
OpenAI GPT-5.6 Sol、Terra 和 Luna 直连默认使用 `272000` 上下文窗口，使请求保持在 OpenAI 短上下文定价层内。要选择使用 OpenAI 的 105 万上下文窗口，请为你使用的每个模型增大该值：

```json
{
  "providers": {
    "openai": {
      "modelOverrides": {
        "gpt-5.6-sol": {
          "contextWindow": 1050000
        }
      }
    }
  }
}
```

The override preserves the built-in pricing metadata. Requests with more than 272K total input tokens use GPT-5.6's long-context rates for the entire request. Apply the same override to `gpt-5.6-terra` or `gpt-5.6-luna` when needed.
该覆盖保留内置定价元数据。总输入 token 超过 27.2 万的请求对整个请求使用 GPT-5.6 的长上下文费率。需要时对 `gpt-5.6-terra` 或 `gpt-5.6-luna` 应用相同覆盖。

Behavior notes:
行为说明：
- `modelOverrides` are applied to built-in provider models and matching extension-registered provider models.
- `modelOverrides` 应用于内置提供商模型和匹配的扩展注册提供商模型。
- Unknown model IDs are ignored.
- 未知模型 ID 会被忽略。
- You can combine provider-level `baseUrl`/`headers` with `modelOverrides`.
- 你可以把提供商级 `baseUrl`/`headers` 与 `modelOverrides` 组合。
- Overriding `name` changes model matching and secondary detail text only; the footer and primary model lists continue to show the model `id`.
- 覆盖 `name` 只改变模型匹配和次要详情文本；页脚和主要模型列表继续显示模型 `id`。
- If `models` is also defined for a provider, custom models are merged after built-in overrides. A custom model with the same `id` replaces the overridden built-in model entry.
- 如果提供商还定义了 `models`，自定义模型在内置覆盖之后合并。相同 `id` 的自定义模型替换被覆盖的内置模型条目。

## Anthropic Messages Compatibility
## Anthropic Messages 兼容性

For providers or proxies using `api: "anthropic-messages"`, use `compat` to control Anthropic-specific request compatibility.
对于使用 `api: "anthropic-messages"` 的提供商或代理，使用 `compat` 控制 Anthropic 特定的请求兼容性。

By default pi sends per-tool `eager_input_streaming: true`. If a proxy or Anthropic-compatible backend rejects that field, set `supportsEagerToolInputStreaming` to `false`. Pi will omit `tools[].eager_input_streaming` and send the legacy `fine-grained-tool-streaming-2025-05-14` beta header for tool-enabled requests instead.
默认情况下 pi 为每个工具发送 `eager_input_streaming: true`。如果代理或 Anthropic 兼容后端拒绝该字段，把 `supportsEagerToolInputStreaming` 设为 `false`。Pi 会省略 `tools[].eager_input_streaming`，并改为对启用工具的请求发送旧的 `fine-grained-tool-streaming-2025-05-14` beta 头。

Some Anthropic models require adaptive thinking (`thinking.type: "adaptive"` plus `output_config.effort`) instead of the legacy budget-based thinking payload. Built-in models set this automatically. For custom providers or aliases that route to those models, set `forceAdaptiveThinking` to `true`.
一些 Anthropic 模型要求自适应思考（`thinking.type: "adaptive"` 加 `output_config.effort`）而不是旧的基于预算的思考负载。内置模型自动设置。对于路由到这些模型的自定义提供商或别名，把 `forceAdaptiveThinking` 设为 `true`。

Some Anthropic-compatible providers emit thinking blocks with empty signatures and still expect them on replay. Set `allowEmptySignature` to `true` only for those providers; real Anthropic rejects empty thinking signatures.
一些 Anthropic 兼容提供商发出签名为空的思考块，并在重放时仍然期待它们。只为这些提供商把 `allowEmptySignature` 设为 `true`；真正的 Anthropic 会拒绝空的思考签名。

Built-in Anthropic models enable `supportsStrictTools` in their model metadata. Custom Anthropic-compatible models must set it to `true` when their endpoint accepts strict JSON-schema tool definitions.
内置 Anthropic 模型在其模型元数据中启用 `supportsStrictTools`。当自定义 Anthropic 兼容模型的端点接受严格的 JSON-schema 工具定义时，必须把它设为 `true`。

```json
{
  "providers": {
    "anthropic-proxy": {
      "baseUrl": "https://proxy.example.com",
      "api": "anthropic-messages",
      "apiKey": "$ANTHROPIC_PROXY_KEY",
      "compat": {
        "supportsEagerToolInputStreaming": false,
        "supportsLongCacheRetention": true,
        "forceAdaptiveThinking": true,
        "allowEmptySignature": true
      },
      "models": [
        {
          "id": "claude-opus-4-7",
          "reasoning": true,
          "input": ["text", "image"]
        }
      ]
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `supportsEagerToolInputStreaming` | Whether the provider accepts per-tool `eager_input_streaming`. Default: `true`. Set to `false` to omit that field and use the legacy fine-grained tool streaming beta header on tool-enabled requests. |
| `supportsLongCacheRetention` | Whether the provider accepts Anthropic long cache retention (`cache_control.ttl: "1h"`) when cache retention is `long`. Default: `true`. |
| `sendSessionAffinityHeaders` | Whether to send `x-session-affinity` from the session id when caching is enabled. Default: auto-detected for known providers. |
| `supportsCacheControlOnTools` | Whether the provider accepts Anthropic-style `cache_control` markers on tool definitions. Default: `true`. |
| `forceAdaptiveThinking` | Whether to send adaptive thinking (`thinking.type: "adaptive"` plus `output_config.effort`) for this model. Built-in adaptive models set this automatically. Default: `false`. |
| `allowEmptySignature` | Whether to replay empty thinking signatures as `signature: ""` instead of converting thinking to text. Default: `false`. |
| `supportsStrictTools` | Whether the provider accepts strict JSON-schema tool definitions. Default: `false`; built-in Anthropic models enable it in generated metadata. |

| 字段 | 描述 |
|-------|-------------|
| `supportsEagerToolInputStreaming` | 提供商是否接受每工具的 `eager_input_streaming`。默认：`true`。设为 `false` 可省略该字段，并在启用工具的请求上使用旧的细粒度工具流式 beta 头。 |
| `supportsLongCacheRetention` | 当缓存保留为 `long` 时，提供商是否接受 Anthropic 长缓存保留（`cache_control.ttl: "1h"`）。默认：`true`。 |
| `sendSessionAffinityHeaders` | 启用缓存时是否从会话 id 发送 `x-session-affinity`。默认：对已知提供商自动检测。 |
| `supportsCacheControlOnTools` | 提供商是否接受工具定义上的 Anthropic 风格 `cache_control` 标记。默认：`true`。 |
| `forceAdaptiveThinking` | 是否为该模型发送自适应思考（`thinking.type: "adaptive"` 加 `output_config.effort`）。内置自适应模型自动设置。默认：`false`。 |
| `allowEmptySignature` | 是否以 `signature: ""` 重放空的思考签名，而不是把思考转换为文本。默认：`false`。 |
| `supportsStrictTools` | 提供商是否接受严格的 JSON-schema 工具定义。默认：`false`；内置 Anthropic 模型在生成的元数据中启用它。 |


## OpenAI Compatibility
## OpenAI 兼容性

For providers with partial OpenAI compatibility, use the `compat` field.
对于部分兼容 OpenAI 的提供商，使用 `compat` 字段。

- Provider-level `compat` applies defaults to all models under that provider.
- 提供商级 `compat` 为该提供商下所有模型应用默认值。
- Model-level `compat` overrides provider-level values for that model.
- 模型级 `compat` 覆盖该模型的提供商级值。

```json
{
  "providers": {
    "local-llm": {
      "baseUrl": "http://localhost:8080/v1",
      "api": "openai-completions",
      "compat": {
        "supportsUsageInStreaming": false,
        "maxTokensField": "max_tokens"
      },
      "models": [...]
    }
  }
}
```

| Field | Description |
|-------|-------------|
| `supportsStore` | Provider supports `store` field |
| `supportsDeveloperRole` | Use `developer` vs `system` role |
| `supportsReasoningEffort` | Support for `reasoning_effort` parameter |
| `supportsUsageInStreaming` | Supports `stream_options: { include_usage: true }` (default: `true`) |
| `supportsFinishReason` | Whether streamed responses include `finish_reason`. When `false`, pi infers `stop` or `toolUse` when the stream ends. Default: `true`. |
| `maxTokensField` | Use `max_completion_tokens` or `max_tokens` |
| `requiresToolResultName` | Include `name` on tool result messages |
| `requiresAssistantAfterToolResult` | Insert an assistant message before a user message after tool results |
| `requiresThinkingAsText` | Convert thinking blocks to plain text |
| `requiresReasoningContentOnAssistantMessages` | Include empty `reasoning_content` on all replayed assistant messages when reasoning is enabled |
| `thinkingFormat` | Use `reasoning_effort`, `openrouter`, `deepseek`, `together`, `baseten`, `zai`, `qwen`, `chat-template`, or `qwen-chat-template` thinking parameters |
| `chatTemplateKwargs` | `chat_template_kwargs` values for `thinkingFormat: "chat-template"`; use `{ "$var": "thinking.enabled" }`, `{ "$var": "thinking.effort" }`, or `{ "$var": "thinking.budget" }` for pi-controlled thinking values |
| `chatTemplateArgs` | `chat_template_args` values for `thinkingFormat: "baseten"`; use `{ "$var": "thinking.enabled" }`, `{ "$var": "thinking.effort" }`, or `{ "$var": "thinking.budget" }` for pi-controlled thinking values |
| `thinkingTokenBudgetField` | Top-level request field used to cap reasoning tokens from `thinkingBudgets`, clamped so at least 1024 tokens remain for the answer. `"thinking_token_budget"` (vLLM), `"thinking_budget"` (Qwen/DashScope/SGLang), `"thinking_budget_tokens"` (llama.cpp). Off by default; not set on the generated catalog. |
| `supportsThinkingTokenBudget` | Alias for `thinkingTokenBudgetField: "thinking_token_budget"` (vLLM). Prefer `thinkingTokenBudgetField`. Default: `false`. |
| `cacheControlFormat` | Use Anthropic-style `cache_control` markers on the system prompt, last tool definition, and last user, assistant, or tool-result text content. Currently only `anthropic` is supported. |
| `sendSessionAffinityHeaders` | For `openai-completions`, send session-affinity headers from the session id when caching is enabled. Default: `false`. |
| `sessionAffinityFormat` | For `openai-completions` and `openai-responses`, the session-affinity header format: `openai` sends `session_id`/`x-client-request-id` (completions also `x-session-affinity`), `openai-nosession` omits the underscore-containing `session_id` header, `openrouter` sends `x-session-id`. Does not affect the `prompt_cache_key` body param. Default: auto-detected. |
| `supportsStrictMode` | Whether the provider accepts strict JSON-schema function tool definitions. Defaults depend on the API; built-in OpenAI models carry explicit capability metadata. |
| `supportsOpenAIGrammarTools` | Whether OpenAI-compatible APIs emit custom Lark/regex grammar tools. When `false`, grammar-constrained tools fall back to normal function tools. Default: `false`; the built-in model catalog enables it for GPT-5+ models on OpenAI, OpenAI Codex, Azure OpenAI, GitHub Copilot, opencode, and Cloudflare AI Gateway. |
| `deferredToolsMode` | Use provider-specific deferred tool serialization. Currently only `"kimi"` is supported for Kimi's OpenAI-compatible Chat Completions format. |
| `supportsLongCacheRetention` | Whether the provider accepts long cache retention when cache retention is `long`: `prompt_cache_retention: "24h"` for OpenAI prompt caching, or `cache_control.ttl: "1h"` when `cacheControlFormat` is `anthropic`. Default: `true`. |
| `openRouterRouting` | OpenRouter provider routing preferences. This object is sent as-is in the `provider` field of the [OpenRouter API request](https://openrouter.ai/docs/guides/routing/provider-selection). |
| `vercelGatewayRouting` | Vercel AI Gateway routing config for provider selection (`only`, `order`) |

| 字段 | 描述 |
|-------|-------------|
| `supportsStore` | 提供商支持 `store` 字段 |
| `supportsDeveloperRole` | 使用 `developer` 还是 `system` 角色 |
| `supportsReasoningEffort` | 支持 `reasoning_effort` 参数 |
| `supportsUsageInStreaming` | 支持 `stream_options: { include_usage: true }`（默认：`true`） |
| `supportsFinishReason` | 流式响应是否包含 `finish_reason`。为 `false` 时，pi 在流结束时推断 `stop` 或 `toolUse`。默认：`true`。 |
| `maxTokensField` | 使用 `max_completion_tokens` 或 `max_tokens` |
| `requiresToolResultName` | 在工具结果消息上包含 `name` |
| `requiresAssistantAfterToolResult` | 在工具结果之后、用户消息之前插入助手消息 |
| `requiresThinkingAsText` | 把思考块转换为纯文本 |
| `requiresReasoningContentOnAssistantMessages` | 启用推理时在所有重放的助手消息上包含空的 `reasoning_content` |
| `thinkingFormat` | 使用 `reasoning_effort`、`openrouter`、`deepseek`、`together`、`baseten`、`zai`、`qwen`、`chat-template` 或 `qwen-chat-template` 思考参数 |
| `chatTemplateKwargs` | `thinkingFormat: "chat-template"` 的 `chat_template_kwargs` 值；pi 控制的思考值用 `{ "$var": "thinking.enabled" }`、`{ "$var": "thinking.effort" }` 或 `{ "$var": "thinking.budget" }` |
| `chatTemplateArgs` | `thinkingFormat: "baseten"` 的 `chat_template_args` 值；pi 控制的思考值用 `{ "$var": "thinking.enabled" }`、`{ "$var": "thinking.effort" }` 或 `{ "$var": "thinking.budget" }` |
| `thinkingTokenBudgetField` | 用于按 `thinkingBudgets` 限制推理 token 的顶层请求字段，钳制为至少为答案保留 1024 个 token。`"thinking_token_budget"`（vLLM）、`"thinking_budget"`（Qwen/DashScope/SGLang）、`"thinking_budget_tokens"`（llama.cpp）。默认关闭；不在生成的目录上设置。 |
| `supportsThinkingTokenBudget` | `thinkingTokenBudgetField: "thinking_token_budget"`（vLLM）的别名。优先使用 `thinkingTokenBudgetField`。默认：`false`。 |
| `cacheControlFormat` | 在系统提示词、最后一个工具定义以及最后一条用户、助手或工具结果文本内容上使用 Anthropic 风格的 `cache_control` 标记。目前只支持 `anthropic`。 |
| `sendSessionAffinityHeaders` | 对 `openai-completions`，启用缓存时从会话 id 发送会话亲和头。默认：`false`。 |
| `sessionAffinityFormat` | 对 `openai-completions` 和 `openai-responses`，会话亲和头的格式：`openai` 发送 `session_id`/`x-client-request-id`（completions 还有 `x-session-affinity`），`openai-nosession` 省略带下划线的 `session_id` 头，`openrouter` 发送 `x-session-id`。不影响 `prompt_cache_key` 请求体参数。默认：自动检测。 |
| `supportsStrictMode` | 提供商是否接受严格的 JSON-schema 函数工具定义。默认取决于 API；内置 OpenAI 模型带有显式的能力元数据。 |
| `supportsOpenAIGrammarTools` | OpenAI 兼容 API 是否发出自定义 Lark/正则文法工具。为 `false` 时，文法约束工具回退为普通函数工具。默认：`false`；内置模型目录为 OpenAI、OpenAI Codex、Azure OpenAI、GitHub Copilot、opencode 和 Cloudflare AI Gateway 上的 GPT-5+ 模型启用它。 |
| `deferredToolsMode` | 使用提供商特定的延迟工具序列化。目前只有 `"kimi"` 支持 Kimi 的 OpenAI 兼容 Chat Completions 格式。 |
| `supportsLongCacheRetention` | 当缓存保留为 `long` 时提供商是否接受长缓存保留：OpenAI 提示词缓存为 `prompt_cache_retention: "24h"`，`cacheControlFormat` 为 `anthropic` 时为 `cache_control.ttl: "1h"`。默认：`true`。 |
| `openRouterRouting` | OpenRouter 提供商路由偏好。该对象原样放在 [OpenRouter API 请求](https://openrouter.ai/docs/guides/routing/provider-selection)的 `provider` 字段中发送。 |
| `vercelGatewayRouting` | 用于提供商选择的 Vercel AI Gateway 路由配置（`only`、`order`） |


`openrouter` uses `reasoning: { effort }`. `together` uses `reasoning: { enabled }` and also `reasoning_effort` when `supportsReasoningEffort` is enabled. `qwen` uses top-level `enable_thinking`. Use `qwen-chat-template` for local Qwen-compatible servers that require `chat_template_kwargs.enable_thinking` and `preserve_thinking`. Use `chat-template` for vLLM/Hugging Face chat templates that need configurable `chat_template_kwargs`, such as `chatTemplateKwargs: { "thinking": { "$var": "thinking.enabled" } }` for DeepSeek V3.x templates. Use `thinkingFormat: "baseten"` with `chatTemplateArgs` for providers that expose toggle controls through `chat_template_args` and optionally support top-level `reasoning_effort`.
`openrouter` 使用 `reasoning: { effort }`。`together` 使用 `reasoning: { enabled }`，并在启用 `supportsReasoningEffort` 时也使用 `reasoning_effort`。`qwen` 使用顶层的 `enable_thinking`。对需要 `chat_template_kwargs.enable_thinking` 和 `preserve_thinking` 的本地 Qwen 兼容服务器使用 `qwen-chat-template`。对需要可配置 `chat_template_kwargs` 的 vLLM/Hugging Face 聊天模板使用 `chat-template`，例如为 DeepSeek V3.x 模板设置 `chatTemplateKwargs: { "thinking": { "$var": "thinking.enabled" } }`。对通过 `chat_template_args` 暴露切换控制、并可选支持顶层 `reasoning_effort` 的提供商，把 `thinkingFormat` 设为 `"baseten"` 并配合 `chatTemplateArgs`。

`thinkingTokenBudgetField` is independent of `thinkingFormat`. Do not enable it on the generated Qwen catalog: those models already send `reasoning_effort`, and DashScope rejects `thinking_budget` together with `reasoning_effort`.
`thinkingTokenBudgetField` 与 `thinkingFormat` 相互独立。不要在生成的 Qwen 目录上启用它：那些模型已经发送 `reasoning_effort`，而 DashScope 会拒绝同时出现 `thinking_budget` 和 `reasoning_effort`。

`cacheControlFormat: "anthropic"` is for OpenAI-compatible providers that expose Anthropic-style prompt caching through `cache_control` markers on text content and tool definitions.
`cacheControlFormat: "anthropic"` 用于通过文本内容和工具定义上的 `cache_control` 标记暴露 Anthropic 风格提示词缓存的 OpenAI 兼容提供商。

Example:
示例：

```json
{
  "providers": {
    "openrouter": {
      "baseUrl": "https://openrouter.ai/api/v1",
      "apiKey": "$OPENROUTER_API_KEY",
      "api": "openai-completions",
      "models": [
        {
          "id": "openrouter/anthropic/claude-3.5-sonnet",
          "name": "OpenRouter Claude 3.5 Sonnet",
          "compat": {
            "openRouterRouting": {
              "allow_fallbacks": true,
              "require_parameters": false,
              "data_collection": "deny",
              "zdr": true,
              "enforce_distillable_text": false,
              "order": ["anthropic", "amazon-bedrock", "google-vertex"],
              "only": ["anthropic", "amazon-bedrock"],
              "ignore": ["gmicloud", "friendli"],
              "quantizations": ["fp16", "bf16"],
              "sort": {
                "by": "price",
                "partition": "model"
              },
              "max_price": {
                "prompt": 10,
                "completion": 20
              },
              "preferred_min_throughput": {
                "p50": 100,
                "p90": 50
              },
              "preferred_max_latency": {
                "p50": 1,
                "p90": 3,
                "p99": 5
              }
            }
          }
        }
      ]
    }
  }
}
```

Vercel AI Gateway example:
Vercel AI Gateway 示例：

```json
{
  "providers": {
    "vercel-ai-gateway": {
      "baseUrl": "https://ai-gateway.vercel.sh/v1",
      "apiKey": "$AI_GATEWAY_API_KEY",
      "api": "openai-completions",
      "models": [
        {
          "id": "moonshotai/kimi-k2.5",
          "name": "Kimi K2.5 (Fireworks via Vercel)",
          "reasoning": true,
          "input": ["text", "image"],
          "cost": { "input": 0.6, "output": 3, "cacheRead": 0, "cacheWrite": 0 },
          "contextWindow": 262144,
          "maxTokens": 262144,
          "compat": {
            "vercelGatewayRouting": {
              "only": ["fireworks", "novita"],
              "order": ["fireworks", "novita"]
            }
          }
        }
      ]
    }
  }
}
```
