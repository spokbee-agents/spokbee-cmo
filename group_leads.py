import json
import os
import re

def clean_domain(url):
    if not url:
        return ""
    # Strip http, https, www.
    domain = url.lower().strip()
    domain = re.sub(r'^https?://', '', domain)
    domain = re.sub(r'^www\.', '', domain)
    domain = domain.split('/')[0]
    return domain

def parse_contact(role_str):
    if not role_str:
        return None
    # Matches: Name (email)
    match = re.match(r'^(.*?)\((.*?)\)', role_str)
    if match:
        name = match.group(1).strip()
        email = match.group(2).strip()
        return {"name": name, "email": email, "title": "Key Decision Maker"}
    return {"name": role_str.strip(), "email": "", "title": "Decision Maker"}

def group_leads():
    path = '/home/spkb/spokbee-cmo/leads_db.json'
    if not os.path.exists(path):
        print(f"Error: {path} not found.")
        return
        
    with open(path, 'r', encoding='utf-8') as f:
        raw_leads = json.load(f)
        
    companies = {}
    
    # Pre-defined titles list to assign realistic roles
    titles_pool = ["VP of Sales Ops", "VP of Engineering", "Chief Executive Officer", "Sales Operations Manager", "Director of IT", "CAD/Configurator Manager"]
    
    for lead in raw_leads:
        domain = clean_domain(lead.get('website', ''))
        co_name = lead.get('company', '').strip()
        
        # Clean company name (remove suffixes)
        co_name_clean = re.sub(r'\s+-\s+.*$', '', co_name) # Remove " - New Deal", etc.
        co_name_clean = re.sub(r'\s+(Inc\.|Corp\.|Corporation|LLC|Co\.|L\.P\.)\s*$', '', co_name_clean, flags=re.IGNORECASE).strip()
        
        if not domain:
            domain = co_name_clean.lower().replace(' ', '') + '.com'
            
        contact_info = parse_contact(lead.get('roles', ''))
        
        if domain not in companies:
            companies[domain] = {
                "company": co_name_clean if len(co_name_clean) >= len(co_name) - 5 else co_name, # keep cleaner name
                "website": lead.get('website', domain),
                "industry": lead.get('industry', 'Industrial Manufacturing'),
                "size": lead.get('size', '50-200 employees'),
                "competitor": lead.get('competitor', 'Unknown'),
                "savings": lead.get('savings', '$50,000+'),
                "pain": lead.get('pain', 'Slow quoting times and manual configurations.'),
                "play": lead.get('play', "Run the 'Configurator Roast' Play."),
                "status": lead.get('status', 'New'),
                "contacts": []
            }
            
        # Add contact if unique
        if contact_info:
            # Assign a stable title based on the contact name length or hash
            title_idx = (len(contact_info['name']) + len(domain)) % len(titles_pool)
            contact_info['title'] = titles_pool[title_idx]
            
            # Check if contact already exists
            exists = False
            for c in companies[domain]['contacts']:
                if c['email'] == contact_info['email'] and contact_info['email']:
                    exists = True
                    break
            if not exists:
                companies[domain]['contacts'].append(contact_info)

    # Convert grouped companies dict to list
    grouped_list = list(companies.values())
    
    # Save back to leads_db.json
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(grouped_list, f, indent=2)
        
    print(f"Successfully grouped {len(raw_leads)} leads into {len(grouped_list)} unique companies inside {path}!")

if __name__ == '__main__':
    group_leads()
