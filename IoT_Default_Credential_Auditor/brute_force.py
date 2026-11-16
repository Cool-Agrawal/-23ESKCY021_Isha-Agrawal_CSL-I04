"""
Bounded brute-force demonstration based on the mapped lab experiment.
This is an offline simulation only; it does not send guesses to any service.
"""
CHARSET = "ABCD"
MAX_LENGTH = 5
MAX_ATTEMPTS = 1500

def brute_force_demo(target):
    attempts = 0
    found = None

    def generate(prefix, length):
        nonlocal attempts, found
        if found is not None or attempts >= MAX_ATTEMPTS:
            return
        if len(prefix) == length:
            attempts += 1
            if prefix == target:
                found = prefix
            return
        for char in CHARSET:
            generate(prefix + char, length)
            if found is not None or attempts >= MAX_ATTEMPTS:
                return

    if not target or len(target) > MAX_LENGTH or any(c not in CHARSET for c in target):
        return {"status": "TARGET OUTSIDE DEMO SEARCH SPACE", "attempts": 0, "match": ""}
    for length in range(1, MAX_LENGTH + 1):
        generate("", length)
        if found is not None or attempts >= MAX_ATTEMPTS:
            break
    return {"status": "MATCH FOUND" if found else "NOT FOUND WITHIN LIMIT",
            "attempts": attempts, "match": found or ""}

if __name__ == "__main__":
    target = input("Enter a demo password using A-D (max 5 chars): ").strip().upper()
    print(brute_force_demo(target))
