# Codex Quota Lens

Codex Quota Lens は、Codex/ChatGPT の rate-limit reset credits を確認するための小さな Codex skill です。ローカルの Codex 認証状態から、利用可能なリセット回数、残り時間、有効期限、リマインダー時刻を読みやすく表示します。

このリポジトリには、役割を絞った 1 つの skill だけを保存しています。バックグラウンドサービスはインストールせず、認証情報を保存せず、外部システムにも書き込みません。問い合わせを実行するときだけ、ローカルの Codex auth を読み取ります。

## 含まれる skill

### `codex-quota-lens`

現在の Codex/ChatGPT reset credits を問い合わせ、英語・中国語・日本語で表示します。時刻はマシンのローカルタイムゾーン、または指定した IANA タイムゾーンに変換できます。

〖依存〗サードパーティ Python パッケージは不要です。ローカル Codex が ChatGPT でログイン済みで、`chatgpt.com` に接続できる必要があります。

〖外部リクエスト〗問い合わせ実行時のみ、ChatGPT web の reset-credit 状態エンドポイントにアクセスします。

利用シーン：

- 現在利用可能な Codex リセット回数を確認する。
- 各 reset credit の有効期限までの残り時間を確認する。
- 有効期限を日本、中国、米国などのローカル時刻に変換する。
- 期限の 1 日前と 1 時間前のリマインダー時刻を作る。
- JSON 出力をスクリプト、通知、その他の自動化に渡す。

## インストール

Codex にこのリポジトリから skill をインストールするよう依頼します。

```text
https://github.com/tsetsugekka/codex-quota-lens から Codex Quota Lens をインストールしてください。
```

一時的に使うだけなら、リポジトリを clone してスクリプトを直接実行できます。

## 直接実行

リポジトリのルートで実行します。

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang auto --timezone auto
```

日本語 + 日本時間：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang ja --timezone Asia/Tokyo
```

中国語 + 中国時間：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang zh --timezone Asia/Shanghai
```

英語 + 米国太平洋時間：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang en --timezone America/Los_Angeles
```

機械可読 JSON：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang ja --timezone Asia/Tokyo --json
```

Codex auth ファイルを指定する場合：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --auth-file ~/.codex/auth.json
```

## リクエスト例

```text
用日语显示我的 Codex reset credits，并按日本时间列出提醒时间。

查询一下我当前 Codex 重置次数和有效期，用北京时间显示。

Show my current Codex quota reset status in English and Pacific Time.

現在の reset-credit 状態を JSON で出力して。

各 reset credit について、期限の 1 日前と 1 時間前の通知時刻を教えて。
```

## 出力内容

テキスト出力には次の情報が含まれます。

- 利用可能なリセット回数
- 各 credit の残り時間
- 各 credit のローカル有効期限
- 期限の 1 日前のリマインダー時刻
- 期限の 1 時間前のリマインダー時刻

JSON 出力には次のフィールドが含まれます。

- `language`
- `timezone`
- `generated_at_utc`
- `available_count`
- `credits[].remaining`
- `credits[].expires_at_utc`
- `credits[].expires_at_local`
- `credits[].reminders[]`

## 安全性

- スクリプトは、現在の ChatGPT access token を取得するためだけにローカル Codex `auth.json` を読み取ります。
- token は ChatGPT reset-credit 状態エンドポイントへの Authorization header としてのみ送信され、出力されません。
- このリポジトリには token、cookie、`.codex/`、SQLite 状態、セッションログ、`.env` ファイルを保存しません。
- `.gitignore` は `.codex/`、`auth.json`、`.env*`、`*.sqlite` などのローカル状態を除外します。
- エンドポイントまたは Codex auth 形式が変わった場合は、認証情報を手動でコピーせず、スクリプトを更新してください。

## リポジトリ構成

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

## 言語

- 中文：`README.zh.md`
- English: `README.md`
- 日本語：`README.ja.md`
