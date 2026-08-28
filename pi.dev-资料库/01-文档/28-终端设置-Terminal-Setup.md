> 📄 来源 Source: https://pi.dev/docs/latest/terminal-setup
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Terminal Setup
# 终端设置

Pi uses the [Kitty keyboard protocol](https://sw.kovidgoyal.net/kitty/keyboard-protocol/) for reliable modifier key detection. Most modern terminals support this protocol, but some require configuration.
Pi 使用 [Kitty 键盘协议](https://sw.kovidgoyal.net/kitty/keyboard-protocol/)来可靠地检测修饰键。大多数现代终端都支持该协议，但有些需要配置。

## Capability Overrides
## 能力覆盖

Pi auto-detects OSC 8 hyperlinks, inline image protocols, and truecolor. If detection fails behind a terminal proxy or multiplexer, use these advanced overrides:
Pi 自动检测 OSC 8 超链接、内联图片协议和真彩色。如果检测在终端代理或多路复用器后面失败，请使用以下高级覆盖项：

| Capability | Environment variable | JSON setting |
|------------|----------------------|--------------|
| OSC 8 hyperlinks | `PI_HYPERLINKS=1\|0\|auto` | `terminal.hyperlinks: true\|false\|"auto"` |
| Inline images | `PI_IMAGE_PROTOCOL=kitty\|iterm2\|none\|auto` | `terminal.images: "kitty"\|"iterm2"\|false\|"auto"` |
| Truecolor | `PI_TRUE_COLOR=1\|0\|auto` | `terminal.trueColor: true\|false\|"auto"` |

| 能力 | 环境变量 | JSON 设置 |
|------------|----------------------|--------------|
| OSC 8 超链接 | `PI_HYPERLINKS=1\|0\|auto` | `terminal.hyperlinks: true\|false\|"auto"` |
| 内联图片 | `PI_IMAGE_PROTOCOL=kitty\|iterm2\|none\|auto` | `terminal.images: "kitty"\|"iterm2"\|false\|"auto"` |
| 真彩色 | `PI_TRUE_COLOR=1\|0\|auto` | `terminal.trueColor: true\|false\|"auto"` |


Settings take precedence over environment variables; unset or `auto` preserves detection. Only force capabilities supported by the complete terminal path, since unsupported escape sequences can corrupt rendering.
设置优先于环境变量；未设置或 `auto` 会保留检测结果。只强制完整终端路径都支持的能力，因为不受支持的转义序列可能破坏渲染。

## Kitty
## Kitty

Works out of the box.
开箱即用。

## iTerm2
## iTerm2

### Regular TUI mode
### 常规 TUI 模式

Works out of the box.
开箱即用。

### Fullscreen TUI mode
### 全屏 TUI 模式

Pi owns the viewport, so iTerm2 sends mouse-wheel reports instead of scrolling its native scrollback. With iTerm2's default fast-trackpad behavior, those reports can lose most of an accelerated wheel delta, making fullscreen scrolling much slower than regular scrolling.
Pi 拥有视口，因此 iTerm2 发送鼠标滚轮报告而不是滚动其原生回滚缓冲区。按照 iTerm2 默认的快速触控板行为，这些报告可能丢失大部分加速滚轮增量，使全屏滚动比常规滚动慢得多。

If fast mouse-wheel gestures move only about one line at a time in fullscreen mode:
如果全屏模式下快速鼠标滚轮手势一次只移动大约一行：

1. Open **iTerm2 → Settings → Advanced**.
1. 打开 **iTerm2 → Settings → Advanced**。
2. Search for **Trackpad scrolls fast?** and set it to **No**.
2. 搜索 **Trackpad scrolls fast?** 并将其设为 **No**。

This is an iTerm2-wide workaround and may also change native trackpad scrolling. The underlying behavior is tracked in [iTerm2 issue 9619](https://gitlab.com/gnachman/iterm2/-/work_items/9619).
这是 iTerm2 全局的变通方法，也可能改变原生触控板滚动。底层行为在 [iTerm2 issue 9619](https://gitlab.com/gnachman/iterm2/-/work_items/9619) 中跟踪。

## Apple Terminal
## Apple Terminal

Pi enables enhanced key reporting when available. If Terminal.app still sends plain Return for `Shift+Enter`, pi uses a local macOS modifier fallback to treat that Return as `Shift+Enter`.
Pi 在可用时启用增强按键上报。如果 Terminal.app 仍然为 `Shift+Enter` 发送普通 Return，pi 会使用本地 macOS 修饰键后备把该 Return 视为 `Shift+Enter`。

This fallback only works when pi runs on the same Mac as Terminal.app. It cannot detect the local keyboard over remote SSH.
此后备只在 pi 与 Terminal.app 运行在同一台 Mac 上时有效。通过远程 SSH 无法检测本地键盘。

## Ghostty
## Ghostty

Add to your Ghostty config (`~/Library/Application Support/com.mitchellh.ghostty/config` on macOS, `~/.config/ghostty/config` on Linux):
添加到你的 Ghostty 配置（macOS 上为 `~/Library/Application Support/com.mitchellh.ghostty/config`，Linux 上为 `~/.config/ghostty/config`）：

```
keybind = alt+backspace=text:\x1b\x7f
```

Older Claude Code versions may have added this Ghostty mapping:
较旧的 Claude Code 版本可能添加过这个 Ghostty 映射：

```
keybind = shift+enter=text:\n
```

That mapping sends a raw linefeed byte. Inside pi, that is indistinguishable from `Ctrl+J`, so tmux and pi no longer see a real `shift+enter` key event.
该映射发送原始换行字节。在 pi 内部，这与 `Ctrl+J` 无法区分，因此 tmux 和 pi 不再看到真正的 `shift+enter` 按键事件。

If Claude Code 2.x or newer is the only reason you added that mapping, you can remove it, unless you want to use Claude Code in tmux, where it still requires that Ghostty mapping.
如果 Claude Code 2.x 或更新版本是你添加该映射的唯一原因，可以删除它，除非你想在 tmux 中使用 Claude Code——在那里它仍然需要该 Ghostty 映射。

Pi binds `Ctrl+J` as a default newline alias, so `Shift+Enter` keeps working in tmux via that remap without extra pi configuration.
Pi 将 `Ctrl+J` 绑定为默认的换行别名，因此 `Shift+Enter` 在 tmux 中通过该重映射继续工作，无需额外的 pi 配置。

### Fullscreen TUI mode
### 全屏 TUI 模式

In fullscreen mode, links remain clickable, but Ghostty does not show its hover underline or lower-left URL preview while pi captures mouse input. Hold `Shift+Command` on macOS or `Shift+Ctrl` on Linux to use Ghostty's native link handling.
在全屏模式下，链接仍然可以点击，但在 pi 捕获鼠标输入时，Ghostty 不显示悬停下划线或左下角的 URL 预览。按住 macOS 上的 `Shift+Command` 或 Linux 上的 `Shift+Ctrl` 可使用 Ghostty 的原生链接处理。

## WezTerm
## WezTerm

WezTerm usually works out of the box for `Shift+Enter` via xterm modifyOtherKeys. To use the Kitty keyboard protocol explicitly, create `~/.wezterm.lua`:
WezTerm 通过 xterm modifyOtherKeys 通常开箱即用支持 `Shift+Enter`。要显式使用 Kitty 键盘协议，创建 `~/.wezterm.lua`：

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()
config.enable_kitty_keyboard = true
return config
```

On macOS, WezTerm binds `Option+Enter` to fullscreen by default. To use `Option+Enter` for pi follow-up queueing, add this key override:
在 macOS 上，WezTerm 默认把 `Option+Enter` 绑定为全屏。要用 `Option+Enter` 做 pi 的 follow-up 排队，请添加这个按键覆盖：

```lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()
config.keys = {
  {
    key = 'Enter',
    mods = 'ALT',
    action = wezterm.action.SendString('\x1b[13;3u'),
  },
}
return config
```

If you already have a `config.keys` table, add the entry to it.
如果你已经有 `config.keys` 表，请把该条目添加进去。

On WSL, WezTerm may require a visible hardware cursor for IME candidate window positioning. If CJK IME candidates do not follow the text cursor, set `PI_HARDWARE_CURSOR=1` before running pi or set `showHardwareCursor` to `true` in settings.
在 WSL 上，WezTerm 可能需要可见的硬件光标来定位 IME 候选窗口。如果 CJK 输入法候选框不跟随文本光标，请在运行 pi 前设置 `PI_HARDWARE_CURSOR=1`，或在设置中把 `showHardwareCursor` 设为 `true`。

## Alacritty
## Alacritty

Alacritty usually works out of the box for `Shift+Enter`. On macOS, `Option+Enter` may arrive as plain `Enter`. To use `Option+Enter` for pi follow-up queueing, add to `~/.config/alacritty/alacritty.toml`:
Alacritty 通常开箱即用支持 `Shift+Enter`。在 macOS 上，`Option+Enter` 可能以普通 `Enter` 的形式到达。要用 `Option+Enter` 做 pi 的 follow-up 排队，请添加到 `~/.config/alacritty/alacritty.toml`：

```toml
[[keyboard.bindings]]
key = "Enter"
mods = "Alt"
chars = "\u001b[13;3u"
```

Restart Alacritty after changing the config.
更改配置后请重启 Alacritty。

## VS Code (Integrated Terminal)
## VS Code（集成终端）

VS Code 1.109.5 and newer enable Kitty keyboard protocol in the integrated terminal by default, so `Shift+Enter` should work out of the box.
VS Code 1.109.5 及更新版本默认在集成终端中启用 Kitty 键盘协议，因此 `Shift+Enter` 应该开箱即用。

VS Code versions older than 1.109.5 need an explicit terminal keybinding for `Shift+Enter`.
早于 1.109.5 的 VS Code 版本需要为 `Shift+Enter` 添加显式的终端键位。

`keybindings.json` locations:
`keybindings.json` 位置：
- macOS: `~/Library/Application Support/Code/User/keybindings.json`
- macOS：`~/Library/Application Support/Code/User/keybindings.json`
- Linux: `~/.config/Code/User/keybindings.json`
- Linux：`~/.config/Code/User/keybindings.json`
- Windows: `%APPDATA%\\Code\\User\\keybindings.json`
- Windows：`%APPDATA%\Code\User\keybindings.json`

Add to `keybindings.json`:
添加到 `keybindings.json`：

```json
{
  "key": "shift+enter",
  "command": "workbench.action.terminal.sendSequence",
  "args": { "text": "\u001b[13;2u" },
  "when": "terminalFocus"
}
```

## Windows Terminal
## Windows Terminal

Pi uses Windows-style keybindings when running natively on Windows or in WSL:
在 Windows 原生运行或在 WSL 中运行时，Pi 使用 Windows 风格的键位：

- `Alt+V` pastes an image or clipboard text.
- `Alt+V` 粘贴图片或剪贴板文本。
- `Ctrl+F` searches the transcript in fullscreen mode, and `Ctrl+Up`/`Ctrl+Down` jump between marked messages.
- `Ctrl+F` 在全屏模式搜索对话记录，`Ctrl+Up`/`Ctrl+Down` 在标记的消息之间跳转。
- `Alt+P` cycles to the previous model.
- `Alt+P` 循环切换到上一个模型。
- `Ctrl+Z` undoes editing on native Windows; WSL uses `Alt+Z` so `Ctrl+Z` can suspend pi.
- `Ctrl+Z` 在原生 Windows 上撤销编辑；WSL 使用 `Alt+Z`，以便 `Ctrl+Z` 可以挂起 pi。
- `Ctrl+Q` queues a follow-up message and `Alt+Q` restores queued messages.
- `Ctrl+Q` 排队 follow-up 消息，`Alt+Q` 恢复排队的消息。

Add to `settings.json` (Ctrl+Shift+, or Settings → Open JSON file) to forward `Shift+Enter` for inserting a new line:
添加到 `settings.json`（Ctrl+Shift+, 或 Settings → Open JSON file）以转发 `Shift+Enter` 插入新行：

```json
{
  "actions": [
    {
      "command": { "action": "sendInput", "input": "\u001b[13;2u" },
      "keys": "shift+enter"
    }
  ]
}
```

Windows Terminal binds `Alt+Enter` to fullscreen by default. To use it instead of pi's `Ctrl+Q` default for follow-up queueing, configure Windows Terminal to send the key and bind `app.message.followUp` to `alt+enter` in pi.
Windows Terminal 默认把 `Alt+Enter` 绑定为全屏。要改用它来做 pi 默认由 `Ctrl+Q` 承担的 follow-up 排队，请配置 Windows Terminal 发送该按键，并在 pi 中把 `app.message.followUp` 绑定到 `alt+enter`。

If you already have an `actions` array, add the object to it. Fully close and reopen Windows Terminal after changing its settings.
如果你已有 `actions` 数组，请把该对象添加进去。更改设置后请完全关闭并重新打开 Windows Terminal。

## xfce4-terminal, terminator
## xfce4-terminal、terminator

These terminals have limited escape sequence support. Modified Enter keys like `Ctrl+Enter` and `Shift+Enter` cannot be distinguished from plain `Enter`, preventing custom keybindings such as `submit: ["ctrl+enter"]` from working.
这些终端对转义序列的支持有限。`Ctrl+Enter` 和 `Shift+Enter` 等带修饰键的 Enter 无法与普通 `Enter` 区分，导致 `submit: ["ctrl+enter"]` 之类的自定义键位无法工作。

For the best experience, use a terminal that supports the Kitty keyboard protocol:
为获得最佳体验，请使用支持 Kitty 键盘协议的终端：
- [Kitty](https://sw.kovidgoyal.net/kitty/)
- [Kitty](https://sw.kovidgoyal.net/kitty/)
- [Ghostty](https://ghostty.org/)
- [Ghostty](https://ghostty.org/)
- [WezTerm](https://wezfurlong.org/wezterm/)
- [WezTerm](https://wezfurlong.org/wezterm/)
- [iTerm2](https://iterm2.com/)
- [iTerm2](https://iterm2.com/)
- [Alacritty](https://github.com/alacritty/alacritty) (requires compilation with Kitty protocol support)
- [Alacritty](https://github.com/alacritty/alacritty)（需要以支持 Kitty 协议的方式编译）

## IntelliJ IDEA (Integrated Terminal)
## IntelliJ IDEA（集成终端）

The built-in terminal has limited escape sequence support. Shift+Enter cannot be distinguished from Enter in IntelliJ's terminal.
内置终端对转义序列的支持有限。在 IntelliJ 的终端中，Shift+Enter 无法与 Enter 区分。

If you want the hardware cursor visible, set `PI_HARDWARE_CURSOR=1` before running pi (disabled by default for compatibility).
如果希望硬件光标可见，请在运行 pi 前设置 `PI_HARDWARE_CURSOR=1`（默认禁用以保证兼容性）。

Consider using a dedicated terminal emulator for the best experience.
建议使用专门的终端模拟器以获得最佳体验。
