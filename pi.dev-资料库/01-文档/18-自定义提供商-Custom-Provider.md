> 📄 来源 Source: https://pi.dev/docs/latest/custom-provider
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Custom Providers
# 自定义提供商

Extensions can register custom model providers via `pi.registerProvider()`. This enables:
扩展可以通过 `pi.registerProvider()` 注册自定义模型提供商。这使以下能力成为可能：

- **Proxies** - Route requests through corporate proxies or API gateways
- **代理** - 通过公司代理或 API 网关路由请求
- **Custom endpoints** - Use self-hosted or private model deployments
- **自定义端点** - 使用自托管或私有模型部署
- **OAuth/SSO** - Add authentication flows for enterprise providers
- **OAuth/SSO** - 为企业级提供商添加认证流程
- **Custom APIs** - Implement streaming for non-standard LLM APIs
- **自定义 API** - 为非标准 LLM API 实现流式传输

## Example Extensions
## 示例扩展

See these complete provider examples:
参见这些完整的提供商示例：

- [`examples/extensions/custom-provider-anthropic/`](../examples/extensions/custom-provider-anthropic/)
- [`examples/extensions/custom-provider-anthropic/`](../examples/extensions/custom-provider-anthropic/)
- [`examples/extensions/custom-provider-gitlab-duo/`](../examples/extensions/custom-provider-gitlab-duo/)
- [`examples/extensions/custom-provider-gitlab-duo/`](../examples/extensions/custom-provider-gitlab-duo/)

## Table of Contents
## 目录

- [Example Extensions](#example-extensions)
- [示例扩展](#example-extensions)
- [Quick Reference](#quick-reference)
- [快速参考](#quick-reference)
- [Override Existing Provider](#override-existing-provider)
- [覆盖现有提供商](#override-existing-provider)
- [Register New Provider](#register-new-provider)
- [注册新提供商](#register-new-provider)
- [Unregister Provider](#unregister-provider)
- [注销提供商](#unregister-provider)
- [OAuth Support](#oauth-support)
- [OAuth 支持](#oauth-support)
- [Custom Streaming API](#custom-streaming-api)
- [自定义流式 API](#custom-streaming-api)
- [Context Overflow Errors](#context-overflow-errors)
- [上下文溢出错误](#context-overflow-errors)
- [Testing Your Implementation](#testing-your-implementation)
- [测试你的实现](#testing-your-implementation)
- [Config Reference](#config-reference)
- [配置参考](#config-reference)
- [Model Definition Reference](#model-definition-reference)
- [模型定义参考](#model-definition-reference)

## Quick Reference
## 快速参考

Extensions can register either a complete pi-ai `Provider` or use the legacy provider-config form. Prefer a complete provider when custom authentication, filtering, refresh, or streaming behavior is required. Pi composes `models.json` overrides above registered native providers.
扩展可以注册完整的 pi-ai `Provider`，或使用旧式的提供商配置形式。当需要自定义认证、过滤、刷新或流式行为时，优先选择完整 provider。Pi 会把 `models.json` 覆盖组合在已注册的原生 provider 之上。

```typescript
import { createProvider, openAICompletionsApi } from "@earendil-works/pi-ai";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerProvider(createProvider({
    id: "native-local",
    name: "Native Local",
    baseUrl: "http://localhost:8080/v1",
    auth: {
      apiKey: {
        name: "Local server API key",
        async login(interaction) {
          return {
            type: "api_key",
            key: await interaction.prompt({ type: "secret", message: "API key" })
          };
        },
        async resolve({ credential }) {
          return credential?.key
            ? { auth: { apiKey: credential.key }, source: "stored API key" }
            : undefined;
        }
      }
    },
    models: [],
    api: openAICompletionsApi()
  }));

  // Legacy provider-config form:
  // Override baseUrl for existing provider
  pi.registerProvider("anthropic", {
    baseUrl: "https://proxy.example.com"
  });

  // Register new provider with models
  pi.registerProvider("my-provider", {
    name: "My Provider",
    baseUrl: "https://api.example.com",
    apiKey: "$MY_API_KEY",
    api: "openai-completions",
    models: [
      {
        id: "my-model",
        name: "My Model",
        reasoning: false,
        input: ["text", "image"],
        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
        contextWindow: 128000,
        maxTokens: 4096
      }
    ]
  });
}
```

The extension factory can also be `async`. For dynamic model discovery, fetch and register models in the factory instead of `session_start`. pi waits for the factory before startup continues, so the provider is available during interactive startup and to `pi --list-models`.
扩展工厂也可以是 `async` 的。对于动态模型发现，请在工厂中（而不是 `session_start`）获取并注册模型。pi 会等待工厂完成后再继续启动，因此该提供商在交互式启动期间以及 `pi --list-models` 中都可用。

## Override Existing Provider
## 覆盖现有提供商

The simplest use case: redirect an existing provider through a proxy.
最简单的用例：把现有提供商重定向到代理。

```typescript
// All Anthropic requests now go through your proxy
pi.registerProvider("anthropic", {
  baseUrl: "https://proxy.example.com"
});

// Add custom headers to OpenAI requests
pi.registerProvider("openai", {
  headers: {
    "X-Custom-Header": "value"
  }
});

// Both baseUrl and headers
pi.registerProvider("google", {
  baseUrl: "https://ai-gateway.corp.com/google",
  headers: {
    "X-Corp-Auth": "$CORP_AUTH_TOKEN"  // env var or literal
  }
});
```

When only `baseUrl` and/or `headers` are provided (no `models`), all existing models for that provider are preserved with the new endpoint.
当只提供 `baseUrl` 和/或 `headers`（没有 `models`）时，该提供商的所有现有模型都会保留并使用新端点。

## Register New Provider
## 注册新提供商

To add a completely new provider, specify `models` along with the required configuration.
要添加全新的提供商，请指定 `models` 以及所需的配置。

If the model list comes from a remote endpoint, use an async extension factory:
如果模型列表来自远程端点，请使用异步扩展工厂：

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default async function (pi: ExtensionAPI) {
  const response = await fetch("http://localhost:1234/v1/models");
  const payload = (await response.json()) as {
    data: Array<{
      id: string;
      name?: string;
      context_window?: number;
      max_tokens?: number;
    }>;
  };

  pi.registerProvider("local-openai", {
    baseUrl: "http://localhost:1234/v1",
    apiKey: "$LOCAL_OPENAI_API_KEY",
    api: "openai-completions",
    models: payload.data.map((model) => ({
      id: model.id,
      name: model.name ?? model.id,
      reasoning: false,
      input: ["text"],
      cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
      contextWindow: model.context_window ?? 128000,
      maxTokens: model.max_tokens ?? 4096,
    })),
  });
}
```

This registers the fetched models before startup finishes.
这会在启动完成之前注册获取到的模型。

```typescript
pi.registerProvider("my-llm", {
  baseUrl: "https://api.my-llm.com/v1",
  apiKey: "$MY_LLM_API_KEY",  // env var reference
  api: "openai-completions",  // which streaming API to use
  models: [
    {
      id: "my-llm-large",
      name: "My LLM Large",
      reasoning: true,        // supports extended thinking
      input: ["text", "image"],
      cost: {
        input: 3.0,           // $/million tokens
        output: 15.0,
        cacheRead: 0.3,
        cacheWrite: 3.75
      },
      contextWindow: 200000,
      maxTokens: 16384
    }
  ]
});
```

When `models` is provided, it **replaces** all existing models for that provider.
当提供 `models` 时，它会**替换**该提供商的所有现有模型。

`apiKey` and custom header values use the same config value syntax as `models.json`: `!command` at the start executes a command for the whole value, `$ENV_VAR` and `${ENV_VAR}` interpolate environment variables, `$$` emits a literal `$`, and `$!` emits a literal `!`.
`apiKey` 和自定义请求头的值使用与 `models.json` 相同的配置值语法：开头的 `!command` 会执行命令并取其完整输出作为值，`$ENV_VAR` 和 `${ENV_VAR}` 插值环境变量，`$$` 输出字面量 `$`，`$!` 输出字面量 `!`。

## Unregister Provider
## 注销提供商

Use `pi.unregisterProvider(name)` to remove a provider that was previously registered via `pi.registerProvider(name, ...)`:
使用 `pi.unregisterProvider(name)` 移除之前通过 `pi.registerProvider(name, ...)` 注册的提供商：

```typescript
// Register
pi.registerProvider("my-llm", {
  baseUrl: "https://api.my-llm.com/v1",
  apiKey: "$MY_LLM_API_KEY",
  api: "openai-completions",
  models: [
    {
      id: "my-llm-large",
      name: "My LLM Large",
      reasoning: true,
      input: ["text", "image"],
      cost: { input: 3.0, output: 15.0, cacheRead: 0.3, cacheWrite: 3.75 },
      contextWindow: 200000,
      maxTokens: 16384
    }
  ]
});

// Later, remove it
pi.unregisterProvider("my-llm");
```

Unregistering removes that provider's dynamic models, API key fallback, OAuth provider registration, and custom stream handler registrations. Any built-in models or provider behavior that were overridden are restored.
注销会移除该提供商的动态模型、API 密钥后备、OAuth 提供商注册和自定义流处理程序注册。任何被覆盖的内置模型或提供商行为都会被恢复。

Calls made after the initial extension load phase are applied immediately, so no `/reload` is required.
在初始扩展加载阶段之后进行的调用会立即生效，因此无需 `/reload`。

### API Types
### API 类型

The `api` field determines which streaming implementation is used:
`api` 字段决定使用哪种流式实现：

| API | Use for |
|-----|---------|
| `anthropic-messages` | Anthropic Claude API and compatibles |
| `openai-completions` | OpenAI Chat Completions API and compatibles |
| `openai-responses` | OpenAI Responses API |
| `azure-openai-responses` | Azure OpenAI Responses API |
| `openai-codex-responses` | OpenAI Codex Responses API |
| `mistral-conversations` | Native Mistral Chat Completions streaming |
| `google-generative-ai` | Google Generative AI API |
| `google-vertex` | Google Vertex AI API |
| `bedrock-converse-stream` | Amazon Bedrock Converse API |

| API | 用于 |
|-----|---------|
| `anthropic-messages` | Anthropic Claude API 及兼容实现 |
| `openai-completions` | OpenAI Chat Completions API 及兼容实现 |
| `openai-responses` | OpenAI Responses API |
| `azure-openai-responses` | Azure OpenAI Responses API |
| `openai-codex-responses` | OpenAI Codex Responses API |
| `mistral-conversations` | 原生 Mistral Chat Completions 流式 |
| `google-generative-ai` | Google Generative AI API |
| `google-vertex` | Google Vertex AI API |
| `bedrock-converse-stream` | Amazon Bedrock Converse API |


Most OpenAI-compatible providers work with `openai-completions`. Use model-level `thinkingLevelMap` for model-specific thinking levels, and `compat` for provider quirks. The `xhigh` and `max` levels are opt-in, require non-null map entries, and may be separated by unsupported holes:
大多数 OpenAI 兼容提供商都可以使用 `openai-completions`。对模型特定的思考等级请使用模型级 `thinkingLevelMap`，对提供商的怪癖请使用 `compat`。`xhigh` 和 `max` 等级是可选开启的，需要非空的映射条目，并且可能被不支持的空洞分隔：

```typescript
models: [{
  id: "custom-model",
  // ...
  reasoning: true,
  thinkingLevelMap: {              // map pi levels to provider values; null hides unsupported levels
    minimal: null,
    low: null,
    medium: null,
    high: "default",
    xhigh: null,
    max: "max"
  },
  compat: {
    supportsDeveloperRole: false,   // use "system" instead of "developer"
    supportsReasoningEffort: true,
    maxTokensField: "max_tokens",   // instead of "max_completion_tokens"
    requiresToolResultName: true,   // tool results need name field
    thinkingFormat: "qwen",        // top-level enable_thinking: true
    cacheControlFormat: "anthropic" // Anthropic-style cache_control markers
  }
}]
```

Use `openrouter` for OpenRouter-style `reasoning: { effort }` controls. Use `together` for Together-style `reasoning: { enabled }` controls; with `supportsReasoningEffort`, it also sends `reasoning_effort`. Use `qwen-chat-template` for local Qwen-compatible servers that read `chat_template_kwargs.enable_thinking` and need `preserve_thinking`.
使用 `openrouter` 实现 OpenRouter 风格的 `reasoning: { effort }` 控制。使用 `together` 实现 Together 风格的 `reasoning: { enabled }` 控制；配合 `supportsReasoningEffort` 时它还会发送 `reasoning_effort`。对读取 `chat_template_kwargs.enable_thinking` 并需要 `preserve_thinking` 的本地 Qwen 兼容服务器，使用 `qwen-chat-template`。
Use `cacheControlFormat: "anthropic"` for OpenAI-compatible providers that expose Anthropic-style prompt caching via `cache_control` on the system prompt, last tool definition, and last user, assistant, or tool-result text content.
对通过系统提示词、最后一个工具定义以及最后一条用户、助手或工具结果文本内容上的 `cache_control` 暴露 Anthropic 风格提示词缓存的 OpenAI 兼容提供商，使用 `cacheControlFormat: "anthropic"`。

For Anthropic-compatible providers using `api: "anthropic-messages"`, set `compat.forceAdaptiveThinking: true` on models or providers whose upstream model requires adaptive thinking (`thinking.type: "adaptive"` plus `output_config.effort`). Built-in adaptive Claude models set this automatically. Set `compat.allowEmptySignature: true` only for providers that emit empty thinking signatures and expect `signature: ""` on replay.
对使用 `api: "anthropic-messages"` 的 Anthropic 兼容提供商，在上游模型要求自适应思考（`thinking.type: "adaptive"` 加 `output_config.effort`）的模型或提供商上设置 `compat.forceAdaptiveThinking: true`。内置的自适应 Claude 模型会自动设置。只为发出空思考签名、并期待重放时出现 `signature: ""` 的提供商设置 `compat.allowEmptySignature: true`。

> Migration note: Mistral moved from `openai-completions` to `mistral-conversations`.
> 迁移说明：Mistral 已从 `openai-completions` 迁移到 `mistral-conversations`。
> Use `mistral-conversations` for native Mistral models.
> 对原生 Mistral 模型请使用 `mistral-conversations`。
> If you intentionally route Mistral-compatible/custom endpoints through `openai-completions`, set `compat` flags explicitly as needed.
> 如果你有意把 Mistral 兼容/自定义端点通过 `openai-completions` 路由，请按需显式设置 `compat` 标志。

### Auth Header
### 认证头

If your provider expects `Authorization: Bearer <key>` but doesn't use a standard API, set `authHeader: true`:
如果你的提供商期待 `Authorization: Bearer <key>` 但不使用标准 API，请设置 `authHeader: true`：

```typescript
pi.registerProvider("custom-api", {
  baseUrl: "https://api.example.com",
  apiKey: "$MY_API_KEY",
  authHeader: true,  // adds Authorization: Bearer header
  api: "openai-completions",
  models: [...]
});
```

The key is resolved for each request. An explicit request `Authorization` header takes precedence over the generated value.
密钥会在每次请求时解析。显式的请求 `Authorization` 头优先于生成的值。

## OAuth Support
## OAuth 支持

Add OAuth/SSO authentication that integrates with `/login`:
添加与 `/login` 集成的 OAuth/SSO 认证：

```typescript
import type { OAuthCredentials, OAuthLoginCallbacks } from "@earendil-works/pi-ai";

pi.registerProvider("corporate-ai", {
  baseUrl: "https://ai.corp.com/v1",
  api: "openai-responses",
  models: [...],
  oauth: {
    name: "Corporate AI (SSO)",

    async login(callbacks: OAuthLoginCallbacks): Promise<OAuthCredentials> {
      const method = await callbacks.onSelect({
        message: "Select login method:",
        options: [
          { id: "browser", label: "Browser OAuth" },
          { id: "device", label: "Device code" }
        ]
      });
      if (!method) throw new Error("Login cancelled");

      let code: string;
      if (method === "device") {
        callbacks.onDeviceCode({
          userCode: "ABCD-1234",
          verificationUri: "https://sso.corp.com/device",
          intervalSeconds: 5,
          expiresInSeconds: 900
        });
        code = await pollDeviceCodeUntilComplete();
      } else {
        callbacks.onAuth({ url: "https://sso.corp.com/authorize?..." });
        code = await callbacks.onPrompt({ message: "Enter SSO code:" });
      }

      // Exchange for tokens (your implementation)
      const tokens = await exchangeCodeForTokens(code);

      return {
        refresh: tokens.refreshToken,
        access: tokens.accessToken,
        expires: Date.now() + tokens.expiresIn * 1000
      };
    },

    async refreshToken(credentials: OAuthCredentials, signal: AbortSignal): Promise<OAuthCredentials> {
      const tokens = await refreshAccessToken(credentials.refresh, signal);
      return {
        refresh: tokens.refreshToken ?? credentials.refresh,
        access: tokens.accessToken,
        expires: Date.now() + tokens.expiresIn * 1000
      };
    },

    getApiKey(credentials: OAuthCredentials): string {
      return credentials.access;
    }
  }
});
```

After registration, users can authenticate via `/login corporate-ai`.
注册后，用户可以通过 `/login corporate-ai` 进行认证。

### OAuthLoginCallbacks
### OAuthLoginCallbacks

The `callbacks` object provides UI-neutral interactions for the provider-owned flow:
`callbacks` 对象为提供商拥有的流程提供与 UI 无关的交互：

```typescript
interface OAuthLoginCallbacks {
  // Open URL in browser (for OAuth redirects)
  onAuth(params: { url: string }): void;

  // Show device code (for device authorization flow)
  onDeviceCode(params: {
    userCode: string;
    verificationUri: string;
    intervalSeconds?: number;
    expiresInSeconds?: number;
  }): void;

  // Show transient progress
  onProgress?(message: string): void;

  // Prompt user for input (for manual token entry)
  onPrompt(params: { message: string }): Promise<string>;

  // Show an interactive selector, e.g. to choose browser OAuth vs device code
  onSelect(params: {
    message: string;
    options: { id: string; label: string }[];
  }): Promise<string | undefined>;
}
```

### OAuthCredentials
### OAuthCredentials

Credentials are persisted in `~/.pi/agent/auth.json`:
凭据持久化在 `~/.pi/agent/auth.json` 中：

```typescript
interface OAuthCredentials {
  refresh: string;   // Refresh token (for refreshToken())
  access: string;    // Access token (returned by getApiKey())
  expires: number;   // Expiration timestamp in milliseconds
}
```

## Custom Streaming API
## 自定义流式 API

For providers with non-standard APIs, implement `streamSimple`. Study the existing API implementations before writing your own:
对于非标准 API 的提供商，请实现 `streamSimple`。在编写自己的实现之前，请先研究现有的 API 实现：

**Reference implementations:**
**参考实现：**
- [anthropic-messages.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/anthropic-messages.ts) - Anthropic Messages API
- [anthropic-messages.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/anthropic-messages.ts) - Anthropic Messages API
- [mistral-conversations.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/mistral-conversations.ts) - Mistral Conversations API
- [mistral-conversations.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/mistral-conversations.ts) - Mistral Conversations API
- [openai-completions.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/openai-completions.ts) - OpenAI Chat Completions
- [openai-completions.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/openai-completions.ts) - OpenAI Chat Completions
- [openai-responses.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/openai-responses.ts) - OpenAI Responses API
- [openai-responses.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/openai-responses.ts) - OpenAI Responses API
- [google-generative-ai.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/google-generative-ai.ts) - Google Generative AI
- [google-generative-ai.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/google-generative-ai.ts) - Google Generative AI
- [bedrock-converse-stream.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/bedrock-converse-stream.ts) - AWS Bedrock
- [bedrock-converse-stream.ts](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/api/bedrock-converse-stream.ts) - AWS Bedrock

### Stream Pattern
### 流模式

All providers follow the same pattern:
所有提供商都遵循相同的模式：

```typescript
import {
  type AssistantMessage,
  type AssistantMessageEventStream,
  type Context,
  type Model,
  type SimpleStreamOptions,
  calculateCost,
  createAssistantMessageEventStream,
} from "@earendil-works/pi-ai";

function streamMyProvider(
  model: Model<any>,
  context: Context,
  options?: SimpleStreamOptions
): AssistantMessageEventStream {
  const stream = createAssistantMessageEventStream();

  (async () => {
    // Initialize output message
    const output: AssistantMessage = {
      role: "assistant",
      content: [],
      api: model.api,
      provider: model.provider,
      model: model.id,
      usage: {
        input: 0,
        output: 0,
        cacheRead: 0,
        cacheWrite: 0,
        totalTokens: 0,
        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, total: 0 },
      },
      stopReason: "pending",
      timestamp: Date.now(),
    };

    try {
      // Push start event
      stream.push({ type: "start", partial: output });

      // Make API request and process response...
      // Push content events as they arrive and set stopReason from the terminal event.
      if (output.stopReason === "pending") {
        throw new Error("Provider stream ended without a stop reason");
      }
      if (output.stopReason === "error" || output.stopReason === "aborted") {
        throw new Error(output.errorMessage || "An unknown error occurred");
      }

      // Push done event
      stream.push({
        type: "done",
        reason: output.stopReason,
        message: output
      });
      stream.end();
    } catch (error) {
      output.stopReason = options?.signal?.aborted ? "aborted" : "error";
      output.errorMessage = error instanceof Error ? error.message : String(error);
      stream.push({ type: "error", reason: output.stopReason, error: output });
      stream.end();
    }
  })();

  return stream;
}
```

### Event Types
### 事件类型

Push events via `stream.push()` in this order:
按以下顺序通过 `stream.push()` 推送事件：

1. `{ type: "start", partial: output }` - Stream started
1. `{ type: "start", partial: output }` - 流已开始

2. Content events (repeatable, track `contentIndex` for each block):
2. 内容事件（可重复，为每个块跟踪 `contentIndex`）：
   - `{ type: "text_start", contentIndex, partial }` - Text block started
   - `{ type: "text_start", contentIndex, partial }` - 文本块开始
   - `{ type: "text_delta", contentIndex, delta, partial }` - Text chunk
   - `{ type: "text_delta", contentIndex, delta, partial }` - 文本块片段
   - `{ type: "text_end", contentIndex, content, partial }` - Text block ended
   - `{ type: "text_end", contentIndex, content, partial }` - 文本块结束
   - `{ type: "thinking_start", contentIndex, partial }` - Thinking started
   - `{ type: "thinking_start", contentIndex, partial }` - 思考开始
   - `{ type: "thinking_delta", contentIndex, delta, partial }` - Thinking chunk
   - `{ type: "thinking_delta", contentIndex, delta, partial }` - 思考片段
   - `{ type: "thinking_end", contentIndex, content, partial }` - Thinking ended
   - `{ type: "thinking_end", contentIndex, content, partial }` - 思考结束
   - `{ type: "toolcall_start", contentIndex, partial }` - Tool call started
   - `{ type: "toolcall_start", contentIndex, partial }` - 工具调用开始
   - `{ type: "toolcall_delta", contentIndex, delta, partial }` - Tool call JSON chunk
   - `{ type: "toolcall_delta", contentIndex, delta, partial }` - 工具调用 JSON 片段
   - `{ type: "toolcall_end", contentIndex, toolCall, partial }` - Tool call ended
   - `{ type: "toolcall_end", contentIndex, toolCall, partial }` - 工具调用结束

3. `{ type: "done", reason, message }` or `{ type: "error", reason, error }` - Stream ended
3. `{ type: "done", reason, message }` 或 `{ type: "error", reason, error }` - 流结束

The `partial` field in each event contains the current `AssistantMessage` state. Update `output.content` as you receive data, then include `output` as the `partial`.
每个事件中的 `partial` 字段包含当前的 `AssistantMessage` 状态。在收到数据时更新 `output.content`，然后把 `output` 作为 `partial` 包含进去。

### Content Blocks
### 内容块

Add content blocks to `output.content` as they arrive:
在内容到达时把内容块添加到 `output.content`：

```typescript
// Text block
output.content.push({ type: "text", text: "" });
stream.push({ type: "text_start", contentIndex: output.content.length - 1, partial: output });

// As text arrives
const block = output.content[contentIndex];
if (block.type === "text") {
  block.text += delta;
  stream.push({ type: "text_delta", contentIndex, delta, partial: output });
}

// When block completes
stream.push({ type: "text_end", contentIndex, content: block.text, partial: output });
```

### Tool Calls
### 工具调用

Tool calls require accumulating JSON and parsing:
工具调用需要累积 JSON 并解析：

```typescript
// Start tool call
output.content.push({
  type: "toolCall",
  id: toolCallId,
  name: toolName,
  arguments: {}
});
stream.push({ type: "toolcall_start", contentIndex: output.content.length - 1, partial: output });

// Accumulate JSON
let partialJson = "";
partialJson += jsonDelta;
try {
  block.arguments = JSON.parse(partialJson);
} catch {}
stream.push({ type: "toolcall_delta", contentIndex, delta: jsonDelta, partial: output });

// Complete
stream.push({
  type: "toolcall_end",
  contentIndex,
  toolCall: { type: "toolCall", id, name, arguments: block.arguments },
  partial: output
});
```

### Usage and Cost
### 用量与成本

Update usage from API response and calculate cost:
从 API 响应更新用量并计算成本：

```typescript
output.usage.input = response.usage.input_tokens;
output.usage.output = response.usage.output_tokens;
output.usage.cacheRead = response.usage.cache_read_tokens ?? 0;
output.usage.cacheWrite = response.usage.cache_write_tokens ?? 0;
output.usage.totalTokens = output.usage.input + output.usage.output +
                           output.usage.cacheRead + output.usage.cacheWrite;
calculateCost(model, output.usage);
```

### Context Overflow Errors
### 上下文溢出错误

When a request exceeds the model's context window, pi can recover automatically by compacting the conversation and retrying. This recovery only kicks in if pi recognizes the failure as an overflow.
当请求超过模型的上下文窗口时，pi 可以通过压缩对话并重试来自动恢复。只有当 pi 把该失败识别为溢出时，这种恢复才会触发。

Detection runs on the finalized assistant message:
检测在最终确定的助手消息上运行：

- `stopReason === "error"`
- `stopReason === "error"`
- `errorMessage` matches one of pi's known overflow patterns (see [`packages/ai/src/utils/overflow.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/utils/overflow.ts))
- `errorMessage` 匹配 pi 已知的溢出模式之一（见 [`packages/ai/src/utils/overflow.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/utils/overflow.ts)）

If your provider returns overflow errors with a message pi does not recognize, normalize the error from the same extension that registers the provider. Use a `message_end` handler to rewrite the assistant message so its `errorMessage` starts with a phrase pi recognizes. The generic fallback `context_length_exceeded` is the safest choice.
如果你的提供商返回的溢出错误消息 pi 无法识别，请在注册该提供商的同一扩展中规范化该错误。使用 `message_end` 处理程序重写助手消息，使其 `errorMessage` 以 pi 认可的短语开头。通用后备 `context_length_exceeded` 是最安全的选择。

```typescript
const MY_PROVIDER_OVERFLOW_PATTERN = /your provider's overflow phrase/i;

export default function (pi: ExtensionAPI) {
  pi.registerProvider("my-provider", { /* ... */ });

  pi.on("message_end", (event, ctx) => {
    const message = event.message;
    if (message.role !== "assistant") return;
    if (message.stopReason !== "error") return;
    if (
      message.provider !== "my-provider" &&
      ctx.model?.provider !== "my-provider"
    )
      return;

    const errorMessage = message.errorMessage ?? "";
    if (errorMessage.includes("context_length_exceeded")) return;
    if (!MY_PROVIDER_OVERFLOW_PATTERN.test(errorMessage)) return;

    return {
      message: {
        ...message,
        errorMessage: `context_length_exceeded: ${errorMessage}`,
      },
    };
  });
}
```

`message_end` runs before pi tracks the assistant message for auto-compaction, so the rewritten `errorMessage` is what pi checks. With this in place, pi will:
`message_end` 在 pi 为自动压缩跟踪助手消息之前运行，因此被重写的 `errorMessage` 正是 pi 检查的内容。有了它，pi 将：

1. Detect the overflow from `errorMessage`.
1. 从 `errorMessage` 检测到溢出。
2. Drop the failed assistant message from live context.
2. 从实时上下文中丢弃失败的助手消息。
3. Run compaction.
3. 运行压缩。
4. Retry the request once.
4. 重试请求一次。

Guard the rewrite carefully:
请谨慎地限定重写范围：

- Scope it to your provider (`message.provider` and `ctx.model?.provider`) so unrelated errors from other providers are untouched.
- 把它限定在你的提供商（`message.provider` 和 `ctx.model?.provider`）上，这样来自其他提供商的无关错误不会被触碰。
- Match a provider-specific pattern, not pi's generic overflow patterns. Rewriting rate-limit or throttling errors (`rate limit`, `too many requests`) would falsely trigger compaction instead of pi's normal retry-with-backoff path.
- 匹配提供商特定的模式，而不是 pi 的通用溢出模式。重写速率限制或节流错误（`rate limit`、`too many requests`）会错误地触发压缩，而不是 pi 正常的退避重试路径。
- Skip when `errorMessage` already includes `context_length_exceeded` so the handler is idempotent.
- 当 `errorMessage` 已经包含 `context_length_exceeded` 时跳过，这样处理程序是幂等的。

### Registration
### 注册

Register your stream function:
注册你的流函数：

```typescript
pi.registerProvider("my-provider", {
  baseUrl: "https://api.example.com",
  apiKey: "$MY_API_KEY",
  api: "my-custom-api",
  models: [...],
  streamSimple: streamMyProvider
});
```

## Testing Your Implementation
## 测试你的实现

Test your provider against the same test suites used by built-in providers. Copy and adapt these test files from [packages/ai/test/](https://github.com/earendil-works/pi-mono/tree/main/packages/ai/test):
用与内置提供商相同的测试套件测试你的提供商。从 [packages/ai/test/](https://github.com/earendil-works/pi-mono/tree/main/packages/ai/test) 复制并改造这些测试文件：

| Test | Purpose |
|------|---------|
| `stream.test.ts` | Basic streaming, text output |
| `tokens.test.ts` | Token counting and usage |
| `abort.test.ts` | AbortSignal handling |
| `empty.test.ts` | Empty/minimal responses |
| `context-overflow.test.ts` | Context window limits |
| `image-limits.test.ts` | Image input handling |
| `unicode-surrogate.test.ts` | Unicode edge cases |
| `tool-call-without-result.test.ts` | Tool call edge cases |
| `image-tool-result.test.ts` | Images in tool results |
| `total-tokens.test.ts` | Total token calculation |
| `cross-provider-handoff.test.ts` | Context handoff between providers |

| 测试 | 目的 |
|------|---------|
| `stream.test.ts` | 基础流式传输、文本输出 |
| `tokens.test.ts` | Token 计数与用量 |
| `abort.test.ts` | AbortSignal 处理 |
| `empty.test.ts` | 空/最小响应 |
| `context-overflow.test.ts` | 上下文窗口限制 |
| `image-limits.test.ts` | 图片输入处理 |
| `unicode-surrogate.test.ts` | Unicode 边界情况 |
| `tool-call-without-result.test.ts` | 工具调用边界情况 |
| `image-tool-result.test.ts` | 工具结果中的图片 |
| `total-tokens.test.ts` | 总 token 计算 |
| `cross-provider-handoff.test.ts` | 提供商之间的上下文交接 |


Run tests with your provider/model pairs to verify compatibility.
用你的提供商/模型组合运行测试以验证兼容性。

## Config Reference
## 配置参考

```typescript
interface ProviderConfig {
  /** Display name for the provider in UI such as /login. */
  name?: string;

  /** API endpoint URL. Required when defining models. */
  baseUrl?: string;

  /** API key literal, env interpolation ($ENV_VAR or ${ENV_VAR}), or !command. Required when defining models (unless oauth). */
  apiKey?: string;

  /** API type for streaming. Required at provider or model level when defining models. */
  api?: Api;

  /** Custom streaming implementation for non-standard APIs. */
  streamSimple?: (
    model: Model<Api>,
    context: Context,
    options?: SimpleStreamOptions
  ) => AssistantMessageEventStream;

  /** Custom headers to include in requests. Values use the same resolution syntax as apiKey. */
  headers?: Record<string, string>;

  /** If true, adds Authorization: Bearer header with the resolved API key. */
  authHeader?: boolean;

  /** Models to register. If provided, replaces all existing models for this provider. */
  models?: ProviderModelConfig[];

  /** OAuth provider for /login support. */
  oauth?: {
    name: string;
    login(callbacks: OAuthLoginCallbacks): Promise<OAuthCredentials>;
    refreshToken(credentials: OAuthCredentials, signal: AbortSignal): Promise<OAuthCredentials>;
    getApiKey(credentials: OAuthCredentials): string;
  };
}
```

## Model Definition Reference
## 模型定义参考

```typescript
interface ProviderModelConfig {
  /** Model ID (e.g., "claude-sonnet-4-20250514"). */
  id: string;

  /** Display name (e.g., "Claude 4 Sonnet"). */
  name: string;

  /** API type override for this specific model. */
  api?: Api;

  /** API endpoint URL override for this specific model. */
  baseUrl?: string;

  /** Whether the model supports extended thinking. */
  reasoning: boolean;

  /** Maps pi thinking levels to provider/model-specific values; null marks a level unsupported. */
  thinkingLevelMap?: Partial<Record<"off" | "minimal" | "low" | "medium" | "high" | "xhigh" | "max", string | null>>;

  /** Supported input types. */
  input: ("text" | "image")[];

  /** Cost per million tokens (for usage tracking). */
  cost: {
    input: number;
    output: number;
    cacheRead: number;
    cacheWrite: number;
  };

  /** Maximum context window size in tokens. */
  contextWindow: number;

  /** Maximum output tokens. */
  maxTokens: number;

  /** Custom headers for this specific model. */
  headers?: Record<string, string>;

  /** Compatibility settings for the selected API. */
  compat?: {
    // openai-completions
    supportsStore?: boolean;
    supportsDeveloperRole?: boolean;
    supportsReasoningEffort?: boolean;
    supportsUsageInStreaming?: boolean;
    supportsFinishReason?: boolean;
    supportsStrictMode?: boolean;
    supportsOpenAIGrammarTools?: boolean; // openai-completions/openai-responses; false falls back to normal function tools
    maxTokensField?: "max_completion_tokens" | "max_tokens";
    requiresToolResultName?: boolean;
    requiresAssistantAfterToolResult?: boolean;
    requiresThinkingAsText?: boolean;
    requiresReasoningContentOnAssistantMessages?: boolean;
    thinkingFormat?: "openai" | "openrouter" | "deepseek" | "together" | "baseten" | "zai" | "qwen" | "chat-template" | "qwen-chat-template" | "string-thinking" | "ant-ling";
    chatTemplateKwargs?: Record<string, string | number | boolean | null | { "$var": "thinking.enabled" | "thinking.effort" | "thinking.budget"; omitWhenOff?: boolean }>;
    chatTemplateArgs?: Record<string, string | number | boolean | null | { "$var": "thinking.enabled" | "thinking.effort" | "thinking.budget"; omitWhenOff?: boolean }>;
    thinkingTokenBudgetField?: "thinking_token_budget" | "thinking_budget" | "thinking_budget_tokens";
    supportsThinkingTokenBudget?: boolean;
    cacheControlFormat?: "anthropic";
    sessionAffinityFormat?: "openai" | "openai-nosession" | "openrouter";
    sendSessionAffinityHeaders?: boolean;

    // anthropic-messages
    supportsEagerToolInputStreaming?: boolean;
    supportsLongCacheRetention?: boolean;
    sendSessionAffinityHeaders?: boolean;
    supportsCacheControlOnTools?: boolean;
    forceAdaptiveThinking?: boolean;
    allowEmptySignature?: boolean;
    supportsStrictTools?: boolean;
  };
}
```

`openrouter` sends `reasoning: { effort }`. `deepseek` sends `thinking: { type: "enabled" | "disabled" }` and `reasoning_effort` when enabled. `together` sends `reasoning: { enabled }` and also `reasoning_effort` when `supportsReasoningEffort` is enabled. `qwen` is for DashScope-style top-level `enable_thinking`. Use `qwen-chat-template` for local Qwen-compatible servers that read `chat_template_kwargs.enable_thinking` and need `preserve_thinking`. Use `chat-template` for configurable `chat_template_kwargs`, for example DeepSeek V3.x behind vLLM with `chatTemplateKwargs: { "thinking": { "$var": "thinking.enabled" } }`. Use `thinkingFormat: "baseten"` with `chatTemplateArgs` when the provider expects toggle values under `chat_template_args` and optionally supports top-level `reasoning_effort`.
`openrouter` 发送 `reasoning: { effort }`。`deepseek` 发送 `thinking: { type: "enabled" | "disabled" }`，启用时还发送 `reasoning_effort`。`together` 发送 `reasoning: { enabled }`，并在启用 `supportsReasoningEffort` 时也发送 `reasoning_effort`。`qwen` 用于 DashScope 风格的顶层 `enable_thinking`。对读取 `chat_template_kwargs.enable_thinking` 并需要 `preserve_thinking` 的本地 Qwen 兼容服务器使用 `qwen-chat-template`。对可配置的 `chat_template_kwargs` 使用 `chat-template`，例如 vLLM 后面的 DeepSeek V3.x 配合 `chatTemplateKwargs: { "thinking": { "$var": "thinking.enabled" } }`。当提供商期待 `chat_template_args` 下的切换值、并可选支持顶层 `reasoning_effort` 时，使用 `thinkingFormat: "baseten"` 配合 `chatTemplateArgs`。
`thinkingTokenBudgetField` sends a clamped per-level thinking budget as a top-level request field (`thinking_token_budget` on vLLM, `thinking_budget` on Qwen/SGLang, `thinking_budget_tokens` on llama.cpp). `supportsThinkingTokenBudget: true` is an alias for the vLLM field name. Do not combine it with `reasoning_effort` on DashScope Qwen models.
`thinkingTokenBudgetField` 把按等级钳制的思考预算作为顶层请求字段发送（vLLM 上为 `thinking_token_budget`，Qwen/SGLang 上为 `thinking_budget`，llama.cpp 上为 `thinking_budget_tokens`）。`supportsThinkingTokenBudget: true` 是 vLLM 字段名的别名。不要在 DashScope Qwen 模型上把它与 `reasoning_effort` 组合。
`cacheControlFormat: "anthropic"` applies Anthropic-style `cache_control` markers to the system prompt, last tool definition, and last user, assistant, or tool-result text content.
`cacheControlFormat: "anthropic"` 把 Anthropic 风格的 `cache_control` 标记应用到系统提示词、最后一个工具定义以及最后一条用户、助手或工具结果文本内容。
