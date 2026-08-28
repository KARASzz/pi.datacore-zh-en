> 📄 来源 Source: https://pi.dev/docs/latest/sessions
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Sessions
# 会话

Pi saves conversations as sessions so you can continue work, branch from earlier turns, and revisit previous paths.
Pi 将对话保存为会话，这样你可以继续工作、从较早的轮次分支、并重访之前的路径。

## Session Storage
## 会话存储

Sessions auto-save to `~/.pi/agent/sessions/`, organized by working directory. Each session is a JSONL file with a tree structure.
会话自动保存到 `~/.pi/agent/sessions/`，按工作目录组织。每个会话都是一个具有树状结构的 JSONL 文件。

```bash
pi -c                  # Continue most recent session
pi -r                  # Browse and select from past sessions
pi --no-session        # Ephemeral mode; do not save
pi --name "my task"    # Set session display name at startup
pi --session <path|id> # Use a specific session file or partial session ID
pi --fork <path|id>    # Fork a session file or partial session ID into a new session
```

Use `/session` in interactive mode to see the current session file, session ID, message count, tokens, and cost.
在交互模式中使用 `/session` 查看当前会话文件、会话 ID、消息数、token 数和成本。

For the JSONL file format and SessionManager API, see [Session Format](session-format.md).
JSONL 文件格式和 SessionManager API 参见[会话格式](session-format.md)。

## Session Commands
## 会话命令

| Command | Description |
|---------|-------------|
| `/resume` | Browse and select previous sessions |
| `/new` | Start a new session |
| `/name <name>` | Set the current session display name |
| `/session` | Show session info |
| `/tree` | Navigate the current session tree |
| `/fork` | Create a new session from a previous user message |
| `/clone` | Duplicate the current active branch into a new session |
| `/compact [prompt]` | Summarize older context; see [Compaction](compaction.md) |
| `/export [file]` | Export session to HTML |
| `/share` | Upload as private GitHub gist with shareable HTML link |

| 命令 | 描述 |
|---------|-------------|
| `/resume` | 浏览并选择以前的会话 |
| `/new` | 开始新会话 |
| `/name <name>` | 设置当前会话的显示名称 |
| `/session` | 显示会话信息 |
| `/tree` | 导航当前会话树 |
| `/fork` | 从之前的用户消息创建新会话 |
| `/clone` | 将当前活动分支复制到新会话 |
| `/compact [prompt]` | 摘要较旧的上下文；参见[压缩](compaction.md) |
| `/export [file]` | 将会话导出为 HTML |
| `/share` | 上传为私有 GitHub gist 并附可分享的 HTML 链接 |


## Resuming and Deleting Sessions
## 恢复与删除会话

`/resume` opens an interactive session picker for the current project. `pi -r` opens the same picker at startup.
`/resume` 为当前项目打开交互式会话选择器。`pi -r` 在启动时打开相同的选择器。

In the picker you can:
在选择器中你可以：

- search by typing
- 通过输入进行搜索
- toggle path display with Ctrl+P
- 用 Ctrl+P 切换路径显示
- toggle sort mode with Ctrl+S
- 用 Ctrl+S 切换排序模式
- filter to named sessions with Ctrl+N
- 用 Ctrl+N 过滤出已命名的会话
- rename with Ctrl+R
- 用 Ctrl+R 重命名
- delete with Ctrl+D, then confirm
- 用 Ctrl+D 删除，然后确认

When available, pi uses the `trash` CLI for deletion instead of permanently removing files.
在可用时，pi 使用 `trash` CLI 进行删除，而不是永久移除文件。

## Naming Sessions
## 命名会话

Use `/name <name>` to set a human-readable session name:
使用 `/name <name>` 设置人类可读的会话名称：

```text
/name Refactor auth module
```

Set the name at startup with `--name` or `-n`:
启动时用 `--name` 或 `-n` 设置名称：

```bash
pi --name "Refactor auth module"
pi --name "CI audit" -p "Review this build failure"
```

Named sessions are easier to find in `/resume` and `pi -r`.
已命名的会话在 `/resume` 和 `pi -r` 中更容易找到。

## Branching with `/tree`
## 用 `/tree` 分支

Sessions are stored as trees. Every entry has an `id` and `parentId`, and the current position is the active leaf. `/tree` lets you jump to any previous point and continue from there without creating a new file.
会话以树的形式存储。每个条目都有 `id` 和 `parentId`，当前位置即活动叶子。`/tree` 让你跳到之前任意一点并从那里继续，而无需创建新文件。

<p align="center"><img src="images/tree-view.png" alt="Tree View" width="600"></p>
<p align="center"><img src="images/tree-view.png" alt="树状视图" width="600"></p>

Example shape:
示例形状：

```text
├─ user: "Hello, can you help..."
│  └─ assistant: "Of course! I can..."
│     ├─ user: "Let's try approach A..."
│     │  └─ assistant: "For approach A..."
│     │     └─ user: "That worked..."  ← active
│     └─ user: "Actually, approach B..."
│        └─ assistant: "For approach B..."
```

### Tree Controls
### 树控制键

| Key | Action |
|-----|--------|
| ↑/↓ | Navigate visible entries |
| ←/→ | Page up/down |
| Ctrl+←/Ctrl+→ or Alt+←/Alt+→ | Fold/unfold or jump between branch segments |
| Shift+L | Set or clear a label on the selected entry |
| Shift+T | Toggle label timestamps |
| Enter | Select entry |
| Escape/Ctrl+C | Cancel |
| Ctrl+O | Cycle filter mode |

| 键 | 动作 |
|-----|--------|
| ↑/↓ | 在可见条目间导航 |
| ←/→ | 上/下翻页 |
| Ctrl+←/Ctrl+→ 或 Alt+←/Alt+→ | 折叠/展开或在分支段之间跳转 |
| Shift+L | 为选中条目设置或清除标签 |
| Shift+T | 切换标签时间戳显示 |
| Enter | 选择条目 |
| Escape/Ctrl+C | 取消 |
| Ctrl+O | 循环切换过滤模式 |


Filter modes are: default, no-tools, user-only, labeled-only, and all. Configure the default with `treeFilterMode` in [Settings](settings.md).
过滤模式有：default、no-tools、user-only、labeled-only 和 all。用[设置](settings.md)中的 `treeFilterMode` 配置默认值。

### Selection Behavior
### 选择行为

Selecting a user or custom message:
选择用户或自定义消息时：

1. Moves the leaf to the selected message's parent.
1. 将叶子移动到所选消息的父节点。
2. Places the selected message text in the editor.
2. 将所选消息文本放入编辑器。
3. Lets you edit and resubmit, creating a new branch.
3. 让你编辑并重新提交，从而创建一个新分支。

Selecting an assistant, tool, compaction, or other non-user entry:
选择助手、工具、压缩或其他非用户条目时：

1. Moves the leaf to that entry.
1. 将叶子移动到该条目。
2. Leaves the editor empty.
2. 编辑器保持为空。
3. Lets you continue from that point.
3. 让你从该点继续。

Selecting the root user message resets the leaf to an empty conversation and places the original prompt in the editor.
选择根用户消息会将叶子重置为空对话，并将原始提示放入编辑器。

## `/tree`, `/fork`, and `/clone`
## `/tree`、`/fork` 与 `/clone`

| Feature | `/tree` | `/fork` | `/clone` |
|---------|---------|---------|----------|
| Output | Same session file | New session file | New session file |
| View | Full tree | User-message selector | Current active branch |
| Typical use | Explore alternatives in place | Start a new session from an earlier prompt | Duplicate current work before continuing |
| Summary | Optional branch summary | None | None |

| 特性 | `/tree` | `/fork` | `/clone` |
|---------|---------|---------|----------|
| 输出 | 同一会话文件 | 新会话文件 | 新会话文件 |
| 视图 | 完整树 | 用户消息选择器 | 当前活动分支 |
| 典型用途 | 原地探索备选方案 | 从较早的提示开始新会话 | 继续之前复制当前工作 |
| 摘要 | 可选分支摘要 | 无 | 无 |


Use `/tree` when you want to keep alternatives together. Use `/fork` or `/clone` when you want a separate session file.
想保留备选方案时使用 `/tree`。想要独立的会话文件时使用 `/fork` 或 `/clone`。

## Branch Summaries
## 分支摘要

When `/tree` switches away from one branch to another, pi can summarize the abandoned branch and attach that summary at the new position. This preserves important context from the path you left without replaying the whole branch.
当 `/tree` 从一个分支切换到另一个分支时，pi 可以摘要被放弃的分支，并将该摘要附加到新位置。这样可以在不重放整个分支的情况下保留你所离开路径的重要上下文。

When prompted, choose one of:
收到提示时，可选择：

1. no summary
1. 不摘要
2. summarize with the default prompt
2. 使用默认提示词摘要
3. summarize with custom focus instructions
3. 使用自定义重点指令摘要

See [Compaction](compaction.md) for branch summarization internals and extension hooks.
分支摘要的内部机制与扩展钩子参见[压缩](compaction.md)。

## Session Format
## 会话格式

Session files are JSONL and contain message entries, model changes, thinking-level changes, labels, compactions, branch summaries, and extension entries.
会话文件为 JSONL 格式，包含消息条目、模型变更、思考等级变更、标签、压缩、分支摘要和扩展条目。

For parsers, extensions, SDK usage, and the full SessionManager API, see [Session Format](session-format.md).
解析器、扩展、SDK 用法以及完整的 SessionManager API 参见[会话格式](session-format.md)。
