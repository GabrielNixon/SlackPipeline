from router import simple_router
from tool_registry import TOOL_REGISTRY

def main():
    print("Enter a time window to summarize system usage:")
    user_query = input(">> ")

    parsed = simple_router(user_query)
    tool_name = parsed["tool"]
    args = parsed["args"]

    if not args["start_date"] or not args["end_date"]:
        args["start_date"] = input("Enter start date (YYYY-MM-DD): ")
        args["end_date"] = input("Enter end date (YYYY-MM-DD): ")

    result = TOOL_REGISTRY[tool_name]["function"](**args)
    print("\n--- Answer ---")
    print(result)

if __name__ == "__main__":
    main()
