#!/usr/bin/env python3
"""
SubEnum V2.0 — Fast Subdomain Enumeration Tool
Author: err0rgod

Multi-threaded subdomain enumerator with HTTP/HTTPS checking,
DNS resolution fallback, and multiple output formats.
"""

import argparse
import csv
import json
import logging
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Optional, Tuple

import requests
import urllib3
from colorama import Fore, Style, init
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3.util.retry import Retry

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("subenum")


# ---------------------------------------------------------------------------
# Banner
# ---------------------------------------------------------------------------

BANNER = r"""
          __________________     _   _______  ____   ____   __ _/
         _/ __ \_  __ \_  __ \/  /_\  \_  __ \/ ___\ /  _ \ / __ |
         \  ___/|  | \/|  | \/\  \_/   \  | \/ /_/  >  <_> ) /_/ |
          \___  >__|   |__|    \_____  /__|  \___  / \____/\____ |
             \/                     \/     /_____/             \/
"""


def print_banner() -> None:
    """Print the tool banner and version info."""
    print(Fore.CYAN + BANNER + Style.RESET_ALL)
    print(" SubEnum V2.0 — Subdomain Enumeration Tool")
    print(" Author: err0rgod\n")


# ---------------------------------------------------------------------------
# HTTP session with retries
# ---------------------------------------------------------------------------

def _build_http_session() -> requests.Session:
    """Build a requests Session with retry strategy."""
    retries = Retry(total=2, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503])
    adapter = HTTPAdapter(max_retries=retries, pool_connections=50, pool_maxsize=200)
    session = requests.Session()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": "SubEnum/2.0"})
    return session


# ---------------------------------------------------------------------------
# Subdomain loading
# ---------------------------------------------------------------------------

def load_subdomains(filename: str) -> List[str]:
    """Load subdomains from a file, one per line."""
    path = Path(filename)
    if not path.exists():
        log.error("File not found: %s", filename)
        sys.exit(1)
    with path.open() as f:
        return [line.strip() for line in f if line.strip()]


# ---------------------------------------------------------------------------
# Checking
# ---------------------------------------------------------------------------

def check_subdomain(full_domain: str, delay: float = 0.0) -> Tuple[str, bool, Optional[int], Optional[str]]:
    """
    Check whether *full_domain* is alive.

    Returns (domain, is_alive, status_code, method_used).
    """
    if delay > 0:
        time.sleep(delay)

    session = _build_http_session()

    # 1) HTTPS HEAD
    for scheme in ("https", "http"):
        try:
            resp = session.head(
                f"{scheme}://{full_domain}",
                timeout=5,
                allow_redirects=True,
                verify=False,
            )
            if resp.status_code < 400:
                return full_domain, True, resp.status_code, f"HEAD/{scheme.upper()}"
        except (requests.ConnectionError, requests.Timeout, requests.RequestException):
            pass

    # 2) DNS resolution fallback
    try:
        socket.getaddrinfo(full_domain, 80, socket.AF_INET)
        return full_domain, True, None, "DNS"
    except (socket.gaierror, OSError):
        pass

    return full_domain, False, None, None


# ---------------------------------------------------------------------------
# Output writers
# ---------------------------------------------------------------------------

def write_txt(results: List[Tuple[str, int, str]], output: str) -> None:
    """Write live subdomains as plain text."""
    with open(output, "w") as f:
        for domain, code, method in results:
            f.write(f"{domain}\n")


def write_csv(results: List[Tuple[str, int, str]], output: str) -> None:
    """Write live subdomains as CSV."""
    with open(output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "status_code", "method"])
        for domain, code, method in results:
            writer.writerow([domain, code or "N/A", method or "N/A"])


def write_json(results: List[Tuple[str, int, str]], output: str) -> None:
    """Write live subdomains as JSON."""
    data = [
        {"domain": domain, "status_code": code, "method": method}
        for domain, code, method in results
    ]
    with open(output, "w") as f:
        json.dump({"live_subdomains": data, "count": len(data)}, f, indent=2)


OUTPUT_WRITERS = {
    "txt": write_txt,
    "csv": write_csv,
    "json": write_json,
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="SubEnum — Multi-threaded subdomain enumeration tool",
    )
    parser.add_argument("-f", "--file", help="Path to subdomains wordlist file")
    parser.add_argument(
        "-d", "--domain", help="Target domain (e.g., example.com)"
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=100, help="Number of threads (default: 100)"
    )
    parser.add_argument(
        "-o", "--output", default="live_subdomains.txt", help="Output file (default: live_subdomains.txt)"
    )
    parser.add_argument(
        "--format",
        choices=["txt", "csv", "json"],
        default="txt",
        help="Output format (default: txt)",
    )
    parser.add_argument(
        "-nc", "--no-color", action="store_true", help="Disable colored output"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose debug logging"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Delay in seconds between requests (default: 0.0)",
    )
    return parser.parse_args(argv)


def prompt_required(prompt_text: str, field_name: str) -> str:
    """Prompt the user for required input."""
    value = input(f"{prompt_text}: ").strip()
    while not value:
        value = input(f"Please enter a valid {field_name}: ").strip()
    return value


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> None:
    """Entry point."""
    print_banner()
    args = parse_args(argv)

    if args.verbose:
        log.setLevel(logging.DEBUG)

    use_color = not args.no_color

    # Get subdomains file
    subdomains_file = args.file or prompt_required(
        "Enter the path to the subdomains .txt file", "path"
    )
    # Get domain
    domain = args.domain or prompt_required(
        "Enter the main domain (e.g., example.com)", "domain"
    )

    subdomains = load_subdomains(subdomains_file)
    if not subdomains:
        log.warning("No subdomains loaded — nothing to check.")
        sys.exit(0)

    full_domains = [f"{sub}.{domain}" for sub in subdomains]
    log.info("Loaded %d subdomains — starting scan with %d threads", len(subdomains), args.threads)
    print()

    live_results: List[Tuple[str, int, str]] = []
    total, live_count, dead_count = len(full_domains), 0, 0

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {
            executor.submit(check_subdomain, fd, args.delay): fd
            for fd in full_domains
        }

        with tqdm(total=total, desc="Scanning", unit="sub") as pbar:
            for future in as_completed(futures):
                try:
                    domain_name, is_live, status_code, method = future.result()
                    if is_live:
                        live_count += 1
                        live_results.append((domain_name, status_code or 0, method or "DNS"))
                        msg = f"[LIVE]  {domain_name}"
                        extra = f" ({status_code}, {method})" if status_code else f" ({method})"
                        if use_color:
                            tqdm.write(f"{Fore.GREEN}{msg}{extra}{Style.RESET_ALL}")
                        else:
                            tqdm.write(f"{msg}{extra}")
                    else:
                        dead_count += 1
                        if args.verbose:
                            msg = f"[DEAD]  {domain_name}"
                            if use_color:
                                tqdm.write(f"{Fore.LIGHTYELLOW_EX}{msg}{Style.RESET_ALL}")
                            else:
                                tqdm.write(msg)
                except Exception as e:
                    log.debug("Error processing subdomain: %s", e)
                finally:
                    pbar.update(1)

    # Write output
    writer = OUTPUT_WRITERS.get(args.format, write_txt)
    writer(live_results, args.output)
    log.info(
        "Done — %d live / %d dead — results saved to %s (%s)",
        live_count,
        dead_count,
        args.output,
        args.format.upper(),
    )


# ---------------------------------------------------------------------------
# Entry
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
