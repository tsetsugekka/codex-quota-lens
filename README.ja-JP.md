# Codex Quota Lens

Codex Quota Lens は、現在の Codex/ChatGPT の rate-limit reset credit 状態を確認し、指定した言語とタイムゾーンで表示する Codex skill です。

ローカルの Codex 認証状態を読み取り、ChatGPT の reset-credit 状態エンドポイントに問い合わせて、次の情報を表示します。

- 利用可能なリセット回数
- 各リセットクレジットの有効期限までの残り時間
- 指定したタイムゾーンでの有効期限
- 期限の 1 日前と 1 時間前のリマインダー時刻

## 言語

- 英語：`--lang en`
- 簡体字中国語：`--lang zh`
- 日本語：`--lang ja`
- システム locale から自動判定：`--lang auto`

## タイムゾーン

`--timezone auto` を使うと、このマシンのローカルタイムゾーンを使用します。IANA タイムゾーンも指定できます。

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang ja --timezone Asia/Tokyo
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang zh --timezone Asia/Shanghai
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang en --timezone America/Los_Angeles
```

## 直接実行

リポジトリのルートで実行します。

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang auto --timezone auto
```

JSON 出力：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang ja --timezone Asia/Tokyo --json
```

Codex auth ファイルを指定する場合：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --auth-file ~/.codex/auth.json
```

## プライバシー

スクリプトはローカルの Codex `auth.json` から ChatGPT access token を読み取り、ChatGPT の reset-credit 状態エンドポイントへの Authorization header としてのみ送信します。token は出力しません。

ローカルの `.codex` ディレクトリ、`auth.json`、セッションログ、SQLite データベースを公開しないでください。

## Skill 構成

```text
skills/codex-quota-lens/
├── SKILL.md
├── agents/openai.yaml
└── scripts/quota_lens.py
```

## 注意

この skill は ChatGPT web の内部エンドポイントを利用します。エンドポイントまたは Codex auth ファイル形式が変更された場合は、結果に依存する前にスクリプトを更新してください。

他の言語：[English](README.md) | [中文](README.zh-CN.md)
