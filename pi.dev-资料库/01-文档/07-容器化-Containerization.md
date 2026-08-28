> 📄 来源 Source: https://pi.dev/docs/latest/containerization
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Containerization
# 容器化

Pi runs with all permissions by default, but in some cases, you will want to have more control over what directories Pi can write to and which accesses it has.
Pi 默认以全部权限运行，但在某些情况下，你会希望对 Pi 可以写入哪些目录、拥有哪些访问权限有更多控制。

There are two general options. You can either
有两种通用方案。你可以：
1. run the whole `pi` process inside an isolated environment, or
1. 在隔离环境中运行整个 `pi` 进程，或者
2. run `pi` on the host and route tool execution into an isolated environment.
2. 在宿主机上运行 `pi`，并将工具执行路由到隔离环境中。

## Choose a pattern
## 选择模式

| Pattern | What is isolated | Best for | Notes |
| --- | --- | --- | --- |
| Gondolin extension | Built-in tools and `!` commands | Local micro-VM isolation while keeping auth on host | See [`examples/extensions/gondolin/`](../examples/extensions/gondolin/). |
| Plain Docker | Whole `pi` process in a local container | Simple local isolation | Provider API keys enter the container. |
| OpenShell | Whole `pi` process in a policy-controlled sandbox | Local or remote managed sandbox | Requires an OpenShell gateway |

| 模式 | 隔离什么 | 最适合 | 备注 |
| --- | --- | --- | --- |
| Gondolin 扩展 | 内置工具和 `!` 命令 | 在认证保留在宿主机的同时获得本地微型虚拟机隔离 | 见 [`examples/extensions/gondolin/`](../examples/extensions/gondolin/)。 |
| 普通 Docker | 整个 `pi` 进程运行在本地容器中 | 简单的本地隔离 | 提供商 API 密钥会进入容器。 |
| OpenShell | 整个 `pi` 进程运行在策略受控的沙箱中 | 本地或远程托管沙箱 | 需要 OpenShell 网关 |


Extensions run wherever the `pi` process runs. If you run host `pi` with a tool-routing extension, other custom extension tools still run on the host unless they also delegate their operations.
扩展运行在 `pi` 进程所在的任何地方。如果你在宿主机上运行 `pi` 并使用工具路由扩展，其他自定义扩展工具仍会在宿主机上运行，除非它们也委托其操作。

## Gondolin
## Gondolin

[Gondolin](https://github.com/earendil-works/gondolin) is a local Linux micro-VM.
[Gondolin](https://github.com/earendil-works/gondolin) 是一个本地 Linux 微型虚拟机。
Use the [example extension](../examples/extensions/gondolin) when you want `pi` on the host but all built-in tools routed into the VM.
当你想让 `pi` 运行在宿主机上、但所有内置工具都路由进虚拟机时，请使用[示例扩展](../examples/extensions/gondolin)。

Setup:
安装：

```bash
cp -R packages/coding-agent/examples/extensions/gondolin ~/.pi/agent/extensions/gondolin
cd ~/.pi/agent/extensions/gondolin
npm install --ignore-scripts
```

Run from the project you want mounted:
从你想要挂载的项目中运行：

```bash
cd /path/to/project
pi -e ~/.pi/agent/extensions/gondolin
```

The extension mounts the host cwd at `/workspace` in the VM and overrides `read`, `write`, `edit`, `bash`, `grep`, `find`, and `ls`.
该扩展将宿主的 cwd 挂载到虚拟机中的 `/workspace`，并覆盖 `read`、`write`、`edit`、`bash`、`grep`、`find` 和 `ls`。
User `!` commands are routed into the VM, as well.
用户的 `!` 命令也会被路由进虚拟机。
File changes under `/workspace` write through to the host.
`/workspace` 下的文件更改会直写（write through）回宿主机。

Requirements: Node.js >= 23.6.0 for `@earendil-works/gondolin`, plus QEMU (requires installation through your package manager).
要求：`@earendil-works/gondolin` 需要 Node.js >= 23.6.0，另外还需要 QEMU（需要通过你的包管理器安装）。

## Plain Docker
## 普通 Docker

Run the whole `pi` process in Docker when you want the simplest local container boundary.
当你想要最简单的本地容器边界时，可在 Docker 中运行整个 `pi` 进程。

`Dockerfile.pi`:
`Dockerfile.pi`：

```dockerfile
FROM node:24-bookworm-slim

RUN apt-get update \
  && apt-get install -y --no-install-recommends bash ca-certificates git ripgrep \
  && rm -rf /var/lib/apt/lists/*
RUN npm install -g --ignore-scripts @earendil-works/pi-coding-agent

WORKDIR /workspace
ENTRYPOINT ["pi"]
```

Build and run:
构建并运行：

```bash
docker build -t pi-sandbox -f Dockerfile.pi .

docker run --rm -it \
  -e ANTHROPIC_API_KEY \
  -v "$PWD:/workspace" \
  -v pi-agent-home:/root/.pi/agent \
  pi-sandbox
```

The `-v "$PWD:/workspace"` mounts your current directory into the container at /workspace such that reads and writes in `/workspace` inside Docker directly affect your host files, like in the Gondolin example.
`-v "$PWD:/workspace"` 将你的当前目录挂载到容器内的 /workspace，这样 Docker 内对 `/workspace` 的读写会直接影响你的宿主文件，就像 Gondolin 示例那样。

Use a named volume for `/root/.pi/agent` if you want container-local settings and sessions. Mounting your host `~/.pi/agent` exposes host auth and session files to the container.
如果你想要容器本地的设置和会话，请为 `/root/.pi/agent` 使用命名卷。挂载宿主的 `~/.pi/agent` 会把宿主的认证和会话文件暴露给容器。

## OpenShell
## OpenShell

Use [NVIDIA OpenShell](https://docs.nvidia.com/openshell/about/overview) when you want a policy-controlled sandbox with filesystem, process, network, credential, and inference controls.
当你想要一个带文件系统、进程、网络、凭据和推理控制的策略受控沙箱时，请使用 [NVIDIA OpenShell](https://docs.nvidia.com/openshell/about/overview)。
OpenShell can run sandboxes through a local gateway backed by Docker, Podman, or a VM runtime, or through a remote Kubernetes gateway.
OpenShell 可以通过由 Docker、Podman 或 VM 运行时支撑的本地网关运行沙箱，也可以通过远程 Kubernetes 网关运行沙箱。

Every sandbox requires an active gateway.
每个沙箱都需要一个活动网关。
Register and select one before creating a sandbox:
在创建沙箱之前，请注册并选择一个网关：

```bash
openshell gateway add <gateway-url> --name <name>
openshell gateway select <name>
```

Launch `pi` inside an OpenShell sandbox:
在 OpenShell 沙箱中启动 `pi`：

```bash
openshell sandbox create --name pi-sandbox --from pi -- pi
```

In this pattern, the whole `pi` process runs inside the sandbox.
在此模式下，整个 `pi` 进程都运行在沙箱内。
Built-in tools, `!` commands, and extension tools execute inside the OpenShell boundary.
内置工具、`!` 命令和扩展工具都在 OpenShell 边界内执行。

If the gateway is remote, project files are not bind-mounted from the host, meaning writes in the sandbox are not reflected on your machine.
如果网关是远程的，项目文件不会从宿主机绑定挂载，这意味着沙箱内的写入不会反映到你的机器上。
Clone the repository inside the sandbox or use OpenShell file transfer commands:
请在沙箱内克隆仓库，或使用 OpenShell 文件传输命令：

```bash
openshell sandbox upload pi-sandbox ./repo /workspace
openshell sandbox download pi-sandbox /workspace/repo ./repo-out
```

OpenShell providers can keep raw model API keys outside the sandbox.
OpenShell 提供商可以把原始模型 API 密钥保存在沙箱之外。
When inference routing is configured, code inside the sandbox can call `https://inference.local`, and the gateway injects the configured provider credentials upstream.
配置推理路由后，沙箱内的代码可以调用 `https://inference.local`，网关会在上游注入所配置的提供商凭据。
Configure Pi to use the corresponding OpenAI-compatible or Anthropic-compatible endpoint if you want model traffic to use this route.
如果你希望模型流量使用此路由，请将 Pi 配置为使用对应的 OpenAI 兼容或 Anthropic 兼容端点。
