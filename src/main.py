from tool_manager import check_tool, install, update
import string

def main():
    while True:
        print("\n--- Automated Tool Manager ---")
        print("1. Check tool")
        print("2. Install tool")
        print("3. Update tool")
        print("q. Quit")

        choice = input("Choose an option: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        if choice == "1":
            tool_name = input("Enter tool name: ").strip().lower()
            result = check_tool(tool_name)
            print(result)

        elif choice == "2":
            tool_name = input("Enter tool name: ").strip().lower()
            result = install(tool_name)
            print(result)

        elif choice == "3":
            tool_name = input("Enter tool name: ").strip().lower()
            result = update(tool_name)
            print(result)

        else:
            print("Invalid option. Please choose 1, 2, 3, or q.")

if __name__ == "__main__":
    main()
