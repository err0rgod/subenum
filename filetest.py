import requests

def load_subdomains(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def check_subdomain(subdomain):
    try:
        response = requests.get(f"http://{subdomain}", timeout=3)
        return response.status_code < 400
    except Exception:
        return False

def main():
    subdomains_file = input("Enter the path to the subdomains .txt file: ")
    subdomains = load_subdomains(subdomains_file)
    domain = input("Enter the main domain (e.g., example.com): ")
    live_subdomains = []

    print("\nTesting subdomains...\n")
    for sub in subdomains:
        full_domain = f"{sub}.{domain}"
        if check_subdomain(full_domain):
            print(f"[LIVE] {full_domain}")
            live_subdomains.append(full_domain)
        else:
            print(f"[DEAD] {full_domain}")

    output_file = "live_subdomains.txt"
    with open(output_file, 'w') as f:
        for live in live_subdomains:
            f.write(live + "\n")
    print(f"\nLive subdomains saved to {output_file}")

if __name__ == "__main__":
    main()