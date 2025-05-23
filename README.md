<p align="center">
  <img src="assets/flashcrawler_icon.png" width="150" alt="FlashCrawler Icon"/>
</p>


# ⚡ FlashCrawler v2.0.0 – Colorful BFS Web Crawler

FlashCrawler is a fast, terminal-friendly Python web crawler that uses **Breadth-First Search (BFS)** to discover URLs. Designed for security researchers, VAPT, and developers, it features colorful terminal output, domain filtering, deduplication by query patterns, and easy extensibility.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Cross--platform-lightgrey)

---

![image](https://github.com/user-attachments/assets/5ab03ea0-abc5-4e98-abfa-702a0716e091)


---

## ✨ Features

* 🔍 **BFS crawling** for broad and shallow discovery
* 🎨 **Rich terminal UI** with progress bars and tables
* 🌐 **Domain-restricted crawling**
* ⏳ Configurable **timeouts and delays**
* 🧠 **Deduplication** based on query parameter patterns (`--dedup-params`)
* ⏳ Here, in v2.0.0 intoduce of **random-useragent** bypassing bot detection
* 📝 **Export results** to files:

  * `found_urls.txt`
  * `found_parameters.txt`
  * `deduplicate_params.txt`

---

## ✨ Installation

```bash
git clone https://github.com/SKaif009/Flash_Crawler.git
```
```bash
cd Flash_Crawler
```
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🚀 Usage

### 🔧 Command-line Options

```bash
python FlashCrawler.py -u <url> [options]
```

### 🔗 Examples

```bash
# Crawl a single site
python FlashCrawler.py -u https://example.com

# Crawl from list, 10s timeout, 1s delay between requests
python FlashCrawler.py -l urls.txt -t 1 --req-timeout 10

# Save results to files
python FlashCrawler.py -u https://example.com -s

# Crawl with parameter-pattern deduplication
python FlashCrawler.py -u https://example.com --dedup-params

# Combine save and dedup
python FlashCrawler.py -u https://example.com -s --dedup-params --rua
```

---

## 🗂 Output Files (in `results/`)

| File                     | Description                                  |
| ------------------------ | -------------------------------------------- |
| `found_urls.txt`         | All discovered and visited URLs              |
| `found_parameters.txt`   | URLs that include query parameters           |
| `deduplicate_params.txt` | One entry per unique query param key pattern |

---

## 🧠 How It Works

1. Starts from a seed URL or list.
2. Uses **Breadth-First Search (BFS)** to crawl internal links.
3. Filters out external domains.
4. Optionally deduplicates URLs with the same query **key structure** (e.g. `id&pid`).
5. Renders a clean, color-coded output table and saves results.

---

## 📦 Requirements

* Python 3.8+
* Install dependencies:



**`requirements.txt`:**

```text
requests
beautifulsoup4
rich
```

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**BlackForgeX**
GitHub: [@SKaif009](https://github.com/SKaif009)

---

## 💬 Contributions & Issues

Contributions, suggestions, and issues are welcome!
Open an [Issue](https://github.com/YOUR_USERNAME/FlashCrawler/issues) or [Pull Request](https://github.com/YOUR_USERNAME/FlashCrawler/pulls).

---
