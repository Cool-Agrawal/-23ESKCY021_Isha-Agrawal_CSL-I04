"""Small wrapper for the dictionary attack experiment."""
from auditor import dictionary_attack

def run_dictionary_attack(service="telnet", username="admin"):
    return dictionary_attack(service, username)

if __name__ == "__main__":
    service = input("Service (telnet/http): ").strip().lower()
    username = input("Username to test [admin]: ").strip() or "admin"
    print(run_dictionary_attack(service, username))
