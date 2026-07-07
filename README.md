# Codex Quota Lens

Codex Quota Lens is a compact Codex skill for inspecting Codex/ChatGPT rate-limit reset credits. It turns the local Codex auth state into a readable quota window: available reset count, remaining lifetime, expiry time, and reminder times in the user's language and local time zone.

This repository contains one focused skill. It does not install a background service, store credentials, or write to external systems. It reads local Codex auth only when a query is run.

## Included Skill

### `codex-quota-lens`

Queries current Codex/ChatGPT reset credits, with output in English, Chinese, or Japanese, and with either local machine time or an explicit IANA time zone.

〖Dependency〗No third-party Python packages. Local Codex must be logged in with ChatGPT, and `chatgpt.com` must be reachable.

〖External request〗Only calls the ChatGPT web reset-credit status endpoint when the query is run.

Use cases:

- Check how many Codex reset credits are currently available.
- See how long each reset credit remains valid.
- Convert expiry times to China, Japan, US, or other local time zones.
- Generate reminder times one day and one hour before expiry.
- Emit JSON for scripts, reminders, or other automation.

## Installation

Ask Codex to install the skill from this repository:

```text
Install Codex Quota Lens from https://github.com/tsetsugekka/codex-quota-lens.
```

For one-off use, clone the repository and run the script directly.

## Direct Usage

From the repository root:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang auto --timezone auto
```

English + Pacific Time:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang en --timezone America/Los_Angeles
```

Chinese + China time:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang zh --timezone Asia/Shanghai
```

Japanese + Japan time:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang ja --timezone Asia/Tokyo
```

Machine-readable JSON:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang en --timezone UTC --json
```

Use a specific Codex auth file:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --auth-file ~/.codex/auth.json
```

## Example Prompts

```text
Show my current Codex quota reset status in English and Pacific Time.

查询一下我当前 Codex 重置次数和有效期，用北京时间显示。

用日语显示我的 Codex reset credits，并按日本时间列出提醒时间。

Output my current reset-credit status as JSON.

Tell me when each reset credit should be reminded 1 day and 1 hour before expiry.
```

## Output

Text output includes:

- reset credit count
- remaining time for each credit
- local expiry time for each credit
- reminder time one day before expiry
- reminder time one hour before expiry

JSON output includes:

- `language`
- `timezone`
- `generated_at_utc`
- `available_count`
- `credits[].remaining`
- `credits[].expires_at_utc`
- `credits[].expires_at_local`
- `credits[].reminders[]`

## Safety

- The script reads local Codex `auth.json` only to obtain the current ChatGPT access token.
- The token is sent only as an Authorization header to the ChatGPT reset-credit status endpoint; it is not printed.
- The repository does not store tokens, cookies, `.codex/`, SQLite state, session logs, or `.env` files.
- `.gitignore` excludes `.codex/`, `auth.json`, `.env*`, `*.sqlite`, and similar local state.
- If the endpoint or Codex auth format changes, update the script instead of copying or exposing credentials manually.

## Repository Layout

```text
skills/
  codex-quota-lens/
    SKILL.md
    agents/
      openai.yaml
    scripts/
      quota_lens.py
README.md
README.zh.md
README.ja.md
LICENSE
```

## Languages

- 中文：`README.zh.md`
- English: `README.md`
- 日本語：`README.ja.md`
