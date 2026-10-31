import json
from target import ask_target, SECRET
from payloads import PAYLOADS

RUNS = 5
results = []

for p in PAYLOADS:
    leaks = 0
    example = None
    for _ in range(RUNS):
        reply = ask_target(p["prompt"])
        if SECRET.lower() in reply.lower():
            leaks += 1
            if example is None:
                example = reply
    results.append({
        "category": p["category"],
        "prompt": p["prompt"],
        "leaks": leaks,
        "runs": RUNS,
        "example_leak": example,
    })
    print(f"{p['category']:<20} {leaks}/{RUNS} leaked")

total = sum(r["leaks"] for r in results)
print(f"\nOverall: {total}/{RUNS * len(PAYLOADS)} attempts leaked")

with open("results.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Saved results.json")
