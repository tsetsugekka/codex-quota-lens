---
name: codex-quota-lens
description: Query and present the current Codex/ChatGPT rate-limit reset credit status from local Codex auth state. Use when the user asks for Codex reset credits, remaining reset count, quota reset availability, expiry times, localized output, reminder times before reset-credit expiry, or usage-window status in English, Chinese, or Japanese.
---

# Codex Quota Lens

## Workflow

1. Run `scripts/quota_lens.py` with Python 3.
2. Choose the output language:
   - Use `--lang zh` for Chinese.
   - Use `--lang ja` for Japanese.
   - Use `--lang en` for English.
   - Use `--lang auto` when the user does not specify a language.
3. Choose the time zone:
   - Use `--timezone auto` for the machine's local time.
   - Use an IANA zone such as `Asia/Shanghai`, `Asia/Tokyo`, or `America/Los_Angeles` when the user specifies a locale.
4. Report `available_count` as the number of available reset credits.
5. For every credit, report remaining time, expiry time, and reminders at one day and one hour before expiry.

## Commands

Use localized text output:

```bash
python3 scripts/quota_lens.py --lang auto --timezone auto
```

Use Chinese and China time:

```bash
python3 scripts/quota_lens.py --lang zh --timezone Asia/Shanghai
```

Use Japanese and Japan time:

```bash
python3 scripts/quota_lens.py --lang ja --timezone Asia/Tokyo
```

Use English and a specific local time zone:

```bash
python3 scripts/quota_lens.py --lang en --timezone America/Los_Angeles
```

Return machine-readable JSON:

```bash
python3 scripts/quota_lens.py --lang en --timezone UTC --json
```

## Security

The script reads the access token from Codex's local `auth.json`, then calls the ChatGPT web endpoint for rate-limit reset credits. Never print, log, paste, commit, or otherwise expose the access token. Do not publish `.codex/`, `auth.json`, session logs, or local SQLite state.

## Failure Handling

- If the network is restricted, ask for approval to run the same command with network access.
- If `auth.json` is missing or malformed, tell the user Codex is not logged in locally or the auth file format has changed.
- If the endpoint returns HTTP errors, report only the status code unless the user asks for deeper debugging. Do not echo request headers.

## Reminder Handling

When the user asks for reminders, query fresh data first. Create reminders at the localized times corresponding to:

- `expires_at - 1 day`
- `expires_at - 1 hour`

Always show the reminder schedule in the query result even if no calendar or automation reminder is created.
