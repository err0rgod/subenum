import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_subdomains(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def check_subdomain(full_domain):
    try:
        response = requests.get(f"http://{full_domain}", timeout=3)
        return full_domain, response.status_code < 400
    except Exception:
        return full_domain, False

def main():
    subdomains_file = input("Enter the path to the subdomains .txt file (default: subdomains-1000.txt): ")
    if not subdomains_file.strip():
        subdomains_file = "subdomains-1000.txt"
    subdomains = load_subdomains(subdomains_file)
    domain = input("Enter the main domain (e.g., example.com): ")
    live_subdomains = []

    print("\nTesting subdomains...\n")
    full_domains = [f"{sub}.{domain}" for sub in subdomains]

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_domain = {executor.submit(check_subdomain, d): d for d in full_domains}
        for future in as_completed(future_to_domain):
            full_domain, is_live = future.result()
            if is_live:
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