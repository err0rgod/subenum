import requests
from concurrent.futures import ThreadPoolExecutor
import argparse
from tqdm import tqdm
from colorama import Fore, Style, init
import urllib3

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_subdomains(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def check_subdomain(full_domain):
    try:
        response = requests.head(f"http://{full_domain}", timeout=3, allow_redirects=True)
        return full_domain, response.status_code < 400
    except Exception:
        return full_domain, False

def main():
    parser = argparse.ArgumentParser(description="Subdomain checker")
    parser.add_argument('-f', '--file', default='subdomains-1000.txt', help='Subdomains file')
    parser.add_argument('-t', '--threads', type=int, default=100, help='Number of threads')
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
        results = list(tqdm(executor.map(check_subdomain, full_domains), total=len(full_domains), desc="Overall Progress"))
        for full_domain, is_live in results:
            if is_live:
                print(f"{Fore.GREEN}[LIVE]{Style.RESET_ALL} {full_domain}")
                live_subdomains.append(full_domain)
            else:
                print(f"{Fore.LIGHTYELLOW_EX}[DEAD]{Style.RESET_ALL} {full_domain}")

    with open(args.output, 'w') as f:
        for live in live_subdomains:
            f.write(live + "\n")
    print(f"\nLive subdomains saved to {args.output}")

if __name__ == "__main__":
    main()