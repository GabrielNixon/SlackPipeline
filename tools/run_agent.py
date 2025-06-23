from router import simple_router, parse_natural_date_range
from tool_registry import TOOL_REGISTRY

def main():
    print("Enter a time window to summarize system usage:")
    query = input(">> ")

    tool_name = simple_router(query)
    if not tool_name:
        print("Sorry, I don't understand that yet.")
        return

    try:
        start, end = parse_natural_date_range(query)
        target = "summary"
        if "cpu" in query.lower():
            target = "cpu"
        elif "gpu" in query.lower():
            target = "gpu"
        elif "down" in query.lower():
            target = "down"

        result = TOOL_REGISTRY[tool_name]["function"](
            start_date=start.strftime("%Y-%m-%d"),
            end_date=end.strftime("%Y-%m-%d"),
            target=target
        )
        print("\n--- Answer ---")
        print(result)

    except Exception as e:
        print("Error parsing input:", e)

if __name__ == "__main__":
    main()
