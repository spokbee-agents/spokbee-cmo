export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', true);
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader(
    'Access-Control-Allow-Headers',
    'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version'
  );

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { token, leads } = req.body;
  if (!token) {
    return res.status(400).json({ error: 'Missing HubSpot token' });
  }
  if (!leads || !Array.isArray(leads)) {
    return res.status(400).json({ error: 'Missing or invalid leads array' });
  }

  try {
    const results = [];
    
    for (const lead of leads) {
      // Clean email generation
      const cleanDomain = lead.website ? lead.website.replace(/^https?:\/\//, '').replace(/^www\./, '') : '';
      const email = cleanDomain ? `info@${cleanDomain}` : `${lead.company.toLowerCase().replace(/[^a-z0-9]/g, '')}@spokbee-target.com`;
      
      const hubspotPayload = {
        properties: {
          email: email,
          firstname: lead.company,
          lastname: 'CMO Target Prospect',
          company: lead.company,
          website: lead.website || '',
          industry: lead.industry || '',
          description: `Current Competitor Used: ${lead.competitor}\nProjected Savings: ${lead.savings}\n\nDetected Pain Point:\n${lead.pain}\n\nSpokbee Attack Play:\n${lead.play}`
        }
      };

      const response = await fetch('https://api.hubapi.com/crm/v3/objects/contacts', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(hubspotPayload)
      });

      const responseData = await response.json();
      results.push({
        company: lead.company,
        status: response.status,
        success: response.status === 201 || response.status === 200,
        id: responseData.id || null,
        error: response.status !== 201 && response.status !== 200 ? responseData : null
      });
    }

    return res.status(200).json({ success: true, results });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
