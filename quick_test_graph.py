import requests
import time

url = "http://47.108.152.16/api/kg/graph"
params = {"limit": 100, "show_all": False}

print(f"Testing: {url}")
print(f"Params: {params}")

start = time.time()
try:
    r = requests.get(url, params=params, timeout=30)
    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s")
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        nodes = len(data.get("data", {}).get("sampleNodes", []))
        rels = len(data.get("data", {}).get("sampleRelations", []))
        print(f"Nodes: {nodes}, Relations: {rels}")
    else:
        print(f"Error: {r.text[:200]}")
except requests.exceptions.Timeout:
    elapsed = time.time() - start
    print(f"TIMEOUT after {elapsed:.2f}s")
except Exception as e:
    elapsed = time.time() - start
    print(f"ERROR after {elapsed:.2f}s: {e}")

