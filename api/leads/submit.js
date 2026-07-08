const FUB_EVENTS_URL = 'https://api.followupboss.com/v1/events';
const SITE_SOURCE = 'westsummerlinhomes.com';
const SITE_SYSTEM = 'WestSummerlinHomes';

function splitName(fullName) {
  const parts = String(fullName || '')
    .trim()
    .split(/\s+/)
    .filter(Boolean);

  if (parts.length === 0) {
    return { firstName: 'Website', lastName: 'Lead' };
  }

  if (parts.length === 1) {
    return { firstName: parts[0], lastName: 'Lead' };
  }

  return {
    firstName: parts[0],
    lastName: parts.slice(1).join(' '),
  };
}

function normalizePhone(phone) {
  return String(phone || '').replace(/\D/g, '');
}

function buildMessage({ address, notes, source }) {
  const lines = ['Home valuation request from westsummerlinhomes.com'];

  if (source) {
    lines.push(`Source page: ${source}`);
  }

  if (address) {
    lines.push(`Property address: ${address}`);
  }

  if (notes) {
    lines.push(`Details: ${notes}`);
  }

  return lines.join('\n');
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const apiKey = process.env.FUB_API_KEY;
  if (!apiKey) {
    return res.status(503).json({ error: 'Lead service is not configured yet.' });
  }

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
    const { name, phone, email, address, notes, source, type } = body || {};

    if (!name || !phone || !address) {
      return res.status(400).json({ error: 'Name, phone, and property address are required.' });
    }

    const digits = normalizePhone(phone);
    if (digits.length < 10) {
      return res.status(400).json({ error: 'Please enter a valid 10-digit phone number.' });
    }

    const { firstName, lastName } = splitName(name);
    const person = {
      firstName,
      lastName,
      phones: [{ value: phone }],
      tags: ['Website Lead', 'Home Valuation'],
    };

    if (email) {
      person.emails = [{ value: email }];
    }

    const payload = {
      source: SITE_SOURCE,
      system: SITE_SYSTEM,
      type: type || 'Seller Inquiry',
      sourceUrl: source || 'https://westsummerlinhomes.com/home-valuation.html',
      message: buildMessage({ address, notes, source }),
      person,
      property: {
        street: address,
      },
    };

    const response = await fetch(FUB_EVENTS_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Basic ${Buffer.from(`${apiKey}:`).toString('base64')}`,
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('FUB submit failed', response.status, errorText);
      return res.status(502).json({ error: 'Unable to submit your request right now. Please call 702-222-1964.' });
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    console.error('Lead submit error', error);
    return res.status(500).json({ error: 'Something went wrong. Please call 702-222-1964.' });
  }
}
