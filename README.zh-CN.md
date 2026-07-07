# Codex Quota Lens

Codex Quota Lens 是一个 Codex skill，用于查询当前 Codex/ChatGPT 的 rate-limit reset credit 状态，并按指定语言和时区展示。

它会读取本机 Codex 登录状态，调用 ChatGPT 的 reset-credit 状态接口，并展示：

- 当前可用重置次数
- 每次重置额度的剩余有效时间
- 按指定时区换算的过期时间
- 过期前 1 天和过期前 1 小时的提醒时间

## 语言

- 英语：`--lang en`
- 简体中文：`--lang zh`
- 日语：`--lang ja`
- 根据系统 locale 自动选择：`--lang auto`

## 时区

使用 `--timezone auto` 读取本机当地时间，也可以传入 IANA 时区：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang zh --timezone Asia/Shanghai
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang ja --timezone Asia/Tokyo
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang en --timezone America/Los_Angeles
```

## 直接运行

在仓库根目录执行：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang auto --timezone auto
```

输出 JSON：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --lang zh --timezone Asia/Shanghai --json
```

指定 Codex auth 文件：

```bash
python3 skills/codex-quota-lens/scripts/quota_lens.py --auth-file ~/.codex/auth.json
```

## 隐私

脚本会从本机 Codex `auth.json` 中读取 ChatGPT access token，只把它作为 Authorization header 发送给 ChatGPT 的 reset-credit 状态接口。脚本不会打印 token。

不要发布本机 `.codex` 目录、`auth.json`、会话日志或本地 SQLite 数据库。

## Skill 结构

```text
skills/codex-quota-lens/
├── SKILL.md
├── agents/openai.yaml
└── scripts/quota_lens.py
```

## 说明

这里使用的是 ChatGPT web 内部接口。如果接口或 Codex auth 文件格式发生变化，需要先更新脚本再依赖查询结果。

其他语言：[English](README.md) | [日本語](README.ja-JP.md)
