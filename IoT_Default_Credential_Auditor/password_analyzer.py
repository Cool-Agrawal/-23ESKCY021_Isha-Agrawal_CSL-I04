"""Simple educational password-strength rules."""
from auditor import weak_password_check

if __name__ == "__main__":
    password = input("Enter a dummy lab password to analyze: ")
    print(weak_password_check(password))
