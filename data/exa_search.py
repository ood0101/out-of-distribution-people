#!/usr/bin/env python3
"""Exa search helper for research agents. Usage:
    python3 data/exa_search.py "query string" [num_results]
    python3 data/exa_search.py --contents "query string" [num_results]
"""
import sys
import json
from exa_py import Exa

EXA_API_KEY = "5d577a60-de6a-4b86-8a8b-ccbb8a3b7393"

def search(query, num_results=5, get_contents=False):
    exa = Exa(api_key=EXA_API_KEY)
    if get_contents:
        result = exa.search_and_contents(query, num_results=num_results, text=True, highlights=True)
    else:
        result = exa.search(query, num_results=num_results, type='auto')

    output = []
    for r in result.results:
        entry = {"title": r.title, "url": r.url, "score": getattr(r, 'score', None)}
        if hasattr(r, 'text') and r.text:
            entry["text"] = r.text[:2000]
        if hasattr(r, 'highlights') and r.highlights:
            entry["highlights"] = r.highlights
        output.append(entry)
    return output

if __name__ == "__main__":
    get_contents = "--contents" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--contents"]
    query = args[0] if args else "test"
    num = int(args[1]) if len(args) > 1 else 5

    results = search(query, num, get_contents)
    print(json.dumps(results, indent=2, ensure_ascii=False))
