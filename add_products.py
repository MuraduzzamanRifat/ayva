"""
AYVA Product Importer — Adds all AYVA products to Shopify via Admin API.

Usage:
    export SHOPIFY_STORE=your-store.myshopify.com
    export SHOPIFY_TOKEN=shpat_xxx          # Admin API token with write_products
    python add_products.py

Requires: pip install requests
"""
import os
import re
import sys
import time
import requests

STORE_URL = os.environ.get("SHOPIFY_STORE", "pu5duj-az.myshopify.com")
ACCESS_TOKEN = os.environ.get("SHOPIFY_TOKEN", "")

HEADERS = {
    "X-Shopify-Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json",
}
API_URL = f"https://{STORE_URL}/admin/api/2024-01"
REQUEST_TIMEOUT = 30
MAX_ATTEMPTS = 4


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
            wait = float(resp.headers.get("Retry-After", 2))
            time.sleep(wait)
            continue
        if 500 <= resp.status_code < 600 and attempt < MAX_ATTEMPTS:
            time.sleep(2 ** attempt)
            continue
        return resp
    return resp


def slugify(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


def product_exists(handle):
    resp = shopify_request("GET", f"/products.json?handle={handle}&fields=id,handle")
    if resp.status_code == 200:
        return bool(resp.json().get("products"))
    return False

# ── ALL AYVA PRODUCTS ──
PRODUCTS = [
    {
        "title": "The Côte Bag",
        "body_html": "<p>Fits laptops up to 13\" | 1 zipped main compartment | 2 internal pockets | Stiffened base — stays upright when packed</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "tote, laptop, everyday",
        "variants": [
            {"option1": "Black", "price": "59.00", "compare_at_price": "99.00"},
            {"option1": "Coffee", "price": "59.00", "compare_at_price": "99.00"},
            {"option1": "Chocolate brown", "price": "59.00", "compare_at_price": "99.00"},
            {"option1": "Pitch green", "price": "59.00", "compare_at_price": "99.00"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/267301/pexels-photo-267301.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Camden Bag",
        "body_html": "<p>The Camden Bag is your go-to for city days and late-night plans. Sleek and versatile, it's designed to fit a 13-inch laptop.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "new, shoulder, laptop",
        "variants": [
            {"option1": "Black", "price": "59.99", "compare_at_price": "99.99"},
            {"option1": "Merlot", "price": "59.99", "compare_at_price": "99.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/19090/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Foldable Makeup Bag",
        "body_html": "<p>Cute. Compact. Chaos-free. The foldable bag your beauty routine deserves.</p>",
        "vendor": "AYVA",
        "product_type": "Accessories",
        "tags": "accessories, makeup",
        "variants": [
            {"option1": "All-white", "price": "24.99", "compare_at_price": "34.99"},
            {"option1": "Muted pink", "price": "24.99", "compare_at_price": "34.99"},
            {"option1": "Brown", "price": "24.99", "compare_at_price": "34.99"},
            {"option1": "Black", "price": "24.99", "compare_at_price": "34.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Bellini Bag",
        "body_html": "<p>A softly structured shoulder bag with a curved shape and buckle detail. Designed for everyday wear with a relaxed yet refined look.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, everyday",
        "variants": [
            {"option1": "Black", "price": "39.95", "compare_at_price": "59.95"},
            {"option1": "Dark Cherry", "price": "39.95", "compare_at_price": "59.95"},
            {"option1": "Silver Black", "price": "39.95", "compare_at_price": "59.95"},
            {"option1": "Silver", "price": "39.95", "compare_at_price": "59.95"},
            {"option1": "Red", "price": "39.95", "compare_at_price": "59.95"},
            {"option1": "All-white", "price": "39.95", "compare_at_price": "59.95"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/6046227/pexels-photo-6046227.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/1478442/pexels-photo-1478442.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Nova Sling",
        "body_html": "<p>A lightweight, slouchy sling bag designed for everyday movement. Crafted in durable nylon with a relaxed silhouette and multiple pockets.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "sling, everyday, nylon",
        "variants": [
            {"option1": "Black", "price": "39.95", "compare_at_price": "70.00"},
            {"option1": "Brown", "price": "39.95", "compare_at_price": "70.00"},
            {"option1": "White", "price": "39.95", "compare_at_price": "70.00"},
            {"option1": "Olive green", "price": "39.95", "compare_at_price": "70.00"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/3261069/pexels-photo-3261069.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/267301/pexels-photo-267301.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Verona Bag",
        "body_html": "<p>The Verona Bag brings effortless shine to any outfit. Its glossy textured finish, silver details and reinforced seams create a durable yet elegant bag.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, glossy",
        "variants": [
            {"option1": "Black", "price": "49.99", "compare_at_price": "74.99"},
            {"option1": "Dark Cherry", "price": "49.99", "compare_at_price": "74.99"},
            {"option1": "Caramel", "price": "49.99", "compare_at_price": "74.99"},
            {"option1": "Stockholm white", "price": "49.99", "compare_at_price": "74.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Milano Bag",
        "body_html": "<p>The Milano Shoulder Bag blends softness with structure in the perfect everyday silhouette. Finished with elegant silver details.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, silver",
        "variants": [
            {"option1": "Black", "price": "39.99", "compare_at_price": "99.99"},
            {"option1": "Coffee", "price": "39.99", "compare_at_price": "99.99"},
            {"option1": "Silver", "price": "39.99", "compare_at_price": "99.99"},
            {"option1": "Gray", "price": "39.99", "compare_at_price": "99.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/19090/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Brooklyn Bag",
        "body_html": "<p>Soft vegan leather with a slouchy, modern shape. Size: 40 x 25 x 15 cm.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "tote, everyday",
        "variants": [
            {"option1": "Black", "price": "54.99", "compare_at_price": "99.00"},
            {"option1": "Windsor Tan", "price": "54.99", "compare_at_price": "99.00"},
            {"option1": "Coffee", "price": "54.99", "compare_at_price": "99.00"},
            {"option1": "Burgundy", "price": "54.99", "compare_at_price": "99.00"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/6046227/pexels-photo-6046227.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Marseille",
        "body_html": "<p>Premium vegan leather, finished with antique brass hardware. Size: 38 cm (L), 29 cm (H), 13 cm (W).</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, premium",
        "variants": [
            {"option1": "Default", "price": "59.99", "compare_at_price": "99.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/1478442/pexels-photo-1478442.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/3261069/pexels-photo-3261069.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Clover Bag",
        "body_html": "<p>Smooth vegan leather with removable heart mirror charm and detachable mini wallet. Size: 26 x 16 x 8 cm.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, mini",
        "variants": [
            {"option1": "Black", "price": "48.99", "compare_at_price": "74.99"},
            {"option1": "Denim Blue", "price": "48.99", "compare_at_price": "74.99"},
            {"option1": "Stockholm White", "price": "48.99", "compare_at_price": "74.99"},
            {"option1": "Pink", "price": "48.99", "compare_at_price": "74.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/267301/pexels-photo-267301.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Amira Bag",
        "body_html": "<p>A beautifully crafted everyday bag with a relaxed silhouette and premium vegan leather finish.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, everyday",
        "variants": [
            {"option1": "Black", "price": "42.99", "compare_at_price": "79.99"},
            {"option1": "Coffee", "price": "42.99", "compare_at_price": "79.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/19090/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Vera Bag",
        "body_html": "<p>A versatile shoulder bag crafted in premium vegan leather with elegant hardware details.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder",
        "variants": [
            {"option1": "Black", "price": "59.99", "compare_at_price": "89.99"},
            {"option1": "Coffee", "price": "59.99", "compare_at_price": "89.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Saria Bag",
        "body_html": "<p>A premium structured bag crafted in luxurious vegan leather.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "premium, structured",
        "variants": [
            {"option1": "Black", "price": "119.00", "compare_at_price": "119.00"},
            {"option1": "Coffee", "price": "119.00", "compare_at_price": "119.00"},
            {"option1": "Windsor tan", "price": "119.00", "compare_at_price": "119.00"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/6046227/pexels-photo-6046227.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/1478442/pexels-photo-1478442.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Sloane Bag",
        "body_html": "<p>A bold twist on timeless. The Sloane blends vintage Y2K attitude with modern edge — crafted in smooth vegan leather with statement hardware.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, statement",
        "variants": [
            {"option1": "Black", "price": "69.99", "compare_at_price": "99.99"},
            {"option1": "Brown", "price": "69.99", "compare_at_price": "99.99"},
            {"option1": "Coffee", "price": "69.99", "compare_at_price": "99.99"},
            {"option1": "Bronze", "price": "69.99", "compare_at_price": "99.99"},
            {"option1": "Pitch green", "price": "69.99", "compare_at_price": "99.99"},
            {"option1": "Burgundy", "price": "69.99", "compare_at_price": "99.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/3261069/pexels-photo-3261069.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/267301/pexels-photo-267301.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Rina Bag",
        "body_html": "<p>A bold suede shoulder bag accented with silver-tone studs for a modern edge. Soft, structured, and made to stand out this season.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, suede",
        "variants": [
            {"option1": "Black", "price": "39.99", "compare_at_price": "89.99"},
            {"option1": "Chocolate brown", "price": "39.99", "compare_at_price": "89.99"},
            {"option1": "Red", "price": "39.99", "compare_at_price": "89.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Seoul Bag",
        "body_html": "<p>A sleek, Korean-inspired shoulder bag with dual front pockets and soft vegan leather finish. Designed for effortless, functional style.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, korean",
        "variants": [
            {"option1": "Silver Black", "price": "49.99", "compare_at_price": "79.99"},
            {"option1": "Glossy Deep Red", "price": "49.99", "compare_at_price": "79.99"},
            {"option1": "Stockholm white", "price": "49.99", "compare_at_price": "79.99"},
            {"option1": "Denim Blue", "price": "49.99", "compare_at_price": "79.99"},
            {"option1": "Coffee", "price": "49.99", "compare_at_price": "79.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/19090/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Maya Bag",
        "body_html": "<p>Maya is a compact shoulder bag designed to carry just what you need — and do it in style. With its softly structured silhouette.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, compact",
        "variants": [
            {"option1": "Black", "price": "79.99", "compare_at_price": "129.99"},
            {"option1": "Glossy Deep Red", "price": "79.99", "compare_at_price": "129.99"},
            {"option1": "Cocoa", "price": "79.99", "compare_at_price": "129.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/6046227/pexels-photo-6046227.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Hayden Bag",
        "body_html": "<p>For the ones who like it practical without losing polish. The Hayden is your go-to everyday bag — structured yet soft, compact yet spacious.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, everyday",
        "variants": [
            {"option1": "Black", "price": "39.99", "compare_at_price": "59.99"},
            {"option1": "Burgundy", "price": "39.99", "compare_at_price": "59.99"},
            {"option1": "Caramel", "price": "39.99", "compare_at_price": "59.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/1478442/pexels-photo-1478442.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/3261069/pexels-photo-3261069.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Briar Bag",
        "body_html": "<p>A structured everyday bag with a modern silhouette, crafted in premium vegan leather.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "bestseller, everyday",
        "variants": [
            {"option1": "Black", "price": "64.99", "compare_at_price": "119.00"},
            {"option1": "Coffee", "price": "64.99", "compare_at_price": "119.00"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/267301/pexels-photo-267301.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Cleo Soft Weave",
        "body_html": "<p>Woven-effect vegan leather exterior with organized compartments. Size: 47 cm (W), 32 cm (H), fits laptops up to 14\".</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "tote, laptop, woven",
        "variants": [
            {"option1": "Black", "price": "54.99", "compare_at_price": "99.00"},
            {"option1": "Burgundy", "price": "54.99", "compare_at_price": "99.00"},
            {"option1": "Coffee", "price": "54.99", "compare_at_price": "99.00"},
            {"option1": "Olive", "price": "54.99", "compare_at_price": "99.00"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/19090/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Noir Frame",
        "body_html": "<p>Suede-textured vegan leather with structured shoulder fit. Size: 40 cm (L), 25 cm (H), 15 cm (W).</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, suede",
        "variants": [
            {"option1": "Coffee", "price": "49.00", "compare_at_price": "99.00"},
            {"option1": "Black", "price": "49.00", "compare_at_price": "99.00"},
            {"option1": "Espresso", "price": "49.00", "compare_at_price": "99.00"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Archive Bag",
        "body_html": "<p>Distressed vegan leather for a lived-in look. Size: 27 cm (W) x 37 cm (H) x 11 cm (D).</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, distressed",
        "variants": [
            {"option1": "Black", "price": "44.99", "compare_at_price": "69.00"},
            {"option1": "Dark Cherry", "price": "44.99", "compare_at_price": "69.00"},
            {"option1": "Windsor Tan", "price": "44.99", "compare_at_price": "69.00"},
            {"option1": "Beige", "price": "44.99", "compare_at_price": "69.00"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/6046227/pexels-photo-6046227.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/1478442/pexels-photo-1478442.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Everyday Petite Tote",
        "body_html": "<p>Soft-touch premium vegan leather with structured shape with natural give. Size: 33 cm (L) x 25 cm (H) x 12 cm (W).</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "tote, petite, everyday",
        "variants": [
            {"option1": "Black", "price": "39.99", "compare_at_price": "79.00"},
            {"option1": "Beige", "price": "39.99", "compare_at_price": "79.00"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/3261069/pexels-photo-3261069.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/267301/pexels-photo-267301.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Soleil Bag",
        "body_html": "<p>Softly structured silhouette, buttery vegan leather, and striking gold buckle. Size: 31 cm (L), 10 cm (W), 29 cm (H).</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, gold",
        "variants": [
            {"option1": "Black", "price": "89.99", "compare_at_price": ""},
            {"option1": "Chocolate Brown", "price": "89.99", "compare_at_price": ""},
            {"option1": "Burgundy", "price": "89.99", "compare_at_price": ""}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Siena Bag",
        "body_html": "<p>Soft vegan leather with structured, minimal shape. Size: 29 x 29.5 x 10 cm.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "shoulder, minimal",
        "variants": [
            {"option1": "Black", "price": "74.99", "compare_at_price": ""},
            {"option1": "Dark Chocolate", "price": "74.99", "compare_at_price": ""}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/19090/pexels-photo.jpg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Plush Bucket Hat",
        "body_html": "<p>A soft, plush bucket hat designed to make any outfit feel instantly elevated. Crafted for warmth without bulk.</p>",
        "vendor": "AYVA",
        "product_type": "Accessories",
        "tags": "accessories, hat",
        "variants": [
            {"option1": "White", "price": "34.95", "compare_at_price": "54.95"},
            {"option1": "Beige", "price": "34.95", "compare_at_price": "54.95"},
            {"option1": "Brown", "price": "34.95", "compare_at_price": "54.95"},
            {"option1": "All-white", "price": "34.95", "compare_at_price": "54.95"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/6046227/pexels-photo-6046227.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "Frost Plush Hat",
        "body_html": "<p>A timeless winter essential crafted in ultra-soft plush. Designed to keep you warm while elevating any cold-weather look.</p>",
        "vendor": "AYVA",
        "product_type": "Accessories",
        "tags": "accessories, hat, winter",
        "variants": [
            {"option1": "Black", "price": "34.95", "compare_at_price": "54.95"},
            {"option1": "White", "price": "34.95", "compare_at_price": "54.95"},
            {"option1": "Beige", "price": "34.95", "compare_at_price": "54.95"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/1478442/pexels-photo-1478442.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/3261069/pexels-photo-3261069.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    },
    {
        "title": "The Petite Luna",
        "body_html": "<p>Soft, sculpted, and unapologetically petite. The Petite Luna is proof that small still makes a statement.</p>",
        "vendor": "AYVA",
        "product_type": "Bags",
        "tags": "mini, petite",
        "variants": [
            {"option1": "Black", "price": "39.99", "compare_at_price": "99.99"},
            {"option1": "Stockholm white", "price": "39.99", "compare_at_price": "99.99"},
            {"option1": "Chocolate brown", "price": "39.99", "compare_at_price": "99.99"},
            {"option1": "Nude beige", "price": "39.99", "compare_at_price": "99.99"}
        ],
        "images": [
            {"src": "https://images.pexels.com/photos/267301/pexels-photo-267301.jpeg?auto=compress&cs=tinysrgb&w=1200"},
            {"src": "https://images.pexels.com/photos/298863/pexels-photo-298863.jpeg?auto=compress&cs=tinysrgb&w=1200"}
        ],
        "options": [{"name": "Color"}]
    }
]

def create_product(product_data):
    title = product_data["title"]
    handle = slugify(title)
    if product_exists(handle):
        print(f"  [skip] {title} — already exists at /products/{handle}")
        return True
    resp = shopify_request("POST", "/products.json", {"product": product_data})
    if resp.status_code == 201:
        body = resp.json()["product"]
        print(f"  ✓ Created: {body['title']} (ID: {body['id']})")
        return True
    print(f"  ✗ Failed: {title} — {resp.status_code}: {redact(resp.text)}")
    return False

def main():
    if not ACCESS_TOKEN:
        print("=" * 60)
        print("  AYVA PRODUCT IMPORTER")
        print("=" * 60)
        print()
        print("ERROR: SHOPIFY_TOKEN env var not set.")
        print()
        print("Set these then re-run:")
        print("  export SHOPIFY_STORE=your-store.myshopify.com")
        print("  export SHOPIFY_TOKEN=shpat_xxx")
        print("  python add_products.py")
        print()
        print("To get a token: Shopify admin → Settings → Apps → Develop apps")
        print("  → Create app → Admin API scopes: write_products, read_products")
        print("  → Install → reveal Admin API access token.")
        print()
        sys.exit(1)

    print("=" * 60)
    print("  AYVA PRODUCT IMPORTER")
    print(f"  Store: {STORE_URL}")
    print(f"  Products to add: {len(PRODUCTS)}")
    print("=" * 60)
    print()

    success = 0
    failed_titles = []

    for i, product in enumerate(PRODUCTS, 1):
        print(f"[{i}/{len(PRODUCTS)}] Adding {product['title']}...")
        if create_product(product):
            success += 1
        else:
            failed_titles.append(product["title"])
        time.sleep(0.6)  # Shopify REST bucket leaks at 2 req/s

    print()
    print("=" * 60)
    print(f"  DONE! ✓ {success} created/skipped | ✗ {len(failed_titles)} failed")
    if failed_titles:
        print()
        print("  Failed products (re-run safe — script is idempotent):")
        for t in failed_titles:
            print(f"    - {t}")
    print("=" * 60)

if __name__ == "__main__":
    main()
