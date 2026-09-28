"""MCP stdio server for Geohash Engine."""
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import GeohashEngine

def handle_rpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "encode_geohash",
                        "description": "Encode lat/lon coordinate into base32 geohash string",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "latitude": {"type": "number"},
                                "longitude": {"type": "number"},
                                "precision": {"type": "integer", "default": 9}
                            },
                            "required": ["latitude", "longitude"]
                        }
                    },
                    {
                        "name": "decode_geohash",
                        "description": "Decode base32 geohash string into lat/lon coordinate",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "geohash": {"type": "string"}
                            },
                            "required": ["geohash"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "encode_geohash":
            lat = float(args.get("latitude"))
            lon = float(args.get("longitude"))
            p = int(args.get("precision", 9))
            res = GeohashEngine.encode(lat, lon, p)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"geohash": res, "precision": p}}
        elif name == "decode_geohash":
            gh = args.get("geohash")
            lat, lon = GeohashEngine.decode(gh)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"latitude": lat, "longitude": lon}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {name} not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_rpc(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
