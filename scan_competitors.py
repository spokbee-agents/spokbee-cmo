# /// script
# dependencies = [
#   "httpx",
# ]
# ///

import json
import httpx
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import os

def detect_competitor(html_content, url):
    html_lower = html_content.lower()
    
    # 1. Tacton
    if "tacton" in html_lower or "tacton-cdn" in html_lower:
        return "Tacton"
        
    # 2. Threekit
    if "threekit" in html_lower or "clara.io" in html_lower:
        return "Threekit"
        
    # 3. Logik.ai
    if "logik.ai" in html_lower or "logik-cdn" in html_lower or "logik_app" in html_lower:
        return "Logik.ai"
        
    # 4. Salsita
    if "salsita" in html_lower or "salsitacloud" in html_lower or "salsita-3d" in html_lower:
        return "Salsita"
        
    # 5. Salesforce CPQ / Steelbrick
    if "steelbrick" in html_lower or "sb.js" in html_lower or "salesforce-cpq" in html_lower:
        return "Salesforce CPQ"
        
    # 6. Oracle CPQ
    if "bigmachines" in html_lower or "oracle-cpq" in html_lower:
        return "Oracle CPQ"
        
    # 7. Epicor CPQ / KBMax
    if "kbmax" in html_lower or "kbmax.com" in html_lower or "epicor-cpq" in html_lower:
        return "Epicor CPQ"
        
    # 8. Infor CPQ
    if "infor-cpq" in html_lower or "tdconfigure" in html_lower:
        return "Infor CPQ"
        
    return "Unknown"

def scan_website(lead):
    company = lead.get('company', 'Unknown Company')
    website = lead.get('website', '')
    if not website:
        return lead, "No Website"
        
    # Standardize URL
    url = website
    if not url.startswith('http'):
        url = 'https://' + url
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # We do a GET request with a short timeout
        # Using follow_redirects=True to handle domain redirects
        with httpx.Client(headers=headers, timeout=5.0, verify=False) as client:
            response = client.get(url, follow_redirects=True)
            if response.status_code == 200:
                competitor = detect_competitor(response.text, url)
                return lead, competitor
            else:
                # Try http if https failed, or vice versa
                if url.startswith('https://'):
                    alt_url = url.replace('https://', 'http://')
                    response = client.get(alt_url, follow_redirects=True)
                    if response.status_code == 200:
                        competitor = detect_competitor(response.text, alt_url)
                        return lead, competitor
                return lead, "Unknown"
    except Exception as e:
        # If connection failed, fallback to Unknown
        return lead, "Unknown"

def main():
    path = '/home/spkb/spokbee-cmo/leads_db.json'
    if not os.path.exists(path):
        print(f"Error: {path} does not exist.")
        return
        
    with open(path, 'r', encoding='utf-8') as f:
        leads = json.load(f)
        
    print(f"Loaded {len(leads)} leads. Starting concurrent tech-stack scan (max 50 workers)...")
    
    updated_leads = []
    stats = {}
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_website, lead): lead for lead in leads}
        
        completed_count = 0
        for future in as_completed(futures):
            lead, competitor = future.result()
            lead['competitor'] = competitor
            
            # Update stats
            stats[competitor] = stats.get(competitor, 0) + 1
            updated_leads.append(lead)
            
            completed_count += 1
            if completed_count % 20 == 0 or completed_count == len(leads):
                print(f"Progress: {completed_count}/{len(leads)} websites scanned...")
                
    # Save back to file
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(updated_leads, f, indent=2)
        
    print("\nScan completed successfully!")
    print("----- Tech Stack Detection Stats -----")
    for comp, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f" - {comp}: {count} leads")
    print(f"Results successfully saved back to {path}!")

if __name__ == '__main__':
    main()
