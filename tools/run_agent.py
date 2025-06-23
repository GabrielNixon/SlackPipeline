from router import simple_router
from tool_registry import TOOL_REGISTRY

def main():
    print("Hi! What would you like to know about the system?")
    print("You can ask about CPU/GPU usage, summaries for last month/week, or how many days the system was underloaded.")
    query = input(">> ")

    try:
        tool_name, params = simple_router(query)
        if tool_name:
            result = TOOL_REGISTRY[tool_name]["function"](**params)
            print("\n--- Answer ---")
            print(result)
        else:
            print("Sorry, I don't understand that question yet.")
    except Exception as e:
        print(f"Error parsing input: {e}")

if __name__ == "__main__":
    main()
