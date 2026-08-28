> 📄 来源 Source: https://pi.dev/docs/latest/json
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

# JSON Event Stream Mode
# JSON 事件流模式

```bash
pi --mode json "Your prompt"
```

Outputs all session events as JSON lines to stdout. Useful for integrating pi into other tools or custom UIs.
将所有会话事件以 JSON 行的形式输出到 stdout。用于把 pi 集成到其他工具或自定义 UI 中。

## Event Types
## 事件类型

Wire events use `JsonAgentSessionEvent`. It matches
线上（wire）事件使用 `JsonAgentSessionEvent`。它与
[`AgentSessionEvent`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/agent-session.ts)
[`AgentSessionEvent`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/agent-session.ts)
except that streaming message updates omit cumulative snapshots:
一致，区别在于流式消息更新会省略累积快照：

```typescript
type WithoutPartial<T> = T extends { partial: unknown } ? Omit<T, "partial"> : T;

type JsonAssistantMessageEvent<T> = T extends { type: "toolcall_start"; partial: unknown }
  ? WithoutPartial<T> & { id: string; toolName: string }
  : WithoutPartial<T>;

type JsonAgentSessionEvent =
  | Exclude<AgentSessionEvent, { type: "message_update" }>
  | {
      type: "message_update";
      usage: Usage;
      assistantMessageEvent: JsonAssistantMessageEvent<AssistantMessageEvent>;
    };
```

`queue_update` emits the full pending steering and follow-up queues whenever they change. `compaction_start` and `compaction_end` cover both manual and automatic compaction.
`queue_update` 在待处理的 steering 与 follow-up 队列发生变化时发出完整队列。`compaction_start` 和 `compaction_end` 同时覆盖手动与自动压缩。

Other base events come from
其他基础事件来自
[`AgentEvent`](https://github.com/earendil-works/pi-mono/blob/main/packages/agent/src/types.ts):
[`AgentEvent`](https://github.com/earendil-works/pi-mono/blob/main/packages/agent/src/types.ts)：

```typescript
type AgentEvent =
  // Agent lifecycle
  | { type: "agent_start" }
  | { type: "agent_end"; messages: AgentMessage[] }
  // Turn lifecycle
  | { type: "turn_start" }
  | { type: "turn_end"; message: AgentMessage; toolResults: ToolResultMessage[] }
  // Message lifecycle
  | { type: "message_start"; message: AgentMessage }
  | { type: "message_update"; message: AgentMessage; assistantMessageEvent: AssistantMessageEvent }
  | { type: "message_end"; message: AgentMessage }
  // Tool execution
  | { type: "tool_execution_start"; toolCallId: string; toolName: string; args: any }
  | { type: "tool_execution_update"; toolCallId: string; toolName: string; args: any; partialResult: any }
  | { type: "tool_execution_end"; toolCallId: string; toolName: string; result: any; isError: boolean };
```

## Message Types
## 消息类型

Base messages from [`packages/ai/src/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/types.ts#L134):
来自 [`packages/ai/src/types.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/ai/src/types.ts#L134) 的基础消息：
- `UserMessage` (line 134)
- `UserMessage`（第 134 行）
- `AssistantMessage` (line 140)
- `AssistantMessage`（第 140 行）
- `ToolResultMessage` (line 152)
- `ToolResultMessage`（第 152 行）

Extended messages from [`packages/coding-agent/src/core/messages.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/messages.ts#L29):
来自 [`packages/coding-agent/src/core/messages.ts`](https://github.com/earendil-works/pi-mono/blob/main/packages/coding-agent/src/core/messages.ts#L29) 的扩展消息：
- `BashExecutionMessage` (line 29)
- `BashExecutionMessage`（第 29 行）
- `CustomMessage` (line 46)
- `CustomMessage`（第 46 行）
- `BranchSummaryMessage` (line 55)
- `BranchSummaryMessage`（第 55 行）
- `CompactionSummaryMessage` (line 62)
- `CompactionSummaryMessage`（第 62 行）

## Output Format
## 输出格式

Each line is a JSON object. The first line is the session header:
每行是一个 JSON 对象。第一行是会话头：

```json
{"type":"session","version":3,"id":"uuid","timestamp":"...","cwd":"/path"}
```

Followed by events as they occur:
随后是随发生而输出的事件：

```json
{"type":"agent_start"}
{"type":"turn_start"}
{"type":"message_start","message":{"role":"assistant","content":[],...}}
{"type":"message_update","usage":{...},"assistantMessageEvent":{"type":"text_delta","contentIndex":0,"delta":"Hello"}}
{"type":"message_end","message":{...}}
{"type":"turn_end","message":{...},"toolResults":[]}
{"type":"agent_end","messages":[...]}
```

`message_update` records are delta-only. They omit both the cumulative `message` field and
`message_update` 记录只包含增量（delta）。它们同时省略了累积的 `message` 字段和
`assistantMessageEvent.partial` to keep stream size linear. The top-level `usage` field contains
`assistantMessageEvent.partial`，以保持流大小线性。顶层的 `usage` 字段包含
the latest cumulative provider-reported usage and may remain zero when a provider only reports
提供商报告的最新累计用量；当提供商只在完成时报告用量时，它可能保持为零。
usage at completion. Use `contentIndex` and `delta` to assemble live text, thinking, or tool-call
如需拼装实时文本、思考或工具调用参数，请使用 `contentIndex` 和 `delta`。
arguments if needed. A `toolcall_start` event also includes the constant-sized `id` and `toolName`
`toolcall_start` 事件还包含固定大小的 `id` 和 `toolName`
fields. `message_end` contains the final authoritative message.
字段。`message_end` 包含最终的权威消息。

## Example
## 示例

```bash
pi --mode json "List files" 2>/dev/null | jq -c 'select(.type == "message_end")'
```
