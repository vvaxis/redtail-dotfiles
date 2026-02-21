#!/usr/bin/env python3
"""Fetch weather data from Open-Meteo for the dashboard."""

import json
import urllib.request
import datetime
import os

CONFIG_DIR = os.path.expanduser("~/.config/dashboard")

# WMO weather code → Portuguese description
WMO_DESC = {
    0: "céu limpo",
    1: "predominantemente limpo", 2: "parcialmente nublado", 3: "nublado",
    45: "nevoeiro", 48: "nevoeiro com geada",
    51: "garoa leve", 53: "garoa moderada", 55: "garoa intensa",
    56: "garoa congelante leve", 57: "garoa congelante",
    61: "chuva leve", 63: "chuva moderada", 65: "chuva forte",
    66: "chuva congelante leve", 67: "chuva congelante",
    71: "neve leve", 73: "neve moderada", 75: "neve forte",
    77: "grãos de neve",
    80: "pancadas leves", 81: "pancadas moderadas", 82: "pancadas fortes",
    85: "neve leve em pancadas", 86: "neve forte em pancadas",
    95: "trovoada", 96: "trovoada com granizo", 99: "trovoada com granizo forte",
}

# WMO weather code → Nerd Font icon (day)
WMO_ICONS_DAY = {
    0: "\ue30d",
    1: "\ue300", 2: "\ue300", 3: "\ue30c",
    45: "\ue303", 48: "\ue303",
    51: "\ue30b", 53: "\ue30b", 55: "\ue308",
    56: "\ue306", 57: "\ue306",
    61: "\ue30b", 63: "\ue308", 65: "\ue308",
    66: "\ue306", 67: "\ue306",
    71: "\ue30a", 73: "\ue30a", 75: "\ue30a",
    77: "\ue30a",
    80: "\ue309", 81: "\ue309", 82: "\ue309",
    85: "\ue30a", 86: "\ue30a",
    95: "\ue305", 96: "\ue30f", 99: "\ue30f",
}

# WMO weather code → Nerd Font icon (night)
WMO_ICONS_NIGHT = {
    0: "\ue32b",
    1: "\ue32c", 2: "\ue32c", 3: "\ue37e",
    45: "\ue346", 48: "\ue346",
    51: "\ue336", 53: "\ue336", 55: "\ue333",
    56: "\ue331", 57: "\ue331",
    61: "\ue336", 63: "\ue333", 65: "\ue333",
    66: "\ue331", 67: "\ue331",
    71: "\ue335", 73: "\ue335", 75: "\ue335",
    77: "\ue335",
    80: "\ue334", 81: "\ue334", 82: "\ue334",
    85: "\ue335", 86: "\ue335",
    95: "\ue330", 96: "\ue338", 99: "\ue338",
}

FALLBACK = {
    "temp": "--",
    "high": "--",
    "low": "--",
    "feels_like": "--",
    "condition": "Erro",
    "icon": "\ue374",
    "humidity": 0,
    "pop": 0,
    "hourly": [],
}


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "dashboard/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode())


def is_night(now, sunrise_str, sunset_str):
    """Check if current time is before sunrise or after sunset."""
    sunrise = datetime.datetime.fromisoformat(sunrise_str)
    sunset = datetime.datetime.fromisoformat(sunset_str)
    return now < sunrise or now >= sunset


def get_icon(wmo_code, night=False):
    icons = WMO_ICONS_NIGHT if night else WMO_ICONS_DAY
    return icons.get(wmo_code, "\ue374")


def get_location():
    """Get coordinates: manual override from file, or auto-detect via IP."""
    loc_file = os.path.join(CONFIG_DIR, "location")
    if os.path.exists(loc_file):
        lat, lon = [v.strip() for v in open(loc_file).read().strip().split(",")]
        return lat, lon
    data = fetch_json("https://ipinfo.io/json")
    lat, lon = data["loc"].split(",")
    return lat, lon


def main():
    lat, lon = get_location()

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"precipitation,weather_code,is_day"
        f"&hourly=temperature_2m,precipitation_probability,weather_code"
        f"&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset"
        f"&timezone=auto&forecast_days=2"
    )

    data = fetch_json(url)

    cur = data["current"]
    daily = data["daily"]
    hourly = data["hourly"]

    temp = round(cur["temperature_2m"])
    feels_like = round(cur["apparent_temperature"])
    humidity = cur["relative_humidity_2m"]
    wmo_code = cur["weather_code"]
    night = cur["is_day"] == 0
    condition = WMO_DESC.get(wmo_code, "Desconhecido")
    icon = get_icon(wmo_code, night)

    # Today's high/low from the daily forecast
    high = round(daily["temperature_2m_max"][0])
    low = round(daily["temperature_2m_min"][0])

    # Sunrise/sunset for day/night icon selection in hourly
    sunrise_today = daily["sunrise"][0]
    sunset_today = daily["sunset"][0]

    # Hourly: find the current hour index, then pick next 4 slots at 3h intervals
    now = datetime.datetime.now()
    current_hour_str = now.strftime("%Y-%m-%dT%H:00")
    try:
        start_idx = hourly["time"].index(current_hour_str)
    except ValueError:
        start_idx = 0

    hourly_slots = []
    max_pop = 0
    for i in range(start_idx, min(start_idx + 12, len(hourly["time"]))):
        pop = hourly["precipitation_probability"][i] or 0
        max_pop = max(max_pop, pop)

        # Pick every 3rd hour for the display slots
        offset = i - start_idx
        if offset % 3 == 0 and len(hourly_slots) < 4:
            slot_time = datetime.datetime.fromisoformat(hourly["time"][i])
            slot_wmo = hourly["weather_code"][i]
            slot_night = is_night(slot_time,  sunrise_today, sunset_today)
            hourly_slots.append({
                "time": f"{slot_time.hour}h",
                "temp": round(hourly["temperature_2m"][i]),
                "icon": get_icon(slot_wmo, slot_night),
                "desc": WMO_DESC.get(slot_wmo, ""),
                "pop": pop,
            })

    print(json.dumps({
        "temp": temp,
        "high": high,
        "low": low,
        "feels_like": feels_like,
        "condition": condition,
        "icon": icon,
        "humidity": humidity,
        "pop": max_pop,
        "hourly": hourly_slots,
    }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(json.dumps(FALLBACK))
