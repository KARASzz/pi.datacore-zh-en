> 📄 来源 Source: https://pi.dev/docs/latest/themes
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

> pi can create themes. Ask it to build one for your setup.
> pi 可以创建主题。让它为你的环境构建一个吧。

# Themes
# 主题

Themes are JSON files that define colors for the TUI.
主题是为 TUI 定义颜色的 JSON 文件。

## Table of Contents
## 目录

- [Locations](#locations)
- [位置](#locations)
- [Selecting a Theme](#selecting-a-theme)
- [选择主题](#selecting-a-theme)
- [Creating a Custom Theme](#creating-a-custom-theme)
- [创建自定义主题](#creating-a-custom-theme)
- [Theme Format](#theme-format)
- [主题格式](#theme-format)
- [Color Tokens](#color-tokens)
- [颜色令牌](#color-tokens)
- [Color Values](#color-values)
- [颜色值](#color-values)
- [Tips](#tips)
- [技巧](#tips)

## Locations
## 位置

Pi loads themes from:
Pi 从以下位置加载主题：

- Built-in: `dark`, `light`
- 内置：`dark`、`light`
- Global: `~/.pi/agent/themes/*.json`
- 全局：`~/.pi/agent/themes/*.json`
- Project: `.pi/themes/*.json` (only after the project is trusted)
- 项目：`.pi/themes/*.json`（仅在项目受信任后）
- Packages: `themes/` directories or `pi.themes` entries in `package.json`
- 包：`themes/` 目录或 `package.json` 中的 `pi.themes` 条目
- Settings: `themes` array with files or directories
- 设置：包含文件或目录的 `themes` 数组
- CLI: `--theme <path>` (repeatable)
- CLI：`--theme <path>`（可重复）

Disable discovery with `--no-themes`.
使用 `--no-themes` 禁用发现。

## Selecting a Theme
## 选择主题

Select a theme via `/settings` or in `settings.json`:
通过 `/settings` 或在 `settings.json` 中选择主题：

```json
{
  "theme": "my-theme"
}
```

On first run, pi detects your terminal background and defaults to `dark` or `light`.
首次运行时，pi 会检测你的终端背景并默认使用 `dark` 或 `light`。

### Initial Theme
### 初始主题

Start an interactive run with a theme without changing the saved setting:
在不更改已保存设置的情况下，用某个主题启动交互运行：

```bash
pi --use-theme light
```

To follow terminal appearance, use `lightTheme/darkTheme` syntax:
要跟随终端外观，使用 `lightTheme/darkTheme` 语法：

```bash
pi --use-theme light/dark
```

The CLI value is the initial theme for that run. Choosing another theme later in `/settings` applies it immediately
CLI 值是该次运行的初始主题。之后在 `/settings` 中选择其他主题会立即应用
and saves it normally.
并正常保存。

## Creating a Custom Theme
## 创建自定义主题

1. Create a theme file:
1. 创建主题文件：

```bash
mkdir -p ~/.pi/agent/themes
vim ~/.pi/agent/themes/my-theme.json
```

2. Define the theme with all required colors (see [Color Tokens](#color-tokens)):
2. 用全部必需的颜色定义主题（参见[颜色令牌](#color-tokens)）：

```json
{
  "$schema": "https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/src/modes/interactive/theme/theme-schema.json",
  "name": "my-theme",
  "vars": {
    "primary": "#00aaff",
    "secondary": 242
  },
  "colors": {
    "accent": "primary",
    "border": "primary",
    "borderAccent": "#00ffff",
    "borderMuted": "secondary",
    "success": "#00ff00",
    "error": "#ff0000",
    "warning": "#ffff00",
    "muted": "secondary",
    "dim": 240,
    "text": "",
    "thinkingText": "secondary",
    "selectedBg": "#2d2d30",
    "scrollbarThumb": "#555566",
    "searchMatchBg": "#2d2d30",
    "searchMatchText": "",
    "userMessageBg": "#2d2d30",
    "userMessageText": "",
    "customMessageBg": "#2d2d30",
    "customMessageText": "",
    "customMessageLabel": "primary",
    "toolPendingBg": "#1e1e2e",
    "toolSuccessBg": "#1e2e1e",
    "toolErrorBg": "#2e1e1e",
    "toolTitle": "primary",
    "toolOutput": "",
    "mdHeading": "#ffaa00",
    "mdLink": "primary",
    "mdLinkUrl": "secondary",
    "mdCode": "#00ffff",
    "mdCodeBlock": "",
    "mdCodeBlockBorder": "secondary",
    "mdQuote": "secondary",
    "mdQuoteBorder": "secondary",
    "mdHr": "secondary",
    "mdListBullet": "#00ffff",
    "toolDiffAdded": "#00ff00",
    "toolDiffRemoved": "#ff0000",
    "toolDiffContext": "secondary",
    "syntaxComment": "secondary",
    "syntaxKeyword": "primary",
    "syntaxFunction": "#00aaff",
    "syntaxVariable": "#ffaa00",
    "syntaxString": "#00ff00",
    "syntaxNumber": "#ff00ff",
    "syntaxType": "#00aaff",
    "syntaxOperator": "primary",
    "syntaxPunctuation": "secondary",
    "thinkingOff": "secondary",
    "thinkingMinimal": "primary",
    "thinkingLow": "#00aaff",
    "thinkingMedium": "#00ffff",
    "thinkingHigh": "#ff00ff",
    "thinkingXhigh": "#ff0000",
    "thinkingMax": "#ff0088",
    "bashMode": "#ffaa00"
  }
}
```

3. Select the theme via `/settings`.
3. 通过 `/settings` 选择该主题。

**Hot reload:** When you edit the currently active custom theme file, pi reloads it automatically for immediate visual feedback.
**热重载：** 当你编辑当前活动的自定义主题文件时，pi 会自动重新加载它，立即提供视觉反馈。

## Theme Format
## 主题格式

```json
{
  "$schema": "https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/src/modes/interactive/theme/theme-schema.json",
  "name": "my-theme",
  "vars": {
    "blue": "#0066cc",
    "gray": 242
  },
  "colors": {
    "accent": "blue",
    "muted": "gray",
    "text": "",
    ...
  }
}
```

- `name` is required, must be unique, and must not contain `/`.
- `name` 必需，必须唯一，且不能包含 `/`。
- `vars` is optional. Define reusable colors here, then reference them in `colors`.
- `vars` 可选。在这里定义可复用的颜色，然后在 `colors` 中引用它们。
- `colors` must define all 51 required tokens. `thinkingMax`, `scrollbarThumb`, and the two search highlight tokens are optional and use the fallbacks listed below.
- `colors` 必须定义全部 51 个必需令牌。`thinkingMax`、`scrollbarThumb` 和两个搜索高亮令牌是可选的，使用下面列出的后备值。

The `$schema` field enables editor auto-completion and validation.
`$schema` 字段启用编辑器自动补全和校验。

## Color Tokens
## 颜色令牌

Every theme must define all 51 required color tokens. The optional tokens preserve compatibility with existing themes: `thinkingMax` falls back to `thinkingXhigh`, `scrollbarThumb` and `searchMatchBg` fall back to `selectedBg`, and `searchMatchText` falls back to `text`. Other search matches use `searchMatchText` on `searchMatchBg` with an underline; the current match reverses that foreground/background pair and uses bold text.
每个主题必须定义全部 51 个必需颜色令牌。可选令牌用于保持与现有主题的兼容：`thinkingMax` 后备到 `thinkingXhigh`，`scrollbarThumb` 和 `searchMatchBg` 后备到 `selectedBg`，`searchMatchText` 后备到 `text`。其他搜索匹配在 `searchMatchBg` 上使用 `searchMatchText` 并加下划线；当前匹配会反转该前景/背景对并使用粗体文本。

### Core UI (11 colors)
### 核心 UI（11 色）

| Token | Purpose |
|-------|---------|
| `accent` | Primary accent (logo, selected items, cursor) |
| `border` | Normal borders |
| `borderAccent` | Highlighted borders |
| `borderMuted` | Subtle borders (editor) |
| `success` | Success states |
| `error` | Error states |
| `warning` | Warning states |
| `muted` | Secondary text |
| `dim` | Tertiary text |
| `text` | Default text (usually `""`) |
| `thinkingText` | Thinking block text |

| 令牌 | 用途 |
|-------|---------|
| `accent` | 主强调色（logo、选中项、光标） |
| `border` | 普通边框 |
| `borderAccent` | 高亮边框 |
| `borderMuted` | 细微边框（编辑器） |
| `success` | 成功状态 |
| `error` | 错误状态 |
| `warning` | 警告状态 |
| `muted` | 次要文本 |
| `dim` | 三级文本 |
| `text` | 默认文本（通常是 `""`） |
| `thinkingText` | 思考块文本 |


### Backgrounds & Content (11 required, 3 optional)
### 背景与内容（11 必需，3 可选）

| Token | Purpose |
|-------|---------|
| `selectedBg` | Selected line background |
| `scrollbarThumb` | Fullscreen scrollbar thumb background; optional, falls back to `selectedBg` |
| `searchMatchBg` | Transcript search match background and current-match text; optional, falls back to `selectedBg` |
| `searchMatchText` | Transcript search match text and current-match background; optional, falls back to `text` |
| `userMessageBg` | User message background |
| `userMessageText` | User message text |
| `customMessageBg` | Extension message background |
| `customMessageText` | Extension message text |
| `customMessageLabel` | Extension message label |
| `toolPendingBg` | Tool box (pending) |
| `toolSuccessBg` | Tool box (success) |
| `toolErrorBg` | Tool box (error) |
| `toolTitle` | Tool title |
| `toolOutput` | Tool output text |

| 令牌 | 用途 |
|-------|---------|
| `selectedBg` | 选中行背景 |
| `scrollbarThumb` | 全屏滚动条滑块背景；可选，后备到 `selectedBg` |
| `searchMatchBg` | 对话记录搜索匹配背景及当前匹配文本；可选，后备到 `selectedBg` |
| `searchMatchText` | 对话记录搜索匹配文本及当前匹配背景；可选，后备到 `text` |
| `userMessageBg` | 用户消息背景 |
| `userMessageText` | 用户消息文本 |
| `customMessageBg` | 扩展消息背景 |
| `customMessageText` | 扩展消息文本 |
| `customMessageLabel` | 扩展消息标签 |
| `toolPendingBg` | 工具框（等待中） |
| `toolSuccessBg` | 工具框（成功） |
| `toolErrorBg` | 工具框（错误） |
| `toolTitle` | 工具标题 |
| `toolOutput` | 工具输出文本 |


### Markdown (10 colors)
### Markdown（10 色）

| Token | Purpose |
|-------|---------|
| `mdHeading` | Headings |
| `mdLink` | Link text |
| `mdLinkUrl` | Link URL |
| `mdCode` | Inline code |
| `mdCodeBlock` | Code block content |
| `mdCodeBlockBorder` | Code block fences |
| `mdQuote` | Blockquote text |
| `mdQuoteBorder` | Blockquote border |
| `mdHr` | Horizontal rule |
| `mdListBullet` | List bullets |

| 令牌 | 用途 |
|-------|---------|
| `mdHeading` | 标题 |
| `mdLink` | 链接文本 |
| `mdLinkUrl` | 链接 URL |
| `mdCode` | 行内代码 |
| `mdCodeBlock` | 代码块内容 |
| `mdCodeBlockBorder` | 代码块围栏 |
| `mdQuote` | 引用块文本 |
| `mdQuoteBorder` | 引用块边框 |
| `mdHr` | 水平分割线 |
| `mdListBullet` | 列表圆点 |


### Tool Diffs (3 colors)
### 工具差异（3 色）

| Token | Purpose |
|-------|---------|
| `toolDiffAdded` | Added lines |
| `toolDiffRemoved` | Removed lines |
| `toolDiffContext` | Context lines |

| 令牌 | 用途 |
|-------|---------|
| `toolDiffAdded` | 新增行 |
| `toolDiffRemoved` | 删除行 |
| `toolDiffContext` | 上下文行 |


### Syntax Highlighting (9 colors)
### 语法高亮（9 色）

| Token | Purpose |
|-------|---------|
| `syntaxComment` | Comments |
| `syntaxKeyword` | Keywords |
| `syntaxFunction` | Function names |
| `syntaxVariable` | Variables |
| `syntaxString` | Strings |
| `syntaxNumber` | Numbers |
| `syntaxType` | Types |
| `syntaxOperator` | Operators |
| `syntaxPunctuation` | Punctuation |

| 令牌 | 用途 |
|-------|---------|
| `syntaxComment` | 注释 |
| `syntaxKeyword` | 关键字 |
| `syntaxFunction` | 函数名 |
| `syntaxVariable` | 变量 |
| `syntaxString` | 字符串 |
| `syntaxNumber` | 数字 |
| `syntaxType` | 类型 |
| `syntaxOperator` | 运算符 |
| `syntaxPunctuation` | 标点 |


### Thinking Level Borders (6 required, 1 optional)
### 思考等级边框（6 必需，1 可选）

Editor border colors indicating thinking level (visual hierarchy from subtle to prominent):
表示思考等级的编辑器边框颜色（视觉层级从细微到醒目）：

| Token | Purpose |
|-------|---------|
| `thinkingOff` | Thinking off |
| `thinkingMinimal` | Minimal thinking |
| `thinkingLow` | Low thinking |
| `thinkingMedium` | Medium thinking |
| `thinkingHigh` | High thinking |
| `thinkingXhigh` | Extra high thinking |
| `thinkingMax` | Maximum thinking; optional, falls back to `thinkingXhigh` |

| 令牌 | 用途 |
|-------|---------|
| `thinkingOff` | 关闭思考 |
| `thinkingMinimal` | 极少思考 |
| `thinkingLow` | 低等思考 |
| `thinkingMedium` | 中等思考 |
| `thinkingHigh` | 高等思考 |
| `thinkingXhigh` | 超高思考 |
| `thinkingMax` | 最大思考；可选，后备到 `thinkingXhigh` |


### Bash Mode (1 color)
### Bash 模式（1 色）

| Token | Purpose |
|-------|---------|
| `bashMode` | Editor border in bash mode (`!` prefix) |

| 令牌 | 用途 |
|-------|---------|
| `bashMode` | bash 模式（`!` 前缀）下的编辑器边框 |


### HTML Export (optional)
### HTML 导出（可选）

The `export` section controls colors for `/export` HTML output. If omitted, colors are derived from `userMessageBg`.
`export` 部分控制 `/export` HTML 输出的颜色。如果省略，颜色从 `userMessageBg` 派生。

```json
{
  "export": {
    "pageBg": "#18181e",
    "cardBg": "#1e1e24",
    "infoBg": "#3c3728"
  }
}
```

## Color Values
## 颜色值

Four formats are supported:
支持四种格式：

| Format | Example | Description |
|--------|---------|-------------|
| Hex | `"#ff0000"` | 6-digit hex RGB |
| 256-color | `39` | xterm 256-color palette index (0-255) |
| Variable | `"primary"` | Reference to a `vars` entry |
| Default | `""` | Terminal's default color |

| 格式 | 示例 | 描述 |
|--------|---------|-------------|
| Hex | `"#ff0000"` | 6 位十六进制 RGB |
| 256 色 | `39` | xterm 256 色调色板索引（0-255） |
| 变量 | `"primary"` | 对 `vars` 条目的引用 |
| 默认 | `""` | 终端默认颜色 |


### 256-Color Palette
### 256 色调色板

- `0-15`: Basic ANSI colors (terminal-dependent)
- `0-15`：基础 ANSI 颜色（取决于终端）
- `16-231`: 6×6×6 RGB cube (`16 + 36×R + 6×G + B` where R,G,B are 0-5)
- `16-231`：6×6×6 RGB 立方体（`16 + 36×R + 6×G + B`，其中 R、G、B 为 0-5）
- `232-255`: Grayscale ramp
- `232-255`：灰度渐变

### Terminal Compatibility
### 终端兼容性

Pi uses 24-bit RGB colors. Most modern terminals support this (iTerm2, Kitty, WezTerm, Windows Terminal, VS Code). For older terminals with only 256-color support, pi falls back to the nearest approximation.
Pi 使用 24 位 RGB 颜色。大多数现代终端都支持（iTerm2、Kitty、WezTerm、Windows Terminal、VS Code）。对于只支持 256 色的较老终端，pi 会回退到最接近的近似值。

Check truecolor support:
检查真彩色支持：

```bash
echo $COLORTERM  # Should output "truecolor" or "24bit"
```

## Tips
## 技巧

**Dark terminals:** Use bright, saturated colors with higher contrast.
**深色终端：** 使用明亮、饱和且对比度更高的颜色。

**Light terminals:** Use darker, muted colors with lower contrast.
**浅色终端：** 使用更暗、柔和且对比度更低的颜色。

**Color harmony:** Start with a base palette (Nord, Gruvbox, Tokyo Night), define it in `vars`, and reference consistently.
**色彩和谐：** 从一个基础调色板（Nord、Gruvbox、Tokyo Night）开始，在 `vars` 中定义它并一致地引用。

**Testing:** Check your theme with different message types, tool states, markdown content, and long wrapped text.
**测试：** 用不同的消息类型、工具状态、markdown 内容和长换行文本检查你的主题。

**VS Code:** Set `terminal.integrated.minimumContrastRatio` to `1` for accurate colors.
**VS Code：** 把 `terminal.integrated.minimumContrastRatio` 设为 `1` 以获得准确的颜色。

## Examples
## 示例

See the built-in themes:
参见内置主题：
- [dark.json](../src/modes/interactive/theme/dark.json)
- [dark.json](../src/modes/interactive/theme/dark.json)
- [light.json](../src/modes/interactive/theme/light.json)
- [light.json](../src/modes/interactive/theme/light.json)
