# Contributing

Thanks for helping improve this template. It is used by people who are not developers, so the bar is simple: a change should make the onboarding clearer, safer or shorter for a beginner.

## Good contributions

- A friction you hit during the onboarding (a confusing question, a command that failed, a step that took too long): open an issue with the step number and what you saw.
- A fix to a skill (`skills/<name>/SKILL.md`) or a script (`scripts/`). Edit the source in `skills/`, never `.claude/skills/` (those are symlinks).
- Support for another Apify actor or another image generator, with its limits stated.

## Ground rules

- **No personal data.** Never commit your `.env`, your photos (`assets/moi/`), your `profile/` or `voice/identite-editoriale.md` once filled, or anything from a client. The template only ships placeholders.
- **No paid call without consent.** Any new paid step must announce its cost and wait for a yes, like the existing ones.
- **Three routes per tool, one of them free**, each with what it can and can't do.
- Writing rules for the doctrine are in `voice/anti-ai-writing-style.md` (no em dashes, no "it's not X, it's Y").

## Pull requests

Keep them small and describe how you tested: which onboarding steps you replayed, with which route. Scripts must keep working with only `requests` installed.
