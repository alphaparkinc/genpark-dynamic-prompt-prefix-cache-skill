from typing import List, Dict, Any

class DynamicPromptPrefixCache:
    def __init__(self):
        self.root: Dict[str, Any] = {}

    def insert(self, tokens: List[str], cache_handle: str) -> Dict[str, Any]:
        curr = self.root
        for tok in tokens:
            if tok not in curr:
                curr[tok] = {}
            curr = curr[tok]
        curr["__handle__"] = cache_handle
        return {"status": "inserted", "cache_handle": cache_handle, "prefix_length": len(tokens)}

    def match(self, tokens: List[str]) -> Dict[str, Any]:
        curr = self.root
        matched = []
        longest_handle = None
        for tok in tokens:
            if tok in curr:
                curr = curr[tok]
                matched.append(tok)
                if "__handle__" in curr:
                    longest_handle = curr["__handle__"]
            else:
                break
        match_len = len(matched)
        total_len = len(tokens)
        hit_ratio = match_len / total_len if total_len > 0 else 0.0
        return {
            "longest_cache_handle": longest_handle,
            "matched_tokens_count": match_len,
            "total_prompt_tokens": total_len,
            "prefix_hit_ratio": round(hit_ratio, 4),
            "estimated_ttft_reduction_pct": round(hit_ratio * 80.0, 2)
        }

    def benchmark_prefix_cache(self) -> Dict[str, Any]:
        sys_tokens = ["System:", "You", "are", "a", "strict", "compiler", "agent", "for", "Python."]
        self.insert(sys_tokens, "h_sys_compiler_v1")
        test_prompt = sys_tokens + ["Analyze", "the", "AST", "syntax", "tree."]
        return self.match(test_prompt)
