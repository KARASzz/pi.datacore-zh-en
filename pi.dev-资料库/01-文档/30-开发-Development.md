> 📄 来源 Source: https://pi.dev/docs/latest/development
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Development
# 开发

See [AGENTS.md](https://github.com/earendil-works/pi-mono/blob/main/AGENTS.md) for additional guidelines.
更多准则参见 [AGENTS.md](https://github.com/earendil-works/pi-mono/blob/main/AGENTS.md)。

## Setup
## 环境搭建

```bash
git clone https://github.com/earendil-works/pi-mono
cd pi-mono
npm install
npm run build
```

Run from source:
从源码运行：

```bash
/path/to/pi-mono/pi-test.sh
```

The script can be run from any directory. Pi keeps the caller's current working directory.
该脚本可以在任何目录中运行。Pi 会保持调用者当前的工作目录。

## Forking / Rebranding
## 分叉 / 更名

Configure via `package.json`:
通过 `package.json` 配置：

```json
{
  "piConfig": {
    "name": "pi",
    "configDir": ".pi"
  }
}
```

Change `name`, `configDir`, and `bin` field for your fork. Affects CLI banner, config paths, and environment variable names.
为你的分叉修改 `name`、`configDir` 和 `bin` 字段。这会影响 CLI 横幅、配置路径和环境变量名称。

## Path Resolution
## 路径解析

Three execution modes: npm install, standalone binary, tsx from source.
三种执行模式：npm 安装、独立二进制、从源码以 tsx 运行。

**Always use `src/config.ts`** for package assets:
**始终使用 `src/config.ts`** 来获取包资源：

```typescript
import { getPackageDir, getThemeDir } from "./config.js";
```

Never use `__dirname` directly for package assets.
绝不要直接用 `__dirname` 获取包资源。

## Debug Command
## 调试命令

`/debug` (hidden) writes to `~/.pi/agent/pi-debug.log`:
`/debug`（隐藏）会写入 `~/.pi/agent/pi-debug.log`：
- Rendered TUI lines with ANSI codes
- 带 ANSI 码的已渲染 TUI 行
- Last messages sent to the LLM
- 最近发送给 LLM 的消息

## Testing
## 测试

```bash
./test.sh                         # Run non-LLM tests (no API keys needed)
npm test                          # Run all tests
npm test -- test/specific.test.ts # Run specific test
```

## Project Structure
## 项目结构

```
packages/
  ai/           # LLM provider abstraction
  agent/        # Agent loop and message types  
  tui/          # Terminal UI components
  coding-agent/ # CLI and interactive mode
```
