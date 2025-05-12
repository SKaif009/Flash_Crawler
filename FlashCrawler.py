#!/usr/bin/env python3
"""
FlashCrawler – Colorful BFS Web Crawler with parameter pattern deduplication
"""
import os
import time
import argparse
from pathlib import Path
from collections import deque
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from rich import box
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

# ────────────── Configuration ────────────── #
console = Console()
parser = argparse.ArgumentParser(
    description="""
⚡ FlashCrawler – Colorful BFS Web Crawler
Crawl websites using a breadth-first search approach and discover all reachable URLs.
""",
    epilog="""
Examples:

  python FlashCrawler.py -u https://example.com
  python FlashCrawler.py -l urls.txt -d 60 -s
  python FlashCrawler.py -u https://example.com --save -t 3

GitHub: https://github.com/SKaif009,  Author : BlackForgeX
""",
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument("-u", "--url", help="Single target URL to crawl")
parser.add_argument("-l", "--list", help="File containing list of URLs to crawl")
parser.add_argument("-d", "--depth", type=int, default=50, help="Max number of pages to crawl (default: 50)")
parser.add_argument("-t", "--time", type=int, default=0, help="Delay between requests in seconds (default: 0)")
parser.add_argument("-s", "--save", action="store_true", help="Save found URLs to 'results/' folder")
parser.add_argument("--req-timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
parser.add_argument("--dedup-params", action="store_true", help="Only crawl one URL per query pattern signature")
args = parser.parse_args()

HEADERS = {"User-Agent": "FlashCrawler/1.0 (+https://github.com/you)"}
TIMEOUT = args.req_timeout
MAX_PAGES = args.depth
DELAY = args.time
SAVE_RESULTS = args.save
DEDUP_PARAM_SIG = args.dedup_params

results_dir = Path("results")
results_dir.mkdir(exist_ok=True)

visited = set()
queue = deque()
found = set()
allowed_domains = set()
seen_param_signatures = set()

# ────────────── Setup URLs ────────────── #
def load_urls():
    urls = set()
    if args.url:
        urls.add(args.url)
    if args.list:
        try:
            with open(args.list, "r") as f:
                urls.update(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            console.print(f"[red]✖ File not found:[/] {args.list}")
            exit(1)
    if not urls:
        console.print("[red]✖ Provide at least one URL with -u or -l[/]")
        exit(1)
    for u in urls:
        allowed_domains.add(urlparse(u).netloc)
    queue.extend(urls)

# ────────────── Helpers ────────────── #
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    ascii_art = r"""FLASH CRAWLER""".strip("\n")
    console.print(f"[bold yellow] ⚡ [/]" +
                  f"[bold bright_magenta]{ascii_art}[/]" +
                  f"[bold yellow] ⚡ [/]", justify="center")
    console.rule("[bold yellow] ⚡ [bold cyan] FlashCrawler – BFS Web Crawler [bold yellow] ⚡", style="bright_magenta")
    console.print("[bold green]Author:[/] BlackForgeX", justify="center")
    console.print("[bold green]GitHub:[/] https://github.com/SKaif009", justify="center")
    console.print()
    console.print(f"[bold cyan]⚙ Max Pages:[/] {MAX_PAGES}    [bold cyan]⏱ Delay:[/] {DELAY}s    [bold cyan]⏰ Timeout:[/] {TIMEOUT}s")
    for url in queue:
        console.print(f"[bold cyan]🌐 Seed:[/] {url}")
    console.print()

def is_valid(url: str) -> bool:
    p = urlparse(url)
    return p.scheme in {"http", "https"} and p.netloc in allowed_domains

def normalize_param_signature(url: str) -> str:
    parsed = urlparse(url)
    keys = sorted(parse_qs(parsed.query).keys())
    if keys:
        return f"{parsed.path}?params={'&'.join(keys)}"
    return parsed.path

def extract(url: str) -> set[str]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        r.raise_for_status()
    except requests.exceptions.Timeout:
        console.log(f"[yellow]⚠ Timeout:[/] {url}")
        return set()
    except requests.exceptions.RequestException as e:
        console.log(f"[red]✖ Request failed:[/] {url} – {e}")
        return set()

    try:
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        console.log(f"[red]✖ HTML parse error:[/] {url} – {e}")
        return set()

    base = r.url
    links = set()
    for tag in soup.find_all("a", href=True):
        abs_url = urljoin(base, tag["href"])
        if is_valid(abs_url):
            if DEDUP_PARAM_SIG:
                sig = normalize_param_signature(abs_url)
                if sig in seen_param_signatures:
                    continue
                seen_param_signatures.add(sig)
            links.add(abs_url)
    return links

# ────────────── Crawl Logic ────────────── #
def crawl():
    banner()
    start = time.perf_counter()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[blue]{task.completed}/{task.total} pages"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as prog:
        task = prog.add_task("Crawling", total=MAX_PAGES)
        while queue and len(visited) < MAX_PAGES:
            url = queue.popleft()
            if url in visited:
                continue
            visited.add(url)

            prog.update(task, advance=1, description=f"[green]Visiting[/] {urlparse(url).netloc}")
            links = extract(url)
            time.sleep(DELAY)
            for link in links:
                if link not in visited and link not in queue:
                    queue.append(link)
            found.update(links)

    elapsed = time.perf_counter() - start
    console.print(f"\n[bold green]✔ Finished in {elapsed:.2f}s[/]")
    show_table()
    if SAVE_RESULTS:
        save_results()

# ────────────── Output Results ────────────── #
def show_table():
    table = Table(title="Discovered URLs", box=box.SIMPLE_HEAVY)
    table.add_column("#", style="cyan", width=4)
    table.add_column("URL", style="white")
    for i, url in enumerate(sorted(visited.union(found)), 1):
        table.add_row(str(i), url)
    console.print(table)
    console.rule("[bold yellow]⚡[bold cyan] FlashCrawler[/]", style="bright_magenta")

def save_results():
    all_urls = visited.union(found)
    urls_file = results_dir / "found_urls.txt"
    params_file = results_dir / "found_parameters.txt"
    dedup_file = results_dir / "deduplicate_params.txt"

    with urls_file.open("w") as u, params_file.open("w") as p, dedup_file.open("w") as d:
        for url in sorted(all_urls):
            u.write(url + "\n")
            if '?' in url:
                p.write(url + "\n")
        if DEDUP_PARAM_SIG:
            for sig in sorted(seen_param_signatures):
                d.write(sig + "\n")

    console.print(f"[green]✔ Saved to:[/] {results_dir}")
    console.print(f"[cyan]Total URLs:[/] {len(all_urls)}")
    console.print(f"[cyan]With parameters:[/] {len([u for u in all_urls if '?' in u])}")
    if DEDUP_PARAM_SIG:
        console.print(f"[cyan]Unique param patterns:[/] {len(seen_param_signatures)}")

# ────────────── Entry Point ────────────── #
if __name__ == "__main__":
    load_urls()
    crawl()