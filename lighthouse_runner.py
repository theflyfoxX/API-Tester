import subprocess
import json
import shutil

def run_lighthouse(url: str, output_prefix: str = "lh_report"):
    if shutil.which("lighthouse") is None:
        raise RuntimeError(" Lighthouse is not installed or not in PATH. Run: npm install -g lighthouse")

    json_path = f"{output_prefix}.report.json"

    command = [
        "lighthouse",
        url,
        "--throttling.cpuSlowdownMultiplier=4",
        "--output=json",
        f"--output-path={json_path}",
        "--quiet",
        "--chrome-flags=--headless"
    ]

    subprocess.run(" ".join(command), shell=True, check=True)
    with open(json_path, "r", encoding="utf-8") as f:
        report = json.load(f)

    audits = report.get("audits", {})
    score = report.get("categories", {}).get("performance", {}).get("score", 0) * 100

    return {
        "url": url,
        "performance_score": round(score),
        "fcp": audits.get("first-contentful-paint", {}).get("displayValue", "N/A"),
        "lcp": audits.get("largest-contentful-paint", {}).get("displayValue", "N/A"),
        "tbt": audits.get("total-blocking-time", {}).get("displayValue", "N/A"),
        "cls": audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A")
    }
