> 📄 来源 Source: https://pi.dev/docs/latest/keybindings
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Keybindings
# 快捷键

All keyboard shortcuts can be customized via `~/.pi/agent/keybindings.json`. Each action can be bound to one or more keys.
所有键盘快捷键都可以通过 `~/.pi/agent/keybindings.json` 自定义。每个动作可以绑定一个或多个按键。

The config file uses the same namespaced keybinding ids that pi uses internally and that extension authors use in `keyHint()` and injected `keybindings` managers.
配置文件使用与 pi 内部相同、扩展作者在 `keyHint()` 和注入的 `keybindings` 管理器中使用的带命名空间的快捷键 id。

Older configs using pre-namespaced ids such as `cursorUp` or `expandTools` are migrated automatically to the namespaced ids on startup.
使用旧式非命名空间 id（如 `cursorUp` 或 `expandTools`）的旧配置会在启动时自动迁移到命名空间 id。

After editing `keybindings.json`, run `/reload` in pi to apply the changes without restarting the session.
编辑 `keybindings.json` 后，在 pi 中运行 `/reload` 即可在不重启会话的情况下应用更改。

## Key Format
## 按键格式

`modifier+key` where modifiers are `ctrl`, `shift`, `alt`, `super` (combinable) and keys are:
`修饰键+按键`，其中修饰键为 `ctrl`、`shift`、`alt`、`super`（可组合），按键为：

- **Letters:** `a-z`
- **字母：** `a-z`
- **Digits:** `0-9`
- **数字：** `0-9`
- **Special:** `escape`, `esc`, `enter`, `return`, `tab`, `space`, `backspace`, `delete`, `insert`, `clear`, `home`, `end`, `pageUp`, `pageDown`, `up`, `down`, `left`, `right`
- **特殊键：** `escape`、`esc`、`enter`、`return`、`tab`、`space`、`backspace`、`delete`、`insert`、`clear`、`home`、`end`、`pageUp`、`pageDown`、`up`、`down`、`left`、`right`
- **Function:** `f1`-`f12`
- **功能键：** `f1`-`f12`
- **Symbols:** `` ` ``, `-`, `=`, `[`, `]`, `\`, `;`, `'`, `,`, `.`, `/`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `(`, `)`, `_`, `+`, `|`, `~`, `{`, `}`, `:`, `<`, `>`, `?`
- **符号：** `` ` ``、`-`、`=`、`[`、`]`、`\`、`;`、`'`、`,`、`.`、`/`、`!`、`@`、`#`、`$`、`%`、`^`、`&`、`*`、`(`、`)`、`_`、`+`、`|`、`~`、`{`、`}`、`:`、`<`、`>`、`?`

Modifier combinations: `ctrl+shift+x`, `alt+ctrl+x`, `ctrl+shift+alt+x`, `super+k`, `ctrl+super+k`, `ctrl+1`, etc.
修饰键组合：`ctrl+shift+x`、`alt+ctrl+x`、`ctrl+shift+alt+x`、`super+k`、`ctrl+super+k`、`ctrl+1` 等。

`super` bindings require a terminal that reports the modifier separately, typically through the Kitty keyboard protocol. They may not work in terminals without that support.
`super` 绑定需要终端单独上报该修饰键，通常通过 Kitty 键盘协议。在不支持该协议的终端中可能无效。

## All Actions
## 全部动作

### TUI Editor Cursor Movement
### TUI 编辑器光标移动

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `tui.editor.cursorUp` | `up` | Move cursor up, browsing older history at the top |
| `tui.editor.cursorDown` | `down` | Move cursor down, browsing newer history at the bottom |
| `tui.editor.historyPrevious` | *(none)* | Select the previous prompt history entry |
| `tui.editor.historyNext` | *(none)* | Select the next prompt history entry |
| `tui.editor.cursorLeft` | `left`, `ctrl+b` | Move cursor left |
| `tui.editor.cursorRight` | `right`, `ctrl+f` | Move cursor right |
| `tui.editor.cursorWordLeft` | `alt+left`, `ctrl+left`, `alt+b` | Move cursor word left |
| `tui.editor.cursorWordRight` | `alt+right`, `ctrl+right`, `alt+f` | Move cursor word right |
| `tui.editor.cursorLineStart` | `home`, `ctrl+home`, `ctrl+a` | Move to line start |
| `tui.editor.cursorLineEnd` | `end`, `ctrl+end`, `ctrl+e` | Move to line end |
| `tui.editor.jumpForward` | `ctrl+]` | Jump forward to character |
| `tui.editor.jumpBackward` | `ctrl+alt+]` | Jump backward to character |
| `tui.editor.pageUp` | `pageUp`, `ctrl+pageUp` | Scroll up by page |
| `tui.editor.pageDown` | `pageDown`, `ctrl+pageDown` | Scroll down by page |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `tui.editor.cursorUp` | `up` | 向上移动光标，在顶部浏览较早的历史 |
| `tui.editor.cursorDown` | `down` | 向下移动光标，在底部浏览较新的历史 |
| `tui.editor.historyPrevious` | *（无）* | 选择上一条提示历史条目 |
| `tui.editor.historyNext` | *（无）* | 选择下一条提示历史条目 |
| `tui.editor.cursorLeft` | `left`, `ctrl+b` | 向左移动光标 |
| `tui.editor.cursorRight` | `right`, `ctrl+f` | 向右移动光标 |
| `tui.editor.cursorWordLeft` | `alt+left`, `ctrl+left`, `alt+b` | 向左移动一个词 |
| `tui.editor.cursorWordRight` | `alt+right`, `ctrl+right`, `alt+f` | 向右移动一个词 |
| `tui.editor.cursorLineStart` | `home`, `ctrl+home`, `ctrl+a` | 移动到行首 |
| `tui.editor.cursorLineEnd` | `end`, `ctrl+end`, `ctrl+e` | 移动到行尾 |
| `tui.editor.jumpForward` | `ctrl+]` | 向前跳到字符 |
| `tui.editor.jumpBackward` | `ctrl+alt+]` | 向后跳到字符 |
| `tui.editor.pageUp` | `pageUp`, `ctrl+pageUp` | 向上翻页 |
| `tui.editor.pageDown` | `pageDown`, `ctrl+pageDown` | 向下翻页 |


The dedicated history actions always change history entries, regardless of the cursor position in a multiline prompt. Explicit history bindings take precedence over application actions while the main editor is focused, so binding `tui.editor.historyPrevious` to `ctrl+p` overrides model cycling in that context without changing `Ctrl+P` in selectors.
专用的历史动作总是切换历史条目，无论光标在多行提示中的什么位置。当主编辑器获得焦点时，显式的历史绑定优先于应用动作，因此把 `tui.editor.historyPrevious` 绑定到 `ctrl+p` 会在该上下文中覆盖模型循环切换，而不改变选择器中的 `Ctrl+P`。

### TUI Editor Deletion
### TUI 编辑器删除

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `tui.editor.deleteCharBackward` | `backspace` | Delete character backward |
| `tui.editor.deleteCharForward` | `delete`, `ctrl+d` | Delete character forward |
| `tui.editor.deleteWordBackward` | `ctrl+w`, `alt+backspace` | Delete word backward |
| `tui.editor.deleteWordForward` | `alt+d`, `alt+delete` | Delete word forward |
| `tui.editor.deleteToLineStart` | `ctrl+u` | Delete to line start |
| `tui.editor.deleteToLineEnd` | `ctrl+k` | Delete to line end |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `tui.editor.deleteCharBackward` | `backspace` | 向后删除字符 |
| `tui.editor.deleteCharForward` | `delete`, `ctrl+d` | 向前删除字符 |
| `tui.editor.deleteWordBackward` | `ctrl+w`, `alt+backspace` | 向后删除一个词 |
| `tui.editor.deleteWordForward` | `alt+d`, `alt+delete` | 向前删除一个词 |
| `tui.editor.deleteToLineStart` | `ctrl+u` | 删除到行首 |
| `tui.editor.deleteToLineEnd` | `ctrl+k` | 删除到行尾 |


### TUI Input
### TUI 输入

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `tui.input.newLine` | `shift+enter`, `ctrl+j` | Insert new line |
| `tui.input.submit` | `enter` | Submit input |
| `tui.input.tab` | `tab` | Tab / autocomplete |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `tui.input.newLine` | `shift+enter`, `ctrl+j` | 插入新行 |
| `tui.input.submit` | `enter` | 提交输入 |
| `tui.input.tab` | `tab` | Tab / 自动补全 |


### TUI Kill Ring
### TUI 剪切环（Kill Ring）

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `tui.editor.yank` | `ctrl+y` | Paste most recently deleted text |
| `tui.editor.yankPop` | `alt+y` | Cycle through deleted text after yank |
| `tui.editor.undo` | `ctrl+-` (`ctrl+z` on Windows; `alt+z` on WSL) | Undo last edit |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `tui.editor.yank` | `ctrl+y` | 粘贴最近删除的文本 |
| `tui.editor.yankPop` | `alt+y` | 在 yank 之后循环切换已删除的文本 |
| `tui.editor.undo` | `ctrl+-`（Windows 上为 `ctrl+z`；WSL 上为 `alt+z`） | 撤销上一次编辑 |


### TUI Clipboard and Selection
### TUI 剪贴板与选择

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `tui.input.copy` | `ctrl+c` | Copy selection |
| `tui.select.up` | `up` | Move selection up |
| `tui.select.down` | `down` | Move selection down |
| `tui.select.pageUp` | `pageUp` | Page up in list |
| `tui.select.pageDown` | `pageDown` | Page down in list |
| `tui.select.confirm` | `enter` | Confirm selection |
| `tui.select.cancel` | `escape`, `ctrl+c` | Cancel selection |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `tui.input.copy` | `ctrl+c` | 复制选区 |
| `tui.select.up` | `up` | 向上移动选择 |
| `tui.select.down` | `down` | 向下移动选择 |
| `tui.select.pageUp` | `pageUp` | 列表中向上翻页 |
| `tui.select.pageDown` | `pageDown` | 列表中向下翻页 |
| `tui.select.confirm` | `enter` | 确认选择 |
| `tui.select.cancel` | `escape`, `ctrl+c` | 取消选择 |


### TUI Fullscreen Viewport
### TUI 全屏视口

These actions apply when interactive mode uses `--tui-mode fullscreen` and target the primary transcript scroll region. Two-finger trackpad and mouse-wheel input scroll the region under the pointer, falling back to the transcript over the fixed editor/status/footer dock. Clicking an OSC 8 hyperlink opens it in the default handler. Dragging with the primary mouse button selects text and copies it to the clipboard; holding at the transcript's top or bottom edge auto-scrolls into off-screen content. See [Terminal setup](terminal-setup.md) for terminal-specific mouse and trackpad behavior.
这些动作在交互模式使用 `--tui-mode fullscreen` 时生效，作用于主对话记录滚动区域。双指触控板和鼠标滚轮输入滚动指针下的区域，回退到固定编辑器/状态/页脚停靠区上方的对话记录。点击 OSC 8 超链接会用默认处理程序打开它。用主鼠标键拖动可以选择文本并复制到剪贴板；在对话记录顶部或底部边缘按住会自动滚动到屏幕外内容。终端特定的鼠标和触控板行为参见[终端设置](terminal-setup.md)。

Fullscreen transcript bindings take precedence over editor bindings. The default unmodified navigation keys therefore control the transcript in fullscreen mode, while their `ctrl` variants continue to control the editor. Outside fullscreen mode, both variants control the editor.
全屏对话记录绑定优先于编辑器绑定。因此默认的无修饰导航键在全屏模式下控制对话记录，而它们的 `ctrl` 变体继续控制编辑器。在全屏模式之外，两种变体都控制编辑器。

| Key | Default mode | Fullscreen mode |
|-----|--------------|-----------------|
| `home`, `end` | Editor | Transcript |
| `ctrl+home`, `ctrl+end` | Editor | Editor |
| `pageUp`, `pageDown` | Editor | Transcript |
| `ctrl+pageUp`, `ctrl+pageDown` | Editor | Editor |

| 按键 | 默认模式 | 全屏模式 |
|-----|--------------|-----------------|
| `home`, `end` | 编辑器 | 对话记录 |
| `ctrl+home`, `ctrl+end` | 编辑器 | 编辑器 |
| `pageUp`, `pageDown` | 编辑器 | 对话记录 |
| `ctrl+pageUp`, `ctrl+pageDown` | 编辑器 | 编辑器 |


This routing remains configurable through the ordinary action bindings. For example, `"tui.altScreen.pageUp": "ctrl+pageUp"` makes `pageUp` control the editor and `ctrl+pageUp` control the transcript in fullscreen mode. Bind `tui.altScreen.halfPageUp` and `tui.altScreen.halfPageDown` for half-page steps, or bind `tui.altScreen.lineUp` and `tui.altScreen.lineDown` for single-line steps. Setting `"tui.altScreen.pageUp": []` disables that transcript shortcut entirely. User bindings replace the defaults for that action.
此路由仍然可以通过普通的动作绑定进行配置。例如，`"tui.altScreen.pageUp": "ctrl+pageUp"` 会让 `pageUp` 控制编辑器、`ctrl+pageUp` 在全屏模式下控制对话记录。绑定 `tui.altScreen.halfPageUp` 和 `tui.altScreen.halfPageDown` 可实现半页滚动，或绑定 `tui.altScreen.lineUp` 和 `tui.altScreen.lineDown` 实现单行滚动。设置 `"tui.altScreen.pageUp": []` 会完全禁用该对话记录快捷键。用户绑定会替换该动作的默认值。

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `tui.altScreen.pageUp` | `pageUp` | Scroll the transcript up by one page |
| `tui.altScreen.pageDown` | `pageDown` | Scroll the transcript down by one page |
| `tui.altScreen.halfPageUp` | *(none)* | Scroll the transcript up by half a page |
| `tui.altScreen.halfPageDown` | *(none)* | Scroll the transcript down by half a page |
| `tui.altScreen.lineUp` | *(none)* | Scroll the transcript up by one line |
| `tui.altScreen.lineDown` | *(none)* | Scroll the transcript down by one line |
| `tui.altScreen.previousPrompt` | `ctrl+shift+up`, `ctrl+up` (`ctrl+up` only on Windows and WSL) | Jump to the previous marked message |
| `tui.altScreen.nextPrompt` | `ctrl+shift+down`, `ctrl+down` (`ctrl+down` only on Windows and WSL) | Jump to the next marked message |
| `tui.altScreen.search` | `ctrl+shift+f` (`ctrl+f` on Windows and WSL) | Search the rendered transcript |
| `tui.altScreen.searchNext` | `enter`, `ctrl+g` | Select the next search match while searching |
| `tui.altScreen.searchPrevious` | `shift+enter`, `ctrl+shift+g` | Select the previous search match while searching |
| `tui.altScreen.searchClose` | `escape` | Close transcript search |
| `tui.altScreen.top` | `home` | Scroll to the beginning of the transcript |
| `tui.altScreen.bottom` | `end` | Scroll to the transcript end and follow new output |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `tui.altScreen.pageUp` | `pageUp` | 对话记录向上滚动一页 |
| `tui.altScreen.pageDown` | `pageDown` | 对话记录向下滚动一页 |
| `tui.altScreen.halfPageUp` | *（无）* | 对话记录向上滚动半页 |
| `tui.altScreen.halfPageDown` | *（无）* | 对话记录向下滚动半页 |
| `tui.altScreen.lineUp` | *（无）* | 对话记录向上滚动一行 |
| `tui.altScreen.lineDown` | *（无）* | 对话记录向下滚动一行 |
| `tui.altScreen.previousPrompt` | `ctrl+shift+up`, `ctrl+up`（Windows 和 WSL 上仅 `ctrl+up`） | 跳到上一个标记的消息 |
| `tui.altScreen.nextPrompt` | `ctrl+shift+down`, `ctrl+down`（Windows 和 WSL 上仅 `ctrl+down`） | 跳到下一个标记的消息 |
| `tui.altScreen.search` | `ctrl+shift+f`（Windows 和 WSL 上为 `ctrl+f`） | 搜索已渲染的对话记录 |
| `tui.altScreen.searchNext` | `enter`, `ctrl+g` | 搜索时选择下一个匹配 |
| `tui.altScreen.searchPrevious` | `shift+enter`, `ctrl+shift+g` | 搜索时选择上一个匹配 |
| `tui.altScreen.searchClose` | `escape` | 关闭对话记录搜索 |
| `tui.altScreen.top` | `home` | 滚动到对话记录开头 |
| `tui.altScreen.bottom` | `end` | 滚动到对话记录末尾并跟随新输出 |


### Application
### 应用程序

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.interrupt` | `escape` | Cancel / abort |
| `app.clear` | `ctrl+c` | Clear editor (first) / exit (second) |
| `app.exit` | `ctrl+d` | Exit (when editor empty) |
| `app.suspend` | `ctrl+z` (none on Windows) | Suspend to background |
| `app.editor.external` | `ctrl+g` | Open in external editor (`externalEditor`, `$VISUAL`, `$EDITOR`, Notepad on Windows, or `nano` elsewhere) |
| `app.clipboard.pasteImage` | `ctrl+v` (`alt+v` on Windows and WSL) | Paste image or text from clipboard |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `app.interrupt` | `escape` | 取消 / 中止 |
| `app.clear` | `ctrl+c` | 清空编辑器（第一次）/ 退出（第二次） |
| `app.exit` | `ctrl+d` | 退出（编辑器为空时） |
| `app.suspend` | `ctrl+z`（Windows 上无） | 挂起到后台 |
| `app.editor.external` | `ctrl+g` | 在外部编辑器中打开（`externalEditor`、`$VISUAL`、`$EDITOR`、Windows 上的记事本或其他平台上的 `nano`） |
| `app.clipboard.pasteImage` | `ctrl+v`（Windows 和 WSL 上为 `alt+v`） | 从剪贴板粘贴图片或文本 |


### Sessions
### 会话

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.session.new` | *(none)* | Start a new session (`/new`) |
| `app.session.tree` | *(none)* | Open session tree navigator (`/tree`) |
| `app.session.fork` | *(none)* | Fork current session (`/fork`) |
| `app.session.resume` | *(none)* | Open session resume picker (`/resume`) |
| `app.session.togglePath` | `ctrl+p` | Toggle path display |
| `app.session.toggleSort` | `ctrl+s` | Toggle sort mode |
| `app.session.toggleNamedFilter` | `ctrl+n` | Toggle named-only filter |
| `app.session.rename` | `ctrl+r` | Rename session |
| `app.session.delete` | `ctrl+d` | Delete session |
| `app.session.deleteNoninvasive` | `ctrl+backspace` | Delete session when query is empty |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `app.session.new` | *（无）* | 开始新会话（`/new`） |
| `app.session.tree` | *（无）* | 打开会话树导航器（`/tree`） |
| `app.session.fork` | *（无）* | 分叉当前会话（`/fork`） |
| `app.session.resume` | *（无）* | 打开会话恢复选择器（`/resume`） |
| `app.session.togglePath` | `ctrl+p` | 切换路径显示 |
| `app.session.toggleSort` | `ctrl+s` | 切换排序模式 |
| `app.session.toggleNamedFilter` | `ctrl+n` | 切换仅显示命名会话的过滤 |
| `app.session.rename` | `ctrl+r` | 重命名会话 |
| `app.session.delete` | `ctrl+d` | 删除会话 |
| `app.session.deleteNoninvasive` | `ctrl+backspace` | 查询为空时删除会话 |


### Models and Thinking
### 模型与思考

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.model.select` | `ctrl+l` | Open model selector |
| `app.model.cycleForward` | `ctrl+p` | Cycle to next model |
| `app.model.cycleBackward` | `shift+ctrl+p` (`alt+p` on Windows and WSL) | Cycle to previous model |
| `app.thinking.cycle` | `shift+tab` | Cycle thinking level |
| `app.thinking.toggle` | `ctrl+t` | Collapse or expand thinking blocks |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `app.model.select` | `ctrl+l` | 打开模型选择器 |
| `app.model.cycleForward` | `ctrl+p` | 循环到下一个模型 |
| `app.model.cycleBackward` | `shift+ctrl+p`（Windows 和 WSL 上为 `alt+p`） | 循环到上一个模型 |
| `app.thinking.cycle` | `shift+tab` | 循环切换思考等级 |
| `app.thinking.toggle` | `ctrl+t` | 折叠或展开思考块 |


### Display and Message Queue
### 显示与消息队列

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.tools.expand` | `ctrl+o` | Collapse or expand tool output |
| `app.message.copy` | `ctrl+x` | Copy the selected message in `/tree`; otherwise copy the last assistant message, or the active fullscreen text selection when `fullscreenCopyOnSelect` is disabled |
| `app.message.followUp` | `alt+enter` (`ctrl+q` on Windows and WSL) | Queue follow-up message |
| `app.message.dequeue` | `alt+up` (`alt+q` on Windows and WSL) | Restore queued messages to editor |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `app.tools.expand` | `ctrl+o` | 折叠或展开工具输出 |
| `app.message.copy` | `ctrl+x` | 在 `/tree` 中复制选中的消息；否则复制最后一条助手消息，或在 `fullscreenCopyOnSelect` 禁用时复制活动的全屏文本选区 |
| `app.message.followUp` | `alt+enter`（Windows 和 WSL 上为 `ctrl+q`） | 排队 follow-up 消息 |
| `app.message.dequeue` | `alt+up`（Windows 和 WSL 上为 `alt+q`） | 把排队的消息恢复到编辑器 |


### Tree Navigation
### 树导航

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.tree.foldOrUp` | `ctrl+left`, `alt+left` | Fold current branch segment, or jump to the previous segment start |
| `app.tree.unfoldOrDown` | `ctrl+right`, `alt+right` | Unfold current branch segment, or jump to the next segment start or branch end |
| `app.tree.editLabel` | `shift+l` | Edit the label on the selected tree node |
| `app.tree.toggleLabelTimestamp` | `shift+t` | Toggle label timestamps in the tree |
| `app.tree.filter.default` | `ctrl+d` | Set tree filter to default view |
| `app.tree.filter.noTools` | `ctrl+t` | Toggle tree filter that hides tool results |
| `app.tree.filter.userOnly` | `ctrl+u` | Toggle tree filter that shows only user messages |
| `app.tree.filter.labeledOnly` | `ctrl+l` | Toggle tree filter that shows only labeled entries |
| `app.tree.filter.all` | `ctrl+a` | Toggle tree filter that shows all entries |
| `app.tree.filter.cycleForward` | `ctrl+o` | Cycle tree filter forward |
| `app.tree.filter.cycleBackward` | `shift+ctrl+o` | Cycle tree filter backward |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `app.tree.foldOrUp` | `ctrl+left`, `alt+left` | 折叠当前分支段，或跳到上一段开头 |
| `app.tree.unfoldOrDown` | `ctrl+right`, `alt+right` | 展开当前分支段，或跳到下一段开头或分支末尾 |
| `app.tree.editLabel` | `shift+l` | 编辑选中树节点上的标签 |
| `app.tree.toggleLabelTimestamp` | `shift+t` | 在树中切换标签时间戳 |
| `app.tree.filter.default` | `ctrl+d` | 把树过滤器设为默认视图 |
| `app.tree.filter.noTools` | `ctrl+t` | 切换隐藏工具结果的树过滤器 |
| `app.tree.filter.userOnly` | `ctrl+u` | 切换只显示用户消息的树过滤器 |
| `app.tree.filter.labeledOnly` | `ctrl+l` | 切换只显示有标签条目的树过滤器 |
| `app.tree.filter.all` | `ctrl+a` | 切换显示所有条目的树过滤器 |
| `app.tree.filter.cycleForward` | `ctrl+o` | 向前循环树过滤器 |
| `app.tree.filter.cycleBackward` | `shift+ctrl+o` | 向后循环树过滤器 |


### Scoped Models Selector
### Scoped 模型选择器

Used inside the scoped models selector (opened via `/scoped-models`).
在 scoped 模型选择器（通过 `/scoped-models` 打开）内部使用。

| Keybinding id | Default | Description |
|--------|---------|-------------|
| `app.models.save` | `ctrl+s` | Save current model selection to settings |
| `app.models.enableAll` | `ctrl+a` | Enable all models (or all matching the current search) |
| `app.models.clearAll` | `ctrl+x` | Clear all models (or all matching the current search) |
| `app.models.toggleProvider` | `ctrl+p` | Toggle all models for the current provider |
| `app.models.reorderUp` | `alt+up` | Move the selected model up in the cycle order |
| `app.models.reorderDown` | `alt+down` | Move the selected model down in the cycle order |

| 快捷键 id | 默认值 | 描述 |
|--------|---------|-------------|
| `app.models.save` | `ctrl+s` | 把当前模型选择保存到设置 |
| `app.models.enableAll` | `ctrl+a` | 启用所有模型（或所有匹配当前搜索的模型） |
| `app.models.clearAll` | `ctrl+x` | 清空所有模型（或所有匹配当前搜索的模型） |
| `app.models.toggleProvider` | `ctrl+p` | 切换当前提供商的所有模型 |
| `app.models.reorderUp` | `alt+up` | 在循环顺序中上移所选模型 |
| `app.models.reorderDown` | `alt+down` | 在循环顺序中下移所选模型 |


## Custom Configuration
## 自定义配置

Create `~/.pi/agent/keybindings.json`:
创建 `~/.pi/agent/keybindings.json`：

```json
{
  "tui.editor.historyPrevious": "ctrl+p",
  "tui.editor.historyNext": "ctrl+n",
  "tui.editor.deleteWordBackward": ["ctrl+w", "alt+backspace"]
}
```

Each action can have a single key or an array of keys. User config overrides defaults.
每个动作可以是单个按键或按键数组。用户配置覆盖默认值。

On native Windows, `app.suspend` has no default binding because Windows terminals do not support Unix job control. If you bind it manually, pi shows a status message instead of suspending. In WSL, the normal Linux `ctrl+z`/`fg` behavior still applies.
在原生 Windows 上，`app.suspend` 没有默认绑定，因为 Windows 终端不支持 Unix 作业控制。如果你手动绑定它，pi 会显示状态消息而不是挂起。在 WSL 中，正常的 Linux `ctrl+z`/`fg` 行为仍然适用。

### Emacs Example
### Emacs 示例

```json
{
  "tui.editor.historyPrevious": "ctrl+p",
  "tui.editor.historyNext": "ctrl+n",
  "tui.editor.cursorLeft": ["left", "ctrl+b"],
  "tui.editor.cursorRight": ["right", "ctrl+f"],
  "tui.editor.cursorWordLeft": ["alt+left", "alt+b"],
  "tui.editor.cursorWordRight": ["alt+right", "alt+f"],
  "tui.editor.deleteCharForward": ["delete", "ctrl+d"],
  "tui.editor.deleteCharBackward": ["backspace", "ctrl+h"],
  "tui.input.newLine": ["shift+enter", "ctrl+j"]
}
```

### Vim Example
### Vim 示例

```json
{
  "tui.editor.cursorUp": ["up", "alt+k"],
  "tui.editor.cursorDown": ["down", "alt+j"],
  "tui.editor.cursorLeft": ["left", "alt+h"],
  "tui.editor.cursorRight": ["right", "alt+l"],
  "tui.editor.cursorWordLeft": ["alt+left", "alt+b"],
  "tui.editor.cursorWordRight": ["alt+right", "alt+w"]
}
```
