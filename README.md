# wechat-multifix — run two (or more) WeChat accounts on one Mac

**English** · [中文](README.zh-CN.md)

**Run WeChat multi-instance on macOS: one command (or one sentence to your AI agent) clones WeChat into a second app with its own colored icon, so you can tell your accounts apart at a glance.**

<p align="center">
  <img src="skills/wechat-multifix/icons/previews/black.png" width="72" alt="black"/> &nbsp;
  <img src="skills/wechat-multifix/icons/previews/cyan.png" width="72" alt="cyan"/> &nbsp;
  <img src="skills/wechat-multifix/icons/previews/purple.png" width="72" alt="purple"/> &nbsp;
  <img src="skills/wechat-multifix/icons/previews/orange.png" width="72" alt="orange"/> &nbsp;
  <img src="skills/wechat-multifix/icons/previews/navy.png" width="72" alt="navy"/> &nbsp;
  <img src="skills/wechat-multifix/icons/previews/darkgray.png" width="72" alt="darkgray"/>
</p>

> **Unofficial. Use at your own risk.** This tool copies `/Applications/WeChat.app` and re-signs the copy locally with an ad-hoc signature. It is not made or endorsed by Tencent, and it may stop working after a WeChat update.

## Highlights

- **Second WeChat in one step** — copy, new Bundle ID, re-sign, new icon.
- **6 icon colors** (black, cyan, purple, orange, navy, dark gray) — the original stays green.
- **One-sentence repair** after WeChat updates: say "修复微信多开" ("repair WeChat multi-instance") to your agent. Chat history is kept.
- **More than two** — the same recipe makes WeChat3, WeChat4, and so on.
- **Works as an agent skill** for Claude Code, Codex, OpenClaw, Hermes and other agents; also fully usable by hand.

## Install

Easiest: give an AI agent this prompt.

```
Install the macOS WeChat multi-instance tool.

1. Read the skill at .agents/skills/wechat-multifix/SKILL.md
2. Follow its install flow.

Before installing, ask me which icon color I want (black / cyan / purple / orange / navy / dark gray).
When done, tell me the Bundle ID of WeChat and WeChat2 and whether they differ.
```

Or by hand (the black icon is used here; pick another file from `skills/wechat-multifix/icons/`):

```bash
SKILL_DIR="$PWD/skills/wechat-multifix"   # run from the repo root
ICON="AppIcon-black.icns"

cp -R /Applications/WeChat.app /Applications/WeChat2.app
/usr/libexec/PlistBuddy -c "Set :CFBundleIdentifier com.tencent.xinWeChat2" /Applications/WeChat2.app/Contents/Info.plist
/usr/libexec/PlistBuddy -c "Set :CFBundleName WeChat2" /Applications/WeChat2.app/Contents/Info.plist
xattr -cr /Applications/WeChat2.app
codesign --force --deep --sign - /Applications/WeChat2.app
chown -R $(whoami):admin /Applications/WeChat2.app
cp "$SKILL_DIR/icons/$ICON" /Applications/WeChat2.app/Contents/Resources/AppIcon.icns
codesign --force --deep --sign - /Applications/WeChat2.app
open -a /Applications/WeChat2.app
```

## Use with Claude Code / Codex

```bash
npx skills add risingjerry/wechat-multifix
```

Or copy `skills/wechat-multifix` to `~/.claude/skills/` (Claude Code) or `~/.agents/skills/` (Codex and compatible agents). Then say, for example:

- `Install WeChat multi-instance, I want the purple icon.`
- `修复微信多开` (repair after a WeChat update)
- `Make me a third WeChat with the orange icon.`

The agent asks for the icon color before it touches anything.

## The six icons

| Color | File | Feel |
|---|---|---|
| Black | `AppIcon-black.icns` | quiet, dark-mode friendly |
| Cyan | `AppIcon-cyan.icns` | fresh, techy |
| Purple | `AppIcon-purple.icns` | elegant, creative |
| Orange | `AppIcon-orange.icns` | warm, lively |
| Navy | `AppIcon-navy.icns` | calm, business |
| Dark gray | `AppIcon-darkgray.icns` | minimal |

The original `WeChat.app` keeps its green icon.

## How it works

Every macOS app is identified by its Bundle ID, so a plain copy of WeChat collides with the original. The tool gives the copy its own Bundle ID (`com.tencent.xinWeChat2`), strips extended attributes, re-signs it ad-hoc, and swaps the icon. The copy keeps its data in `~/Library/Containers/com.tencent.xinWeChat2/`, separate from the app itself, which is why a repair does not lose chat history.

## Limits and requirements

- macOS with `/Applications/WeChat.app` already installed; the commands need permission to write to `/Applications`.
- **A WeChat update overwrites `WeChat2.app`** and resets its Bundle ID to the original. Then neither app starts. Run the repair (below). To avoid surprises you can turn off automatic WeChat updates and repair on your own schedule.
- The copy is re-signed locally, so it is not Tencent-signed. Unofficial; use at your own risk.
- Notifications must be enabled by hand (see the FAQ).

## FAQ

### How do I run two WeChat accounts on a Mac?
Install this tool, pick an icon color, then open `WeChat` and `WeChat2` and log in to a different account in each. Open both with `open -a /Applications/WeChat.app; sleep 0.5; open -a /Applications/WeChat2.app`.

### WeChat2 stopped opening after a WeChat update. What now?
An update resets WeChat2's Bundle ID, so macOS treats both apps as the same one. Tell your agent "修复微信多开", or rerun the install commands; they rebuild WeChat2 and restore the icon. Your chat history is stored outside the app and is kept.

### Will I lose my chat history?
Not by repairing. History lives in `~/Library/Containers/com.tencent.xinWeChat2/`. Only the uninstall step that deletes that folder removes it, and it is irreversible.

### macOS says the app is damaged or cannot be opened.
Right-click `WeChat2.app` and choose **Open** the first time.

### Why do I get no Dock badge or notification from WeChat2?
Turn them on twice: inside WeChat2 under **Settings → Notifications** (new message notification, sound, preview), and in macOS **System Settings → Notifications → WeChat2**. macOS often does not show the permission prompt for the copy.

### How do I make a third or fourth WeChat?
Use the multi-instance recipe in the skill: change the number, for example `WeChat3` with Bundle ID `com.tencent.xinWeChat3`, and pick another icon.

## Uninstall

```bash
rm -rf /Applications/WeChat2.app
rm -rf ~/Library/Containers/com.tencent.xinWeChat2   # chat history of that account, irreversible
```

Do the same with `WeChat3`, `WeChat4`, ... if you made them. The original `WeChat.app` is never touched.

## License

MIT. WeChat is a trademark of Tencent; this project is not affiliated with Tencent.

---

If this saved you a second phone, a star helps others find it.

[![Star History Chart](https://api.star-history.com/svg?repos=risingjerry/wechat-multifix&type=Date)](https://star-history.com/#risingjerry/wechat-multifix&Date)
