> 📄 来源 Source: https://pi.dev/docs/latest/windows
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Windows Setup
# Windows 设置

Pi uses Git Bash by default on Windows. Checked locations (in order):
Pi 在 Windows 上默认使用 Git Bash。按顺序检查以下位置：

1. Custom path from `~/.pi/agent/settings.json`
1. `~/.pi/agent/settings.json` 中的自定义路径
2. Git Bash (`C:\Program Files\Git\bin\bash.exe`)
2. Git Bash（`C:\Program Files\Git\bin\bash.exe`）
3. `bash.exe` on PATH (Cygwin, MSYS2, WSL)
3. PATH 上的 `bash.exe`（Cygwin、MSYS2、WSL）

For most users, [Git for Windows](https://git-scm.com/download/win) is sufficient.
对多数用户而言，[Git for Windows](https://git-scm.com/download/win) 就足够了。

## PowerShell Tool
## PowerShell 工具

The optional `powershell` tool runs commands through `pwsh.exe` when available, otherwise Windows PowerShell. It starts PowerShell with `-NoProfile -NonInteractive -ExecutionPolicy Bypass`. Administrator-enforced execution policies can still take precedence.
可选的 `powershell` 工具在可用时通过 `pwsh.exe` 运行命令，否则使用 Windows PowerShell。它以 `-NoProfile -NonInteractive -ExecutionPolicy Bypass` 启动 PowerShell。管理员强制执行的执行策略仍可优先生效。

Use `defaultTools` to replace the model-facing `bash` tool:
使用 `defaultTools` 替换面向模型的 `bash` 工具：

```json
{
  "defaultTools": ["read", "powershell", "edit", "write"]
}
```

Or enable both while comparing behavior:
或者在对比行为时同时启用两者：

```json
{
  "defaultTools": ["read", "bash", "powershell", "edit", "write"]
}
```

The `!` and `!!` editor commands still use Bash.
`!` 和 `!!` 编辑器命令仍使用 Bash。

## Custom Bash Path
## 自定义 Bash 路径

```json
{
  "shellPath": "C:\\cygwin64\\bin\\bash.exe"
}
```
