# 🚀 SubEnum: Fast Subdomain Enumerator

SubEnum is a blazing-fast, multi-threaded subdomain enumeration tool written in Python. It checks a list of possible subdomains for a given domain and tells you which ones are live—complete with colored output and a progress bar!

---

## ✨ Features

- **Super Fast:** Multi-threaded for maximum speed.
- **Progress Bar:** See your scan progress in real time.
- **Colored Output:** Instantly spot live (green) and dead (orange) subdomains.
- **Customizable:** Choose your subdomain list, thread count, and output file.
- **HTTP HEAD Requests:** Fast and lightweight checks.
- **Optional Color:** Turn off colored output for logs or scripts.
- **Easy to Use:** Simple command-line interface.

---

## 🛠️ Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/subenum.git
    cd subenum
    ```

2. **Install dependencies in a virtual environment (recommended):**
    ```sh
    chmod +x install.sh
    ./install.sh
    ```
    Or manually:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

---

## ⚡ Usage

```sh
python subenum.py -f subdomains.txt -d example.com -t 100 -o live.txt
```

**Arguments:**

| Argument         | Description                                 | Default                   |
|------------------|---------------------------------------------|---------------------------|
| `-f, --file`     | Subdomains wordlist file                    | (required, prompts if not provided) |
| `-d, --domain`   | Target domain (e.g., example.com)           | (required, prompts if not provided) |
| `-t, --threads`  | Number of threads                           | 100                       |
| `-o, --output`   | Output file for live subdomains             | live_subdomains.txt       |
| `-nc, --no-color`| Disable colored output                      | (color enabled by default)|

**Example:**
```sh
python subenum.py -f subdomains.txt -d example.com -t 200 -o live.txt
```

**Disable colored output:**
```sh
python subenum.py -f subdomains.txt -d example.com -nc
```

**If you omit `-f` or `-d`, the tool will prompt you interactively.**

---

## 📦 Output

- **Live subdomains** are printed in green (unless `-nc` is used) and saved to your output file.
- **Dead subdomains** are printed in light orange.

---

## 📝 Example Screenshot

<!-- Replace the link below with your actual screenshot if available -->
![screenshot](https://user-images.githubusercontent.com/yourusername/subenum-demo.png)

---

## 💡 Tips

- Use a large subdomain wordlist for better results.
- Increase threads for faster scans, but be mindful of your network and target rate limits.
- Try both HTTP and HTTPS for more comprehensive results.

---

## 🧑‍💻 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT License

---

**Happy hacking! 🚀**