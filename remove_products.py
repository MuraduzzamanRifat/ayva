"""
AYVA Product Remover — Deletes products on a Shopify store via Admin API.

Scoped by vendor so it ONLY touches what add_products.py created.
Dry-run by default: shows what would be deleted, requires --yes to actually
delete.

Usage:
    export SHOPIFY_STORE=your-store.myshopify.com
    export SHOPIFY_TOKEN=shpat_xxx          # Admin API token with write_products
    python remove_products.py               # dry-run (lists matches)
    python remove_products.py --yes         # actually deletes

Requires: pip install requests
"""
import os
import sys
import time
import requests

STORE_URL = os.environ.get("SHOPIFY_STORE", "pu5duj-az.myshopify.com")
ACCESS_TOKEN = os.environ.get("SHOPIFY_TOKEN", "")
VENDOR_FILTER = "AYVA"
API_URL = f"https://{STORE_URL}/admin/api/2024-01"
REQUEST_TIMEOUT = 30
MAX_ATTEMPTS = 4

HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json",
}


def redact(s):
    if not s or not ACCESS_TOKEN:
        return s
    return str(s).replace(ACCESS_TOKEN, "[REDACTED]")


def shopify_request(method, path, payload=None):
    url = f"{API_URL}{path}"
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            resp = requests.request(
                method, url, headers=HEADERS, json=payload, timeout=REQUEST_TIMEOUT
            )
        except requests.RequestException:
            if attempt < MAX_ATTEMPTS:
                time.sleep(2 ** attempt)
                continue
            raise
        if resp.status_code == 429 and attempt < MAX_ATTEMPTS:
            time.sleep(float(resp.headers.get("Retry-After", 2)))
            continue
        if 500 <= resp.status_code < 600 and attempt < MAX_ATTEMPTS:
            time.sleep(2 ** attempt)
            continue
        return resp
    return resp


def list_all_products():
    products, page_info = [], None
    while True:
        path = f"/products.json?limit=250&vendor={VENDOR_FILTER}&fields=id,title,handle,vendor"
        if page_info:
            path += f"&page_info={page_info}"
        resp = shopify_request("GET", path)
        if resp.status_code != 200:
            raise RuntimeError(f"GET {path} -> {resp.status_code}: {redact(resp.text)}")
        batch = resp.json().get("products", [])
        products.extend(batch)
        link = resp.headers.get("Link", "")
        if 'rel="next"' not in link:
            break
        next_page = link.split('page_info=')[-1].split('>')[0].split('&')[0]
        page_info = next_page
    return products


def delete_product(product_id):
    resp = shopify_request("DELETE", f"/products/{product_id}.json")
    return resp.status_code == 200, redact(resp.text) if resp.status_code != 200 else ""


def main():
    if not ACCESS_TOKEN:
        print("ERROR: SHOPIFY_TOKEN env var not set.")
        print("  export SHOPIFY_STORE=your-store.myshopify.com")
        print("  export SHOPIFY_TOKEN=shpat_xxx")
        sys.exit(1)

    dry_run = "--yes" not in sys.argv

    print("=" * 60)
    print(f"  AYVA PRODUCT REMOVER")
    print(f"  Store: {STORE_URL}")
    print(f"  Vendor filter: {VENDOR_FILTER!r}")
    print(f"  Mode: {'DRY-RUN (pass --yes to delete)' if dry_run else 'DELETE'}")
    print("=" * 60)
    print()

    products = list_all_products()
    if not products:
        print(f"  No products found with vendor={VENDOR_FILTER!r}.")
        return

    print(f"  Found {len(products)} product(s):")
    for p in products:
        print(f"    - {p['title']}  (id={p['id']}, handle={p['handle']})")
    print()

    if dry_run:
        print("  Dry-run only. Pass --yes to actually delete.")
        return

    ok = 0
    failed = []
    for p in products:
        success, err = delete_product(p["id"])
        if success:
            print(f"    ✓ deleted: {p['title']}")
            ok += 1
        else:
            print(f"    ✗ failed:  {p['title']} — {err[:200]}")
            failed.append(p["title"])
        time.sleep(0.6)

    print()
    print("=" * 60)
    print(f"  DONE! ✓ {ok} deleted | ✗ {len(failed)} failed")
    if failed:
        for t in failed:
            print(f"    - {t}")
    print("=" * 60)


if __name__ == "__main__":
    main()
