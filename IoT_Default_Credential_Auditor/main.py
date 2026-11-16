"""Command-line launcher for the IoT Default-Credential Auditor."""
import threading
import time
from pathlib import Path
from telnet_emulator import start_server as start_telnet
from http_emulator import start_server as start_http
from auditor import audit_service, dictionary_attack, weak_password_check, save_report
from brute_force import brute_force_demo

def start_lab():
    threading.Thread(target=start_telnet, daemon=True).start()
    threading.Thread(target=start_http, daemon=True).start()
    time.sleep(0.4)

def show_menu():
    print("\n" + "=" * 54)
    print("          IoT DEFAULT-CREDENTIAL AUDITOR")
    print("=" * 54)
    print("1. Check Telnet default credentials")
    print("2. Check HTTP default credentials")
    print("3. Run dictionary attack on local service")
    print("4. Run bounded brute-force simulation")
    print("5. Analyze password strength")
    print("6. Run complete audit and generate CSV report")
    print("7. Exit")

def main():
    start_lab()
    print("Local lab services started on 127.0.0.1.")
    report_rows = []
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            result = audit_service("telnet")
            report_rows.append(result)
            print(result)
        elif choice == "2":
            result = audit_service("http")
            report_rows.append(result)
            print(result)
        elif choice == "3":
            service = input("Service (telnet/http): ").strip().lower()
            if service not in {"telnet", "http"}:
                print("Please enter telnet or http.")
                continue
            username = input("Username [admin]: ").strip() or "admin"
            result = dictionary_attack(service, username)
            print(result)
            report_rows.append({"service": result["service"], "status": result["status"],
                                "username": username, "password": result["password"],
                                "detail": f"Dictionary attempts: {result['attempts']}"})
        elif choice == "4":
            target = input("Demo password using A-D, maximum 5 characters: ").strip().upper()
            print(brute_force_demo(target))
        elif choice == "5":
            password = input("Enter a dummy password: ")
            print(weak_password_check(password))
        elif choice == "6":
            telnet_result = audit_service("telnet")
            http_result = audit_service("http")
            report_rows.extend([telnet_result, http_result])
            path = save_report(report_rows)
            print("\nAudit completed.")
            print("Telnet:", telnet_result["status"])
            print("HTTP:", http_result["status"])
            print("Report saved to:", path)
        elif choice == "7":
            print("Exiting the auditor. Lab services will stop.")
            break
        else:
            print("Invalid choice. Select 1-7.")

if __name__ == "__main__":
    main()
