# Codex Quota Lens

Codex Quota Lens 是一个面向 Codex/ChatGPT rate-limit reset credits 的轻量查询 skill。它把本机 Codex 登录状态中的 reset-credit 窗口整理成可读结果，并按用户语言和当地时间输出剩余次数、过期时间和提醒时间。

这个仓库只保存一个边界清晰的 skill：不安装后台服务，不保存凭据，不写入外部系统；需要查询时才读取本机 Codex auth 并请求当前状态。

## 当前包含的 skill

### `codex-quota-lens`

查询当前 Codex/ChatGPT reset credits，可按英语、中文、日语输出，并支持本机时区或指定 IANA 时区。

〖依赖〗无第三方 Python 包；需要本机 Codex 已通过 ChatGPT 登录，并允许访问 `chatgpt.com`。

〖外部请求〗只在用户运行查询时访问 ChatGPT web 的 reset-credit 状态接口。

适用场景：

- 查看当前还有几次 Codex 重置额度可用。
- 查看每次 reset credit 还有多久过期。
- 把过期时间换算成中国、日本、美国等当地时间。
- 生成过期前 1 天和过期前 1 小时的提醒时间。
- 需要 JSON 输出，交给其他脚本、自动化或提醒流程继续处理。

## 安装

在 Codex 里直接发送这个仓库链接，并说明要安装 skill：

```text
请从 https://github.com/tsetsugekka/codex-quota-lens 安装 Codex Quota Lens。
```

如果只想临时使用，也可以克隆仓库后直接运行脚本，不需要安装 skill。

## 直接运行

在仓库根目录执行：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang auto --timezone auto
```

中文 + 中国时间：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang zh --timezone Asia/Shanghai
```

日语 + 日本时间：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang ja --timezone Asia/Tokyo
```

英语 + 美西时间：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang en --timezone America/Los_Angeles
```

机器可读 JSON：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang zh --timezone Asia/Shanghai --json
```

指定 Codex auth 文件：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --auth-file ~/.codex/auth.json
```

## 示例请求

```text
查询一下我当前 Codex 重置次数和有效期，用北京时间显示。

用日语显示我的 Codex reset credits，并按日本时间列出提醒时间。

Show my Codex quota reset status in English and Pacific Time.

查询当前可用重置次数，并输出 JSON。

看一下每个 reset credit 过期前 1 天和 1 小时分别是什么时候。
```

## 输出内容

默认文本输出会包含：

- `Codex 重置次数` / `Codex reset credits` / `Codex リセット回数`
- 每个 credit 的剩余时间
- 每个 credit 的当地过期时间
- 过期前 1 天提醒时间
- 过期前 1 小时提醒时间

JSON 输出包含：

- `language`
- `timezone`
- `generated_at_utc`
- `available_count`
- `credits[].remaining`
- `credits[].expires_at_utc`
- `credits[].expires_at_local`
- `credits[].reminders[]`

## 安全说明

- 脚本只读取本机 Codex `auth.json`，用于取得当前 ChatGPT access token。
- token 只作为 Authorization header 发送给 ChatGPT reset-credit 状态接口；脚本不会打印 token。
- 仓库不会保存 token、cookie、`.codex/`、SQLite 状态库、会话日志或 `.env`。
- `.gitignore` 已排除 `.codex/`、`auth.json`、`.env*`、`*.sqlite` 等本地敏感文件。
- 如果接口或 Codex auth 文件格式变化，查询可能失败；这时应更新脚本，而不是手动复制或暴露凭据。

## 仓库结构

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

## 语言

- 中文：`README.zh.md`
- English: `README.md`
- 日本語：`README.ja.md`
