import requests
from concurrent.futures import ThreadPoolExecutor
import argparse
from tqdm import tqdm
from colorama import Fore, Style, init
import urllib3



print(r"          __________________     _   _______  ____   ____   __ _/")
print(r"         _/ __ \_  __ \_  __ \/  /_\  \_  __ \/ ___\ /  _ \ / __ | ")
print(r"         \  ___/|  | \/|  | \/\  \_/   \  | \/ /_/  >  <_> ) /_/ | ")
print(r"          \___  >__|   |__|    \_____  /__|  \___  / \____/\____ | ")
print(r"             \/                     \/     /_____/             \/ ")


print("Subenum V1.0 - Subdomain Enumeration Tool")
print("Author: err0rgod")


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
    parser.add_argument('-nc', '--no-color', action='store_true', help='Disable colored output')
    args = parser.parse_args()

    use_color = not args.no_color

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
                if use_color:
                    print(f"{Fore.GREEN}[LIVE] {full_domain}{Style.RESET_ALL}")
                else:
                    print(f"[LIVE] {full_domain}")
                live_subdomains.append(full_domain)
            else:
                if use_color:
                    print(f"{Fore.LIGHTYELLOW_EX}[DEAD] {full_domain}{Style.RESET_ALL}")
                else:
                    print(f"[DEAD] {full_domain}")

    with open(args.output, 'w') as f:
        for live in live_subdomains:
            f.write(live + "\n")
    print(f"\nLive subdomains saved to {args.output}")

if __name__ == "__main__":
    main()