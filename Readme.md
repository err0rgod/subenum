# SubEnum V2.0 🚀

**Multi-threaded subdomain enumeration tool** — fast, reliable, with HTTP/HTTPS checking, DNS fallback, and multiple output formats.

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
[![GitHub](https://img.shields.io/badge/GitHub-err0rgod-181717?logo=github)](https://github.com/err0rgod)

---

## ✨ Features

- ⚡ **Multi-threaded scanning** — uses `ThreadPoolExecutor` for parallel subdomain checking
- 🔒 **HTTP + HTTPS checks** — tries HTTPS first, falls back to HTTP
- 🌐 **DNS resolution fallback** — detects live domains even when HTTP is blocked
- 📊 **Real-time progress bar** — via `tqdm`
- 🎨 **Colored terminal output** — via `colorama` (toggle with `-nc`)
- 📁 **Multiple output formats** — TXT, CSV, or JSON
- ⏱️ **Rate limiting** — `--delay` flag to avoid rate bans
- 🔁 **Retry logic** — automatic retries on 429/5xx errors
- 📝 **Verbose mode** — `-v` for debug-level logging
- 🧠 **Interactive prompts** — works without arguments (asks for missing input)

---

## 🛠️ Installation

```bash
# Clone the repo
git clone https://github.com/err0rgod/subenum.git
cd subenum

# Option A — using install script
chmod +x install.sh
./install.sh

# Option B — manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Requirements
- Python 3.8+
- `requests`, `tqdm`, `colorama`

---

## ⚡ Usage

### Minimal (interactive)
```bash
python subenum.py
```
You'll be prompted for the subdomain file and target domain.

### Full command
```bash
python subenum.py -f subdomains.txt -d example.com -t 150 -o results.json --format json
```

### With rate limiting & verbose logging
```bash
python subenum.py -f subdomains.txt -d example.com --delay 0.05 -v
```

### Disable colors
```bash
python subenum.py -f subdomains.txt -d example.com -nc
```

---

## 📋 Arguments

| Argument         | Description                                | Default                  |
|------------------|--------------------------------------------|--------------------------|
| `-f, --file`     | Subdomains wordlist file                   | (prompts if missing)     |
| `-d, --domain`   | Target domain                              | (prompts if missing)     |
| `-t, --threads`  | Number of concurrent threads               | `100`                    |
| `-o, --output`   | Output file path                           | `live_subdomains.txt`    |
| `--format`       | Output format (`txt`, `csv`, `json`)       | `txt`                    |
| `-nc, --no-color`| Disable colored output                     | (colors enabled)         |
| `-v, --verbose`  | Enable debug-level logging                 | (off)                    |
| `--delay`        | Delay in seconds between requests          | `0.0`                    |

---

## 📁 Output Formats

### TXT (default)
```
subdomain1.example.com
subdomain2.example.com
```

### CSV
```csv
domain,status_code,method
subdomain1.example.com,200,HEAD/HTTPS
subdomain2.example.com,,DNS
```

### JSON
```json
{
  "live_subdomains": [
    {"domain": "subdomain1.example.com", "status_code": 200, "method": "HEAD/HTTPS"}
  ],
  "count": 1
}
```

---

## 💡 Tips

- Use a **large wordlist** for better coverage
- Adjust `-t` based on your network and target limits
- Use `--delay 0.1` to avoid getting rate-limited
- Use `--format json` if you need structured data for further processing
- Run with `-v` to debug connectivity issues

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

**Happy hacking! 🖤**
