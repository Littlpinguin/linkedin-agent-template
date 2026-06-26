# linkedin-agent-template

**A personal LinkedIn agent template for Claude Code / Cowork.** You open it, type `start`, and it calibrates itself on *your* voice from your real posts. After that, it writes posts that sound like you and produces the visuals to go with them (AI-remixed images, cards, carousels).

Not a generic content generator: an agent that learns your writing style **and** your visual taste, then sticks to them.

## Load it into Claude (copy-paste)

**Option A — clone and open (recommended):**

```bash
git clone https://github.com/Littlpinguin/linkedin-agent-template.git my-linkedin-agent
cd my-linkedin-agent
claude
```

Then, inside Claude Code, just type:

```
start
```

The agent reads `CLAUDE.md`, sees it isn't configured yet, and launches its onboarding.

**Option B — start from the GitHub template:** click the green **Use this template → Create a new repository** button at the top of this page, then clone your new repo and run `claude` in it.

**Option C — one-liner with the GitHub CLI:**

```bash
gh repo create my-linkedin-agent --template Littlpinguin/linkedin-agent-template --private --clone && cd my-linkedin-agent && claude
```

> Using **Cowork** instead of the CLI? Open the folder in Cowork and type `start` in the chat. No GitHub account needed: you can also just download the ZIP from the green **Code** button.
>
> Don't have Claude Code yet? See [claude.com/claude-code](https://claude.com/claude-code).

## What the onboarding does

On first launch, the agent:

1. asks for **your LinkedIn posts export** (`.xls` / `.xlsx` / `.csv`), **your company website URL**, and **3-4 post visuals you like** (drop them in `assets/references-visuelles/`);
2. analyzes your posts (hooks, registers that work, cadence, formats), your site (company, offer, audience, tone) and your reference visuals (to infer your visual style);
3. writes your editorial identity (`voice/identite-editoriale.md`), your visual style (`profile/style-visuel.md`) and fills in your config (`profile/config.md`);
4. asks a few questions to fine-tune (audience, goals, brand color, signature title, visual style, off-limits topics);
5. wraps up: you can write your first post.

> **How to get your LinkedIn posts:** *Settings → Data privacy → Get a copy of your data → tick "Posts" (Shares)*. Or use any spreadsheet with one row per post: a text column, and ideally likes / comments / shares / date columns (to spot what performs).

## Requirements

- **Claude Code** or **Cowork** (the agent and its skills run inside it).
- **Python 3** with:
  - `pip install requests` (image generation);
  - `pip install playwright && playwright install chromium` (cards and carousels).
- **A Google AI Studio key** for image generation: copy `.env.example` to `.env` and set `GOOGLE_AI_API_KEY`.
- **3-5 photos of your face** in `assets/moi/` (for the "Identity Lock" of generated images).

> AI generation (Google API) and screenshots (Chromium) run locally, not in a restricted-network environment.

## The production chain (after setup)

1. **Write**: `my-viral-post` proposes angles in your voice, assembles the post, and tells you which visual format to attach.
2. **Illustrate**, by register:
   - opinion / contrarian → `image-linkedin` (remixed image with your face, meme);
   - expert / educational → `carte-linkedin` (infographic) or `carrousel-linkedin`;
   - field report / tools → card + screenshot.
3. **Compose then export**: a raw image (`outputs/images/`) is recomposed into a finished post via `carte-linkedin`, then exported (PNG 1080×1350 or PDF).
4. **Check and publish**: every skill reviews its render before delivery and logs to `outputs/`.

## Structure

```
linkedin-agent-template/
├── CLAUDE.md                ← the orchestrator (rules + onboarding trigger)
├── skills/
│   ├── onboarding/              ← calibrates the agent on your voice + style (first run)
│   ├── my-viral-post/           ← writes the post (text)
│   ├── image-linkedin/          ← AI-remixed image + meme (Nano Banana Pro)
│   ├── carte-linkedin/          ← single-image card / infographic (HTML→PNG)
│   └── carrousel-linkedin/      ← multipage PDF carousel (source of design tokens)
├── voice/
│   ├── identite-editoriale.md   ← YOUR voice (written during onboarding)
│   └── anti-ai-writing-style.md ← universal anti-AI writing rules
├── profile/
│   ├── config.md            ← your variables (name, company, color, audience, goals)
│   └── style-visuel.md      ← YOUR visual style (inferred from visuals you like)
├── assets/
│   ├── moi/                 ← your face photos + signature avatar
│   ├── marque/             ← your kit (logo, fonts, icons) — optional
│   ├── references-visuelles/ ← 3-4 visuals you like (basis of your style)
│   ├── visuels-generes/    ← raw AI images (TONE reference)
│   └── visuels-posts/      ← finished composed posts (COMPOSITION reference)
├── scripts/                 ← gen-image.py, screenshot.py, export-carousel-pdf.py, journal.py
├── templates/               ← carousel-linkedin-base.html
├── docs/                    ← template design notes
└── .env.example             ← Gemini key for image generation
```

> The agent's doctrine is written in French (it grew out of a French personal-branding agent), but it learns its voice from *your* posts, so it adapts to your language. The trigger word works in any language (`start`, `begin`, `commencer`, `setup`…).

## What makes this template different

- **Pure personal branding**: your face in the images. No secondary brand, no mascot.
- **No imposed frame**: the template forces neither a border, nor a top title, nor a signature. Your visual style is inferred from the 3-4 visuals you drop in, so your posts look like *you*, not like everyone else's template.
- **Anti "AI slop"**: `voice/anti-ai-writing-style.md` bans hype jargon, negative parallelisms ("it's not X, it's Y"), em dashes, and enforces a concrete, number-driven voice.
- **A single accent**: your brand color, chosen at onboarding, editable in `profile/config.md`.
- **Fonts**: system fonts by default (renders with zero install). Drop your `.woff2` files in `assets/marque/fonts/` for pixel-perfect output.
- **Self-contained**: everything stays inside the folder. Outputs and the log live in `outputs/` (gitignored).

## Security

- Never commit `.env` (covered by `.gitignore`).
- Only your own face (with your consent) in `assets/moi/`. No other real person without permission.
- Third-party logos: never fabricate them with AI or scrape them. Ask for the official files.

## License

[MIT](LICENSE). Reuse, modify, redistribute freely.
