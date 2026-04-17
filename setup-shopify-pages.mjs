/**
 * One-shot Shopify page setup.
 *
 * Creates the 5 pages this theme needs (About + 4 policies) with the
 * correct handles and template suffixes, so the theme's /pages/* routes
 * stop 404-ing. Pages are created with empty bodies — the copy lives in
 * the theme templates.
 *
 * Run once after connecting the theme to your store:
 *
 *   1. Shopify admin → Settings → Apps and sales channels → Develop apps
 *      → Create an app → API credentials → Configure Admin API scopes
 *      → enable: write_content, read_content → Install → copy the
 *      "Admin API access token" (starts with shpat_...)
 *
 *   2. In a terminal, from this folder:
 *
 *        export SHOPIFY_STORE=your-store.myshopify.com
 *        export SHOPIFY_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
 *        node setup-shopify-pages.mjs
 *
 *      On Windows PowerShell:
 *
 *        $env:SHOPIFY_STORE="your-store.myshopify.com"
 *        $env:SHOPIFY_TOKEN="shpat_xxxx"
 *        node setup-shopify-pages.mjs
 *
 * Safe to re-run: existing pages with matching handles are skipped.
 */

const STORE = process.env.SHOPIFY_STORE;
const TOKEN = process.env.SHOPIFY_TOKEN;
const API_VERSION = '2024-04';

if (!STORE || !TOKEN) {
  console.error('Missing env vars. Set SHOPIFY_STORE and SHOPIFY_TOKEN.');
  process.exit(1);
}

const PAGES = [
  { title: 'About us',         handle: 'about-us',         template_suffix: 'about' },
  { title: 'Privacy policy',   handle: 'privacy-policy',   template_suffix: 'privacy-policy' },
  { title: 'Refund policy',    handle: 'refund-policy',    template_suffix: 'refund-policy' },
  { title: 'Shipping policy',  handle: 'shipping-policy',  template_suffix: 'shipping-policy' },
  { title: 'Terms of service', handle: 'terms-of-service', template_suffix: 'terms-of-service' },
];

const headers = {
  'X-Shopify-Access-Token': TOKEN,
  'Content-Type': 'application/json',
  Accept: 'application/json',
};

// Scrub the access token from any text about to be thrown / logged.
function redact(s) {
  if (!s || !TOKEN) return s;
  return String(s).split(TOKEN).join('[REDACTED]');
}

// Wrap fetch with 429-retry honoring Retry-After; up to 4 total attempts.
// Caller-supplied headers are overridden by our auth header so a bad caller
// can't accidentally clear the token.
async function shopifyFetch(path, init = {}, attempt = 1) {
  const MAX_ATTEMPTS = 4;
  const res = await fetch(`https://${STORE}/admin/api/${API_VERSION}${path}`, {
    ...init,
    headers: { ...(init.headers || {}), ...headers },
  });
  if (res.status === 429 && attempt < MAX_ATTEMPTS) {
    const retryAfter = Number(res.headers.get('retry-after')) || 2;
    await new Promise((r) => setTimeout(r, retryAfter * 1000));
    return shopifyFetch(path, init, attempt + 1);
  }
  if (!res.ok) {
    const body = await res.text().catch((e) => `<body read failed: ${e.message}>`);
    throw new Error(
      `${init.method || 'GET'} ${path} failed after ${attempt} attempt(s): ${res.status} ${redact(body)}`
    );
  }
  return res.json();
}

async function findByHandle(handle) {
  const { pages } = await shopifyFetch(`/pages.json?handle=${encodeURIComponent(handle)}`);
  return pages?.[0] ?? null;
}

async function createPage({ title, handle, template_suffix }) {
  const { page } = await shopifyFetch('/pages.json', {
    method: 'POST',
    body: JSON.stringify({
      page: { title, handle, template_suffix, body_html: '', published: true },
    }),
  });
  return page;
}

async function updateTemplate(id, template_suffix) {
  const { page } = await shopifyFetch(`/pages/${id}.json`, {
    method: 'PUT',
    body: JSON.stringify({ page: { id, template_suffix } }),
  });
  return page;
}

(async () => {
  console.log(`Setting up 5 pages on ${STORE}...\n`);

  for (const spec of PAGES) {
    try {
      const existing = await findByHandle(spec.handle);
      if (existing) {
        if (existing.template_suffix !== spec.template_suffix) {
          await updateTemplate(existing.id, spec.template_suffix);
          console.log(`  [updated]  /pages/${spec.handle}  (template -> page.${spec.template_suffix})`);
        } else {
          console.log(`  [skipped]  /pages/${spec.handle}  (already correct)`);
        }
      } else {
        await createPage(spec);
        console.log(`  [created]  /pages/${spec.handle}  (template: page.${spec.template_suffix})`);
      }
    } catch (err) {
      console.error(`  [failed]   /pages/${spec.handle}  — ${redact(err.message)}`);
    }
  }

  console.log('\nDone. Visit /pages/about-us on your store to verify.');
})();
