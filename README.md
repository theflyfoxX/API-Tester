

# 🚀 API + Frontend Performance Tester CLI

A powerful command-line tool for **stress testing APIs** and **auditing frontend performance** — all from one unified interface.

- ✅ Load test any HTTP API with concurrency
- 🌐 Audit frontend metrics (LCP, CLS, TBT, etc.) using Lighthouse
- 📊 Save results in a single combined JSON report
- 💄 Terminal-friendly UX for Linux-style scripting

---

## 📦 Features

- 🧪 **API Load Testing**
  - Async HTTP requests with configurable concurrency
  - Measures success rate, latency (avg, min, max), failures

- 🌍 **Frontend Audits (Lighthouse)**
  - LCP, FCP, CLS, TBT, Speed Index
  - Emulates mobile device + CPU/network throttling

- 🗃 **Combined Reporting**
  - Outputs a single JSON file with both API and frontend results

- 🎛 **CLI Options**
  - Linux-style flags for flexibility
  - Easily scriptable for CI or batch usage

---

## 🛠 Installation

> **Python 3.8+ required**  
> **Node.js required** (for Lighthouse)

1. Clone the repo:
```bash
git clone https://github.com/theflyfoxX/API-Tester.git
cd api-perf-cli
````

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install Lighthouse (global):

```bash
npm install -g lighthouse
```

---

## 🚀 Usage

### ▶️ Run API-only test:

```bash
python main.py test --url https://httpbin.org/get --requests 100 --concurrency 10
```

### 🌐 Run API + Frontend audit:

```bash
python main.py test --url https://example.com --requests 100 --concurrency 20 --frontend --output report.json
```

---

## 📄 Example Report (`report.json`)

```json
{
  "api_test": {
    "url": "https://httpbin.org/get",
    "total": 100,
    "success": 100,
    "failures": 0,
    "avg_latency": 0.124,
    "min_latency": 0.092,
    "max_latency": 0.301
  },
  "frontend_audit": {
    "url": "https://example.com",
    "performance_score": 37,
    "fcp": "9.9 s",
    "lcp": "10.6 s",
    "tbt": "550 ms",
    "cls": "0.137"
  }
}
```

---

## 📁 File Structure

```
api_tester/
├── main.py               # CLI entrypoint
├── tester.py             # API load testing logic
├── metrics.py            # Metrics and summary
├── lighthouse_runner.py  # Lighthouse integration
├── requirements.txt
└── README.md
```

---

## 📚 To Do / Coming Soon

* [ ] Support for custom headers and payloads
* [ ] Real-time progress bar with `rich`
* [ ] Upload results to a dashboard
* [ ] CI-friendly output mode (no colors)



