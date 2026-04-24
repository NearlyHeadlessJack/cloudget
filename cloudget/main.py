import re
import time
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

REGIONS = [
    ("全国", "chinaall"),
    ("华北", "huabei"),
    ("东北", "dongbei"),
    ("华东", "huadong"),
    ("华中", "huazhong"),
    ("华南", "huanan"),
    ("西南", "xinan"),
    ("西北", "xibei"),
]

NMC_BASE = "https://www.nmc.cn"
CACHE_TTL = 300  # 5-minute cache

_cache = {}  # {slug: (cache_time, [{timestamp, label, url}, ...])}


def scrape_region_times(slug):
    """Fetch available radar image time points for a region from nmc.cn."""
    now = time.time()
    if slug in _cache:
        cached_at, data = _cache[slug]
        if now - cached_at < CACHE_TTL:
            return data

    url = f"{NMC_BASE}/publish/radar/{slug}.html"
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    urls = re.findall(r'data-img="([^"]*)"', resp.text)
    times = []
    for img_url in urls:
        m = re.search(r'_PI_(\d{17})\.PNG', img_url)
        if not m:
            continue
        ts = m.group(1)
        label = f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}"
        times.append({"timestamp": ts, "label": label, "url": img_url})

    times.sort(key=lambda x: x["timestamp"], reverse=True)
    _cache[slug] = (now, times)
    return times


@app.route("/")
def index():
    return render_template("index.html", regions=REGIONS)


@app.route("/api/times/<slug>")
def api_times(slug):
    try:
        data = scrape_region_times(slug)
        return jsonify({"ok": True, "data": data})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


@app.route("/api/radar/<slug>/<timestamp>")
def api_radar(slug, timestamp):
    try:
        data = scrape_region_times(slug)
        for item in data:
            if item["timestamp"] == timestamp:
                return jsonify({"ok": True, "url": item["url"]})
        return jsonify({"ok": False, "error": "timestamp not found"}), 404
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=9999)
