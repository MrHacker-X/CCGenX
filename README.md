<div align="center">

# ⃤ C C G E N X ⃤

### *The offline test-card generator — Luhn-valid numbers for QA, not for crime.*

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-38;5;179?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux%20%7C%20macOS-38;5;150?style=flat-square)
![Network](https://img.shields.io/badge/Network-Zero%20·%20Offline-38;5;245?style=flat-square)
![Stars](https://img.shields.io/github/stars/MrHacker-X/CCGenX?style=flat-square&color=38;5;179)

</div>

---

## 📋 Table of Contents

- [🎯 Why CCGenX?](#-why-ccgenx)
- [🧭 Tool Purpose](#-tool-purpose)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [✨ Features](#-features)
- [⌨️ Usage](#%EF%B8%8F-usage)
- [🖥️ Preview](#%EF%B8%8F-preview)
- [🧰 Tech Stack](#-tech-stack)
- [⚠️ Disclaimer](#%EF%B8%8F-disclaimer)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👨‍💻 Developer](#-developer)

---

## 🎯 Why CCGenX?

> Every developer who has ever built a payment form has needed **test card numbers** — and most "card generators" out there are broken scrapers that hammer third-party websites with stale cookies, leak your IP to ad trackers and die the day those sites change.
>
> **CCGenX v2.0 flips the model.** It generates Luhn-valid test cards **100% locally** — zero network, zero cookies, zero tracking, zero failure points. Pure math, pure speed, pure privacy. The old scraping engine is gone forever; what replaced it is a deterministic, offline engine you can actually trust in CI.

---

## 🧭 Tool Purpose

**CCGenX exists for exactly three legitimate purposes — and nothing else:**

| # | Purpose | Example |
|---|---------|---------|
| 1️⃣ | **QA & software testing** | Filling checkout forms, payment-field validation and e-commerce test flows with realistic, Luhn-valid data |
| 2️⃣ | **Developer & API sandbox testing** | Testing Stripe, PayPal Sandbox, Razorpay test-mode or your own backend's card-parsing logic |
| 3️⃣ | **Learning & education** | Understanding the Luhn checksum algorithm, card-number structure and BIN ranges in a computer-science context |

**What this tool is NOT:** it is **not** a way to obtain working credit cards, bypass payments, or make purchases. The numbers it generates pass the Luhn checksum — a mathematical property — but they are **not issued by any bank, linked to no account, and hold zero money**. Any real-world use is impossible with these cards and illegal with anyone else's.

If you need official test cards for production payment integrations, use the provider's own published test numbers (e.g. Stripe's `4242 4242 4242 4242`).

---

## 🚀 Quick Start

```bash
git clone https://github.com/MrHacker-X/CCGenX.git
cd CCGenX
python3 ccgenx.py            # interactive mode
```

One-shot CLI — no menu needed:

```bash
python3 ccgenx.py -b visa                          # 1 Visa card
python3 ccgenx.py -b mastercard -c 10 -o cards.txt # 10 cards to file
python3 ccgenx.py -v 4532015112830366              # Luhn-validate a number
```

---

## 📦 Installation

**No dependencies. No pip install. Just Python.**

CCGenX v2.0 uses **only the Python standard library** — `requests`, `bs4`, `colorama` and every third-party dependency from the old version are gone.

```bash
git clone https://github.com/MrHacker-X/CCGenX.git
cd CCGenX
chmod +x ccgenx.py
python3 ccgenx.py
```

<details>
<summary><b>🛠 Optional — install as a system command</b></summary>

```bash
mkdir -p ~/.local/bin
cp ccgenx.py ~/.local/bin/ccgenx
chmod +x ~/.local/bin/ccgenx
export PATH="$HOME/.local/bin:$PATH"   # add to .bashrc / .zshrc once
```

Then run it from anywhere:

```bash
ccgenx --version
ccgenx -b amex -c 5 -f pretty
```

</details>

### Supported Systems

| OS | Status | Notes |
|----|--------|-------|
| 🐧 Linux | ✅ Fully supported | Debian, Ubuntu, Arch, Kali, Fedora… |
| 📱 Termux (Android) | ✅ Fully supported | `pkg install python` and run |
| 🍎 macOS | ✅ Fully supported | Ships with Python 3 |
| 🪟 Windows | ⚠️ Partial | Works under WSL / Git Bash; plain cmd.exe shows raw ANSI codes |
| 🐍 Python | ✅ 3.6+ | Standard library only — nothing to install |

---

## ✨ Features

| | Feature | Description |
|---|---------|-------------|
| 🔢 | **Luhn-valid generation** | Every card passes the Luhn checksum — computed locally, verified per card |
| 🏦 | **7 major brands** | Visa, Mastercard, Amex, Discover, JCB, Diners Club, UnionPay |
| 📶 | **100% offline** | Zero network calls — the entire scraper/cookie engine of v1.x is deleted |
| 🎛️ | **Dual interface** | Interactive menu *and* a scriptable one-shot CLI (`--brand --count --out`) |
| 🔁 | **Reproducible output** | `--seed` gives deterministic cards for regression tests |
| 🧪 | **Built-in validator** | `--validate` or menu option 3 checks any number and detects its brand |
| 💾 | **Bulk export** | Up to 500 cards per run in `raw`, `full` (pipe-format) or `pretty` |
| 🎨 | **Typographic UI** | Clean, muted, premium palette — no ASCII art, no flicker, no fake progress |
| 🛡️ | **Zero dependencies** | Pure Python standard library — runs anywhere Python runs |
| 👁️ | **Honest labeling** | Every generated card is marked *test card — not real* in the output |

<details>
<summary><b>🔄 What changed from v1.x?</b></summary>

| v1.x (old) | v2.0 (now) |
|------------|------------|
| Scraped vccgenerator.org with hardcoded 2022 cookies | Fully offline generation — nothing to break |
| Printed Telegram channel spam | Removed completely |
| Fake flicker "animation" (`.postr.sh` + 100 KB ANSI art) | Deleted — clean startup, instant results |
| 3 heavy dependencies (requests, bs4, colorama) | Standard library only |
| No validation, no error handling | Luhn self-check, graceful Ctrl+C, input guards |
| Dead `corex/` module | Removed |

</details>

---

## ⌨️ Usage

### Interactive mode

```bash
python3 ccgenx.py
```

| Option | Action |
|--------|--------|
| `1` | Generate a single test card (pick a brand) |
| `2` | Bulk generator — save up to 500 cards to a file |
| `3` | Validate a number — Luhn check + brand detection |
| `4` | About — tool info, maker & contact links |
| `0` | Exit |

### One-shot CLI

| Flag | Description | Example |
|------|-------------|---------|
| `-b, --brand` | Brand or `random` | `-b amex` |
| `-c, --count` | How many cards (1–500) | `-c 25` |
| `-f, --format` | `raw` \| `full` \| `pretty` | `-f pretty` |
| `-o, --out` | Write to file instead of stdout | `-o cards.txt` |
| `-v, --validate` | Luhn-validate a number and exit (exit code 0/1) | `-v 4242424242424242` |
| `--seed` | Deterministic RNG seed | `--seed 42` |
| `--version` | Print version | |

### Output formats

```
raw    →  4532015112830366
full   →  4532015112830366|11|27|582          (pipe format for test suites)
pretty →  Visa | 4532 0151 1283 0366 | 11/2027 | cvv 582
```

> 💡 `--validate` returns exit code `0` for a valid number and `1` for invalid — perfect for shell scripts and CI pipelines.

---

## 🖥️ Preview

<div align="center">

<img src="https://i.ibb.co/Lhk7vHgY/image.png" alt="CCGenX v2.0 — terminal preview" width="720">

</div>

```text
  ──────────────────────────────────────────────────────────
  C C G E N X                                     v2.0.0
  offline luhn-valid test-card generator · zero network · zero tracking
  ──────────────────────────────────────────────────────────
  test data only — these cards hold no money and cannot buy anything

  [1] generate single card  ····  one luhn-valid test card
  [2] bulk generator        ····  save many cards to a file
  [3] validate a number     ····  luhn + brand check
  [4] about                 ····  maker · tool · license
  [0] exit
  › choice: 1

  pick a brand

  [1] Visa              ····  prefix 4147…
  [2] Mastercard        ····  prefix 51…
  [3] American Express  ····  prefix 34…
  [4] Discover          ····  prefix 6011…
  [5] JCB               ····  prefix 3528…
  [6] Diners Club       ····  prefix 300…
  [7] UnionPay          ····  prefix 6200…
  [a] random brand      ····  pick one at random
  [0] back
  › choice: 3

  ──────────────────────────────────────────────────────────
  American Express  ·  test card — not real

  number        ····  3782 822463 10005
  luhn          ····  valid
  expiry        ····  07/2029
  cvv           ····  8464
  pin           ····  0042
  ──────────────────────────────────────────────────────────
```

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.6+ |
| Dependencies | **None** — 100% standard library |
| Core | `random`, `datetime`, `argparse`, `os`, `sys` |
| UI | Hand-rolled ANSI palette with tty/`NO_COLOR` auto-detection |
| Algorithm | Luhn checksum (ISO/IEC 7812-1) |

---

## ⚠️ Disclaimer

> ### Read this before using CCGenX.
>
> 1. **These cards are fake.** CCGenX produces numbers that satisfy the Luhn checksum — a public mathematical formula. They are **not** issued by any bank, connected to no account, and contain **no money**.
> 2. **They cannot buy anything.** No real merchant, payment processor or bank will ever accept these numbers. Any attempt to use them at a checkout will simply fail validation.
> 3. **Legitimate use only.** This tool is built for **software QA, developer sandbox testing and education** — nothing else. Use it on your own test forms, your own sandbox accounts and your own learning projects.
> 4. **Fraud is a crime.** Attempting payment fraud, identity theft or any unauthorized financial activity is illegal in every jurisdiction and can lead to prosecution. This tool does not enable it — but misusing *any* card-related tooling is your own legal risk.
> 5. **No warranty, no liability.** CCGenX is provided "as is", under the MIT License, with no warranty of any kind. The author is **not responsible** for any misuse, damage or legal consequences caused by use or abuse of this tool. By using CCGenX you accept full responsibility for your own actions.

---

## 🤝 Contributing

Contributions are welcome!

```bash
# 1. fork it
# 2. create your branch
git checkout -b feature/amazing-feature
# 3. commit
git commit -m "Add amazing feature"
# 4. push
git push origin feature/amazing-feature
# 5. open a Pull Request
```

Ideas worth exploring: unit-test suite, more BIN ranges, JSON/CSV export, `--luhn-only` batch lint mode.

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

---

## 👨‍💻 Developer

| | |
|---|---|
| **Dev** | MrHacker-X |
| **GitHub** | [github.com/MrHacker-X](https://github.com/MrHacker-X) |
| **Email** | [contact@vritrasec.com](mailto:contact@vritrasec.com) |
| **Website** | [vritrasec.com](https://vritrasec.com) |
| **Network** | [link.vritrasec.com](https://link.vritrasec.com) |

---

<div align="center">

### ⭐ Star the repo if CCGenX saved you an afternoon of fake-card plumbing ⭐

*Built with discipline by MrHacker-X — test data only, always.*

</div>
