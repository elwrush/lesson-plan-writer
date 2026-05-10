import os, sys, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from tavily import TavilyClient

client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

response = client.search(
    query="Apple video subtitles formatting design animation highlights pop technique",
    search_depth="advanced",
    max_results=8,
    include_answer=True,
    include_raw_content=False,
)

print("=== AI ANSWER ===")
print(response.get("answer", "(none)"))
print()

for r in response["results"]:
    print(f"--- {r['title']} ---")
    print(f"URL: {r['url']}")
    print(f"Score: {r['score']}")
    print(f"Snippet: {r['content']}")
    print()