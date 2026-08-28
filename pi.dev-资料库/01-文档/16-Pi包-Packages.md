> 📄 来源 Source: https://pi.dev/docs/latest/packages
>
> 🌐 中英对照版：每行英文原文之后紧跟其中文翻译；代码块保持原样不翻译。
> Bilingual edition: each English line is followed by its Chinese translation. Code blocks are kept verbatim.

> pi can help you create pi packages. Ask it to bundle your extensions, skills, prompt templates, or themes.
> pi 可以帮你创建 pi 包。让它把你的扩展、技能、提示词模板或主题打包吧。

# Pi Packages
# Pi 包

Pi packages bundle extensions, skills, prompt templates, and themes so you can share them through npm or git. A package can declare resources in `package.json` under the `pi` key, or use conventional directories.
Pi 包把扩展、技能、提示词模板和主题打包在一起，便于通过 npm 或 git 分享。包可以在 `package.json` 的 `pi` 键下声明资源，或使用约定目录。

## Table of Contents
## 目录

- [Install and Manage](#install-and-manage)
- [安装与管理](#install-and-manage)
- [Package Sources](#package-sources)
- [包来源](#package-sources)
- [Creating a Pi Package](#creating-a-pi-package)
- [创建 Pi 包](#creating-a-pi-package)
- [Package Structure](#package-structure)
- [包结构](#package-structure)
- [Dependencies](#dependencies)
- [依赖](#dependencies)
- [Package Filtering](#package-filtering)
- [包过滤](#package-filtering)
- [Enable and Disable Resources](#enable-and-disable-resources)
- [启用与禁用资源](#enable-and-disable-resources)
- [Scope and Deduplication](#scope-and-deduplication)
- [作用域与去重](#scope-and-deduplication)

## Install and Manage
## 安装与管理

> **Security:** Pi packages run with full system access. Extensions execute arbitrary code, and skills can instruct the model to perform any action including running executables. Review source code before installing third-party packages.
> **安全提示：** Pi 包以完整系统权限运行。扩展执行任意代码，技能可以指示模型执行任何操作，包括运行可执行文件。安装第三方包前请审查源代码。

```bash
pi install npm:@foo/bar@1.0.0
pi install git:github.com/user/repo@v1
pi install https://github.com/user/repo  # raw URLs work too
pi install /absolute/path/to/package
pi install ./relative/path/to/package

pi remove npm:@foo/bar
pi list                     # show installed packages from settings
pi update                   # update pi only
pi update --all             # update pi, update packages, and reconcile pinned git refs
pi update --extensions      # update packages and reconcile pinned git refs only
pi update --models          # refresh model catalogs only
pi update --self            # update pi only
pi update --self --force    # reinstall pi even if current
pi update npm:@foo/bar      # update one package
pi update --extension npm:@foo/bar
```

These commands manage pi packages and `pi update` can update the pi CLI installation. For experimental installer-managed installations, `pi update` installs the exact checked version into a staged, lockfile-backed release and activates it only after verification, leaving the current release intact if the update fails. Managed installations do not support `--force`; rerun the installer to repair one. To uninstall pi itself, see [Quickstart](quickstart.md#uninstall).
这些命令管理 pi 包，`pi update` 还可以更新 pi CLI 安装。对于实验性的安装器托管安装，`pi update` 会把检查过的确切版本安装到一个由 lockfile 支持的暂存发布中，并只在验证通过后激活，更新失败时保持当前发布不变。托管安装不支持 `--force`；如需修复请重新运行安装器。要卸载 pi 本体，参见[快速开始](quickstart.md#uninstall)。

By default, `install` and `remove` write to user settings (`~/.pi/agent/settings.json`). Use `-l` to write to project settings (`.pi/settings.json`) instead. Project settings can be shared with your team, and pi installs any missing packages automatically on startup after the project is trusted.
默认情况下，`install` 和 `remove` 写入用户设置（`~/.pi/agent/settings.json`）。使用 `-l` 改为写入项目设置（`.pi/settings.json`）。项目设置可以与团队共享，并且在项目受信任后，pi 会在启动时自动安装任何缺失的包。

To try a package without installing it, use `--extension` or `-e`. This installs to a temporary directory for the current run only:
想在不安装的情况下试用包，请使用 `--extension` 或 `-e`。它会安装到临时目录，仅对当前运行有效：

```bash
pi -e npm:@foo/bar
pi -e git:github.com/user/repo
```

## Package Sources
## 包来源

Pi accepts three source types in settings and `pi install`.
Pi 在设置和 `pi install` 中接受三种来源类型。

### npm
### npm

```
npm:@scope/pkg@1.2.3
npm:pkg
```

- Versioned specs are pinned and skipped by package updates (`pi update --extensions`, `pi update --all`).
- 带版本号的规格会被固定（pin），包更新（`pi update --extensions`、`pi update --all`）会跳过它们。
- User installs go under `~/.pi/agent/npm/`.
- 用户安装位于 `~/.pi/agent/npm/` 下。
- Project installs go under `.pi/npm/`.
- 项目安装位于 `.pi/npm/` 下。
- Set `npmCommand` in `settings.json` to pin npm package lookup and install operations to a specific wrapper command such as `mise` or `asdf`.
- 在 `settings.json` 中设置 `npmCommand`，把 npm 包查找和安装操作固定到特定的包装命令，例如 `mise` 或 `asdf`。

Example:
示例：

```json
{
  "npmCommand": ["mise", "exec", "node@20", "--", "npm"]
}
```

### git
### git

```
git:github.com/user/repo@v1
git:git@github.com:user/repo@v1
https://github.com/user/repo@v1
ssh://git@github.com/user/repo@v1
```

- Without `git:` prefix, only protocol URLs are accepted (`https://`, `http://`, `ssh://`, `git://`).
- 不带 `git:` 前缀时，只接受协议 URL（`https://`、`http://`、`ssh://`、`git://`）。
- With `git:` prefix, shorthand formats are accepted, including `github.com/user/repo` and `git@github.com:user/repo`.
- 带 `git:` 前缀时，接受简写格式，包括 `github.com/user/repo` 和 `git@github.com:user/repo`。
- HTTPS and SSH URLs are both supported.
- HTTPS 和 SSH URL 都受支持。
- SSH URLs use your configured SSH keys automatically (respects `~/.ssh/config`).
- SSH URL 自动使用你配置的 SSH 密钥（遵循 `~/.ssh/config`）。
- For non-interactive runs (for example CI), you can set `GIT_TERMINAL_PROMPT=0` to disable credential prompts and set `GIT_SSH_COMMAND` (for example `ssh -o BatchMode=yes -o ConnectTimeout=5`) to fail fast.
- 对于非交互运行（例如 CI），可以设置 `GIT_TERMINAL_PROMPT=0` 禁用凭据提示，并设置 `GIT_SSH_COMMAND`（例如 `ssh -o BatchMode=yes -o ConnectTimeout=5`）以快速失败。
- Refs are pinned tags or commits. `pi update --extensions` and `pi update --all` do not move them to newer refs, but they do reconcile an existing clone to the configured ref.
- 引用（ref）是固定的标签或提交。`pi update --extensions` 和 `pi update --all` 不会把它们移动到更新的引用，但会把现有克隆与配置的引用重新对齐。
- Use `pi install git:host/user/repo@new-ref` to update settings and move an existing package to a new pinned ref.
- 使用 `pi install git:host/user/repo@new-ref` 更新设置并把现有包移动到新的固定引用。
- Cloned to `~/.pi/agent/git/<host>/<path>` (global) or `.pi/git/<host>/<path>` (project).
- 克隆到 `~/.pi/agent/git/<host>/<path>`（全局）或 `.pi/git/<host>/<path>`（项目）。
- When reconciliation changes the checkout, pi resets and cleans the clone, then runs `npm install` if `package.json` exists.
- 当重新对齐更改了检出内容时，pi 会重置并清理克隆，然后如果存在 `package.json` 则运行 `npm install`。

**SSH examples:**
**SSH 示例：**
```bash
# git@host:path shorthand (requires git: prefix)
pi install git:git@github.com:user/repo

# ssh:// protocol format
pi install ssh://git@github.com/user/repo

# With version ref
pi install git:git@github.com:user/repo@v1.0.0
```

### Local Paths
### 本地路径

```
/absolute/path/to/package
./relative/path/to/package
```

Local paths point to files or directories on disk and are added to settings without copying. Relative paths are resolved against the settings file they appear in. If the path is a file, it loads as a single extension. If it is a directory, pi loads resources using package rules.
本地路径指向磁盘上的文件或目录，添加到设置时不会复制。相对路径相对于它们所在的设置文件解析。如果路径是文件，它作为单个扩展加载。如果是目录，pi 按包规则加载资源。

## Creating a Pi Package
## 创建 Pi 包

Add a `pi` manifest to `package.json` or use conventional directories. Include the `pi-package` keyword for discoverability.
在 `package.json` 中添加 `pi` 清单，或使用约定目录。包含 `pi-package` 关键字以便被发现。

```json
{
  "name": "my-package",
  "keywords": ["pi-package"],
  "pi": {
    "extensions": ["./extensions"],
    "skills": ["./skills"],
    "prompts": ["./prompts"],
    "themes": ["./themes"]
  }
}
```

Paths are relative to the package root. Arrays support glob patterns and `!exclusions`. Positive manifest globs discover visible paths in lexical order. List dot-prefixed paths directly. If a glob would need to continue through a symlink, list the symlinked resource root directly.
路径相对于包根目录。数组支持 glob 模式和 `!排除`。正向清单 glob 按字典序发现可见路径。点前缀路径请直接列出。如果 glob 需要穿过符号链接继续匹配，请直接列出符号链接的资源根目录。

### Gallery Metadata
### 画廊元数据

The [package gallery](https://pi.dev/packages) displays packages tagged with `pi-package`. Add `video` or `image` fields to show a preview:
[包画廊](https://pi.dev/packages)展示带 `pi-package` 标签的包。添加 `video` 或 `image` 字段以显示预览：

```json
{
  "name": "my-package",
  "keywords": ["pi-package"],
  "pi": {
    "extensions": ["./extensions"],
    "video": "https://example.com/demo.mp4",
    "image": "https://example.com/screenshot.png"
  }
}
```

- **video**: MP4 only. On desktop, autoplays on hover. Clicking opens a fullscreen player.
- **video**：仅 MP4。在桌面上，悬停时自动播放。点击打开全屏播放器。
- **image**: PNG, JPEG, GIF, or WebP. Displayed as a static preview.
- **image**：PNG、JPEG、GIF 或 WebP。显示为静态预览。

If both are set, video takes precedence.
如果两者都设置，视频优先。

## Package Structure
## 包结构

### Convention Directories
### 约定目录

If no `pi` manifest is present, pi auto-discovers resources from these directories:
如果没有 `pi` 清单，pi 会从以下目录自动发现资源：

- `extensions/` loads `.ts` and `.js` files
- `extensions/` 加载 `.ts` 和 `.js` 文件
- `skills/` recursively finds `SKILL.md` folders and loads top-level `.md` files as skills
- `skills/` 递归查找 `SKILL.md` 文件夹，并把顶层 `.md` 文件加载为技能
- `prompts/` loads `.md` files
- `prompts/` 加载 `.md` 文件
- `themes/` loads `.json` files
- `themes/` 加载 `.json` 文件

## Dependencies
## 依赖

Third party runtime dependencies belong in `dependencies` in `package.json`. Dependencies that do not register extensions, skills, prompt templates, or themes also belong in `dependencies`. When pi installs a package from npm or git, it runs `npm install`, so those dependencies are installed automatically.
第三方运行时依赖应放在 `package.json` 的 `dependencies` 中。不注册扩展、技能、提示词模板或主题的依赖也应放在 `dependencies` 中。当 pi 从 npm 或 git 安装包时，它会运行 `npm install`，因此这些依赖会自动安装。

Pi bundles core packages for extensions and skills. If you import any of these, list them in `peerDependencies` with a `"*"` range and do not bundle them: `@earendil-works/pi-ai`, `@earendil-works/pi-agent-core`, `@earendil-works/pi-coding-agent`, `@earendil-works/pi-tui`, `typebox`.
Pi 为扩展和技能内置了核心包。如果你导入了其中任何一个，请在 `peerDependencies` 中以 `"*"` 范围列出它们，并且不要打包它们：`@earendil-works/pi-ai`、`@earendil-works/pi-agent-core`、`@earendil-works/pi-coding-agent`、`@earendil-works/pi-tui`、`typebox`。

Other pi packages must be bundled in your tarball. Add them to `dependencies` and `bundledDependencies`, then reference their resources through `node_modules/` paths. Pi loads packages with separate module roots, so separate installs do not collide or share modules.
其他 pi 包必须打包进你的 tarball。把它们加入 `dependencies` 和 `bundledDependencies`，然后通过 `node_modules/` 路径引用它们的资源。Pi 以独立的模块根加载包，因此独立安装不会冲突或共享模块。

Example:
示例：

```json
{
  "dependencies": {
    "shitty-extensions": "^1.0.1"
  },
  "bundledDependencies": ["shitty-extensions"],
  "pi": {
    "extensions": ["extensions", "node_modules/shitty-extensions/extensions"],
    "skills": ["skills", "node_modules/shitty-extensions/skills"]
  }
}
```

## Package Filtering
## 包过滤

Filter what a package loads using the object form in settings:
使用设置中的对象形式过滤包加载的内容：

```json
{
  "packages": [
    "npm:simple-pkg",
    {
      "source": "npm:my-package",
      "extensions": ["extensions/*.ts", "!extensions/legacy.ts"],
      "skills": [],
      "prompts": ["prompts/review.md"],
      "themes": ["+themes/legacy.json"]
    }
  ]
}
```

`+path` and `-path` are exact paths relative to the package root.
`+path` 和 `-path` 是相对于包根目录的精确路径。

- Omit a key to load all of that type.
- 省略某个键则加载该类型的全部。
- Use `[]` to load none of that type.
- 使用 `[]` 则不加载该类型的任何内容。
- `!pattern` excludes matches.
- `!pattern` 排除匹配项。
- `+path` force-includes an exact path.
- `+path` 强制包含精确路径。
- `-path` force-excludes an exact path.
- `-path` 强制排除精确路径。
- Filters layer on top of the manifest. They narrow down what is already allowed.
- 过滤器叠加在清单之上。它们在已允许的内容基础上进一步收窄。

## Enable and Disable Resources
## 启用与禁用资源

Use `pi config` to enable or disable extensions, skills, prompt templates, and themes from installed packages and local directories. `pi config` starts in global settings (`~/.pi/agent/settings.json`); press Tab to switch between global and project-local modes. Use `pi config -l` to start in project overrides (`.pi/settings.json`) with inherited global resources dimmed.
使用 `pi config` 启用或禁用来自已安装包和本地目录的扩展、技能、提示词模板和主题。`pi config` 从全局设置（`~/.pi/agent/settings.json`）开始；按 Tab 在全局和项目本地模式之间切换。使用 `pi config -l` 从项目覆盖（`.pi/settings.json`）开始，继承的全局资源会变暗显示。

## Scope and Deduplication
## 作用域与去重

Packages can appear in both global and project settings. If the same package appears in both, the project entry wins unless the project entry has `autoload: false`, in which case it is applied as a delta over the global entry. Identity is determined by:
包可以同时出现在全局和项目设置中。如果同一个包出现在两者中，项目条目优先，除非项目条目有 `autoload: false`，此时它会作为全局条目之上的增量应用。身份由以下方式确定：

- npm: package name
- npm：包名
- git: repository URL without ref
- git：不带引用的仓库 URL
- local: resolved absolute path
- 本地：解析后的绝对路径
