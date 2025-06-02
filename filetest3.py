import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

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
    parser = argparse.ArgumentParser(description="Subdomain checker")
    parser.add_argument('-f', '--file', default='subdomains-1000.txt', help='Subdomains file')
    parser.add_argument('-t', '--threads', type=int, default=20, help='Number of threads')
    parser.add_argument('-o', '--output', default='live_subdomains.txt', help='Output file')
    parser.add_argument('-d', '--domain', required=False, help='Main domain (e.g., example.com)')
    args = parser.parse_args()

    subdomains = load_subdomains(args.file)
    if args.domain:
        domain = args.domain
    else:
        domain = input("Enter the main domain (e.g., example.com): ")
    live_subdomains = []

    print("\nTesting subdomains...\n")
    full_domains = [f"{sub}.{domain}" for sub in subdomains]

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_domain = {executor.submit(check_subdomain, d): d for d in full_domains}
        for future in as_completed(future_to_domain):
            full_domain, is_live = future.result()
            if is_live:
                print(f"[LIVE] {full_domain}")
                live_subdomains.append(full_domain)
            else:
                print(f"[DEAD] {full_domain}")

    with open(args.output, 'w') as f:
        for live in live_subdomains:
            f.write(live + "\n")
    print(f"\nLive subdomains saved to {args.output}")

if __name__ == "__main__":
    main()