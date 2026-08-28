> 📄 来源 Source: https://pi.dev/docs/latest/session-format
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Session File Format
# 会话文件格式

Sessions are stored as JSONL (JSON Lines) files. Each line is a JSON object with a `type` field. Session entries form a tree structure via `id`/`parentId` fields, enabling in-place branching without creating new files.
会话以 JSONL（JSON Lines）文件存储。每行是一个带 `type` 字段的 JSON 对象。会话条目通过 `id`/`parentId` 字段构成树状结构，支持原地分支而无需创建新文件。

## File Location
## 文件位置

```
~/.pi/agent/sessions/--<path>--/<timestamp>_<uuid>.jsonl
```

Where `<path>` is the working directory with `/` replaced by `-`.
其中 `<path>` 是把 `/` 替换为 `-` 后的工作目录。

## Deleting Sessions
## 删除会话

Sessions can be removed by deleting their `.jsonl` files under `~/.pi/agent/sessions/`.
可以通过删除 `~/.pi/agent/sessions/` 下对应的 `.jsonl` 文件来移除会话。

Pi also supports deleting sessions interactively from `/resume` (select a session and press `Ctrl+D`, then confirm). When available, pi uses the `trash` CLI to avoid permanent deletion.
Pi 也支持从 `/resume` 交互式删除会话（选择会话并按 `Ctrl+D`，然后确认）。在可用时，pi 使用 `trash` CLI 以避免永久删除。

## Session Version
## 会话版本

Sessions have a version field in the header:
会话在头部有版本字段：

- **Version 1**: Linear entry sequence (legacy, auto-migrated on load)
- **版本 1**：线性条目序列（旧版，加载时自动迁移）
- **Version 2**: Tree structure with `id`/`parentId` linking
- **版本 2**：带 `id`/`parentId` 链接的树状结构
- **Version 3**: Renamed `hookMessage` role to `custom` (extensions unification)
- **版本 3**：把 `hookMessage` 角色改名为 `custom`（扩展统一）

Existing sessions are automatically migrated to the current version (v3) when loaded.
现有会话在加载时会自动迁移到当前版本（v3）。

## Source Files
## 源文件

Source on GitHub ([pi-mono](https://github.com/earendil-works/pi-mono)):
GitHub 上的源码（[pi-mono](https://github.com/earendil-works/pi-mono)）：
- [`packages/coding-agent/src/core/session-manager.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/session-manager.ts) - Session entry types and SessionManager
- [`packages/coding-agent/src/core/session-manager.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/session-manager.ts) - 会话条目类型与 SessionManager
- [`packages/coding-agent/src/core/messages.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/messages.ts) - Extended message types (BashExecutionMessage, CustomMessage, etc.)
- [`packages/coding-agent/src/core/messages.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/messages.ts) - 扩展消息类型（BashExecutionMessage、CustomMessage 等）
- [`packages/ai/src/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/types.ts) - Base message types (UserMessage, AssistantMessage, ToolResultMessage)
- [`packages/ai/src/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/types.ts) - 基础消息类型（UserMessage、AssistantMessage、ToolResultMessage）
- [`packages/agent/src/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/agent/src/types.ts) - AgentMessage union type
- [`packages/agent/src/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/agent/src/types.ts) - AgentMessage 联合类型

For TypeScript definitions in your project, inspect `node_modules/@earendil-works/pi-coding-agent/dist/` and `node_modules/@earendil-works/pi-ai/dist/`.
要在你的项目中查看 TypeScript 定义，请检查 `node_modules/@earendil-works/pi-coding-agent/dist/` 和 `node_modules/@earendil-works/pi-ai/dist/`。

## Message Types
## 消息类型

Session entries contain `AgentMessage` objects. Understanding these types is essential for parsing sessions and writing extensions.
会话条目包含 `AgentMessage` 对象。理解这些类型对解析会话和编写扩展至关重要。

### Content Blocks
### 内容块

Messages contain arrays of typed content blocks:
消息包含类型化内容块的数组：

```typescript
interface TextContent {
  type: "text";
  text: string;
}

interface ImageContent {
  type: "image";
  data: string;      // base64 encoded
  mimeType: string;  // e.g., "image/jpeg", "image/png"
}

interface ThinkingContent {
  type: "thinking";
  thinking: string;
}

interface ToolCall {
  type: "toolCall";
  id: string;
  name: string;
  arguments: Record<string, any>;
}
```

### Base Message Types (from pi-ai)
### 基础消息类型（来自 pi-ai）

```typescript
interface UserMessage {
  role: "user";
  content: string | (TextContent | ImageContent)[];
  timestamp: number;  // Unix ms
}

interface AssistantMessage {
  role: "assistant";
  content: (TextContent | ThinkingContent | ToolCall)[];
  api: string;
  provider: string;
  model: string;
  usage: Usage;
  stopReason: "stop" | "length" | "toolUse" | "error" | "aborted";
  errorMessage?: string;
  timestamp: number;
}

interface ToolResultMessage {
  role: "toolResult";
  toolCallId: string;
  toolName: string;
  content: (TextContent | ImageContent)[];
  details?: any;      // Tool-specific metadata
  usage?: Usage;      // Nested LLM work performed by the tool
  isError: boolean;
  timestamp: number;
}

interface Usage {
  input: number;
  output: number;
  cacheRead: number;
  cacheWrite: number;
  totalTokens: number;
  cost: {
    input: number;
    output: number;
    cacheRead: number;
    cacheWrite: number;
    total: number;
  };
}
```

The exported pi-ai `StopReason` type also includes `"pending"`, but that value is reserved for partial messages in streaming events. Terminal `done`/`error` messages replace it with a completion reason before pi persists the assistant message, so `"pending"` should never appear in session JSONL.
导出的 pi-ai `StopReason` 类型还包括 `"pending"`，但该值保留给流式事件中的部分消息。终止的 `done`/`error` 消息在 pi 持久化助手消息之前会用完成原因替换它，因此 `"pending"` 不应出现在会话 JSONL 中。

### Extended Message Types (from pi-coding-agent)
### 扩展消息类型（来自 pi-coding-agent）

```typescript
interface BashExecutionMessage {
  role: "bashExecution";
  command: string;
  output: string;
  exitCode: number | undefined;
  cancelled: boolean;
  truncated: boolean;
  fullOutputPath?: string;
  excludeFromContext?: boolean;  // true for !! prefix commands
  timestamp: number;
}

interface CustomMessage {
  role: "custom";
  customType: string;            // Extension identifier
  content: string | (TextContent | ImageContent)[];
  display: boolean;              // Show in TUI
  details?: any;                 // Extension-specific metadata
  timestamp: number;
}

interface BranchSummaryMessage {
  role: "branchSummary";
  summary: string;
  fromId: string;                // Entry we branched from
  timestamp: number;
}

interface CompactionSummaryMessage {
  role: "compactionSummary";
  summary: string;
  tokensBefore: number;
  timestamp: number;
}
```

### AgentMessage Union
### AgentMessage 联合类型

```typescript
type AgentMessage =
  | UserMessage
  | AssistantMessage
  | ToolResultMessage
  | BashExecutionMessage
  | CustomMessage
  | BranchSummaryMessage
  | CompactionSummaryMessage;
```

## Entry Base
## 条目基类

All entries (except `SessionHeader`) extend `SessionEntryBase`:
所有条目（`SessionHeader` 除外）都继承 `SessionEntryBase`：

```typescript
interface SessionEntryBase {
  type: string;
  id: string;           // 8-char hex ID
  parentId: string | null;  // Parent entry ID (null for first entry)
  timestamp: string;    // ISO timestamp
}
```

## Entry Types
## 条目类型

### SessionHeader
### SessionHeader

First line of the file. Metadata only, not part of the tree (no `id`/`parentId`).
文件的第一行。仅元数据，不属于树（没有 `id`/`parentId`）。

```json
{"type":"session","version":3,"id":"uuid","timestamp":"2024-12-03T14:00:00.000Z","cwd":"/path/to/project"}
```

For sessions with a parent (created via `/fork`, `/clone`, or `newSession({ parentSession })`):
对于有父会话的会话（通过 `/fork`、`/clone` 或 `newSession({ parentSession })` 创建）：

```json
{"type":"session","version":3,"id":"uuid","timestamp":"2024-12-03T14:00:00.000Z","cwd":"/path/to/project","parentSession":"/path/to/original/session.jsonl"}
```

### SessionMessageEntry
### SessionMessageEntry

A message in the conversation. The `message` field contains an `AgentMessage`.
对话中的一条消息。`message` 字段包含一个 `AgentMessage`。

```json
{"type":"message","id":"a1b2c3d4","parentId":"prev1234","timestamp":"2024-12-03T14:00:01.000Z","message":{"role":"user","content":"Hello"}}
{"type":"message","id":"b2c3d4e5","parentId":"a1b2c3d4","timestamp":"2024-12-03T14:00:02.000Z","message":{"role":"assistant","content":[{"type":"text","text":"Hi!"}],"provider":"anthropic","model":"claude-sonnet-4-5","usage":{...},"stopReason":"stop"}}
{"type":"message","id":"c3d4e5f6","parentId":"b2c3d4e5","timestamp":"2024-12-03T14:00:03.000Z","message":{"role":"toolResult","toolCallId":"call_123","toolName":"bash","content":[{"type":"text","text":"output"}],"isError":false}}
```

### ModelChangeEntry
### ModelChangeEntry

Emitted when the user switches models mid-session.
当用户在会话中途切换模型时产生。

```json
{"type":"model_change","id":"d4e5f6g7","parentId":"c3d4e5f6","timestamp":"2024-12-03T14:05:00.000Z","provider":"openai","modelId":"gpt-4o"}
```

### ThinkingLevelChangeEntry
### ThinkingLevelChangeEntry

Emitted when the user changes the thinking/reasoning level.
当用户更改思考/推理等级时产生。

```json
{"type":"thinking_level_change","id":"e5f6g7h8","parentId":"d4e5f6g7","timestamp":"2024-12-03T14:06:00.000Z","thinkingLevel":"high"}
```

### CompactionEntry
### CompactionEntry

Created when context is compacted. Stores a summary of earlier messages.
在上下文被压缩时创建。存储较早消息的摘要。

```json
{"type":"compaction","id":"f6g7h8i9","parentId":"e5f6g7h8","timestamp":"2024-12-03T14:10:00.000Z","summary":"User discussed X, Y, Z...","firstKeptEntryId":"c3d4e5f6","tokensBefore":50000}
```

Newer harness-generated compactions embed the retained post-compaction context directly on the entry, instead of `firstKeptEntryId`:
较新的框架生成的压缩会把保留的压缩后上下文直接内嵌在条目上，而不是 `firstKeptEntryId`：

```json
{"type":"compaction","id":"f6g7h8i9","parentId":"e5f6g7h8","timestamp":"2024-12-03T14:10:00.000Z","summary":"User discussed X, Y, Z...","tokensBefore":50000,"retainedTail":[{"role":"user","content":"latest request"},{"role":"assistant","content":[{"type":"text","text":"latest reply"}],"provider":"anthropic","model":"claude-sonnet-4-5","usage":{...},"stopReason":"stop"}]}
```

Optional fields:
可选字段：
- `usage`: LLM usage from generating the summary; included in session token and cost totals
- `usage`：生成摘要时的 LLM 用量；计入会话 token 和成本总计
- `retainedTail`: Materialized `AgentMessage[]` kept after compaction. This is optional only for backward compatibility with older sessions. Newer harness-generated compactions include it so we can rebuild context from this checkpoint without walking older entries before the compaction entry.
- `retainedTail`：压缩后保留的实体化 `AgentMessage[]`。仅为了向后兼容旧会话而是可选的。较新的框架生成的压缩包含它，因此我们可以从这个检查点重建上下文，而无需遍历压缩条目之前的较旧条目。
- `details`: Implementation-specific data (e.g., `{ readFiles: string[], modifiedFiles: string[] }` for default, or custom data for extensions)
- `details`：实现特定的数据（例如默认实现的 `{ readFiles: string[], modifiedFiles: string[] }`，或扩展的自定义数据）
- `fromHook`: `true` if generated by an extension, `false`/`undefined` if pi-generated (legacy field name)
- `fromHook`：如果由扩展生成则为 `true`，pi 生成为 `false`/`undefined`（旧字段名）
- `firstKeptEntryId`: for compatibility with old entry format.
- `firstKeptEntryId`：用于兼容旧条目格式。

### BranchSummaryEntry
### BranchSummaryEntry

Created when switching branches via `/tree` with an LLM generated summary of the left branch up to the common ancestor. Captures context from the abandoned path.
在通过 `/tree` 切换分支时创建，带有一个由 LLM 生成的、关于被离开分支直至公共祖先的摘要。捕获被放弃路径的上下文。

```json
{"type":"branch_summary","id":"g7h8i9j0","parentId":"a1b2c3d4","timestamp":"2024-12-03T14:15:00.000Z","fromId":"f6g7h8i9","summary":"Branch explored approach A..."}
```

Optional fields:
可选字段：
- `usage`: LLM usage from generating the summary; included in session token and cost totals
- `usage`：生成摘要时的 LLM 用量；计入会话 token 和成本总计
- `details`: File tracking data (`{ readFiles: string[], modifiedFiles: string[] }`) for default, or custom data for extensions
- `details`：默认为文件跟踪数据（`{ readFiles: string[], modifiedFiles: string[] }`），扩展可为自定义数据
- `fromHook`: `true` if generated by an extension, `false`/`undefined` if pi-generated (legacy field name)
- `fromHook`：如果由扩展生成则为 `true`，pi 生成为 `false`/`undefined`（旧字段名）

### CustomEntry
### CustomEntry

Extension state persistence. Does NOT participate in LLM context.
扩展状态持久化。不参与 LLM 上下文。

```json
{"type":"custom","id":"h8i9j0k1","parentId":"g7h8i9j0","timestamp":"2024-12-03T14:20:00.000Z","customType":"my-extension","data":{"count":42}}
```

Use `customType` to identify your extension's entries on reload. Interactive mode can render custom entries via `pi.registerEntryRenderer(customType, renderer)`, but they still do not participate in LLM context.
使用 `customType` 在重新加载时识别你扩展的条目。交互模式可以通过 `pi.registerEntryRenderer(customType, renderer)` 渲染自定义条目，但它们仍不参与 LLM 上下文。

### CustomMessageEntry
### CustomMessageEntry

Extension-injected messages that DO participate in LLM context.
由扩展注入、且参与 LLM 上下文的消息。

```json
{"type":"custom_message","id":"i9j0k1l2","parentId":"h8i9j0k1","timestamp":"2024-12-03T14:25:00.000Z","customType":"my-extension","content":"Injected context...","display":true}
```

Fields:
字段：
- `content`: String or `(TextContent | ImageContent)[]` (same as UserMessage)
- `content`：字符串或 `(TextContent | ImageContent)[]`（与 UserMessage 相同）
- `display`: `true` = show in TUI with distinct styling, `false` = hidden
- `display`：`true` = 在 TUI 中以独特样式显示，`false` = 隐藏
- `details`: Optional extension-specific metadata (not sent to LLM)
- `details`：可选的扩展特定元数据（不发送给 LLM）

### LabelEntry
### LabelEntry

User-defined bookmark/marker on an entry.
条目上的用户定义书签/标记。

```json
{"type":"label","id":"j0k1l2m3","parentId":"i9j0k1l2","timestamp":"2024-12-03T14:30:00.000Z","targetId":"a1b2c3d4","label":"checkpoint-1"}
```

Set `label` to `undefined` to clear a label.
把 `label` 设为 `undefined` 可清除标签。

### SessionInfoEntry
### SessionInfoEntry

Session metadata (e.g., user-defined display name). Set via `/name`, `--name` / `-n`, or `pi.setSessionName()` in extensions.
会话元数据（例如用户定义的显示名称）。通过 `/name`、`--name`/`-n` 或扩展中的 `pi.setSessionName()` 设置。

```json
{"type":"session_info","id":"k1l2m3n4","parentId":"j0k1l2m3","timestamp":"2024-12-03T14:35:00.000Z","name":"Refactor auth module"}
```

The session name is displayed in the session selector (`/resume`) instead of the first message when set.
设置后，会话名称会在会话选择器（`/resume`）中显示，而不是第一条消息。

## Tree Structure
## 树结构

Entries form a tree:
条目构成一棵树：
- First entry has `parentId: null`
- 第一个条目的 `parentId` 为 `null`
- Each subsequent entry points to its parent via `parentId`
- 每个后续条目通过 `parentId` 指向其父条目
- Branching creates new children from an earlier entry
- 分支会从较早的条目创建新的子节点
- The "leaf" is the current position in the tree
- “叶子”是树中的当前位置

```
[user msg] ─── [assistant] ─── [user msg] ─── [assistant] ─┬─ [user msg] ← current leaf
                                                            │
                                                            └─ [branch_summary] ─── [user msg] ← alternate branch
```

## Context Building
## 上下文构建

`buildContextEntries()` walks from the current leaf to the root, producing the active entry list while honoring compaction:
`buildContextEntries()` 从当前叶子走向根，在尊重压缩的前提下生成活动条目列表：

1. Collects all entries on the path
1. 收集路径上的所有条目
2. If a `CompactionEntry` is on the path:
2. 如果路径上有 `CompactionEntry`：
   - Includes the compaction entry first
   - 先包含压缩条目
   - If `retainedTail` is present, it acts as a self-contained checkpoint and entries after the compaction are included
   - 如果存在 `retainedTail`，它充当自包含检查点，并包含压缩之后的条目
   - Otherwise entries from `firstKeptEntryId` to the compaction are included
   - 否则包含从 `firstKeptEntryId` 到压缩之间的条目
   - Then entries after compaction are included
   - 然后包含压缩之后的条目
3. Preserves non-message entries in the selected range so interactive mode can render them
3. 保留所选范围内的非消息条目，以便交互模式可以渲染它们

`buildSessionContext()` builds on that entry list to produce the message list for the LLM:
`buildSessionContext()` 在该条目列表的基础上生成给 LLM 的消息列表：

1. Extracts current model and thinking level settings from the full path
1. 从完整路径提取当前模型和思考等级设置
2. Converts selected entries to messages:
2. 把所选条目转换为消息：
   - `message` -> stored `AgentMessage`
   - `message` -> 存储的 `AgentMessage`
   - `compaction` -> `compactionSummary` plus `retainedTail` when present
   - `compaction` -> `compactionSummary`，加上存在时的 `retainedTail`
   - `branch_summary` -> `branchSummary`
   - `branch_summary` -> `branchSummary`
   - `custom_message` -> `CustomMessage`
   - `custom_message` -> `CustomMessage`
   - `custom` -> no context message
   - `custom` -> 无上下文消息

This makes newer compactions act like self-contained checkpoints. `retainedTail` is optional only so older sessions that only store `firstKeptEntryId` continue to load correctly.
这使得较新的压缩表现得像自包含检查点。`retainedTail` 之所以可选，只是为了让只存储 `firstKeptEntryId` 的旧会话仍能正确加载。

## Parsing Example
## 解析示例

```typescript
import { readFileSync } from "fs";

const lines = readFileSync("session.jsonl", "utf8").trim().split("\n");

for (const line of lines) {
  const entry = JSON.parse(line);

  switch (entry.type) {
    case "session":
      console.log(`Session v${entry.version ?? 1}: ${entry.id}`);
      break;
    case "message":
      console.log(`[${entry.id}] ${entry.message.role}: ${JSON.stringify(entry.message.content)}`);
      break;
    case "compaction":
      console.log(`[${entry.id}] Compaction: ${entry.tokensBefore} tokens summarized`);
      break;
    case "branch_summary":
      console.log(`[${entry.id}] Branch from ${entry.fromId}`);
      break;
    case "custom":
      console.log(`[${entry.id}] Custom (${entry.customType}): ${JSON.stringify(entry.data)}`);
      break;
    case "custom_message":
      console.log(`[${entry.id}] Extension message (${entry.customType}): ${entry.content}`);
      break;
    case "label":
      console.log(`[${entry.id}] Label "${entry.label}" on ${entry.targetId}`);
      break;
    case "model_change":
      console.log(`[${entry.id}] Model: ${entry.provider}/${entry.modelId}`);
      break;
    case "thinking_level_change":
      console.log(`[${entry.id}] Thinking: ${entry.thinkingLevel}`);
      break;
  }
}
```

## SessionManager API
## SessionManager API

Key methods for working with sessions programmatically.
以编程方式处理会话的关键方法。

### Static Creation Methods
### 静态创建方法
- `SessionManager.create(cwd, sessionDir?)` - New session
- `SessionManager.create(cwd, sessionDir?)` - 新会话
- `SessionManager.open(path, sessionDir?)` - Open existing session file
- `SessionManager.open(path, sessionDir?)` - 打开现有会话文件
- `SessionManager.continueRecent(cwd, sessionDir?)` - Continue most recent or create new
- `SessionManager.continueRecent(cwd, sessionDir?)` - 继续最近的会话或创建新会话
- `SessionManager.inMemory(cwd?)` - No file persistence
- `SessionManager.inMemory(cwd?)` - 不持久化到文件
- `SessionManager.forkFrom(sourcePath, targetCwd, sessionDir?)` - Fork session from another project
- `SessionManager.forkFrom(sourcePath, targetCwd, sessionDir?)` - 从另一个项目分叉会话

### Static Listing Methods
### 静态列举方法
- `SessionManager.list(cwd, sessionDir?, onProgress?)` - List sessions for a directory
- `SessionManager.list(cwd, sessionDir?, onProgress?)` - 列出某目录的会话
- `SessionManager.listAll(onProgress?)` - List all sessions across all projects
- `SessionManager.listAll(onProgress?)` - 列出所有项目的全部会话

### Instance Methods - Session Management
### 实例方法 - 会话管理
- `newSession(options?)` - Start a new session (options: `{ parentSession?: string }`)
- `newSession(options?)` - 开始新会话（options：`{ parentSession?: string }`）
- `setSessionFile(path)` - Switch to a different session file
- `setSessionFile(path)` - 切换到不同的会话文件
- `createBranchedSession(leafId)` - Extract branch to new session file
- `createBranchedSession(leafId)` - 把分支提取到新会话文件

### Instance Methods - Appending (all return entry ID)
### 实例方法 - 追加（全部返回条目 ID）
- `appendMessage(message)` - Add message
- `appendMessage(message)` - 添加消息
- `appendThinkingLevelChange(level)` - Record thinking change
- `appendThinkingLevelChange(level)` - 记录思考等级变更
- `appendModelChange(provider, modelId)` - Record model change
- `appendModelChange(provider, modelId)` - 记录模型变更
- `appendCompaction(summary, firstKeptEntryId, tokensBefore, details?, fromHook?)` - Add compaction
- `appendCompaction(summary, firstKeptEntryId, tokensBefore, details?, fromHook?)` - 添加压缩
- `appendCustomEntry(customType, data?)` - Extension state (not in context)
- `appendCustomEntry(customType, data?)` - 扩展状态（不在上下文中）
- `appendSessionInfo(name)` - Set session display name
- `appendSessionInfo(name)` - 设置会话显示名称
- `appendCustomMessageEntry(customType, content, display, details?)` - Extension message (in context)
- `appendCustomMessageEntry(customType, content, display, details?)` - 扩展消息（在上下文中）
- `appendLabelChange(targetId, label)` - Set/clear label
- `appendLabelChange(targetId, label)` - 设置/清除标签

### Instance Methods - Tree Navigation
### 实例方法 - 树导航
- `getLeafId()` - Current position
- `getLeafId()` - 当前位置
- `getLeafEntry()` - Get current leaf entry
- `getLeafEntry()` - 获取当前叶子条目
- `getEntry(id)` - Get entry by ID
- `getEntry(id)` - 按 ID 获取条目
- `getBranch(fromId?)` - Walk from entry to root
- `getBranch(fromId?)` - 从条目走向根
- `getTree()` - Get full tree structure
- `getTree()` - 获取完整树结构
- `getChildren(parentId)` - Get direct children
- `getChildren(parentId)` - 获取直接子节点
- `getLabel(id)` - Get label for entry
- `getLabel(id)` - 获取条目标签
- `branch(entryId)` - Move leaf to earlier entry
- `branch(entryId)` - 把叶子移动到较早条目
- `resetLeaf()` - Reset leaf to null (before any entries)
- `resetLeaf()` - 把叶子重置为 null（所有条目之前）
- `branchWithSummary(entryId, summary, details?, fromHook?)` - Branch with context summary
- `branchWithSummary(entryId, summary, details?, fromHook?)` - 带上下文摘要分支

### Instance Methods - Context & Info
### 实例方法 - 上下文与信息
- `buildContextEntries()` - Get active branch entries with compaction applied
- `buildContextEntries()` - 获取应用压缩后的活动分支条目
- `buildSessionContext()` - Get messages, thinkingLevel, and model for LLM
- `buildSessionContext()` - 获取给 LLM 的消息、思考等级和模型
- `getEntries()` - All entries (excluding header)
- `getEntries()` - 全部条目（不含头部）
- `getHeader()` - Session header metadata
- `getHeader()` - 会话头部元数据
- `getSessionName()` - Get display name from latest session_info entry
- `getSessionName()` - 从最近的 session_info 条目获取显示名称
- `getCwd()` - Working directory
- `getCwd()` - 工作目录
- `getSessionDir()` - Session storage directory
- `getSessionDir()` - 会话存储目录
- `getSessionId()` - Session UUID
- `getSessionId()` - 会话 UUID
- `getSessionFile()` - Session file path (undefined for in-memory)
- `getSessionFile()` - 会话文件路径（内存会话为 undefined）
- `isPersisted()` - Whether session is saved to disk
- `isPersisted()` - 会话是否已保存到磁盘
