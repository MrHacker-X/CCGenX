#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CCGenX — offline, Luhn-valid TEST card generator.

Generates fake card numbers that pass the Luhn checksum so QA engineers can
test payment forms, checkout flows and sandbox integrations. The numbers are
mathematically valid but are NOT issued by any bank, hold no money and can
never complete a real transaction.

Author : MrHacker-X  (https://github.com/MrHacker-X)
Site   : https://vritrasec.com
License: MIT
"""

import argparse
import datetime
import os
import random
import sys

__version__ = "2.0.0"
PROG = os.path.basename(sys.argv[0]) or "ccgenx"


class SafeExit(Exception):
    """User aborted input (Ctrl+D / closed stdin) — handled centrally, clean exit."""

# --------------------------------------------------------------------------
# palette — muted, premium. disabled when not a tty or NO_COLOR is set
# --------------------------------------------------------------------------


def _color_ok() -> bool:
    if os.environ.get("NO_COLOR"):
        return False
    try:
        return sys.stdout.isatty()
    except Exception:
        return False


COLOR = _color_ok()
WH = "\033[1;97m" if COLOR else ""   # bright white
YL = "\033[38;5;179m" if COLOR else ""   # gold
GR = "\033[38;5;150m" if COLOR else ""   # sage green
DM = "\033[38;5;245m" if COLOR else ""   # dim grey
XX = "\033[0m" if COLOR else ""

RULE = "─" * 58

# --------------------------------------------------------------------------
# brand database — public BIN ranges, offline only
# --------------------------------------------------------------------------

BRANDS = {
    "visa": {
        "label": "Visa",
        "prefixes": ["4147", "4532", "4539", "4716", "4917", "4485"],
        "length": 16, "cvv": 3,
    },
    "mastercard": {
        "label": "Mastercard",
        "prefixes": ["51", "52", "53", "54", "55", "2221", "2360", "2649"],
        "length": 16, "cvv": 3,
    },
    "amex": {
        "label": "American Express",
        "prefixes": ["34", "37"],
        "length": 15, "cvv": 4,
    },
    "discover": {
        "label": "Discover",
        "prefixes": ["6011", "644", "645", "646", "647", "648", "649", "65"],
        "length": 16, "cvv": 3,
    },
    "jcb": {
        "label": "JCB",
        "prefixes": ["3528", "3541", "3560", "3589"],
        "length": 16, "cvv": 3,
    },
    "diners": {
        "label": "Diners Club",
        "prefixes": ["300", "301", "302", "303", "304", "305", "36", "38"],
        "length": 14, "cvv": 3,
    },
    "unionpay": {
        "label": "UnionPay",
        "prefixes": ["6200", "6210", "6212", "6222", "6226", "6260"],
        "length": 16, "cvv": 3,
    },
}


# --------------------------------------------------------------------------
# core engine — pure functions, no I/O, fully testable
# --------------------------------------------------------------------------


def luhn_checksum(number: str) -> int:
    """Luhn checksum of a digit string."""
    digits = [int(d) for d in number]
    total = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10


def is_luhn_valid(number: str) -> bool:
    return bool(number) and number.isdigit() and len(number) >= 12 \
        and luhn_checksum(number) == 0


# generic (IIN-range) fallbacks for numbers outside the curated BIN list
_GENERIC_PREFIXES = [
    ("34", "American Express"), ("37", "American Express"),
    ("30", "Diners Club"), ("36", "Diners Club"), ("38", "Diners Club"),
    ("35", "JCB"),
    ("6011", "Discover"), ("65", "Discover"),
    ("62", "UnionPay"),
    ("50", "Mastercard"), ("51", "Mastercard"), ("52", "Mastercard"),
    ("53", "Mastercard"), ("54", "Mastercard"), ("55", "Mastercard"),
    ("22", "Mastercard"), ("23", "Mastercard"), ("24", "Mastercard"),
    ("25", "Mastercard"), ("26", "Mastercard"), ("27", "Mastercard"),
    ("4", "Visa"),
]


def detect_brand(number: str) -> str:
    """Best-effort brand guess: curated BINs first, then generic IIN ranges."""
    for spec in BRANDS.values():
        for p in spec["prefixes"]:
            if number.startswith(p):
                return spec["label"]
    for p, label in _GENERIC_PREFIXES:
        if number.startswith(p):
            return label
    return "Unknown"


def generate_card(brand: str, rng: random.Random = random) -> dict:
    """Generate one Luhn-valid test card dict for a brand key."""
    spec = BRANDS[brand]
    prefix = rng.choice(spec["prefixes"])
    body = prefix + "".join(
        rng.choice("0123456789") for _ in range(spec["length"] - len(prefix) - 1)
    )
    check = (10 - luhn_checksum(body + "0")) % 10
    today = datetime.date.today()
    return {
        "brand": spec["label"],
        "number": body + str(check),
        "cvv": "".join(rng.choice("0123456789") for _ in range(spec["cvv"])),
        "month": f"{rng.randint(1, 12):02d}",
        "year": str(today.year + rng.randint(1, 6)),
        "pin": f"{rng.randint(0, 9999):04d}",
    }


def format_number(number: str) -> str:
    """Pretty spacing: Amex 4-6-5, Diners 4-6-4, everything else 4-4-4-…"""
    if len(number) == 15:
        return f"{number[:4]} {number[4:10]} {number[10:]}"
    if len(number) == 14:
        return f"{number[:4]} {number[4:10]} {number[10:]}"
    return " ".join(number[i:i + 4] for i in range(0, len(number), 4))


# --------------------------------------------------------------------------
# ui helpers — typographic, no ascii art
# --------------------------------------------------------------------------


def banner() -> None:
    wordmark = "C C G E N X"
    subtitle = f"v{__version__}"
    pad = " " * max(1, 58 - 2 - len(wordmark) - len(subtitle))
    print()
    print(f"  {YL}{RULE}{XX}")
    print(f"  {WH}{wordmark}{XX}{pad}{DM}{subtitle}{XX}")
    print(f"  {DM}offline luhn-valid test-card generator · zero network · zero tracking{XX}")
    print(f"  {YL}{RULE}{XX}")
    print(f"  {DM}test data only — these cards hold no money and cannot buy anything{XX}")
    print()


def rule() -> None:
    print(f"  {YL}{RULE}{XX}")


def kv(key: str, val: str, width: int = 14) -> None:
    gap = " " * max(0, width - len(key))
    print(f"  {YL}{key}{XX}{gap}  {DM}····{XX}  {WH}{val}{XX}")


def item(num: str, label: str, desc: str = "", dim: bool = False,
         align: int = 13) -> None:
    gap = (" " * max(0, align - len(label))) if desc else ""
    tail = f"  {DM}····  {desc}{XX}" if desc else ""
    c = DM if dim else GR
    print(f"  [{YL}{num}{XX}] {c}{label}{XX}{gap}{tail}")


def pause() -> None:
    try:
        input(f"  {YL}›{XX} {DM}enter to return{XX}")
    except EOFError:
        raise SafeExit from None
    print()


def ask(prompt: str) -> str:
    """Prompt the user; Ctrl+C and Ctrl+D both trigger a clean, safe exit."""
    try:
        return input(f"  {YL}›{XX} {prompt}: ").strip()
    except EOFError:
        print()
        raise SafeExit from None
    # KeyboardInterrupt propagates to the central handler in main()


# --------------------------------------------------------------------------
# actions
# --------------------------------------------------------------------------


def brand_menu(rng: random.Random = random) -> str:
    """Dynamic-width brand picker. Returns brand key or '' on abort."""
    keys = list(BRANDS.keys())
    labels = [BRANDS[k]["label"] for k in keys]
    w = max(len(l) for l in labels)
    print(f"\n  {WH}pick a brand{XX}\n")
    for i, key in enumerate(keys, 1):
        spec = BRANDS[key]
        item(str(i), labels[i - 1],
             f"prefix {spec['prefixes'][0]}…", align=w)
    item("a", "random brand", "pick one at random", dim=True, align=w)
    item("0", "back", "", dim=True, align=w)
    ch = ask("choice").lower()
    if ch == "a":
        return rng.choice(keys)
    if ch == "0":
        return ""
    if ch.isdigit() and 1 <= int(ch) <= len(keys):
        return keys[int(ch) - 1]
    print(f"  {DM}invalid choice{XX}")
    return ""


def show_card(card: dict) -> None:
    print(f"\n  {YL}{RULE}{XX}")
    print(f"  {WH}{card['brand']}{XX}{DM}  ·  test card — not real{XX}\n")
    kv("number", format_number(card["number"]))
    kv("luhn", f"{GR}valid{XX}" if is_luhn_valid(card["number"]) else "invalid")
    kv("expiry", f"{card['month']}/{card['year']}")
    kv("cvv", card["cvv"])
    kv("pin", card["pin"])
    print(f"  {YL}{RULE}{XX}\n")


def action_single(rng: random.Random) -> None:
    brand = brand_menu(rng)
    if not brand:
        return
    show_card(generate_card(brand, rng))


def action_bulk(rng: random.Random) -> None:
    brand = brand_menu(rng)
    if not brand:
        return
    raw = ask("how many cards (1-500)")
    try:
        count = max(1, min(500, int(raw)))
    except ValueError:
        print(f"  {DM}invalid count — cancelled{XX}\n")
        return
    fmt = ask("format — raw | full | pretty [full]").lower() or "full"
    if fmt not in ("raw", "full", "pretty"):
        fmt = "full"
    path = ask("output file [cards.txt]") or "cards.txt"

    cards = [generate_card(brand, rng) for _ in range(count)]
    try:
        with open(path, "w", encoding="utf-8") as fh:
            for c in cards:
                if fmt == "raw":
                    fh.write(c["number"] + "\n")
                elif fmt == "pretty":
                    fh.write(
                        f"{c['brand']} | {format_number(c['number'])} | "
                        f"{c['month']}/{c['year']} | cvv {c['cvv']}\n")
                else:
                    fh.write(
                        f"{c['number']}|{c['month']}|{c['year'][-2:]}|{c['cvv']}\n")
    except OSError as exc:
        print(f"  {DM}write failed: {exc}{XX}\n")
        return

    print(f"\n  {YL}{RULE}{XX}")
    print(f"  {WH}saved{XX}\n")
    kv("file", os.path.abspath(path))
    kv("count", str(count))
    kv("brand", BRANDS[brand]["label"])
    kv("format", fmt)
    kv("luhn", f"{GR}all valid{XX}"
        if all(is_luhn_valid(c["number"]) for c in cards) else "error")
    print(f"  {YL}{RULE}{XX}")
    print(f"  {DM}sample: {cards[0]['number']}|{cards[0]['month']}|"
          f"{cards[0]['year'][-2:]}|{cards[0]['cvv']}{XX}\n")


def action_validate() -> None:
    raw = ask("card number").replace(" ", "").replace("-", "")
    if not raw:
        return
    ok = is_luhn_valid(raw)
    print(f"\n  {YL}{RULE}{XX}")
    kv("number", raw)
    kv("brand", detect_brand(raw))
    kv("luhn", f"{GR}valid{XX}" if ok else f"{DM}invalid{XX}")
    print(f"  {YL}{RULE}{XX}\n")


def action_about() -> None:
    """About screen — tool + maker, then enter returns to the menu."""
    print()
    rule()
    print(f"  {WH}about{XX}\n")
    kv("tool", f"CCGenX v{__version__}")
    kv("type", "offline luhn-valid test-card generator")
    kv("engine", "luhn checksum (iso/iec 7812-1)")
    kv("brands", "visa · mastercard · amex · discover · jcb ·")
    kv("", "diners club · unionpay")
    kv("network", "zero — 100% local, nothing leaves your machine")
    kv("license", "MIT")
    print()
    kv("dev", "MrHacker-X")
    kv("github", "github.com/MrHacker-X")
    kv("email", "contact@vritrasec.com")
    kv("website", "vritrasec.com")
    kv("link", "link.vritrasec.com")
    print()
    print(f"  {DM}test data only — these cards hold no money and cannot buy anything{XX}")
    print()
    try:
        input(f"  {YL}›{XX} {DM}press enter to continue{XX}")
    except EOFError:
        raise SafeExit from None
    # KeyboardInterrupt propagates to the central handler in main()


MENU = [
    ("1", "generate single card", "one luhn-valid test card"),
    ("2", "bulk generator", "save many cards to a file"),
    ("3", "validate a number", "luhn + brand check"),
    ("4", "about", "maker · tool · license"),
    ("0", "exit", ""),
]


def menu() -> None:
    while True:
        banner()
        w = max(len(t[1]) for t in MENU)
        for num, label, *rest in MENU:
            item(num, label, rest[0] if rest else "", dim=(num == "0"),
                 align=w)
        ch = ask("choice")
        if ch == "1":
            action_single(RNG)
        elif ch == "2":
            action_bulk(RNG)
        elif ch == "3":
            action_validate()
        elif ch == "4":
            action_about()
        elif ch in ("0", "q", "quit", "exit"):
            print(f"  {DM}stay safe — test data only.{XX}\n")
            return
        else:
            print(f"  {DM}invalid choice{XX}\n")


RNG = random.Random()


# --------------------------------------------------------------------------
# one-shot cli
# --------------------------------------------------------------------------


def cli(args: argparse.Namespace) -> int:
    rng = random.Random(args.seed) if args.seed is not None else random.Random()
    if args.validate:
        raw = args.validate.replace(" ", "").replace("-", "")
        ok = is_luhn_valid(raw)
        print(f"  {YL}{RULE}{XX}")
        kv("number", raw)
        kv("brand", detect_brand(raw))
        kv("luhn", f"{GR}valid{XX}" if ok else f"{DM}invalid{XX}")
        print(f"  {YL}{RULE}{XX}")
        return 0 if ok else 1

    if not args.brand:
        menu()
        return 0

    brand = args.brand.lower()
    if brand == "random":
        brand = rng.choice(list(BRANDS.keys()))
    if brand not in BRANDS:
        print(f"  {DM}unknown brand '{args.brand}' — pick one of: "
              f"{', '.join(BRANDS)} or 'random'{XX}")
        return 2

    count = max(1, min(500, args.count))
    cards = [generate_card(brand, rng) for _ in range(count)]
    if args.out:
        try:
            with open(args.out, "w", encoding="utf-8") as fh:
                for c in cards:
                    if args.format == "raw":
                        fh.write(c["number"] + "\n")
                    elif args.format == "pretty":
                        fh.write(f"{c['brand']} | {format_number(c['number'])}"
                                 f" | {c['month']}/{c['year']} | cvv {c['cvv']}\n")
                    else:
                        fh.write(f"{c['number']}|{c['month']}|"
                                 f"{c['year'][-2:]}|{c['cvv']}\n")
            print(f"  {YL}····{XX} {count} card(s) → {WH}{args.out}{XX}")
        except OSError as exc:
            print(f"  {DM}write failed: {exc}{XX}")
            return 1
    else:
        for c in cards:
            if args.format == "raw":
                print(c["number"])
            elif args.format == "pretty":
                print(f"{c['brand']} | {format_number(c['number'])} | "
                      f"{c['month']}/{c['year']} | cvv {c['cvv']}")
            else:
                print(f"{c['number']}|{c['month']}|{c['year'][-2:]}|{c['cvv']}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog=PROG,
        description="CCGenX — offline luhn-valid test card generator "
                    "(test data only, never for fraud).")
    parser.add_argument("-b", "--brand", help="visa|mastercard|amex|discover|"
                        "jcb|diners|unionpay|random")
    parser.add_argument("-c", "--count", type=int, default=1,
                        help="how many cards (1-500, default 1)")
    parser.add_argument("-f", "--format", default="full",
                        choices=["raw", "full", "pretty"],
                        help="output format (default full)")
    parser.add_argument("-o", "--out", help="write to file instead of stdout")
    parser.add_argument("-v", "--validate", metavar="NUMBER",
                        help="luhn-validate an existing number and exit")
    parser.add_argument("--seed", type=int, default=None,
                        help="rng seed for reproducible output")
    parser.add_argument("--version", action="version",
                        version=f"{PROG} {__version__}")
    args = parser.parse_args()

    try:
        sys.exit(cli(args))
    except SafeExit:
        print(f"  {DM}safe exit — test data only.{XX}\n")
        sys.exit(0)
    except KeyboardInterrupt:
        print(f"\n  {DM}safe exit — test data only.{XX}\n")
        sys.exit(130)


if __name__ == "__main__":
    main()
