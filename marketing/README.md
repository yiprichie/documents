# Marketing team

Marketing Manager = the main Claude session. It delegates to three bots (defined in `.claude/agents/`), reviews their work, and gives the owner a single update.

| Bot | File | Output |
|---|---|---|
| News Scout | `news-scout-bot.md` | ranked news brief |
| Facebook Graphics | `facebook-graphics-bot.md` | Canva graphics + captions |
| IG Reels | `ig-reels-bot.md` | shoot-ready Reel packages |

Flow: News Scout -> picks -> Graphics + Reels -> Manager review -> owner update.
Reports land in `marketing/reports/`. Fill in `marketing/BRAND.md` first.
Nothing is published automatically; all output is drafts for the owner.
