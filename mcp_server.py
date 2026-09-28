import sys, json
from client import DynamicPromptPrefixCache

cache = DynamicPromptPrefixCache()

def handle_jsonrpc(line):
    global cache
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-dynamic-prompt-prefix-cache-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "insert_prefix", "description": "Insert prefix tokens and associate handle.", "inputSchema": {"type": "object", "properties": {"tokens": {"type": "array"}, "cache_handle": {"type": "string"}}, "required": ["tokens", "cache_handle"]}},
                {"name": "match_prefix", "description": "Match incoming tokens against prefix trie.", "inputSchema": {"type": "object", "properties": {"tokens": {"type": "array"}}, "required": ["tokens"]}},
                {"name": "benchmark_prefix_cache", "description": "Run prefix cache benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "insert_prefix":
                res = cache.insert(args.get("tokens", []), args.get("cache_handle", "default"))
            elif tool == "match_prefix":
                res = cache.match(args.get("tokens", []))
            elif tool == "benchmark_prefix_cache":
                res = cache.benchmark_prefix_cache()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
