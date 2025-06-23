import json
from tool_registry import TOOL_REGISTRY

def simple_router(query: str):
    keywords = ["summary", "average", "cpu", "gpu", "queue", "utilization", "report"]
    if any(word in query.lower() for word in keywords):
        return "slack_summary"
    return None


def main():
    print("Enter a time window to summarize system usage:")
    user_query = input(">> ")

    tool_name = simple_router(user_query)
    if tool_name:
        args = {}
        for arg in TOOL_REGISTRY[tool_name]["args"]:
            val = input(f"Enter value for {arg}: ")
            args[arg] = val

        result = TOOL_REGISTRY[tool_name]["function"](**args)
        print("\n--- Answer ---")
        print(result)
    else:
        print("Sorry, I don't know how to help with that yet.")

if __name__ == "__main__":
    main()
