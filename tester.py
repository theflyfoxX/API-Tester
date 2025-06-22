# tester.py
import asyncio
import httpx
import time
from metrics import summarize_metrics

async def send_request(client, url, method):
    start = time.perf_counter()
    try:
        response = await client.request(method, url)
        duration = time.perf_counter() - start
        return (response.status_code, duration)
    except Exception:
        return ("ERROR", 0)

async def run_load_test(url, total, concurrency, method):
    semaphore = asyncio.Semaphore(concurrency)
    results = []

    async with httpx.AsyncClient(timeout=10.0) as client:
        async def worker():
            async with semaphore:
                result = await send_request(client, url, method)
                results.append(result)

        await asyncio.gather(*[worker() for _ in range(total)])

    return results

def run_test(url, total, concurrency, method, report=None):
    results = asyncio.run(run_load_test(url, total, concurrency, method))
    
    total_r = len(results)
    successes = [r for r in results if isinstance(r[0], int) and r[0] < 400]
    failures = total_r - len(successes)
    latencies = [r[1] for r in successes]

    metrics = {
        "url": url,
        "total": total_r,
        "success": len(successes),
        "failures": failures,
        "avg_latency": round(sum(latencies)/len(latencies), 3) if latencies else None,
        "min_latency": round(min(latencies), 3) if latencies else None,
        "max_latency": round(max(latencies), 3) if latencies else None
    }

    return metrics
