> 📄 来源 Source: https://pi.dev/docs/latest/llama-cpp
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# llama.cpp
# llama.cpp

Pi supports the [llama.cpp](https://github.com/ggml-org/llama.cpp) router server. The router discovers multiple GGUF models and loads or unloads them on demand.
Pi 支持 [llama.cpp](https://github.com/ggml-org/llama.cpp) 路由服务器。该路由器会发现多个 GGUF 模型并按需加载或卸载。

Use a current llama.cpp build with router support. Follow the [build instructions](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md) or install a [prebuilt release](https://github.com/ggml-org/llama.cpp/releases) for your platform.
请使用带路由器支持的较新 llama.cpp 构建。遵循[构建说明](https://github.com/ggml-org/llama.cpp/blob/master/docs/build.md)，或为你的平台安装[预构建版本](https://github.com/ggml-org/llama.cpp/releases)。

## Start the router
## 启动路由器

Start `llama-server` without `--model` or `-m`. Passing a model starts single-model mode instead of router mode.
启动 `llama-server` 时不要带 `--model` 或 `-m`。传入模型会启动单模型模式而不是路由器模式。

```bash
llama-server \
  --models-dir ~/models \
  --no-models-autoload \
  --jinja \
  --host 127.0.0.1 \
  --port 8080 \
  -ngl 999 \
  -c 32768
```

Important options:
重要选项：

- `--models-dir ~/models` discovers local GGUF files.
- `--models-dir ~/models` 发现本地 GGUF 文件。
- `--no-models-autoload` keeps loading explicit through `/llama`.
- `--no-models-autoload` 让加载保持显式，通过 `/llama` 进行。
- `--jinja` enables compatible chat templates and tool calling.
- `--jinja` 启用兼容的聊天模板与工具调用。
- `-ngl 999` offloads as many layers as possible to the GPU.
- `-ngl 999` 尽可能多地把层卸载到 GPU。
- `-c 32768` sets the context window for each loaded model. Omit it to use the model's native context, which may require substantially more memory.
- `-c 32768` 为每个加载的模型设置上下文窗口。省略它则使用模型的原生上下文，这可能需要显著更多内存。

A single-file model can sit directly in the model directory. Put multimodal and multi-shard models in separate subdirectories:
单文件模型可以直接放在模型目录中。多模态和多分片模型请放在单独的子目录中：

```text
~/models/
├── llama-3.2-1b-Q4_K_M.gguf
├── gemma-3-4b-it-Q4_K_M/
│   ├── gemma-3-4b-it-Q4_K_M.gguf
│   └── mmproj-F16.gguf
└── large-model-Q4_K_M/
    ├── large-model-Q4_K_M-00001-of-00003.gguf
    ├── large-model-Q4_K_M-00002-of-00003.gguf
    └── large-model-Q4_K_M-00003-of-00003.gguf
```

Restart the router after manually adding files. For per-model context sizes and other options, use [llama.cpp model presets](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md#model-presets).
手动添加文件后请重启路由器。每个模型的上下文大小和其他选项请使用 [llama.cpp 模型预设](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md#model-presets)。

## Configure Pi
## 配置 Pi

Start Pi and configure the provider:
启动 Pi 并配置提供商：

```text
/login llama.cpp
```

Enter the router URL and optional API key. The default URL is `http://127.0.0.1:8080`.
输入路由器 URL 和可选的 API 密钥。默认 URL 为 `http://127.0.0.1:8080`。

If you start the router with `--no-models-autoload`, `/login llama.cpp` only stores the connection. Run `/llama` to load a model, then `/model` to select the loaded model for the current session.
如果你以 `--no-models-autoload` 启动路由器，`/login llama.cpp` 只保存连接。请运行 `/llama` 加载模型，然后运行 `/model` 为当前会话选择已加载的模型。

Environment variables can configure the same values without `/login`:
环境变量可以在不使用 `/login` 的情况下配置相同的值：

```bash
export LLAMA_BASE_URL=http://127.0.0.1:8080
export LLAMA_API_KEY=optional-secret
pi
```

If the server uses an API key, start `llama-server` with the matching `--api-key` value. Keep `--host 127.0.0.1` for local-only access.
如果服务器使用 API 密钥，请以匹配的 `--api-key` 值启动 `llama-server`。保持 `--host 127.0.0.1` 以仅限本地访问。

## Manage models
## 管理模型

Run:
运行：

```text
/llama
```

- Select an unloaded model to load it.
- 选择未加载的模型以加载它。
- Select a loaded model to unload it.
- 选择已加载的模型以卸载它。
- Select **Download model…**, search Hugging Face, then choose a repository and quantization. Exact `owner/repository[:quant]` values also work.
- 选择 **Download model…**，搜索 Hugging Face，然后选择仓库和量化。精确的 `owner/repository[:quant]` 值也可以。
- Press Escape during a load or download to confirm cancellation.
- 在加载或下载期间按 Escape 确认取消。

Hugging Face search uses `HF_TOKEN` when set, then checks `$HF_TOKEN_PATH`, `$HF_HOME/token`, `$XDG_CACHE_HOME/huggingface/token`, and `~/.cache/huggingface/token`. Search also works without authentication, subject to lower rate limits. Pi warns before downloading gated repositories and links to their access page. The llama.cpp server performs the download, so its process must also have `HF_TOKEN` when the selected repository requires access.
Hugging Face 搜索在设置了 `HF_TOKEN` 时使用它，然后依次检查 `$HF_TOKEN_PATH`、`$HF_HOME/token`、`$XDG_CACHE_HOME/huggingface/token` 和 `~/.cache/huggingface/token`。未认证也可以搜索，但速率限制更低。Pi 在下载受限（gated）仓库前会发出警告并链接到其访问页面。下载由 llama.cpp 服务器执行，因此当所选仓库需要访问权限时，其进程也必须有 `HF_TOKEN`。

If other models are loaded, Pi asks whether to unload them first or keep them loaded. Pi does not silently unload models and never deletes model files. The router may be shared with other clients, so `/llama` always displays the router's current state.
如果加载了其他模型，Pi 会询问是先卸载它们还是保持加载。Pi 不会悄悄卸载模型，也从不删除模型文件。路由器可能与其他客户端共享，因此 `/llama` 总是显示路由器的当前状态。

Only loaded models appear in `/model`. After loading a model, run `/model` to select it for the current Pi session.
只有已加载的模型会出现在 `/model` 中。加载模型后，运行 `/model` 为当前 Pi 会话选择它。

If the router disconnects, `/llama` shows **Retry** and **Close**. Retry reconnects and refreshes model state without replaying the interrupted operation.
如果路由器断开连接，`/llama` 会显示 **Retry** 和 **Close**。Retry 会重新连接并刷新模型状态，而不会重放被中断的操作。

## Troubleshooting
## 故障排除

Check that the router is reachable:
检查路由器是否可达：

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/models
```

- **No models in `/llama`:** Check `--models-dir`, the directory layout, and restart the router.
- **`/llama` 中没有模型：** 检查 `--models-dir` 和目录布局，并重启路由器。
- **Model missing from `/model`:** Load it with `/llama` first.
- **`/model` 中缺少模型：** 先用 `/llama` 加载它。
- **Load fails or uses too much memory:** Lower `-c` or unload another model.
- **加载失败或占用内存过多：** 调低 `-c` 或卸载其他模型。
- **Server is not in router mode:** Start it without `--model`, `-m`, or `-hf`.
- **服务器不在路由器模式：** 启动时不要带 `--model`、`-m` 或 `-hf`。
