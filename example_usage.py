from client import DynamicPromptPrefixCache

def run_example():
    print("=== GenPark Dynamic Prompt Prefix Cache Example ===")
    cache = DynamicPromptPrefixCache()
    cache.insert(["Role:", "Financial", "Analyst", "Rule:", "GAAP"], "handle_fin_analyst")
    query = ["Role:", "Financial", "Analyst", "Rule:", "GAAP", "Summarize", "Q3", "10-Q"]
    res = cache.match(query)
    print("Matched Handle:", res["longest_cache_handle"])
    print("TTFT Reduction (%):", res["estimated_ttft_reduction_pct"])

if __name__ == "__main__":
    run_example()
