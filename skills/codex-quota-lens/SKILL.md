---
name: codex-quota-lens
description: 查询并展示当前 Codex/ChatGPT rate-limit reset credits 状态，适用于用户询问 Codex 重置次数、剩余额度、reset credit 是否可用、过期时间、过期前提醒时间、使用窗口状态，或需要按中文、英语、日语和本地时区输出配额信息。Also supports English and Japanese quota reset status queries.
---

# Codex Quota Lens

使用本 skill 查询当前 Codex/ChatGPT reset credits，并把本机 Codex 登录状态中的额度窗口整理成用户可读结果：可用重置次数、每个 credit 的剩余时间、过期时间，以及过期前 1 天和 1 小时的提醒时间。

## 工作流

1. 使用 Python 3 运行 `scripts/quota_lens.py`。
2. 根据用户语言选择输出：
   - 中文使用 `--lang zh`。
   - 日语使用 `--lang ja`。
   - 英语使用 `--lang en`。
   - 用户没有指定语言时使用 `--lang auto`。
3. 根据用户所在地或要求选择时区：
   - 默认使用 `--timezone auto`，按本机本地时区显示。
   - 用户指定地区时，使用 IANA 时区，例如 `Asia/Shanghai`、`Asia/Tokyo`、`America/Los_Angeles`。
4. 把 `available_count` 解释为当前可用 reset credit 数。
5. 对每个 credit，报告剩余时间、当地过期时间、过期前 1 天提醒时间、过期前 1 小时提醒时间。
6. 如果用户需要自动化或进一步处理，使用 `--json` 输出机器可读结果。

## 常用命令

按用户语言和本机时区自动输出：

```bash
python3 scripts/quota_lens.py --lang auto --timezone auto
```

中文 + 中国时间：

```bash
python3 scripts/quota_lens.py --lang zh --timezone Asia/Shanghai
```

日语 + 日本时间：

```bash
python3 scripts/quota_lens.py --lang ja --timezone Asia/Tokyo
```

英语 + 指定美国时区：

```bash
python3 scripts/quota_lens.py --lang en --timezone America/Los_Angeles
```

机器可读 JSON：

```bash
python3 scripts/quota_lens.py --lang zh --timezone Asia/Shanghai --json
```

指定 Codex auth 文件：

```bash
python3 scripts/quota_lens.py --auth-file ~/.codex/auth.json
```

## 输出解释

- `available_count`：当前可用的 Codex/ChatGPT reset credit 数量。
- `expires_at_local`：按指定时区换算后的过期时间。
- `remaining`：距离过期还剩多久。
- `reminders`：过期前 1 天和 1 小时的提醒时间。

当用户问“还能重置几次”“额度什么时候过期”“什么时候提醒我”时，优先用文本解释；当用户要求脚本、自动化或精确字段时，再使用 JSON。

## 安全

脚本会从本机 Codex `auth.json` 读取 access token，然后调用 ChatGPT web 的 reset-credit 状态接口。必须遵守：

- 不要打印、记录、粘贴、提交或泄露 access token。
- 不要发布 `.codex/`、`auth.json`、session logs、SQLite 状态库、`.env` 或其他本地凭据文件。
- 如果网络受限，先说明需要联网访问 ChatGPT 状态接口，再请求用户允许联网运行。
- 如果 `auth.json` 缺失或格式变化，告诉用户本机 Codex 未登录或 auth 文件格式已变化。
- 如果接口返回 HTTP 错误，只报告状态码和简要原因；除非用户要求深入调试，不要输出请求头或敏感响应。

## 提醒处理

当用户要求创建提醒时，先重新查询最新 quota 状态，再按本地化时间创建提醒：

- `expires_at - 1 day`
- `expires_at - 1 hour`

即使没有创建日历或自动化提醒，也要在查询结果中显示建议提醒时间。

