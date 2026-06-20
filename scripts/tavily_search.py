#!/usr/bin/env python3
"""
tavily_search.py — Search Tavily for existing Pandoc Lua filter solutions.

RED phase workflow: when test_pandoc_and_lua_registry.py::TestLuaFilterRegistry
fails because an unregistered custom filter exists, use this script to search
for existing solutions before writing bespoke code.

Usage:
    python scripts/tavily_search.py "pandoc lua filter reveal.js audio autoplay"
    python scripts/tavily_search.py "pandoc lua filter youtube embed iframe"
    python scripts/tavily_search.py --save "search query"

    --save: also write results to a JSON file for registry reference

Exit codes:
    0 — no existing solution found (OK to write custom code)
    1 — existing solution found (use it instead)
    2 — search error
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from tavily import TavilyClient


def search(query: str) -> dict:
    """Run a Tavily search for existing Lua filter solutions."""
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    # Add context to the query if it's not already there
    if "pandoc" not in query.lower():
        query = f"pandoc lua filter {query}"
    if "existing" not in query.lower() and "alternative" not in query.lower():
        query = f"{query} existing alternative library"

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=10,
        include_answer=True,
        include_raw_content=True,
    )

    return response


def analyze_results(response: dict) -> dict:
    """Determine if any result is a pre-existing solution worth using."""
    answer = response.get("answer", "")

    # Keywords suggesting an existing solution was found
    existing_indicators = [
        "github.com/pandoc/lua-filters",
        "github.com/pandoc-ext",
        "pandoc lua filter",
        "lua filter for pandoc",
        "available filter",
        "you can use",
        "there is a filter",
        "pandoc provides",
        "built-in support",
        "natively supported",
    ]

    results = response.get("results", [])
    high_score_results = [r for r in results if r.get("score", 0) > 0.5]

    existing_found = False
    relevant_results = []

    for r in high_score_results:
        title = r.get("title", "")
        url = r.get("url", "")
        content = r.get("content", "")

        # Check indicators
        has_indicator = any(ind in (title + content).lower() for ind in existing_indicators)
        if has_indicator:
            existing_found = True
            relevant_results.append(r)

    return {
        "existing_found": existing_found,
        "answer": answer,
        "relevant_count": len(relevant_results),
        "results": [
            {
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "score": r.get("score", 0),
                "snippet": r.get("content", "")[:300],
            }
            for r in relevant_results
        ],
        "total_results": len(results),
    }


def main():
    save = False
    args = sys.argv[1:]

    if "--save" in args:
        save = True
        args.remove("--save")

    if not args:
        print(__doc__)
        sys.exit(2)

    query = " ".join(args)
    print(f"Searching: {query}")
    print()

    try:
        response = search(query)
    except Exception as e:
        print(f"Search error: {e}", file=sys.stderr)
        sys.exit(2)

    analysis = analyze_results(response)

    if save:
        output = {
            "query": query,
            "date": __import__("datetime").datetime.now().strftime("%Y-%m-%d"),
            "answer": analysis["answer"],
            "results": analysis["results"],
            "existing_found": analysis["existing_found"],
            "total_results": analysis["total_results"],
        }
        out_path = (
            f"tavily_search_{__import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Saved to: {out_path}")

    print("=== AI Answer ===")
    print(analysis["answer"] or "(none)")
    print()

    if analysis["existing_found"]:
        print("✖  EXISTING SOLUTION(S) FOUND")
        print(f"   {analysis['relevant_count']} relevant result(s) at score > 0.5")
        print()
        for r in analysis["results"]:
            print(f"   • {r['title']}")
            print(f"     {r['url']}")
            print(f"     Score: {r['score']}")
            print(f"     {r['snippet']}")
            print()
        print("Action: Use the existing solution instead of writing custom code.")
        sys.exit(1)
    else:
        print(f"✔  No existing solution found ({analysis['total_results']} total results)")
        print()
        print("Action: OK to write custom code. Then update lua-filter-registry.json")
        print("with the search query, date, and justification.")
        sys.exit(0)


if __name__ == "__main__":
    main()
