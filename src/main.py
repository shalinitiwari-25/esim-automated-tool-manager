from tool_manager import check_tool, install, update, list_tools, get_tool_info, check_update, update_with_check
import string

def main():
    while True:
        print("\n--- Automated Tool Manager ---")
        print("1. Check tool")
        print("2. Install tool")
        print("3. Update tool (check + update)")
        print("4. List supported tools")
        print("5. Check for updates only")
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
            result = update_with_check(tool_name)
            print(result)
        
        elif choice == "4":
            print("\nSupported tools:")

            for tool in list_tools():
                print(get_tool_info(tool))

        elif choice == "5":
            tool_name = input("Enter tool name: ").strip().lower()
            result = check_update(tool_name)
            print(result)

        else:
            print("Invalid option. Please choose 1, 2, 3, or q.")

if __name__ == "__main__":
    main()
