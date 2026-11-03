# Marketing team

Marketing Manager = the main Claude session. It delegates to three bots (defined in `.claude/agents/`), reviews their work, and gives the owner a single update.

| Bot | Role | File | Output |
|---|---|---|---|
| Joe | Market research | `joe.md` | ranked news/trend brief |
| John | Facebook design | `john.md` | Canva graphics + captions |
| Jack | IG script writer | `jack.md` | Reel scripts |

Flow: Joe -> picks -> John + Jack -> Manager review -> owner update.
Reports land in `marketing/reports/`. Fill in `marketing/BRAND.md` first.
Nothing is published automatically; all output is drafts for the owner.

Poster style for John: `POSTER_STYLE.md` (reference image in `assets/`).
