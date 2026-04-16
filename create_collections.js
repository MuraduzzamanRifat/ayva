/**
 * AYVA Collection Creator
 * Creates all collections matching ayvaofficial.com
 *
 * Usage:
 *   1. Get your Admin API access token (see instructions below)
 *   2. Paste it in ACCESS_TOKEN below
 *   3. Run: node create_collections.js
 *
 * To get token: Shopify Admin → Settings → Apps → Develop apps → Create app
 *   → API scopes: write_products, read_products
 *   → Install → Copy Admin API access token
 */

const https = require('https');

const STORE = 'pu5du4-az.myshopify.com';
const ACCESS_TOKEN = ''; // <-- PASTE TOKEN HERE

const COLLECTIONS = [
  {
    title: 'All Bags',
    body_html: '<p>Timeless, versatile & modern handbags designed in Stockholm.</p>',
    rules: [{ column: 'type', relation: 'equals', condition: 'Bags' }],
    sort_order: 'best-selling',
    image_url: 'https://ayvaofficial.com/cdn/shop/collections/Untitled_design_84.png?v=1773014513&width=1080'
  },
  {
    title: 'NEW',
    body_html: '<p>Our latest arrivals — fresh styles, just dropped.</p>',
    rules: [{ column: 'tag', relation: 'equals', condition: 'new' }],
    sort_order: 'created-desc',
    image_url: 'https://ayvaofficial.com/cdn/shop/collections/14_94f9f338-42de-49d2-b3f8-2adbccbdd0f7.png?v=1773014442&width=1080'
  },
  {
    title: 'Accessories',
    body_html: '<p>Bag charms, hats, and extras to complete your look.</p>',
    rules: [{ column: 'type', relation: 'equals', condition: 'Accessories' }],
    sort_order: 'best-selling',
    image_url: 'https://ayvaofficial.com/cdn/shop/collections/black_month_sale_4.png?v=1762722286&width=1080'
  },
  {
    title: 'AYVA Everyday',
    body_html: '<p>Your go-to bags for work, weekends, and everything in between.</p>',
    rules: [{ column: 'tag', relation: 'equals', condition: 'everyday' }],
    sort_order: 'best-selling',
    image_url: 'https://ayvaofficial.com/cdn/shop/collections/TheBriarBagGrayopen.png?v=1762721783&width=1080'
  },
  {
    title: 'AYVA Mini',
    body_html: '<p>Small bags, big style. Compact designs that still make a statement.</p>',
    rules: [{ column: 'tag', relation: 'equals', condition: 'mini' }],
    sort_order: 'best-selling',
    image_url: 'https://ayvaofficial.com/cdn/shop/collections/CelineBagmatchalifestyle.png?v=1762721721&width=1080'
  },
  {
    title: 'Bag Charms',
    body_html: '<p>Playful charms to personalize your bag.</p>',
    rules: [{ column: 'tag', relation: 'equals', condition: 'charm' }],
    sort_order: 'best-selling',
    image_url: 'https://ayvaofficial.com/cdn/shop/collections/black_month_sale_4.png?v=1762722286&width=1080'
  },
  {
    title: 'Bestsellers',
    body_html: '<p>Our most-loved bags — the ones everyone keeps coming back for.</p>',
    rules: [{ column: 'tag', relation: 'equals', condition: 'bestseller' }],
    sort_order: 'best-selling'
  }
];

function makeRequest(method, path, data) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: STORE,
      path: `/admin/api/2024-01${path}`,
      method,
      headers: {
        'X-Shopify-Access-Token': ACCESS_TOKEN,
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(body) });
        } catch {
          resolve({ status: res.statusCode, data: body });
        }
      });
    });

    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

async function createCollection(col) {
  const payload = {
    smart_collection: {
      title: col.title,
      body_html: col.body_html,
      rules: col.rules,
      sort_order: col.sort_order,
      published: true
    }
  };

  if (col.image_url) {
    payload.smart_collection.image = { src: col.image_url };
  }

  const res = await makeRequest('POST', '/smart_collections.json', payload);

  if (res.status === 201) {
    console.log(`  ✓ Created: ${col.title} (ID: ${res.data.smart_collection.id})`);
    return true;
  } else {
    console.log(`  ✗ Failed: ${col.title} — ${res.status}: ${JSON.stringify(res.data).substring(0, 200)}`);
    return false;
  }
}

async function main() {
  if (!ACCESS_TOKEN) {
    console.log('='.repeat(60));
    console.log('  AYVA COLLECTION CREATOR');
    console.log('='.repeat(60));
    console.log('');
    console.log('ERROR: No API access token set!');
    console.log('');
    console.log('To get your token:');
    console.log('1. Go to Shopify Admin → Settings → Apps and sales channels');
    console.log('2. Click "Develop apps" → "Create an app"');
    console.log('3. Name: "AYVA Setup"');
    console.log('4. Admin API scopes: write_products, read_products');
    console.log('5. Install app → Copy Admin API access token');
    console.log('6. Paste it in this script (ACCESS_TOKEN variable)');
    console.log('7. Run: node create_collections.js');
    console.log('');
    process.exit(1);
  }

  console.log('='.repeat(60));
  console.log('  AYVA COLLECTION CREATOR');
  console.log(`  Store: ${STORE}`);
  console.log(`  Collections to create: ${COLLECTIONS.length}`);
  console.log('='.repeat(60));
  console.log('');

  let success = 0;
  for (const col of COLLECTIONS) {
    console.log(`Creating ${col.title}...`);
    if (await createCollection(col)) success++;
    await new Promise(r => setTimeout(r, 500));
  }

  console.log('');
  console.log('='.repeat(60));
  console.log(`  DONE! ${success}/${COLLECTIONS.length} collections created`);
  console.log('='.repeat(60));
  console.log('');
  console.log('Next: Set up navigation menu');
  console.log('  Go to Online Store → Navigation → Main menu');
  console.log('  Add: ALL BAGS, NEW, ACCESSORIES, INFO (dropdown)');
}

main().catch(console.error);
