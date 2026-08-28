> 📄 来源 Source: https://pi.dev/docs/latest/skills
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

> pi can create skills. Ask it to build one for your use case.
> pi 可以创建技能。让它为你的用例构建一个吧。

# Skills
# 技能

Skills are self-contained capability packages that the agent loads on-demand. A skill provides specialized workflows, setup instructions, helper scripts, and reference documentation for specific tasks.
技能是代理按需加载的自包含能力包。技能为特定任务提供专门的工作流、设置说明、辅助脚本和参考文档。

Pi implements the [Agent Skills standard](https://agentskills.io/specification), warning about most violations but remaining lenient. Pi allows skill names to differ from their parent directory even though the standard disallows it; that rule is suboptimal for shared skill directories used across multiple agent harnesses.
Pi 实现了 [Agent Skills 标准](https://agentskills.io/specification)，对大多数违规会发出警告，但保持宽容。Pi 允许技能名称与其父目录不同，尽管标准不允许这样做；这条规则对于在多个代理框架之间共享的技能目录来说并不理想。

## Table of Contents
## 目录

- [Locations](#locations)
- [位置](#locations)
- [How Skills Work](#how-skills-work)
- [技能如何工作](#how-skills-work)
- [Skill Commands](#skill-commands)
- [技能命令](#skill-commands)
- [Skill Structure](#skill-structure)
- [技能结构](#skill-structure)
- [Frontmatter](#frontmatter)
- [Frontmatter](#frontmatter)
- [Validation](#validation)
- [校验](#validation)
- [Example](#example)
- [示例](#example)
- [Skill Repositories](#skill-repositories)
- [技能仓库](#skill-repositories)

## Locations
## 位置

> **Security:** Skills can instruct the model to perform any action and may include executable code the model invokes. Review skill content before use.
> **安全提示：** 技能可以指示模型执行任何操作，并可能包含模型会调用的可执行代码。使用前请审查技能内容。

Pi loads skills from:
Pi 从以下位置加载技能：

- Global:
- 全局：
  - `~/.pi/agent/skills/`
  - `~/.pi/agent/skills/`
  - `~/.agents/skills/`
  - `~/.agents/skills/`
- Project (only after the project is trusted):
- 项目（仅在项目受信任后）：
  - `.pi/skills/`
  - `.pi/skills/`
  - `.agents/skills/` in `cwd` and ancestor directories (up to git repo root, or filesystem root when not in a repo)
  - `cwd` 及祖先目录中的 `.agents/skills/`（直到 git 仓库根目录；不在仓库中时则为文件系统根目录）
- Packages: `skills/` directories or `pi.skills` entries in `package.json`
- 包：`skills/` 目录或 `package.json` 中的 `pi.skills` 条目
- Settings: `skills` array with files or directories
- 设置：包含文件或目录的 `skills` 数组
- CLI: `--skill <path>` (repeatable, additive even with `--no-skills`)
- CLI：`--skill <path>`（可重复，即使有 `--no-skills` 也追加生效）

Discovery rules:
发现规则：
- In `~/.pi/agent/skills/` and `.pi/skills/`, direct root `.md` files are discovered as individual skills when they have valid skill frontmatter with a non-empty `description`
- 在 `~/.pi/agent/skills/` 和 `.pi/skills/` 中，当根目录下的 `.md` 文件具有带非空 `description` 的有效技能 frontmatter 时，会被发现为独立技能
- In all skill locations, directories containing `SKILL.md` are discovered recursively
- 在所有技能位置中，包含 `SKILL.md` 的目录会被递归发现
- In `~/.agents/skills/` and project `.agents/skills/`, root `.md` files are ignored, but nested `.md` files in grouping folders are discovered when they declare skill frontmatter
- 在 `~/.agents/skills/` 和项目 `.agents/skills/` 中，根目录的 `.md` 文件会被忽略，但分组文件夹中声明了技能 frontmatter 的嵌套 `.md` 文件会被发现
- Root Markdown files other than `SKILL.md` that do not look like skills are ignored silently
- 除 `SKILL.md` 之外、看起来不像技能的根目录 Markdown 文件会被静默忽略

Disable discovery with `--no-skills` (explicit `--skill` paths still load).
使用 `--no-skills` 禁用发现（显式的 `--skill` 路径仍会加载）。

### Using Skills from Other Harnesses
### 使用来自其他框架的技能

To use skills from Claude Code or OpenAI Codex, add their directories to settings:
要使用 Claude Code 或 OpenAI Codex 的技能，请把它们的目录加入设置：

```json
{
  "skills": [
    "~/.claude/skills",
    "~/.codex/skills"
  ]
}
```

For project-level Claude Code skills, add to `.pi/settings.json`:
对于项目级 Claude Code 技能，请添加到 `.pi/settings.json`：

```json
{
  "skills": ["../.claude/skills"]
}
```

## How Skills Work
## 技能如何工作

1. At startup, pi scans skill locations and extracts names and descriptions
1. 启动时，pi 扫描技能位置并提取名称和描述
2. The system prompt includes available skills in XML format per the [specification](https://agentskills.io/integrate-skills)
2. 系统提示词按[规范](https://agentskills.io/integrate-skills)以 XML 格式包含可用技能
3. When a task matches, the agent uses `read` to load the full SKILL.md (models don't always do this; use prompting or `/skill:name` to force it)
3. 当任务匹配时，代理使用 `read` 加载完整的 SKILL.md（模型并不总是这样做；请用提示词或 `/skill:name` 强制执行）
4. The agent follows the instructions, using relative paths to reference scripts and assets
4. 代理遵循指令，使用相对路径引用脚本和资源

This is progressive disclosure: only descriptions are always in context, full instructions load on-demand.
这就是渐进式披露（progressive disclosure）：上下文中始终只有描述，完整指令按需加载。

## Skill Commands
## 技能命令

Skills register as `/skill:name` commands:
技能注册为 `/skill:name` 命令：

```bash
/skill:brave-search           # Load and execute the skill
/skill:pdf-tools extract      # Load skill with arguments
```

Arguments after the command are appended to the skill content as `User: <args>`.
命令后的参数会以 `User: <args>` 的形式附加到技能内容中。

Toggle skill commands via `/settings` in interactive mode or in `settings.json`:
在交互模式中通过 `/settings` 或在 `settings.json` 中切换技能命令：

```json
{
  "enableSkillCommands": true
}
```

## Skill Structure
## 技能结构

A skill is a directory with a `SKILL.md` file. Everything else is freeform.
技能是一个包含 `SKILL.md` 文件的目录。其余内容都是自由格式。

```
my-skill/
├── SKILL.md              # Required: frontmatter + instructions
├── scripts/              # Helper scripts
│   └── process.sh
├── references/           # Detailed docs loaded on-demand
│   └── api-reference.md
└── assets/
    └── template.json
```

### SKILL.md Format
### SKILL.md 格式

````markdown
---
name: my-skill
description: What this skill does and when to use it. Be specific.
---

# My Skill

## Setup

Run once before first use:
```bash
cd /path/to/skill && npm install
```

## Usage

```bash
./scripts/process.sh <input>
```
````

Use relative paths from the skill directory:
使用技能目录中的相对路径：

```markdown
See [the reference guide](references/REFERENCE.md) for details.
```

## Frontmatter
## Frontmatter

Per the [Agent Skills specification](https://agentskills.io/specification#frontmatter-required):
依据 [Agent Skills 规范](https://agentskills.io/specification#frontmatter-required)：

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Max 64 chars. Lowercase a-z, 0-9, hyphens. Unlike the standard, Pi does not require this to match the parent directory because that standard requirement is suboptimal for shared skill directories. |
| `description` | Yes | Max 1024 chars. What the skill does and when to use it. |
| `license` | No | License name or reference to bundled file. |
| `compatibility` | No | Max 500 chars. Environment requirements. |
| `metadata` | No | Arbitrary key-value mapping. |
| `allowed-tools` | No | Space-delimited list of pre-approved tools (experimental). |
| `disable-model-invocation` | No | When `true`, skill is hidden from system prompt. Users must use `/skill:name`. |

| 字段 | 必需 | 描述 |
|-------|----------|-------------|
| `name` | 是 | 最多 64 个字符。小写 a-z、0-9、连字符。与标准不同，Pi 不要求它与父目录一致，因为该标准要求对共享技能目录并不理想。 |
| `description` | 是 | 最多 1024 个字符。技能做什么以及何时使用。 |
| `license` | 否 | 许可证名称或对捆绑文件的引用。 |
| `compatibility` | 否 | 最多 500 个字符。环境要求。 |
| `metadata` | 否 | 任意键值映射。 |
| `allowed-tools` | 否 | 预批准工具的空格分隔列表（实验性）。 |
| `disable-model-invocation` | 否 | 为 `true` 时，技能在系统提示词中隐藏。用户必须使用 `/skill:name`。 |


### Name Rules
### 名称规则

- 1-64 characters
- 1-64 个字符
- Lowercase letters, numbers, hyphens only
- 仅小写字母、数字和连字符
- No leading/trailing hyphens
- 开头/结尾不能是连字符
- No consecutive hyphens
- 不能有连续连字符
Pi does not require the name to match the parent directory. The Agent Skills standard does, but that requirement is suboptimal for shared skill directories used by multiple tools.
Pi 不要求名称与父目录一致。Agent Skills 标准有此要求，但该要求对多个工具共享的技能目录并不理想。

Valid: `pdf-processing`, `data-analysis`, `code-review`
有效：`pdf-processing`、`data-analysis`、`code-review`
Invalid: `PDF-Processing`, `-pdf`, `pdf--processing`
无效：`PDF-Processing`、`-pdf`、`pdf--processing`

### Description Best Practices
### 描述最佳实践

The description determines when the agent loads the skill. Be specific.
描述决定代理何时加载技能。请务必具体。

Good:
好的示例：
```yaml
description: Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents.
```

Poor:
差的示例：
```yaml
description: Helps with PDFs.
```

## Validation
## 校验

Pi validates skills against the Agent Skills standard. Most issues produce warnings but still load the skill:
Pi 根据 Agent Skills 标准校验技能。大多数问题产生警告但仍加载技能：

- Name exceeds 64 characters or contains invalid characters
- 名称超过 64 个字符或包含无效字符
- Name starts/ends with hyphen or has consecutive hyphens
- 名称以连字符开头/结尾或有连续连字符
- Description exceeds 1024 characters
- 描述超过 1024 个字符

Unknown frontmatter fields are ignored.
未知的 frontmatter 字段会被忽略。

Declared skills with missing descriptions are not loaded. Malformed `SKILL.md` files and `SKILL.md` files without a description produce warnings and are not loaded. Other Markdown files without valid skill frontmatter are ignored.
缺少描述的已声明技能不会被加载。格式错误的 `SKILL.md` 文件和没有描述的 `SKILL.md` 文件会产生警告且不被加载。其他没有有效技能 frontmatter 的 Markdown 文件会被忽略。

Name collisions (same name from different locations) warn and keep the first skill found.
名称冲突（来自不同位置的同名技能）会警告并保留找到的第一个技能。

## Example
## 示例

```
brave-search/
├── SKILL.md
├── search.js
└── content.js
```

**SKILL.md:**
**SKILL.md：**
````markdown
---
name: brave-search
description: Web search and content extraction via Brave Search API. Use for searching documentation, facts, or any web content.
---

# Brave Search

## Setup

```bash
cd /path/to/brave-search && npm install
```

## Search

```bash
./search.js "query"              # Basic search
./search.js "query" --content    # Include page content
```

## Extract Page Content

```bash
./content.js https://example.com
```
````

## Skill Repositories
## 技能仓库

- [Anthropic Skills](https://github.com/anthropics/skills) - Document processing (docx, pdf, pptx, xlsx), web development
- [Anthropic Skills](https://github.com/anthropics/skills) - 文档处理（docx、pdf、pptx、xlsx）、Web 开发
- [Pi Skills](https://github.com/badlogic/pi-skills) - Web search, browser automation, Google APIs, transcription
- [Pi Skills](https://github.com/badlogic/pi-skills) - 网页搜索、浏览器自动化、Google API、转录
