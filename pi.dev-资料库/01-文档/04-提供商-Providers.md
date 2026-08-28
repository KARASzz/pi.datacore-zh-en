> 📄 来源 Source: https://pi.dev/docs/latest/providers
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Providers
# 提供商

Pi supports subscription-based providers via OAuth and API key providers via environment variables or auth file. Built-in catalogs ship with pi; configured providers may refresh newer catalogs and cache them in `~/.pi/agent/models-store.json` for offline use.
Pi 通过 OAuth 支持订阅制提供商，并通过环境变量或认证文件支持 API 密钥型提供商。内置目录随 pi 一起发布；配置的提供商可以刷新更新的目录并缓存到 `~/.pi/agent/models-store.json` 供离线使用。

## Table of Contents
## 目录

- [Subscriptions](#subscriptions)
- [订阅](#subscriptions)
- [API Keys](#api-keys)
- [API 密钥](#api-keys)
- [Auth File](#auth-file)
- [认证文件](#auth-file)
- [Cloud Providers](#cloud-providers)
- [云提供商](#cloud-providers)
- [llama.cpp](#llamacpp)
- [llama.cpp](#llamacpp)
- [Custom Providers](#custom-providers)
- [自定义提供商](#custom-providers)
- [Resolution Order](#resolution-order)
- [解析顺序](#resolution-order)

## Subscriptions
## 订阅

Use `/login` in interactive mode, then select a provider:
在交互模式中使用 `/login`，然后选择一个提供商：

- ChatGPT Plus/Pro (Codex)
- ChatGPT Plus/Pro（Codex）
- Claude Pro/Max
- Claude Pro/Max
- GitHub Copilot
- GitHub Copilot
- xAI (Grok/X subscription)
- xAI（Grok/X 订阅）
- OpenRouter (OAuth-minted API key billed from OpenRouter credits)
- OpenRouter（OAuth 铸造的 API 密钥，从 OpenRouter 额度计费）
- Radius
- Radius

Use `/logout` to clear credentials. Tokens are stored in `~/.pi/agent/auth.json` and auto-refresh when expired. OpenRouter instead mints a user-controlled API key that does not expire automatically.
使用 `/logout` 清除凭据。令牌存储在 `~/.pi/agent/auth.json` 中，过期时自动刷新。OpenRouter 则铸造一个由用户控制的、不会自动过期的 API 密钥。

### OpenAI Codex
### OpenAI Codex

- Requires ChatGPT Plus or Pro subscription
- 需要 ChatGPT Plus 或 Pro 订阅
- Officially endorsed by OpenAI: [Codex for OSS](https://developers.openai.com/community/codex-for-oss)
- 获得 OpenAI 官方认可：[Codex for OSS](https://developers.openai.com/community/codex-for-oss)

### Claude Pro/Max
### Claude Pro/Max

Anthropic subscription auth is active for Claude Pro/Max accounts. Third-party harness usage draws from [extra usage](https://claude.ai/settings/usage) and is billed per token, not against Claude plan limits.
Anthropic 订阅认证对 Claude Pro/Max 账户开放。第三方框架的使用从[额外用量](https://claude.ai/settings/usage)中扣除，按 token 计费，不占用 Claude 套餐限额。

### GitHub Copilot
### GitHub Copilot

- Press Enter for github.com, or enter your GitHub Enterprise Server domain
- 对 github.com 按回车，或输入你的 GitHub Enterprise Server 域名
- If you get "model not supported", enable it in VS Code: Copilot Chat → model selector → select model → "Enable"
- 如果出现“模型不受支持”，请在 VS Code 中启用它：Copilot Chat → 模型选择器 → 选择模型 → “Enable”

### xAI (Grok/X subscription)
### xAI（Grok/X 订阅）

- Run `/login xai`, then select **Use a subscription**
- 运行 `/login xai`，然后选择 **Use a subscription**
- `XAI_API_KEY` remains available through **Use an API key**
- `XAI_API_KEY` 仍可通过 **Use an API key** 使用

### OpenRouter
### OpenRouter

- Run `/login openrouter`, then select **Sign in with OpenRouter** to open the OpenRouter PKCE authorization flow
- 运行 `/login openrouter`，然后选择 **Sign in with OpenRouter** 以打开 OpenRouter PKCE 授权流程
- The authorization creates a user-controlled OpenRouter API key billed from your OpenRouter credits
- 授权会创建一个由用户控制的 OpenRouter API 密钥，从你的 OpenRouter 额度计费
- On remote/headless machines (e.g. over SSH) the browser cannot reach the loopback callback; paste the final redirect URL (or the authorization code) into the login prompt instead
- 在远程/无界面机器上（例如通过 SSH），浏览器无法访问回环回调；请把最终的重定向 URL（或授权码）粘贴到登录提示中
- `OPENROUTER_API_KEY` remains available through **Use an API key**
- `OPENROUTER_API_KEY` 仍可通过 **Use an API key** 使用

### Radius
### Radius

Radius is a dynamic `pi-messages` gateway. `/login radius` stores OAuth tokens in `auth.json`; the gateway catalog is refreshed independently and cached in `models-store.json`. Custom Radius gateways can be declared in `models.json` with `"oauth": "radius"` and a gateway `baseUrl`.
Radius 是一个动态的 `pi-messages` 网关。`/login radius` 把 OAuth 令牌存储在 `auth.json` 中；网关目录独立刷新并缓存在 `models-store.json` 中。自定义 Radius 网关可以在 `models.json` 中用 `"oauth": "radius"` 和网关 `baseUrl` 声明。

## API Keys
## API 密钥

### Environment Variables or Auth File
### 环境变量或认证文件

Use `/login` in interactive mode and select a provider to store an API key in `auth.json`, or set credentials via environment variable:
在交互模式中使用 `/login` 并选择一个提供商，把 API 密钥存储到 `auth.json`，或通过环境变量设置凭据：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
pi
```

| Provider | Environment Variable | `auth.json` key |
|----------|----------------------|------------------|
| Anthropic | `ANTHROPIC_API_KEY` | `anthropic` |
| Ant Ling | `ANT_LING_API_KEY` | `ant-ling` |
| Azure OpenAI Responses | `AZURE_OPENAI_API_KEY` | `azure-openai-responses` |
| OpenAI | `OPENAI_API_KEY` | `openai` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek` |
| NVIDIA NIM | `NVIDIA_API_KEY` | `nvidia` |
| Google Gemini | `GEMINI_API_KEY` | `google` |
| Amazon Bedrock | `AWS_BEARER_TOKEN_BEDROCK` | `amazon-bedrock` |
| Mistral | `MISTRAL_API_KEY` | `mistral` |
| Groq | `GROQ_API_KEY` | `groq` |
| Cerebras | `CEREBRAS_API_KEY` | `cerebras` |
| Cloudflare AI Gateway | `CLOUDFLARE_API_KEY` (+ `CLOUDFLARE_ACCOUNT_ID`, `CLOUDFLARE_GATEWAY_ID`) | `cloudflare-ai-gateway` |
| Cloudflare Workers AI | `CLOUDFLARE_API_KEY` (+ `CLOUDFLARE_ACCOUNT_ID`) | `cloudflare-workers-ai` |
| xAI | `XAI_API_KEY` | `xai` |
| OpenRouter | `OPENROUTER_API_KEY` | `openrouter` |
| Vercel AI Gateway | `AI_GATEWAY_API_KEY` | `vercel-ai-gateway` |
| ZAI Coding Plan (Global) | `ZAI_API_KEY` | `zai` |
| ZAI Coding Plan (China) | `ZAI_CODING_CN_API_KEY` | `zai-coding-cn` |
| OpenCode Zen | `OPENCODE_API_KEY` | `opencode` |
| OpenCode Go | `OPENCODE_API_KEY` | `opencode-go` |
| Radius | `RADIUS_API_KEY` | `radius` |
| Hugging Face | `HF_TOKEN` | `huggingface` |
| Fireworks | `FIREWORKS_API_KEY` | `fireworks` |
| Together AI | `TOGETHER_API_KEY` | `together` |
| Baseten | `BASETEN_API_KEY` | `baseten` |
| Kimi For Coding | `KIMI_API_KEY` | `kimi-coding` |
| MiniMax | `MINIMAX_API_KEY` | `minimax` |
| MiniMax (China) | `MINIMAX_CN_API_KEY` | `minimax-cn` |
| Qwen Token Plan (existing catalog) | `QWEN_TOKEN_PLAN_API_KEY` | `qwen-token-plan` |
| Qwen Token Plan (Individual) | `QWEN_TOKEN_PLAN_API_KEY` | `qwen-token-plan-individual` |
| Qwen Token Plan (China) | `QWEN_TOKEN_PLAN_CN_API_KEY` | `qwen-token-plan-cn` |
| Xiaomi MiMo | `XIAOMI_API_KEY` | `xiaomi` |
| Xiaomi MiMo Token Plan (China) | `XIAOMI_TOKEN_PLAN_CN_API_KEY` | `xiaomi-token-plan-cn` |
| Xiaomi MiMo Token Plan (Amsterdam) | `XIAOMI_TOKEN_PLAN_AMS_API_KEY` | `xiaomi-token-plan-ams` |
| Xiaomi MiMo Token Plan (Singapore) | `XIAOMI_TOKEN_PLAN_SGP_API_KEY` | `xiaomi-token-plan-sgp` |

| 提供商 | 环境变量 | `auth.json` 键 |
|----------|----------------------|------------------|
| Anthropic | `ANTHROPIC_API_KEY` | `anthropic` |
| Ant Ling | `ANT_LING_API_KEY` | `ant-ling` |
| Azure OpenAI Responses | `AZURE_OPENAI_API_KEY` | `azure-openai-responses` |
| OpenAI | `OPENAI_API_KEY` | `openai` |
| DeepSeek | `DEEPSEEK_API_KEY` | `deepseek` |
| NVIDIA NIM | `NVIDIA_API_KEY` | `nvidia` |
| Google Gemini | `GEMINI_API_KEY` | `google` |
| Amazon Bedrock | `AWS_BEARER_TOKEN_BEDROCK` | `amazon-bedrock` |
| Mistral | `MISTRAL_API_KEY` | `mistral` |
| Groq | `GROQ_API_KEY` | `groq` |
| Cerebras | `CEREBRAS_API_KEY` | `cerebras` |
| Cloudflare AI Gateway | `CLOUDFLARE_API_KEY`（+ `CLOUDFLARE_ACCOUNT_ID`、`CLOUDFLARE_GATEWAY_ID`） | `cloudflare-ai-gateway` |
| Cloudflare Workers AI | `CLOUDFLARE_API_KEY`（+ `CLOUDFLARE_ACCOUNT_ID`） | `cloudflare-workers-ai` |
| xAI | `XAI_API_KEY` | `xai` |
| OpenRouter | `OPENROUTER_API_KEY` | `openrouter` |
| Vercel AI Gateway | `AI_GATEWAY_API_KEY` | `vercel-ai-gateway` |
| ZAI Coding Plan（国际） | `ZAI_API_KEY` | `zai` |
| ZAI Coding Plan（中国） | `ZAI_CODING_CN_API_KEY` | `zai-coding-cn` |
| OpenCode Zen | `OPENCODE_API_KEY` | `opencode` |
| OpenCode Go | `OPENCODE_API_KEY` | `opencode-go` |
| Radius | `RADIUS_API_KEY` | `radius` |
| Hugging Face | `HF_TOKEN` | `huggingface` |
| Fireworks | `FIREWORKS_API_KEY` | `fireworks` |
| Together AI | `TOGETHER_API_KEY` | `together` |
| Baseten | `BASETEN_API_KEY` | `baseten` |
| Kimi For Coding | `KIMI_API_KEY` | `kimi-coding` |
| MiniMax | `MINIMAX_API_KEY` | `minimax` |
| MiniMax（中国） | `MINIMAX_CN_API_KEY` | `minimax-cn` |
| Qwen Token Plan（现有目录） | `QWEN_TOKEN_PLAN_API_KEY` | `qwen-token-plan` |
| Qwen Token Plan（个人版） | `QWEN_TOKEN_PLAN_API_KEY` | `qwen-token-plan-individual` |
| Qwen Token Plan（中国） | `QWEN_TOKEN_PLAN_CN_API_KEY` | `qwen-token-plan-cn` |
| Xiaomi MiMo | `XIAOMI_API_KEY` | `xiaomi` |
| Xiaomi MiMo Token Plan（中国） | `XIAOMI_TOKEN_PLAN_CN_API_KEY` | `xiaomi-token-plan-cn` |
| Xiaomi MiMo Token Plan（阿姆斯特丹） | `XIAOMI_TOKEN_PLAN_AMS_API_KEY` | `xiaomi-token-plan-ams` |
| Xiaomi MiMo Token Plan（新加坡） | `XIAOMI_TOKEN_PLAN_SGP_API_KEY` | `xiaomi-token-plan-sgp` |


Reference for environment variables and `auth.json` keys: [`const envMap`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/env-api-keys.ts) in [`packages/ai/src/env-api-keys.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/env-api-keys.ts).
环境变量和 `auth.json` 键的参考：[`packages/ai/src/env-api-keys.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/env-api-keys.ts) 中的 [`const envMap`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/env-api-keys.ts)。

#### Auth File
#### 认证文件

Store credentials in `~/.pi/agent/auth.json`:
把凭据存储在 `~/.pi/agent/auth.json`：

```json
{
  "anthropic": { "type": "api_key", "key": "sk-ant-..." },
  "ant-ling": { "type": "api_key", "key": "..." },
  "openai": { "type": "api_key", "key": "sk-..." },
  "deepseek": { "type": "api_key", "key": "sk-..." },
  "nvidia": { "type": "api_key", "key": "nvapi-..." },
  "google": { "type": "api_key", "key": "..." },
  "opencode": { "type": "api_key", "key": "..." },
  "opencode-go": { "type": "api_key", "key": "..." },
  "together": { "type": "api_key", "key": "..." },
  "qwen-token-plan":  { "type": "api_key", "key": "sk-sp-..." },
  "qwen-token-plan-individual": { "type": "api_key", "key": "sk-sp-..." },
  "qwen-token-plan-cn": { "type": "api_key", "key": "sk-sp-..." },
  "xiaomi": { "type": "api_key", "key": "..." },
  "xiaomi-token-plan-cn":  { "type": "api_key", "key": "..." },
  "xiaomi-token-plan-ams": { "type": "api_key", "key": "..." },
  "xiaomi-token-plan-sgp": { "type": "api_key", "key": "..." }
}
```

`qwen-token-plan-individual` uses the same international endpoint and `QWEN_TOKEN_PLAN_API_KEY` as
`qwen-token-plan-individual` 使用与 `qwen-token-plan` 相同的国际端点和 `QWEN_TOKEN_PLAN_API_KEY`，
`qwen-token-plan`, but limits the picker to the models documented for Individual subscriptions. The existing
但把选择器限制为面向个人订阅所记录的模型。现有的
provider keeps its broader catalog for backward compatibility. When using `auth.json`, store the
提供商为保持向后兼容保留其更广泛的目录。使用 `auth.json` 时，请把
credential under the provider you select; an environment variable is shared by both international providers.
凭据存储在你所选的提供商下；环境变量由两个国际提供商共享。

The file is created with `0600` permissions (user read/write only). Auth file credentials take priority over environment variables.
该文件以 `0600` 权限创建（仅用户可读写）。认证文件凭据优先于环境变量。

API key credentials can also include provider-scoped environment values. These values are used before process environment variables when resolving the credential key, provider/model headers, and provider configuration such as Cloudflare account IDs, Azure OpenAI settings, Vertex project/location, Bedrock settings, `PI_CACHE_RETENTION`, and `HTTP_PROXY`/`HTTPS_PROXY`.
API 密钥凭据还可以包含提供商作用域的环境值。在解析凭据密钥、提供商/模型请求头以及提供商配置（如 Cloudflare 账户 ID、Azure OpenAI 设置、Vertex 项目/位置、Bedrock 设置、`PI_CACHE_RETENTION` 和 `HTTP_PROXY`/`HTTPS_PROXY`）时，这些值先于进程环境变量使用。

```json
{
  "cloudflare-ai-gateway": {
    "type": "api_key",
    "key": "$CLOUDFLARE_API_KEY",
    "env": {
      "CLOUDFLARE_API_KEY": "...",
      "CLOUDFLARE_ACCOUNT_ID": "account-id",
      "CLOUDFLARE_GATEWAY_ID": "gateway-id"
    }
  }
}
```

Use this when pi should use different provider settings than the project shell environment.
当 pi 需要使用与项目 shell 环境不同的提供商设置时，请使用此功能。

### Key Resolution
### 密钥解析

The `key` field supports command execution, environment interpolation, and literals:
`key` 字段支持命令执行、环境变量插值和字面量：

- **Shell command:** `"!command"` at the start executes the whole value as a command and uses stdout (cached for process lifetime)
- **Shell 命令：** 以 `"!command"` 开头会把整个值作为命令执行并使用其 stdout（在进程生命周期内缓存）
  ```json
  { "type": "api_key", "key": "!security find-generic-password -ws 'anthropic'" }
  { "type": "api_key", "key": "!op read 'op://vault/item/credential'" }
  ```
- **Environment interpolation:** `"$ENV_VAR"` or `"${ENV_VAR}"` uses the value of the named variable. Interpolation works inside larger literals.
- **环境变量插值：** `"$ENV_VAR"` 或 `"${ENV_VAR}"` 使用指定变量的值。插值也可用于更大的字面量内部。
  ```json
  { "type": "api_key", "key": "$MY_ANTHROPIC_KEY" }
  { "type": "api_key", "key": "${KEY_PREFIX}_${KEY_SUFFIX}" }
  ```
  `$FOO_BAR` is the variable `FOO_BAR`; use `${FOO}_BAR` when `BAR` is literal text. Missing environment variables make the value unresolved.
  `$FOO_BAR` 是变量 `FOO_BAR`；当 `BAR` 是字面文本时用 `${FOO}_BAR`。缺失的环境变量会使该值无法解析。
- **Escapes:** `"$$"` emits a literal `"$"`; `"$!"` emits a literal `"!"` without triggering command execution.
- **转义：** `"$$"` 输出字面量 `"$"`；`"$!"` 输出字面量 `"!"`，不触发命令执行。
  ```json
  { "type": "api_key", "key": "$$literal-dollar-prefix" }
  { "type": "api_key", "key": "$!literal-bang-prefix" }
  ```
- **Literal value:** Used directly. Plain uppercase strings such as `MY_API_KEY` are literals; use `$MY_API_KEY` for environment variables.
- **字面量值：** 直接使用。诸如 `MY_API_KEY` 的纯大写字符串是字面量；环境变量请用 `$MY_API_KEY`。
  ```json
  { "type": "api_key", "key": "sk-ant-..." }
  { "type": "api_key", "key": "public" }
  ```

OAuth credentials are also stored here after `/login` and managed automatically.
OAuth 凭据在 `/login` 之后也存储在这里，并自动管理。

## Cloud Providers
## 云提供商

### Azure OpenAI
### Azure OpenAI

```bash
export AZURE_OPENAI_API_KEY=...
export AZURE_OPENAI_BASE_URL=https://your-resource.ai.azure.com
# also supported: https://your-resource.cognitiveservices.azure.com
# also supported: https://your-resource.openai.azure.com
# root endpoints are auto-normalized to /openai/v1
# or use resource name instead of base URL
export AZURE_OPENAI_RESOURCE_NAME=your-resource

# Optional
export AZURE_OPENAI_API_VERSION=2024-02-01
export AZURE_OPENAI_DEPLOYMENT_NAME_MAP=gpt-4=my-gpt4,gpt-4o=my-gpt4o
```

### Amazon Bedrock
### Amazon Bedrock

Use `/login amazon-bedrock` to store a Bedrock API key, or configure one of the ambient AWS credential sources below:
使用 `/login amazon-bedrock` 存储 Bedrock API 密钥，或配置以下任一环境式 AWS 凭据来源：

```bash
# Option 1: AWS Profile
export AWS_PROFILE=your-profile

# Option 2: IAM Keys
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...

# Option 3: Bearer Token
export AWS_BEARER_TOKEN_BEDROCK=...

# Optional region (defaults to us-east-1)
export AWS_REGION=us-west-2
```

Also supports ECS task roles (`AWS_CONTAINER_CREDENTIALS_*`) and IRSA (`AWS_WEB_IDENTITY_TOKEN_FILE`).
还支持 ECS 任务角色（`AWS_CONTAINER_CREDENTIALS_*`）和 IRSA（`AWS_WEB_IDENTITY_TOKEN_FILE`）。

```bash
pi --provider amazon-bedrock --model us.anthropic.claude-sonnet-4-20250514-v1:0
```

Prompt caching is enabled automatically for Claude models whose ID contains a recognizable model name (base models and system-defined inference profiles). For application inference profiles (whose ARNs don't contain the model name), set `AWS_BEDROCK_FORCE_CACHE=1` to enable cache points:
对于 ID 中包含可识别模型名称的 Claude 模型（基础模型和系统定义的推理配置文件），提示词缓存会自动启用。对于应用推理配置文件（其 ARN 不包含模型名称），请设置 `AWS_BEDROCK_FORCE_CACHE=1` 以启用缓存点：

```bash
export AWS_BEDROCK_FORCE_CACHE=1
pi --provider amazon-bedrock --model arn:aws:bedrock:us-east-1:123456789012:application-inference-profile/abc123
```

If you are connecting to a Bedrock API proxy, the following environment variables can be used:
如果你连接的是 Bedrock API 代理，可以使用以下环境变量：

```bash
# Set the URL for the Bedrock proxy (standard AWS SDK env var)
export AWS_ENDPOINT_URL_BEDROCK_RUNTIME=https://my.corp.proxy/bedrock

# Set if your proxy does not require authentication
export AWS_BEDROCK_SKIP_AUTH=1

# Set if your proxy only supports HTTP/1.1
export AWS_BEDROCK_FORCE_HTTP1=1
```

### Cloudflare AI Gateway
### Cloudflare AI Gateway

`CLOUDFLARE_API_KEY` can be set via `/login`. The account ID and gateway slug can be set as environment variables or in the API key credential's `env` object in `auth.json`.
`CLOUDFLARE_API_KEY` 可以通过 `/login` 设置。账户 ID 和网关 slug 可以设置为环境变量，或在 `auth.json` 中 API 密钥凭据的 `env` 对象中设置。

```bash
export CLOUDFLARE_API_KEY=...           # or use /login
export CLOUDFLARE_ACCOUNT_ID=...
export CLOUDFLARE_GATEWAY_ID=...        # create at dash.cloudflare.com → AI → AI Gateway
pi --provider cloudflare-ai-gateway --model "claude-sonnet-4-5"
```

Routes to OpenAI, Anthropic, and Workers AI through Cloudflare AI Gateway. Workers AI uses the Unified API (`/compat`) and prefixed model IDs (`workers-ai/@cf/...`). OpenAI uses the OpenAI passthrough route (`/openai`) with native OpenAI model IDs such as `gpt-5.1`. Anthropic uses the Anthropic passthrough route (`/anthropic`) with native Anthropic model IDs such as `claude-sonnet-4-5`.
通过 Cloudflare AI Gateway 路由到 OpenAI、Anthropic 和 Workers AI。Workers AI 使用统一 API（`/compat`）和带前缀的模型 ID（`workers-ai/@cf/...`）。OpenAI 使用 OpenAI 直通路由（`/openai`）和原生 OpenAI 模型 ID，例如 `gpt-5.1`。Anthropic 使用 Anthropic 直通路由（`/anthropic`）和原生 Anthropic 模型 ID，例如 `claude-sonnet-4-5`。

AI Gateway authentication uses `CLOUDFLARE_API_KEY` as `cf-aig-authorization`. Upstream authentication can be one of:
AI Gateway 认证使用 `CLOUDFLARE_API_KEY` 作为 `cf-aig-authorization`。上游认证可以是以下之一：

| Mode | Request auth | Upstream auth |
|------|--------------|---------------|
| Workers AI | Cloudflare token only | Cloudflare-native |
| Unified billing | Cloudflare token only | Cloudflare handles upstream auth and deducts credits |
| Stored BYOK | Cloudflare token only | Cloudflare injects provider keys stored in the AI Gateway dashboard |
| Inline BYOK | Cloudflare token plus upstream `Authorization` header | The request supplies the upstream provider key |

| 模式 | 请求认证 | 上游认证 |
|------|--------------|---------------|
| Workers AI | 仅 Cloudflare 令牌 | Cloudflare 原生 |
| 统一计费 | 仅 Cloudflare 令牌 | Cloudflare 处理上游认证并扣除额度 |
| 存储式 BYOK | 仅 Cloudflare 令牌 | Cloudflare 注入存储在 AI Gateway 控制台中的提供商密钥 |
| 内联 BYOK | Cloudflare 令牌加上上游 `Authorization` 头 | 请求本身提供上游提供商密钥 |


For normal pi usage, prefer unified billing or stored BYOK. Inline BYOK requires configuring an additional upstream `Authorization` header for the Cloudflare AI Gateway provider, for example via a `models.json` provider/model override.
对于正常的 pi 使用，建议使用统一计费或存储式 BYOK。内联 BYOK 需要为 Cloudflare AI Gateway 提供商配置额外的上游 `Authorization` 头，例如通过 `models.json` 提供商/模型覆盖。

### Cloudflare Workers AI
### Cloudflare Workers AI

`CLOUDFLARE_API_KEY` can be set via `/login`. `CLOUDFLARE_ACCOUNT_ID` can be set as an environment variable or in the API key credential's `env` object in `auth.json`.
`CLOUDFLARE_API_KEY` 可以通过 `/login` 设置。`CLOUDFLARE_ACCOUNT_ID` 可以设置为环境变量，或在 `auth.json` 中 API 密钥凭据的 `env` 对象中设置。

```bash
export CLOUDFLARE_API_KEY=...           # or use /login
export CLOUDFLARE_ACCOUNT_ID=...
pi --provider cloudflare-workers-ai --model "@cf/moonshotai/kimi-k2.6"
```

Pi automatically sets `x-session-affinity` for [prefix caching](https://developers.cloudflare.com/workers-ai/features/prompt-caching/) discounts.
Pi 自动为[前缀缓存](https://developers.cloudflare.com/workers-ai/features/prompt-caching/)优惠设置 `x-session-affinity`。

### Google Vertex AI
### Google Vertex AI

Uses Application Default Credentials:
使用应用默认凭据（Application Default Credentials）：

```bash
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT=your-project
export GOOGLE_CLOUD_LOCATION=us-central1
```

Or set `GOOGLE_APPLICATION_CREDENTIALS` to a service account key file.
或者把 `GOOGLE_APPLICATION_CREDENTIALS` 设置为服务账户密钥文件。

## llama.cpp
## llama.cpp

Pi supports the llama.cpp router server. Configure it with `/login llama.cpp`, manage loaded models with `/llama`, and select a loaded model with `/model`.
Pi 支持 llama.cpp 路由服务器。用 `/login llama.cpp` 配置，用 `/llama` 管理已加载的模型，用 `/model` 选择已加载的模型。

See [llama.cpp](llama-cpp.md) for server setup, model directory layout, environment variables, and command usage.
服务器搭建、模型目录布局、环境变量和命令用法参见 [llama.cpp](llama-cpp.md)。

## Custom Providers
## 自定义提供商

**Via models.json:** Add Ollama, LM Studio, vLLM, or any provider that speaks a supported API (OpenAI Completions, OpenAI Responses, Anthropic Messages, Google Generative AI). See [models.md](models.md).
**通过 models.json：** 添加 Ollama、LM Studio、vLLM 或任何说所支持 API（OpenAI Completions、OpenAI Responses、Anthropic Messages、Google Generative AI）的提供商。参见 [models.md](models.md)。

**Via extensions:** For providers that need custom API implementations or OAuth flows, create an extension. See [custom-provider.md](custom-provider.md) and [examples/extensions/custom-provider-gitlab-duo](../examples/extensions/custom-provider-gitlab-duo/).
**通过扩展：** 对于需要自定义 API 实现或 OAuth 流程的提供商，请创建扩展。参见 [custom-provider.md](custom-provider.md) 和 [examples/extensions/custom-provider-gitlab-duo](../examples/extensions/custom-provider-gitlab-duo/)。

## Resolution Order
## 解析顺序

When resolving credentials for a provider:
解析提供商的凭据时：

1. CLI `--api-key` flag
1. CLI `--api-key` 标志
2. `auth.json` entry (API key or OAuth token)
2. `auth.json` 条目（API 密钥或 OAuth 令牌）
3. Environment variable
3. 环境变量
4. Custom provider keys from `models.json`
4. 来自 `models.json` 的自定义提供商密钥
