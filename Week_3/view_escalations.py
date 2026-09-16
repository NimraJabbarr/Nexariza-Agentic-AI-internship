import json
from pathlib import Path

def load_jsonl(path):
    if not Path(path).exists():
        print(f"⚠️ {path} abhi tak nahi bana — koi escalation nahi hui hai.")
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

escalations = load_jsonl("escalations.json")

print(f"\n📋 Total Escalations: {len(escalations)}\n")
for e in escalations:
    print(f"ID: {e['id']}")
    print(f"Time: {e['timestamp']}")
    print(f"User: {e.get('user_name', 'Anonymous')}")
    print(f"Q: {e['question']}")
    print(f"Bot Answer: {e['bot_answer'][:150]}...")
    print("-" * 60)