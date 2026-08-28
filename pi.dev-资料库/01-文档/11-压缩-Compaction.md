> 📄 来源 Source: https://pi.dev/docs/latest/compaction
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# Compaction & Branch Summarization
# 压缩与分支摘要

LLMs have limited context windows. When conversations grow too long, Pi uses compaction to summarize older content while preserving recent work. This page covers both auto-compaction and branch summarization.
LLM 的上下文窗口有限。当对话变得过长时，Pi 使用压缩（compaction）来摘要较旧的内容，同时保留最近的工作。本页面介绍自动压缩与分支摘要。

**Source files** ([pi-mono](https://github.com/earendil-works/pi-mono)):
**源文件**（[pi-mono](https://github.com/earendil-works/pi-mono)）：
- [`packages/coding-agent/src/core/compaction/compaction.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/compaction.ts) - Auto-compaction logic
- [`packages/coding-agent/src/core/compaction/compaction.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/compaction.ts) - 自动压缩逻辑
- [`packages/coding-agent/src/core/compaction/branch-summarization.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts) - Branch summarization
- [`packages/coding-agent/src/core/compaction/branch-summarization.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts) - 分支摘要
- [`packages/coding-agent/src/core/compaction/utils.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/utils.ts) - Shared utilities (file tracking, serialization)
- [`packages/coding-agent/src/core/compaction/utils.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/utils.ts) - 共享工具（文件跟踪、序列化）
- [`packages/coding-agent/src/core/session-manager.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/session-manager.ts) - Entry types (`CompactionEntry`, `BranchSummaryEntry`)
- [`packages/coding-agent/src/core/session-manager.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/session-manager.ts) - 条目类型（`CompactionEntry`、`BranchSummaryEntry`）
- [`packages/coding-agent/src/core/extensions/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/extensions/types.ts) - Extension event types
- [`packages/coding-agent/src/core/extensions/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/extensions/types.ts) - 扩展事件类型

For TypeScript definitions in your project, inspect `node_modules/@earendil-works/pi-coding-agent/dist/`.
要在你的项目中查看 TypeScript 定义，请检查 `node_modules/@earendil-works/pi-coding-agent/dist/`。

## Overview
## 概览

Pi has two summarization mechanisms:
Pi 有两种摘要机制：

| Mechanism | Trigger | Purpose |
|-----------|---------|---------|
| Compaction | Context exceeds threshold, or `/compact` | Summarize old messages to free up context |
| Branch summarization | `/tree` navigation | Preserve context when switching branches |

| 机制 | 触发条件 | 目的 |
|-----------|---------|---------|
| 压缩（Compaction） | 上下文超过阈值，或使用 `/compact` | 摘要旧消息以释放上下文 |
| 分支摘要 | `/tree` 导航 | 切换分支时保留上下文 |


Both use the same structured summary format and track file operations cumulatively. Compaction and branch-summary requests use fresh routing session IDs and, where supported by the provider, disable prompt-cache writes because these one-off prompts are unlikely to be reused.
两者使用相同的结构化摘要格式，并累计跟踪文件操作。压缩和分支摘要请求使用全新的路由会话 ID，并且在提供商支持的情况下禁用提示词缓存写入，因为这些一次性提示词不太可能被复用。

## Compaction
## 压缩

### When It Triggers
### 何时触发

Auto-compaction triggers when:
自动压缩在以下情况触发：

```
contextTokens > contextWindow - reserveTokens
```

By default, `reserveTokens` is 16384 tokens (configurable in `~/.pi/agent/settings.json` or `<project-dir>/.pi/settings.json`). This leaves room for the LLM's response.
默认情况下，`reserveTokens` 为 16384 个 token（可在 `~/.pi/agent/settings.json` 或 `<project-dir>/.pi/settings.json` 中配置）。这为 LLM 的响应留出了空间。

You can also trigger manually with `/compact [instructions]`, where optional instructions focus the summary.
你也可以用 `/compact [instructions]` 手动触发，其中可选的 instructions 用于聚焦摘要。

### How It Works
### 工作原理

1. **Find cut point**: Walk backwards from newest message, accumulating token estimates until `keepRecentTokens` (default 20k, configurable in `~/.pi/agent/settings.json` or `<project-dir>/.pi/settings.json`) is reached
1. **寻找切点**：从最新消息向前回溯，累计 token 估算值，直到达到 `keepRecentTokens`（默认 20k，可在 `~/.pi/agent/settings.json` 或 `<project-dir>/.pi/settings.json` 中配置）
2. **Extract messages**: Collect messages from the previous kept boundary (or session start) up to the cut point
2. **提取消息**：收集从上一个保留边界（或会话开始）到切点之间的消息
3. **Generate summary**: Call LLM to summarize with structured format, passing the previous summary as iterative context when present
3. **生成摘要**：调用 LLM 以结构化格式生成摘要，若存在上一个摘要则作为迭代上下文传入
4. **Append entry**: Save `CompactionEntry` with summary and `firstKeptEntryId`
4. **追加条目**：保存带有摘要和 `firstKeptEntryId` 的 `CompactionEntry`
5. **Rebuilds context**: Session rebuilds the context for the next request, using summary + messages from `firstKeptEntryId` onwards
5. **重建上下文**：会话为下一个请求重建上下文，使用摘要加上从 `firstKeptEntryId` 开始的消息

```
Before compaction:

  entry:  0     1     2     3      4     5     6      7      8     9
        ┌─────┬─────┬─────┬──────┬─────┬─────┬──────┬──────┬─────┬─────┐
        │ hdr │ usr │ ass │ tool │ usr │ ass │ tool │ tool │ ass │ tool│
        └─────┴─────┴─────┴──────┴─────┴─────┴──────┴──────┴─────┴─────┘
                └────────┬───────┘ └──────────────┬──────────────┘
               messagesToSummarize            kept messages
                                   ↑
                          firstKeptEntryId (entry 4)

After compaction (new entry appended):

  entry:  0     1     2     3      4     5     6      7      8     9     10
        ┌─────┬─────┬─────┬──────┬─────┬─────┬──────┬──────┬─────┬─────┬─────┐
        │ hdr │ usr │ ass │ tool │ usr │ ass │ tool │ tool │ ass │ tool│ cmp │
        └─────┴─────┴─────┴──────┴─────┴─────┴──────┴──────┴─────┴─────┴─────┘
               └──────────┬──────┘ └──────────────────────┬───────────────────┘
                 not sent to LLM                    sent to LLM
                                                         ↑
                                              starts from firstKeptEntryId

What the LLM sees:

  ┌────────┬─────────┬─────┬─────┬──────┬──────┬─────┬──────┐
  │ system │ summary │ usr │ ass │ tool │ tool │ ass │ tool │
  └────────┴─────────┴─────┴─────┴──────┴──────┴─────┴──────┘
       ↑         ↑      └─────────────────┬────────────────┘
    prompt   from cmp          messages from firstKeptEntryId
```

On repeated compactions, the summarized span starts at the previous compaction's kept boundary (`firstKeptEntryId`), not at the compaction entry itself, falling back to the entry after the previous compaction if that kept entry cannot be found in the path. This preserves messages that survived the earlier compaction by including them in the next summarization pass as well. Pi also recalculates `tokensBefore` from the rebuilt session context before writing the new `CompactionEntry`, so the token count reflects the actual pre-compaction context being replaced.
在重复压缩时，被摘要的范围从上一次压缩的保留边界（`firstKeptEntryId`）开始，而不是从压缩条目本身开始；如果在路径中找不到那个被保留的条目，则回退到上一压缩条目之后的条目。这样，上一轮压缩后幸存的消息也会被纳入下一轮摘要，从而得以保留。Pi 还会在写入新的 `CompactionEntry` 之前，从重建的会话上下文重新计算 `tokensBefore`，因此 token 数反映的是被替换的实际压缩前上下文。

### Split Turns
### 拆分轮次

A "turn" starts with a user message and includes all assistant responses and tool calls until the next user message. Normally, compaction cuts at turn boundaries.
一个"轮次（turn）"以用户消息开始，包括所有助手响应和工具调用，直到下一条用户消息。通常，压缩在轮次边界处切割。

When a single turn exceeds `keepRecentTokens`, the cut point lands mid-turn at an assistant message. This is a "split turn":
当单个轮次超过 `keepRecentTokens` 时，切点会落在轮次中间的助手消息上。这就是"拆分轮次"（split turn）：

```
Split turn (one huge turn exceeds budget):

  entry:  0     1     2      3     4      5      6     7      8
        ┌─────┬─────┬─────┬──────┬─────┬──────┬──────┬─────┬──────┐
        │ hdr │ usr │ ass │ tool │ ass │ tool │ tool │ ass │ tool │
        └─────┴─────┴─────┴──────┴─────┴──────┴──────┴─────┴──────┘
                ↑                                     ↑
         turnStartIndex = 1                  firstKeptEntryId = 7
                │                                     │
                └──── turnPrefixMessages (1-6) ───────┘
                                                      └── kept (7-8)

  isSplitTurn = true
  messagesToSummarize = []  (no complete turns before)
  turnPrefixMessages = [usr, ass, tool, ass, tool, tool]
```

For split turns, Pi generates two summaries and merges them:
对于拆分轮次，Pi 会生成两个摘要并将它们合并：
1. **History summary**: Previous context (if any)
1. **历史摘要**：之前的上下文（如果有）
2. **Turn prefix summary**: The early part of the split turn
2. **轮次前缀摘要**：拆分轮次的早期部分

### Cut Point Rules
### 切点规则

Valid cut points are:
有效切点为：
- User messages
- 用户消息
- Assistant messages
- 助手消息
- BashExecution messages
- BashExecution 消息
- Custom messages (custom_message, branch_summary)
- 自定义消息（custom_message、branch_summary）

Never cut at tool results (they must stay with their tool call).
绝不在工具结果处切割（它们必须与其工具调用保持在一起）。

### CompactionEntry Structure
### CompactionEntry 结构

Defined in [`session-manager.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/session-manager.ts):
定义于 [`session-manager.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/session-manager.ts)：

```typescript
interface CompactionEntry<T = unknown> {
  type: "compaction";
  id: string;
  parentId: string;
  timestamp: number;
  summary: string;
  firstKeptEntryId: string;
  tokensBefore: number;
  usage?: Usage;       // LLM usage that generated the summary
  fromHook?: boolean;  // true if provided by extension (legacy field name)
  details?: T;         // implementation-specific data
}

// Default compaction uses this for details (from compaction.ts):
interface CompactionDetails {
  readFiles: string[];
  modifiedFiles: string[];
}
```

Extensions can store any JSON-serializable data in `details`. The default compaction tracks file operations, but custom extension implementations can use their own structure. Generated and extension-provided summaries store their LLM `usage` when available so session totals include summarization work.
扩展可以在 `details` 中存储任何可 JSON 序列化的数据。默认压缩会跟踪文件操作，但自定义扩展实现可以使用自己的结构。生成的和扩展提供的摘要会在可用时存储其 LLM `usage`，因此会话总计会包含摘要工作。

See [`prepareCompaction()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/compaction.ts) and [`compact()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/compaction.ts) for the implementation. For direct programmatic summarization, `generateSummary()` returns the summary text and `generateSummaryWithUsage()` returns `{ text, usage }`.
实现参见 [`prepareCompaction()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/compaction.ts) 和 [`compact()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/compaction.ts)。对于直接的程序化摘要，`generateSummary()` 返回摘要文本，`generateSummaryWithUsage()` 返回 `{ text, usage }`。

## Branch Summarization
## 分支摘要

### When It Triggers
### 何时触发

When you use `/tree` to navigate to a different branch, Pi offers to summarize the work you're leaving. This injects context from the left branch into the new branch.
当你使用 `/tree` 导航到另一个分支时，Pi 会提议摘要你正在离开的工作。这会把离开分支的上下文注入新分支。

### How It Works
### 工作原理

1. **Find common ancestor**: Deepest node shared by old and new positions
1. **寻找公共祖先**：新旧位置共享的最深节点
2. **Collect entries**: Walk from old leaf back to common ancestor
2. **收集条目**：从旧叶子回溯到公共祖先
3. **Prepare with budget**: Include messages up to token budget (newest first)
3. **按预算准备**：按 token 预算纳入消息（最新的优先）
4. **Generate summary**: Call LLM with structured format
4. **生成摘要**：以结构化格式调用 LLM
5. **Append entry**: Save `BranchSummaryEntry` at navigation point
5. **追加条目**：在导航点保存 `BranchSummaryEntry`

```
Tree before navigation:

         ┌─ B ─ C ─ D (old leaf, being abandoned)
    A ───┤
         └─ E ─ F (target)

Common ancestor: A
Entries to summarize: B, C, D

After navigation with summary:

         ┌─ B ─ C ─ D
    A ───┤
         └─ E ─ F ─ [summary of B,C,D] (new leaf)
```

### Cumulative File Tracking
### 累计文件跟踪

Both compaction and branch summarization track files cumulatively. When generating a summary, pi extracts file operations from:
压缩和分支摘要都会累计跟踪文件。生成摘要时，pi 从以下位置提取文件操作：
- Tool calls in the messages being summarized
- 被摘要消息中的工具调用
- Previous compaction or branch summary `details` (if any)
- 之前的压缩或分支摘要的 `details`（如果有）

This means file tracking accumulates across multiple compactions or nested branch summaries, preserving the full history of read and modified files.
这意味着文件跟踪会跨多次压缩或嵌套分支摘要累积，保留读过和修改过文件的完整历史。

### BranchSummaryEntry Structure
### BranchSummaryEntry 结构

Defined in [`session-manager.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/session-manager.ts):
定义于 [`session-manager.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/session-manager.ts)：

```typescript
interface BranchSummaryEntry<T = unknown> {
  type: "branch_summary";
  id: string;
  parentId: string;
  timestamp: number;
  summary: string;
  fromId: string;      // Entry we navigated from
  usage?: Usage;       // LLM usage that generated the summary
  fromHook?: boolean;  // true if provided by extension (legacy field name)
  details?: T;         // implementation-specific data
}

// Default branch summarization uses this for details (from branch-summarization.ts):
interface BranchSummaryDetails {
  readFiles: string[];
  modifiedFiles: string[];
}
```

Same as compaction, extensions can store custom data in `details`.
与压缩一样，扩展可以在 `details` 中存储自定义数据。

See [`collectEntriesForBranchSummary()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts), [`prepareBranchEntries()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts), and [`generateBranchSummary()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts) for the implementation.
实现参见 [`collectEntriesForBranchSummary()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts)、[`prepareBranchEntries()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts) 和 [`generateBranchSummary()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/branch-summarization.ts)。

## Summary Format
## 摘要格式

Both compaction and branch summarization use the same structured format:
压缩和分支摘要使用相同的结构化格式：

```markdown
## Goal
[What the user is trying to accomplish]

## Constraints & Preferences
- [Requirements mentioned by user]

## Progress
### Done
- [x] [Completed tasks]

### In Progress
- [ ] [Current work]

### Blocked
- [Issues, if any]

## Key Decisions
- **[Decision]**: [Rationale]

## Next Steps
1. [What should happen next]

## Critical Context
- [Data needed to continue]

<read-files>
path/to/file1.ts
path/to/file2.ts
</read-files>

<modified-files>
path/to/changed.ts
</modified-files>
```

### Message Serialization
### 消息序列化

Before summarization, messages are serialized to text via [`serializeConversation()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/utils.ts):
在摘要之前，消息会通过 [`serializeConversation()`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/compaction/utils.ts) 序列化为文本：

```
[User]: What they said
[Assistant thinking]: Internal reasoning
[Assistant]: Response text
[Assistant tool calls]: read(path="foo.ts"); edit(path="bar.ts", ...)
[Tool result]: Output from tool
```

This prevents the model from treating it as a conversation to continue.
这可以防止模型把它当作一段需要继续的对话。

Tool results are truncated to 2000 characters during serialization. Content beyond that limit is replaced with a marker indicating how many characters were truncated. This keeps summarization requests within reasonable token budgets, since tool results (especially from `read` and `bash`) are typically the largest contributors to context size.
工具结果在序列化期间被截断为 2000 个字符。超出该限制的内容会被替换为一个标记，说明截断了多少字符。这让摘要请求保持在合理的 token 预算内，因为工具结果（尤其是 `read` 和 `bash` 的结果）通常是上下文大小的最大来源。

## Custom Summarization via Extensions
## 通过扩展自定义摘要

Extensions can intercept and customize both compaction and branch summarization. See [`extensions/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/extensions/types.ts) for event type definitions.
扩展可以拦截并自定义压缩与分支摘要。事件类型定义参见 [`extensions/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/extensions/types.ts)。

### session_before_compact
### session_before_compact

Fired before auto-compaction or `/compact`. Can cancel or provide custom summary. See `SessionBeforeCompactEvent` and `CompactionPreparation` in the types file.
在自动压缩或 `/compact` 之前触发。可以取消或提供自定义摘要。`SessionBeforeCompactEvent` 和 `CompactionPreparation` 参见类型定义文件。

```typescript
pi.on("session_before_compact", async (event, ctx) => {
  const { preparation, branchEntries, customInstructions, reason, willRetry, signal } = event;

  // preparation.messagesToSummarize - messages to summarize
  // preparation.turnPrefixMessages - split turn prefix (if isSplitTurn)
  // preparation.previousSummary - previous compaction summary
  // preparation.fileOps - extracted file operations
  // preparation.tokensBefore - context tokens before compaction
  // preparation.firstKeptEntryId - where kept messages start
  // preparation.settings - compaction settings

  // branchEntries - all entries on current branch (for custom state)
  // reason - "manual" (/compact), "threshold", or "overflow"
  // willRetry - whether the aborted turn is retried after compaction (overflow recovery)
  // signal - AbortSignal (pass to LLM calls)

  // Cancel:
  return { cancel: true };

  // Custom summary:
  return {
    compaction: {
      summary: "Your summary...",
      firstKeptEntryId: preparation.firstKeptEntryId,
      tokensBefore: preparation.tokensBefore,
      // usage: summaryResponse.usage, // Optional; included in session totals
      details: { /* custom data */ },
    }
  };
});
```

#### Converting Messages to Text
#### 将消息转换为文本

To generate a summary with your own model, convert messages to text using `serializeConversation`:
要用你自己的模型生成摘要，请使用 `serializeConversation` 将消息转换为文本：

```typescript
import { convertToLlm, serializeConversation } from "@earendil-works/pi-coding-agent";

pi.on("session_before_compact", async (event, ctx) => {
  const { preparation } = event;
  
  // Convert AgentMessage[] to Message[], then serialize to text
  const conversationText = serializeConversation(
    convertToLlm(preparation.messagesToSummarize)
  );
  // Returns:
  // [User]: message text
  // [Assistant thinking]: thinking content
  // [Assistant]: response text
  // [Assistant tool calls]: read(path="..."); bash(command="...")
  // [Tool result]: output text

  // Now send to your model for summarization
  const { summary, usage } = await myModel.summarize(conversationText);
  
  return {
    compaction: {
      summary,
      firstKeptEntryId: preparation.firstKeptEntryId,
      tokensBefore: preparation.tokensBefore,
      usage,
    }
  };
});
```

See [custom-compaction.ts](../examples/extensions/custom-compaction.ts) for a complete example using a different model.
使用不同模型的完整示例参见 [custom-compaction.ts](../examples/extensions/custom-compaction.ts)。

### session_compact_failed
### session_compact_failed

Fired when manual or automatic compaction fails or is aborted. This is useful for telemetry extensions that need to pair `session_before_compact` attempts with terminal outcomes.
在手动或自动压缩失败或中止时触发。这对于需要把 `session_before_compact` 尝试与最终结果配对的遥测扩展很有用。

```typescript
pi.on("session_compact_failed", async (event, ctx) => {
  const { reason, errorMessage, aborted, willRetry, fromExtension } = event;
  // reason - "manual" (/compact), "threshold", or "overflow"
  // errorMessage - present for non-abort failures
  // aborted - true for cancelled/aborted compactions
  // willRetry - whether the aborted turn would have retried after compaction
  // fromExtension - whether extension-provided compaction content was being used
});
```

### session_before_tree
### session_before_tree

Fired before `/tree` navigation. Always fires regardless of whether user chose to summarize. Can cancel navigation or provide custom summary.
在 `/tree` 导航之前触发。无论用户是否选择摘要都会触发。可以取消导航或提供自定义摘要。

```typescript
pi.on("session_before_tree", async (event, ctx) => {
  const { preparation, signal } = event;

  // preparation.targetId - where we're navigating to
  // preparation.oldLeafId - current position (being abandoned)
  // preparation.commonAncestorId - shared ancestor
  // preparation.entriesToSummarize - entries that would be summarized
  // preparation.userWantsSummary - whether user chose to summarize

  // Cancel navigation entirely:
  return { cancel: true };

  // Provide custom summary (only used if userWantsSummary is true):
  if (preparation.userWantsSummary) {
    return {
      summary: {
        summary: "Your summary...",
        // usage: summaryResponse.usage, // Optional; included in session totals
        details: { /* custom data */ },
      }
    };
  }
});
```

See `SessionBeforeTreeEvent` and `TreePreparation` in the types file.
类型定义参见类型文件中的 `SessionBeforeTreeEvent` 和 `TreePreparation`。

## Settings
## 设置

Configure compaction in `~/.pi/agent/settings.json` or `<project-dir>/.pi/settings.json`:
在 `~/.pi/agent/settings.json` 或 `<project-dir>/.pi/settings.json` 中配置压缩：

```json
{
  "compaction": {
    "enabled": true,
    "reserveTokens": 16384,
    "keepRecentTokens": 20000
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Enable auto-compaction |
| `reserveTokens` | `16384` | Tokens to reserve for LLM response |
| `keepRecentTokens` | `20000` | Recent tokens to keep (not summarized) |

| 设置 | 默认值 | 描述 |
|---------|---------|-------------|
| `enabled` | `true` | 启用自动压缩 |
| `reserveTokens` | `16384` | 为 LLM 响应保留的 token 数 |
| `keepRecentTokens` | `20000` | 保留（不摘要）的最近 token 数 |


Disable auto-compaction with `"enabled": false`. You can still compact manually with `/compact`.
将 `"enabled"` 设为 `false` 可禁用自动压缩。你仍可以用 `/compact` 手动压缩。
