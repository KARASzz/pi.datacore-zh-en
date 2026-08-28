> 📄 来源 Source: https://pi.dev/docs/latest/shell-aliases
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Shell Aliases
# Shell 别名

Pi runs bash in non-interactive mode (`bash -c`), which doesn't expand aliases by default.
Pi 以非交互模式（`bash -c`）运行 bash，默认不展开别名。

To enable your shell aliases, add to `~/.pi/agent/settings.json`:
要启用你的 shell 别名，请在 `~/.pi/agent/settings.json` 中添加：

```json
{
  "shellCommandPrefix": "shopt -s expand_aliases\neval \"$(grep '^alias ' ~/.zshrc)\""
}
```

Adjust the path (`~/.zshrc`, `~/.bashrc`, etc.) to match your shell config.
调整路径（`~/.zshrc`、`~/.bashrc` 等）以匹配你的 shell 配置。
