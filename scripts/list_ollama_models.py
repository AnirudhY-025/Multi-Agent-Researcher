import httpx, json

url = 'http://localhost:11434/v1/models'
try:
    r = httpx.get(url, timeout=10)
    print('STATUS', r.status_code)
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception:
        print(r.text)
except Exception as e:
    print('ERROR', str(e))
