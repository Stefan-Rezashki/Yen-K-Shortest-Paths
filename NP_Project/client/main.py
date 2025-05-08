import requests

SERVER = "http://127.0.0.1:8000/yen"

def main():
    payload = {
        "nodes": ["A","B","C","D"],
        "edges": [["A","B",2], ["B","C",3], ["A","C",5], ["C","D",1]],
        "source": "A",
        "target": "D",
        "K": 3
    }
    r = requests.post(SERVER, json=payload)
    r.raise_for_status()
    for i, p in enumerate(r.json()["paths"], 1):
        print(f"{i}: {'→'.join(p['route'])} (cost={p['cost']})")

if __name__ == "__main__":
    main()