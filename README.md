# Codex Quota Lens

Codex Quota Lens is a Codex skill that shows the current Codex/ChatGPT rate-limit reset credit status with localized language and time-zone output.

It reads the local Codex authentication state, calls the ChatGPT reset-credit status endpoint, and reports:

- available reset credit count
- remaining time before each credit expires
- expiry time in the selected local time zone
- reminder times one day and one hour before expiry

## Languages

- English: `--lang en`
- Simplified Chinese: `--lang zh`
- Japanese: `--lang ja`
- Auto-detect from locale: `--lang auto`

## Time Zones

Use `--timezone auto` for the machine's local time zone, or pass an IANA time zone:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang en --timezone America/Los_Angeles
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang zh --timezone Asia/Shanghai
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang ja --timezone Asia/Tokyo
```

## Direct Usage

From the repository root:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang auto --timezone auto
```

JSON output:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang en --timezone UTC --json
```

Use a specific Codex auth file:

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --auth-file ~/.codex/auth.json
```

## Privacy

The script reads the local Codex `auth.json` file to obtain the stored ChatGPT access token, then sends that token only as an Authorization header to the ChatGPT web endpoint used for reset-credit status. It does not print the token.

Do not publish your local `.codex` directory, `auth.json`, session logs, or local SQLite databases.

## Skill Layout

```text
skills/codex-quota-lens/
├── SKILL.md
├── agents/openai.yaml
└── scripts/quota_lens.py
```

## Notes

This uses an internal ChatGPT web endpoint. If the endpoint or Codex auth file format changes, update the script before relying on the result.

Other languages: [中文](README.zh-CN.md) | [日本語](README.ja-JP.md)
