# metrics.py
import json

def summarize_metrics(results, report_path=None):
    total = len(results)
    successes = [r for r in results if isinstance(r[0], int) and r[0] < 400]
    failures = [r for r in results if r[0] == "ERROR" or (isinstance(r[0], int) and r[0] >= 400)]
    latencies = [r[1] for r in successes]

    print("\n=== Test Summary ===")
    print(f"Total Requests: {total}")
    print(f"Success: {len(successes)}")
    print(f"Failures: {len(failures)}")

    if latencies:
        avg = sum(latencies) / len(latencies)
        print(f"Average Latency: {avg:.3f}s")
        print(f"Max Latency: {max(latencies):.3f}s")
        print(f"Min Latency: {min(latencies):.3f}s")

    if report_path:
        report = {
            "total": total,
            "success": len(successes),
            "failures": len(failures),
            "avg_latency": round(sum(latencies)/len(latencies), 3) if latencies else None
        }
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to {report_path}")
