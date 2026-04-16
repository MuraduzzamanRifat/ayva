"""
AYVA Store — AI Image Generator
Generates original lifestyle images matching Scandinavian bag brand aesthetic
Uses OpenAI DALL-E 3
"""
import os
import requests
import base64
import time

API_KEY = os.environ.get("OPENAI_API_KEY", "")
if not API_KEY:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        API_KEY = os.environ.get("OPENAI_API_KEY", "")
    except ImportError:
        pass
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "generated-images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

IMAGES = [
    {
        "name": "01-hero-banner",
        "prompt": "Wide landscape editorial fashion photograph for a premium Scandinavian bag brand. Split composition: left side shows two elegant vegan leather handbags (one dark black, one cream beige with brown trim and decorative charm keychain) artfully placed on a rustic wooden bench in a warm European cafe with wooden walls. Right side shows a stylish young blonde woman in a white t-shirt and wide-leg gray jeans standing in a bright minimalist boutique interior with shelves, casually holding a brown leather shoulder bag. Warm natural lighting, candid editorial style, high-end fashion e-commerce aesthetic. No text or logos.",
        "size": "1792x1024"
    },
    {
        "name": "02-collection-allbags",
        "prompt": "Overhead flat lay photograph of a curated collection of premium vegan leather handbags in various styles (hobo bag, tote, shoulder bag, crossbody) arranged on a clean white marble surface. Colors: black, brown, burgundy, cream. Scandinavian minimal aesthetic, soft natural lighting, fashion e-commerce product photography. No text or logos.",
        "size": "1024x1024"
    },
    {
        "name": "03-collection-new",
        "prompt": "Editorial fashion photograph of a young woman sitting in a modern Scandinavian cafe, casually wearing a stylish outfit with a premium dark leather shoulder bag placed on the table. Multiple bag styles visible in the background on a shelf. Warm tones, natural light from window, candid lifestyle photography for luxury bag brand. No text or logos.",
        "size": "1024x1024"
    },
    {
        "name": "04-collection-accessories",
        "prompt": "Close-up product photography of decorative bag charms and accessories laid on a soft white fabric. Items include pearl charms, gold chain accessories, bow charms, cherry-shaped pendants, and heart keychains. Soft natural lighting, jewelry-style flat lay, premium Scandinavian brand aesthetic. No text or logos.",
        "size": "1024x1024"
    },
    {
        "name": "05-collection-everyday",
        "prompt": "Lifestyle photograph of a woman walking on a European city street carrying a large structured black vegan leather tote bag. She is dressed in smart casual clothing. Autumn city setting with fallen leaves, warm golden hour lighting, editorial street style photography. No text or logos.",
        "size": "1024x1024"
    },
    {
        "name": "06-collection-mini",
        "prompt": "Lifestyle photograph of a fashionable young woman at an outdoor cafe table holding a small compact crossbody mini bag in sage green. Other small elegant mini bags in black and pink visible on the table. Bright natural daylight, European street setting, editorial fashion photography for premium brand. No text or logos.",
        "size": "1024x1024"
    },
    {
        "name": "07-more-than-pretty-bags",
        "prompt": "Bird's eye view photograph of a stylish young blonde woman sitting on a stone sidewalk in a European city, wearing all black outfit with multiple premium handbags around her - a dark burgundy shoulder bag, a black hobo bag, and accessories. Urban concrete texture, overhead shot, editorial fashion photography, moody artistic style. No text or logos.",
        "size": "1024x1024"
    },
    {
        "name": "08-shop-the-look",
        "prompt": "Street style photograph of a large black premium vegan leather hobo bag with silver buckle details, placed on a zebra crossing on a city street. Dramatic urban background slightly blurred, the bag is the hero of the shot. Editorial fashion product photography, high contrast, cinematic feel. No text or logos.",
        "size": "1024x1024"
    },
    {
        "name": "09-style-meets-function",
        "prompt": "Close-up lifestyle photograph of a woman's hands opening a premium black vegan leather shoulder bag, showing the organized interior compartments with a laptop, phone, and cosmetics inside. Clean Scandinavian interior background, soft natural lighting, demonstrating functionality meets style. No text or logos.",
        "size": "1024x1024"
    },
    {
        "name": "10-collection-banner-collage",
        "prompt": "Wide collage-style editorial photograph showing 10 different women in urban European street settings, each carrying a different style of premium vegan leather handbag. Mix of poses: walking, sitting at cafes, standing at crosswalks. Variety of bag styles in black, brown, burgundy, cream. Autumn city vibes, warm tones, street style fashion photography. Grid layout composition with images flowing together. No text or logos.",
        "size": "1792x1024"
    }
]

def generate_image(prompt, size, name):
    """Generate a single image via DALL-E 3"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": "hd",
        "response_format": "b64_json"
    }

    resp = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=payload,
        timeout=120
    )

    if resp.status_code == 200:
        data = resp.json()
        img_b64 = data["data"][0]["b64_json"]
        img_bytes = base64.b64decode(img_b64)
        filepath = os.path.join(OUTPUT_DIR, f"{name}.png")
        with open(filepath, "wb") as f:
            f.write(img_bytes)
        size_mb = len(img_bytes) / (1024 * 1024)
        print(f"  ✓ Saved: {filepath} ({size_mb:.1f} MB)")
        return filepath
    else:
        print(f"  ✗ Failed: {resp.status_code} — {resp.text[:200]}")
        return None

def main():
    print("=" * 60)
    print("  AYVA STORE — AI IMAGE GENERATOR")
    print(f"  Generating {len(IMAGES)} original images")
    print(f"  Output: {OUTPUT_DIR}")
    print("=" * 60)
    print()

    success = 0
    for i, img in enumerate(IMAGES, 1):
        print(f"[{i}/{len(IMAGES)}] Generating {img['name']}...")
        result = generate_image(img["prompt"], img["size"], img["name"])
        if result:
            success += 1
        time.sleep(2)  # Rate limit

    print()
    print("=" * 60)
    print(f"  DONE! {success}/{len(IMAGES)} images generated")
    print("=" * 60)

if __name__ == "__main__":
    main()
