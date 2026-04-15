from Domain_1_Astronomy.system_controller import SystemController
import json


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


if __name__ == "__main__":

    print_section("FULL SYSTEM TEST INITIALIZING")

    controller = SystemController()

    user_query = input("Enter your query: ")

    print_section("SYSTEM EXECUTION STARTED")

    result = controller.handle_query(user_query)

    print_section("SYSTEM RESULT")

    print(json.dumps(result, indent=2))

    print_section("FULL SYSTEM TEST COMPLETE")