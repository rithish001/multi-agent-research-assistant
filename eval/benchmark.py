import json
import time

from graph.graph_builder import app

# Load sample queries
with open("eval/sample_queries.json", "r") as f:
    queries = json.load(f)

results = []

for query in queries:

    print(f"\nRunning Query: {query}")

    start_time = time.time()

    response = app.invoke({"query": query})

    end_time = time.time()

    final_output = response.get("final", "")

    latency = round(end_time - start_time, 2)

    result = {
        "query": query,
        "latency_seconds": latency,
        "output_length": len(final_output),
        "final_output": final_output[:500]  # store preview only
    }

    results.append(result)

# Save benchmark results
with open("eval/results.json", "w") as f:
    json.dump(results, f, indent=4)

print("\n✅ Benchmark completed")