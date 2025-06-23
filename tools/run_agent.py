from tool_registry import TOOL_REGISTRY
from router import simple_router, parse_natural_date_range

def main():
    print("Enter a time window to summarize system usage:")
    user_query = input(">> ")

    tool_name = simple_router(user_query)
    if tool_name:
        start, end = parse_natural_date_range(user_query)

        args = {}
        for arg in TOOL_REGISTRY[tool_name]["args"]:
            if arg == "start_date" and not start:
                val = input("Enter start date (YYYY-MM-DD): ")
                args[arg] = val
            elif arg == "end_date" and not end:
                val = input("Enter end date (YYYY-MM-DD): ")
                args[arg] = val
            elif arg == "start_date":
                args[arg] = start.strftime("%Y-%m-%d")
            elif arg == "end_date":
                args[arg] = end.strftime("%Y-%m-%d")
            else:
                val = input(f"Enter value for {arg}: ")
                args[arg] = val

        result = TOOL_REGISTRY[tool_name]["function"](**args)
        print("\n--- Answer ---")
        print(result)
    else:
        print("Sorry, I don't know how to help with that yet.")

if __name__ == "__main__":
    main()
