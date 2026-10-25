# Agent guide — wechat-multifix

Shell recipes (no compiled code) that copy `/Applications/WeChat.app` to `WeChat2.app`, change its Bundle ID, re-sign it ad-hoc and swap in a colored icon, so a second WeChat account can run on one Mac.

## Layout

- `skills/wechat-multifix/SKILL.md` — the agent skill: install, repair, WeChat3/4/5, uninstall. This is the source of truth for the commands.
- `skills/wechat-multifix/icons/` — six `AppIcon-<color>.icns` files; `icons/previews/` holds PNG previews used by the README.
- `scripts/check-skill.sh` — the only check: frontmatter is valid and every referenced icon/image exists.
- `README.md` (English, canonical) and `README.zh-CN.md` — keep their facts in sync.

## Check

```sh
bash scripts/check-skill.sh
```

CI runs the same script. There is no build step.

## Rules

- Do not run the install/repair commands on the user's machine unless the user asked for it in this session; they modify `/Applications` and re-sign an app.
- Never delete `~/Library/Containers/com.tencent.xinWeChat*` (chat history) unless the user explicitly asks for a full uninstall.
- Keep the disclaimers: unofficial, copies and re-signs WeChat locally, may break after WeChat updates, use at your own risk.
- Do not commit personal data (account names, chat content, local paths).
- Adding an icon means adding `AppIcon-<name>.icns` plus a preview PNG, and listing it in both READMEs and `SKILL.md`.
