#!/usr/bin/env python3
import argparse
import json
import locale
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None


URL = "https://chatgpt.com/backend-api/wham/rate-limit-reset-credits"
DEFAULT_AUTH_FILE = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "auth.json"
SUPPORTED_LANGS = {"en", "zh", "ja"}

MESSAGES = {
    "en": {
        "title": "Codex reset credits: {count}",
        "credit": "Reset credit {index}:",
        "remaining": "  Remaining: {remaining}",
        "expires": "  Expires: {time} ({zone})",
        "reminders": "  Reminders:",
        "one_day": "1 day before expiry",
        "one_hour": "1 hour before expiry",
        "reminder_line": "    - {label}: {time} ({zone})",
        "day": "d",
        "hour": "h",
        "minute": "m",
        "second": "s",
        "network_error": "Query failed: network error: {reason}",
        "http_error": "Query failed: HTTP {code}",
        "auth_missing": "Query failed: auth file not found: {path}",
        "auth_field": "Query failed: auth file is missing field: {field}",
        "json_error": "Query failed: invalid JSON: {message}",
    },
    "zh": {
        "title": "Codex 重置次数：{count}",
        "credit": "第 {index} 次重置：",
        "remaining": "  剩余时间：{remaining}",
        "expires": "  过期时间：{time}（{zone}）",
        "reminders": "  提醒时间：",
        "one_day": "过期前 1 天",
        "one_hour": "过期前 1 小时",
        "reminder_line": "    - {label}：{time}（{zone}）",
        "day": "天",
        "hour": "小时",
        "minute": "分钟",
        "second": "秒",
        "network_error": "查询失败：网络错误：{reason}",
        "http_error": "查询失败：HTTP {code}",
        "auth_missing": "查询失败：找不到 auth 文件：{path}",
        "auth_field": "查询失败：auth 文件缺少字段：{field}",
        "json_error": "查询失败：JSON 无效：{message}",
    },
    "ja": {
        "title": "Codex リセット回数：{count}",
        "credit": "{index} 回目のリセット：",
        "remaining": "  残り時間：{remaining}",
        "expires": "  有効期限：{time}（{zone}）",
        "reminders": "  リマインダー：",
        "one_day": "期限の 1 日前",
        "one_hour": "期限の 1 時間前",
        "reminder_line": "    - {label}：{time}（{zone}）",
        "day": "日",
        "hour": "時間",
        "minute": "分",
        "second": "秒",
        "network_error": "照会に失敗しました：ネットワークエラー：{reason}",
        "http_error": "照会に失敗しました：HTTP {code}",
        "auth_missing": "照会に失敗しました：auth ファイルが見つかりません：{path}",
        "auth_field": "照会に失敗しました：auth ファイルに項目がありません：{field}",
        "json_error": "照会に失敗しました：JSON が無効です：{message}",
    },
}


def detect_lang(value):
    if value and value != "auto":
        normalized = value.lower().replace("_", "-")
    else:
        env_lang = locale.getlocale()[0] or os.environ.get("LANG", "")
        normalized = env_lang.lower().replace("_", "-")

    if normalized.startswith("zh"):
        return "zh"
    if normalized.startswith("ja"):
        return "ja"
    return "en"


def local_timezone():
    return datetime.now().astimezone().tzinfo or timezone.utc


def timezone_label(tz):
    key = getattr(tz, "key", None)
    if key:
        return key
    now = datetime.now(tz)
    name = now.tzname()
    offset = now.strftime("%z")
    if len(offset) == 5:
        offset = f"{offset[:3]}:{offset[3:]}"
    return name or f"UTC{offset}"


def parse_timezone(value):
    if not value or value == "auto":
        return local_timezone()
    if value.upper() == "UTC":
        return timezone.utc
    if ZoneInfo is None:
        raise SystemExit("Named time zones require Python 3.9 or newer.")
    try:
        return ZoneInfo(value)
    except Exception:
        raise SystemExit(f"Invalid time zone: {value}") from None


def parse_time(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def format_duration(seconds, lang):
    labels = MESSAGES[lang]
    seconds = int(seconds)
    sign = "-" if seconds < 0 else ""
    seconds = abs(seconds)
    days, seconds = divmod(seconds, 86_400)
    hours, seconds = divmod(seconds, 3_600)
    minutes, seconds = divmod(seconds, 60)

    if lang == "en":
        return f"{sign}{days}{labels['day']} {hours}{labels['hour']} {minutes}{labels['minute']} {seconds}{labels['second']}"
    return (
        f"{sign}{days}{labels['day']} "
        f"{hours}{labels['hour']} "
        f"{minutes}{labels['minute']} "
        f"{seconds}{labels['second']}"
    )


def load_token(auth_file):
    if not auth_file.exists():
        raise FileNotFoundError(auth_file)
    auth = json.loads(auth_file.read_text(encoding="utf-8"))
    return auth["tokens"]["access_token"]


def fetch_credits(token):
    request = Request(
        URL,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Origin": "https://chatgpt.com",
            "Referer": "https://chatgpt.com/",
        },
    )
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def load_input_json(path):
    if str(path) == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def build_result(data, lang, tz):
    now = datetime.now(timezone.utc)
    zone = timezone_label(tz)
    credits = []
    for index, credit in enumerate(data.get("credits", []), start=1):
        expires_at = parse_time(credit["expires_at"])
        expires_local = expires_at.astimezone(tz)
        reminder_1_day = expires_at - timedelta(days=1)
        reminder_1_hour = expires_at - timedelta(hours=1)
        credits.append(
            {
                "index": index,
                "remaining": format_duration(expires_at.timestamp() - now.timestamp(), lang),
                "expires_at_utc": expires_at.isoformat(timespec="seconds"),
                "expires_at_local": expires_local.isoformat(timespec="seconds"),
                "timezone": zone,
                "reminders": [
                    {
                        "label": MESSAGES[lang]["one_day"],
                        "at_utc": reminder_1_day.isoformat(timespec="seconds"),
                        "at_local": reminder_1_day.astimezone(tz).isoformat(timespec="seconds"),
                        "timezone": zone,
                    },
                    {
                        "label": MESSAGES[lang]["one_hour"],
                        "at_utc": reminder_1_hour.isoformat(timespec="seconds"),
                        "at_local": reminder_1_hour.astimezone(tz).isoformat(timespec="seconds"),
                        "timezone": zone,
                    },
                ],
            }
        )
    return {
        "language": lang,
        "timezone": zone,
        "generated_at_utc": now.isoformat(timespec="seconds"),
        "available_count": data.get("available_count", 0),
        "credits": credits,
    }


def format_local_time(value):
    return parse_time(value).strftime("%Y-%m-%d %H:%M:%S")


def print_text(result):
    labels = MESSAGES[result["language"]]
    print(labels["title"].format(count=result["available_count"]))
    for credit in result["credits"]:
        print(labels["credit"].format(index=credit["index"]))
        print(labels["remaining"].format(remaining=credit["remaining"]))
        print(labels["expires"].format(time=format_local_time(credit["expires_at_local"]), zone=credit["timezone"]))
        print(labels["reminders"])
        for reminder in credit["reminders"]:
            print(
                labels["reminder_line"].format(
                    label=reminder["label"],
                    time=format_local_time(reminder["at_local"]),
                    zone=reminder["timezone"],
                )
            )


def main():
    parser = argparse.ArgumentParser(description="Query Codex reset credits with localized output.")
    parser.add_argument("--auth-file", type=Path, default=DEFAULT_AUTH_FILE)
    parser.add_argument("--input-json", help="Read a saved API response instead of calling the endpoint. Use '-' for stdin.")
    parser.add_argument("--lang", choices=["auto", "en", "zh", "ja"], default="auto")
    parser.add_argument("--timezone", default="auto", help="IANA time zone such as Asia/Tokyo, Asia/Shanghai, America/Los_Angeles, or auto.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    lang = detect_lang(args.lang)
    tz = parse_timezone(args.timezone)
    labels = MESSAGES[lang]

    try:
        if args.input_json:
            data = load_input_json(args.input_json)
        else:
            data = fetch_credits(load_token(args.auth_file))
        result = build_result(data, lang, tz)
    except FileNotFoundError as exc:
        raise SystemExit(labels["auth_missing"].format(path=exc.filename or args.auth_file)) from None
    except HTTPError as exc:
        raise SystemExit(labels["http_error"].format(code=exc.code)) from None
    except URLError as exc:
        raise SystemExit(labels["network_error"].format(reason=exc.reason)) from None
    except KeyError as exc:
        raise SystemExit(labels["auth_field"].format(field=exc)) from None
    except json.JSONDecodeError as exc:
        raise SystemExit(labels["json_error"].format(message=exc.msg)) from None

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)


if __name__ == "__main__":
    main()
