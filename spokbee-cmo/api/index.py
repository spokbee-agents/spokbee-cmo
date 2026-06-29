import os
import json
import httpx
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load local environment variables
load_dotenv()

app = FastAPI(title="Spokbee AI CMO Terminal API")

# Enable CORS for local development and Vercel hosting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core Spokbee CMO Knowledge & Target Lists
TARGET_TIERS = {
    "tier1_form": [
        {"name": "Brenntag", "domain": "brenntag.com", "industry": "Chemical Distribution", "pain": "Formulas & logistical constraints managed via massive spreadsheets; no self-service configure/price.", "play": "Form-Based Configurator"},
        {"name": "Clean Harbors", "domain": "cleanharbors.com", "industry": "Environmental Services", "pain": "Complex industrial waste services require tedious quoting cycles instead of immediate transactional parameters.", "play": "Form-Based Configurator"},
        {"name": "C.H. Robinson", "domain": "chrobinson.com", "industry": "Logistics & Transport", "pain": "Dynamic multi-modal shipping rates are completely locked behind custom request-a-quote channels.", "play": "Form-Based Configurator"}
    ],
    "tier2_image": [
        {"name": "4imprint", "domain": "4imprint.com", "industry": "Promotional Items", "pain": "Has 10,000+ custom promotional SKUs but lacks a real-time, interactive visual overlay/preview on mobile.", "play": "Image-Based Configurator"},
        {"name": "FASTSIGNS", "domain": "fastsigns.com", "industry": "Custom Signage", "pain": "No automated dynamic visual mockups of signage dimensions and materials in-browser.", "play": "Image-Based Configurator"},
        {"name": "Sticker Mule", "domain": "stickermule.com", "industry": "Custom Printing", "pain": "Excellent static proofing, but lacks real constraint-driven bulk pricing models that embed anywhere.", "play": "Image-Based Configurator"}
    ],
    "tier3_3d": [
        {"name": "Winnebago", "domain": "winnebago.com", "industry": "RV/Vehicles", "pain": "3D visualizers are slow, non-interactive, or disconnected from the actual engineering BOM constraints.", "play": "3D Interactive Configurator"},
        {"name": "Malibu Boats", "domain": "malibuboats.com", "industry": "Marine Equipment", "pain": "High-ticket spatial customizations (towers, engines, wraps) are fully manual; lacks live CAD parameter updates.", "play": "3D Interactive Configurator"},
        {"name": "Vermeer", "domain": "vermeer.com", "industry": "Industrial Equipment", "pain": "Heavy excavation equipment options (bucket size, tracks, engine) require manual engineering review before pricing.", "play": "3D Interactive Configurator"}
    ]
}

GTM_PLAYS = {
    "demo": {
        "name": "The 'Unsolicited Interactive Demo' Play",
        "description": "Scrape static product catalog, auto-generate live Spokbee configurator, and draft personalized email containing the demo.",
        "steps": [
            "Initializing scrapers to target domain...",
            "Crawling product pages and catalog schemas...",
            "Extracting 2D flat product images...",
            "Generating Spokbee Logic & constraints (AC-3 constraint engine)...",
            "Synthesizing customized 3D/Image-Based preview payload...",
            "Compiling outreach copy containing the live preview widget URL..."
        ]
    },
    "roast": {
        "name": "The 'Configurator Roast' Play",
        "description": "Deconstruct a prospect's slow, friction-heavy quoting loop and compile a side-by-side 'before vs after' comparison.",
        "steps": [
            "Analyzing target quote-request form...",
            "Mapping checkout friction points and page latency...",
            "Calculating estimated sales leak and revenue drop...",
            "Generating comparison report (Enterprise Legacy CPQ vs Spokbee Fast-to-Live)...",
            "Drafting LinkedIn roast & custom-tailored solution proposal..."
        ]
    },
    "agent_commerce": {
        "name": "The 'Agent-Ready API' Campaign",
        "description": "Pitch to CIOs of target brands to expose their custom product configurations as machine-readable APIs for AI purchasing agents.",
        "steps": [
            "Analyzing product attributes for machine readability...",
            "Mapping API endpoints to `/api/v1/configure` JSON schemas...",
            "Drafting 'Agent Compatible' certification and sales letters...",
            "Compiling automated follow-up sequences..."
        ]
    }
}

class TerminalInput(BaseModel):
    command: str

class GenerateInput(BaseModel):
    prompt: str
    context: str = ""

@app.get("/api/status")
def get_status():
    return {
        "status": "online",
        "cmo_core": "active",
        "environment": "vercel" if os.environ.get("VERCEL") else "local",
        "agents": {
            "reddit_agent": "monitoring",
            "x_agent": "drafting",
            "linkedin_agent": "idle",
            "geo_agent": "active",
            "seo_agent": "monitoring",
            "ugc_agent": "idle"
        },
        "metrics": {
            "enriched_leads": 342,
            "social_reach_growth": "+14.2%",
            "seo_score": 94,
            "active_plays": 3
        }
    }

@app.post("/api/terminal")
def run_terminal(payload: TerminalInput):
    cmd_raw = payload.command.strip()
    if not cmd_raw:
        return {"output": "", "trigger": None}
    
    parts = cmd_raw.split()
    cmd = parts[0].lower()
    args = parts[1:]

    # 1. HELP COMMAND
    if cmd == "help":
        output = (
            "=========================================================\r\n"
            "   SPOKBEE AI CMO - COMMAND CENTER TERMINAL v1.0\r\n"
            "=========================================================\r\n"
            "Available Commands:\r\n"
            "  help                      Display this help manual.\r\n"
            "  status                    Check current system pulse and active CMO agents.\r\n"
            "  leads                     List enriched manufacturer prospects by Tier & Play.\r\n"
            "  plays                     Show available high-converting GTM growth plays.\r\n"
            "  run [play_id] [domain]    Execute a GTM campaign for a target manufacturer.\r\n"
            "                            E.g. 'run demo 4imprint.com' or 'run roast winnebago.com'\r\n"
            "  seo                       Perform real-time SEO audit and keyword gap analysis.\r\n"
            "  geo                       Run Generative Engine Optimization gap report.\r\n"
            "  clear                     Clear the terminal display.\r\n"
            "=========================================================\r\n"
        )
        return {"output": output, "trigger": None}

    # 2. STATUS COMMAND
    elif cmd == "status":
        output = (
            "CMO CORE ENGINE STATUS: [🟢 ACTIVE / RUNNING]\r\n"
            "System Time: 2026-06-19 00:00:00 UTC\r\n"
            "---------------------------------------------------------\r\n"
            "🤖 Reddit Agent:     [🟢 MONITORING] - 12 subreddits tracked. Active thread found.\r\n"
            "🤖 X / Twitter Agent: [🟡 DRAFTING]   - Scheduled thread: 'Legacy CPQ is a Scam'.\r\n"
            "🤖 LinkedIn Agent:   [⚪ IDLE]       - Draft queue full. Awaiting review.\r\n"
            "🤖 GEO Audit Agent:  [🟢 ACTIVE]     - Auditing Perplexity answers for CPQ.\r\n"
            "🤖 SEO Monitor:      [🟢 MONITORING] - Shopify 3D search intent up 40%.\r\n"
            "🤖 UGC Script Agent: [⚪ IDLE]       - Script templates loaded.\r\n"
            "---------------------------------------------------------\r\n"
            "Global Reach Growth: +14.2% (last 7 days)\r\n"
            "Enriched CRM Contacts: 342 high-fit targets.\r\n"
            "Deploy Status: Live on Vercel Global Edge (spokbee-cmo.vercel.app)\r\n"
        )
        return {"output": output, "trigger": None}

    # 3. LEADS COMMAND
    elif cmd == "leads":
        output = "SPOKBEE HIGH-FIT TARGETS CRM (CLAY & RB2B ENRICHED):\r\n\r\n"
        for tier, prospects in TARGET_TIERS.items():
            output += f"--- {tier.replace('_', ' ').upper()} ---\r\n"
            for p in prospects:
                output += f"• {p['name']} ({p['domain']}) | {p['industry']}\r\n"
                output += f"  Pain: {p['pain']}\r\n"
                output += f"  Recommended Play: {p['play']}\r\n\r\n"
        return {"output": output, "trigger": "show_leads"}

    # 4. PLAYS COMMAND
    elif cmd == "plays":
        output = "SPOKBEE GTM GROWTH-HACKING PLAYS:\r\n\r\n"
        for pid, play in GTM_PLAYS.items():
            output += f"ID: {pid}\r\n"
            output += f"Name: {play['name']}\r\n"
            output += f"Description: {play['description']}\r\n"
            output += "Steps:\r\n"
            for step in play['steps']:
                output += f"  -> {step}\r\n"
            output += "---------------------------------------------------------\r\n\r\n"
        return {"output": output, "trigger": None}

    # 5. RUN PLAY COMMAND
    elif cmd == "run":
        if len(args) < 2:
            return {
                "output": "❌ Error: Missing parameters. Usage: run [play_id] [domain]\r\nE.g., 'run demo 4imprint.com' or 'run roast winnebago.com'\r\n",
                "trigger": None
            }
        play_id = args[0].lower()
        domain = args[1].lower()

        if play_id not in GTM_PLAYS:
            return {
                "output": f"❌ Error: GTM play '{play_id}' not found. Type 'plays' to see available plays.\r\n",
                "trigger": None
            }

        # Let's find if we have a mock target or build a custom one on the fly
        target_name = domain.split('.')[0].capitalize()
        target_industry = "Manufacturing"
        target_pain = "Manual quoting and lack of real-time custom product visualizations."
        
        # Search targets
        found = False
        for tier, prospects in TARGET_TIERS.items():
            for p in prospects:
                if p["domain"].lower() in domain or domain in p["domain"].lower():
                    target_name = p["name"]
                    target_industry = p["industry"]
                    target_pain = p["pain"]
                    found = True
                    break
            if found: break

        play = GTM_PLAYS[play_id]
        
        # Build beautiful step-by-step terminal logs
        output = f"⚡ INITIALIZING CAMPAIGN RUN | Play: {play['name']} | Target: {target_name} ({domain})\r\n"
        output += "-------------------------------------------------------------------------\r\n"
        for step in play["steps"]:
            output += f"[+] {step}\r\n"
        
        output += "-------------------------------------------------------------------------\r\n"
        output += "✅ CAMPAIGN COMPILATION SUCCESSFUL!\r\n\r\n"
        
        # Generate outreach email based on play
        email_draft = ""
        if play_id == "demo":
            email_draft = (
                f"Subject: I built a live 3D configurator for {target_name} (in 4 minutes)\r\n\r\n"
                f"Hi Karina,\r\n\r\n"
                f"I was auditing {domain} and loved your product catalog. However, I noticed custom configurations require a manual 'request a quote' form, which kills mobile conversion rates. \r\n\r\n"
                f"Instead of asking for a call, I went ahead and used Spokbee to build a working {play_id} prototype of your core product. You can spin, customize, and price it instantly here:\r\n"
                f"👉 https://spokbee.ai/demo/{target_name.lower()}-configurator-options\r\n\r\n"
                f"We do this in minutes because of our real AC-3 constraint propagation engine. It embeds into Shopify or any website with a single line of HTML. \r\n\r\n"
                f"Do you have 5 minutes next Thursday to see how we could replace your static quote forms with live 3D self-service? I'll have a fully priced model of your top-selling SKU ready for you.\r\n\r\n"
                f"Cheers,\r\n"
                f"Karina | Spokbee AI CMO\r\n"
            )
        elif play_id == "roast":
            email_draft = (
                f"Subject: Quick roast of {target_name}'s checkout flow (and how to fix it)\r\n\r\n"
                f"Hi Team,\r\n\r\n"
                f"I ran a performance and UX audit on {domain}'s custom catalog and found some major conversion friction:\r\n"
                f"1. To customize, a user has to fill a 12-field form (98% drop-off rate on mobile).\r\n"
                f"2. Pricing is hidden behind a manual 24-hour CAD engineering verification queue.\r\n"
                f"3. Zero real-time visualization - users are buying blind.\r\n\r\n"
                f"Here is a side-by-side comparison of your current flow versus a Spokbee-driven self-service loop where the customer gets instant pricing, a 3D visual preview, and an automated bill of materials: \r\n"
                f"👉 https://spokbee.ai/roast/{target_name.lower()}\r\n\r\n"
                f"By moving this logic from your engineering desk to the browser via our WebAssembly engine, we can cut your sales cycles from 3 days to 30 seconds. \r\n\r\n"
                f"Let me know if you want the raw blueprint files!\r\n\r\n"
                f"Best,\r\n"
                f"Karina | Spokbee AI GTM Lead\r\n"
            )
        else:
            email_draft = (
                f"Subject: Is {target_name}'s product catalog ready for AI Procurement Agents?\r\n\r\n"
                f"Hi VP Ops,\r\n\r\n"
                f"In 2026, over 25% of commercial parts are purchased programmatically by procurement AIs. However, {domain}’s options are locked behind static HTML and PDFs.\r\n\r\n"
                f"I took your catalog data and generated an AI-readable schema using Spokbee's Agentic Commerce API. This lets search agents discover, configure, and purchase custom configurations from you autonomously: \r\n"
                f"👉 https://spokbee.ai/api/v1/{target_name.lower()}/schema\r\n\r\n"
                f"Let's get you listed on the Agentic Catalog Registry this week.\r\n\r\n"
                f"Warmly,\r\n"
                f"Karina\r\n"
            )

        output += f"--- OUTBOUND OUTREACH ENVELOPE GENERATED ---\r\n\r\n{email_draft}"
        
        # Trigger frontend to show the customized preview
        trigger_payload = {
            "type": "show_campaign_result",
            "play_id": play_id,
            "domain": domain,
            "target_name": target_name,
            "industry": target_industry,
            "pain": target_pain,
            "email_draft": email_draft
        }
        
        return {"output": output, "trigger": trigger_payload}

    # 6. SEO COMMAND
    elif cmd == "seo":
        output = (
            "=========================================================\r\n"
            "   SPOKBEE.AI - REAL-TIME SEO AUDIT & GAP REPORT\r\n"
            "=========================================================\r\n"
            "Global SEO Score: 94/100 (Excellent Core Web Vitals)\r\n"
            "Domain Authority (Estimated): 32/100 (Growth phase)\r\n\r\n"
            "🔥 CRITICAL KEYWORD OPPORTUNITIES (Intent Spikes):\r\n"
            "1. '3D product configurator for Shopify'  | Volume: 4.2K/mo (+42% YoY) | Rank: #14 (Needs Blog post)\r\n"
            "2. 'No-code CPQ for manufacturing'       | Volume: 1.8K/mo (+55% YoY) | Rank: #8 (Rank rising)\r\n"
            "3. 'WebAssembly dynamic pricing engine'   | Volume: 900/mo  (+12% YoY) | Rank: #4 (Strong fit)\r\n"
            "4. 'CAD to 3D web converter tool'        | Volume: 2.1K/mo (+68% YoY) | Rank: #21 (Build free tool!)\r\n\r\n"
            "🛠️ RECOMMENDATION:\r\n"
            "Publish a high-intent technical article targeting '3D product configurator for Shopify' showing how Spokbee loads glTF assets in <100ms compared to Shopify's slow native viewer.\r\n"
            "=========================================================\r\n"
        )
        return {"output": output, "trigger": "show_seo"}

    # 7. GEO COMMAND
    elif cmd == "geo":
        output = (
            "=========================================================\r\n"
            "   GENERATIVE ENGINE OPTIMIZATION (GEO) REPORT\r\n"
            "=========================================================\r\n"
            "GEO Visibility Rating: 68% (Fair, needs improvement)\r\n"
            "We audited how 4 top LLM engines summarize Spokbee:\r\n\r\n"
            "🤖 Perplexity AI: 'Spokbee is a lightweight 3D product visualizer...'\r\n"
            "   ❌ Gap: Fails to highlight Spokbee's core AC-3 constraint engine and enterprise CRM integrations.\r\n"
            "   👉 Fix: Inject JSON-LD structured schema with `knowsAbout` fields targeting arc-consistency algorithms.\r\n\r\n"
            "🤖 Gemini (Google): 'Spokbee allows manufacturers to display vehicles/equipment in 3D...'\r\n"
            "   ❌ Gap: Misses Agent Commerce and machine-to-machine checkout.\r\n"
            "   👉 Fix: Publish an open-source MCP (Model Context Protocol) server package and register it on HuggingFace.\r\n\r\n"
            "🤖 ChatGPT (OpenAI): 'Spokbee is an interactive e-commerce platform...'\r\n"
            "   ❌ Gap: Confuses Spokbee with generic Shopify product customizers.\r\n"
            "   👉 Fix: Emphasize the 'Speed to Live' and 'No-Code CAD logic' differentiator in PR releases.\r\n\r\n"
            "🛠️ ACTIONS SCHEDULED FOR INGESTION:\r\n"
            "1. Deploy structured JSON-LD Schema to spokbee.ai.\r\n"
            "2. Publish GitHub repository for spokbee-mcp-server.\r\n"
            "=========================================================\r\n"
        )
        return {"output": output, "trigger": "show_geo"}

    # DEFAULT FALLBACK
    else:
        # Check if they type a conversational prompt or something we don't recognize
        # We can simulate a smart AI assistant answering
        output = (
            f"💻 COMMAND NOT RECOGNIZED: '{cmd}'\r\n"
            f"Let me run an on-demand AI thinking loop to draft a strategic marketing response for your query: '{cmd_raw}'...\r\n\r\n"
            "---------------------------------------------------------\r\n"
            "💡 SPOKBEE AI CMO RESPONSE DRAFT:\r\n"
            f"Here is a strategic growth-hacking proposal for Spokbee targeting: '{cmd_raw}'\r\n\r\n"
            "1. THE ANGLE:\r\n"
            "We should lead with Spokbee's 50x cost reduction ($299/mo Pro vs $150K legacy CPQ implementation costs).\r\n"
            "Most mid-market manufacturers believe 3D configurators require heavy custom agencies. We dismantle this myth.\r\n\r\n"
            "2. OUTREACH HOOK:\r\n"
            "\"Why are you spending 6 months and $100K on an Epicor deployment when we built a working 3D configurator of your custom trailers in 10 minutes?\"\r\n\r\n"
            "3. RECOMMENDATION:\r\n"
            "Create a quick 60-second Loom recording showing yourself dragging Onshape assembly nodes into Spokbee, and send it directly to the VP of IT at Club Car.\r\n"
            "---------------------------------------------------------\r\n"
            "Type 'help' to see standard system commands.\r\n"
        )
        return {"output": output, "trigger": None}

@app.post("/api/generate")
def run_generate(payload: GenerateInput):
    openai_key = os.environ.get("OPENAI_API_KEY")
    prompt = payload.prompt
    context = payload.context

    # If the user has configured OpenAI in their Vercel dashboard, let's use it!
    if openai_key:
        try:
            # Simple synchronous call to OpenAI
            from openai import OpenAI
            client = OpenAI(api_key=openai_key)
            system_prompt = (
                "You are Herald, the Chief Marketing Officer (CMO) for Spokbee.ai.\n"
                "Spokbee is an AI-powered CPQ platform turning complex catalogs into live interactive configurators in minutes.\n"
                "Core messaging pillars:\n"
                "1. Speed to Live (minutes not months)\n"
                "2. Real engineering / AC-3 constraint propagation (not simple if/then rules)\n"
                "3. Agent Commerce (machine-readable APIs for AI buying agents)\n"
                "4. 50x cost reduction ($299/mo vs $150K+ legacy CPQ).\n"
                "Write conversational, bold, punchy, non-corporate growth hacking copy. Led with value."
            )
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context: {context}\n\nTask: {prompt}"}
                ],
                temperature=0.7
            )
            return {"text": response.choices[0].message.content, "engine": "openai-gpt-4o-mini"}
        except Exception as e:
            # Fallback on failure
            pass

    # High-quality fallback templates
    if "tweet" in prompt.lower() or "twitter" in prompt.lower() or "x " in prompt.lower():
        text = (
            "🧵 Why legacy CPQ systems ($150K+ setup, 6-month delay) are a scam for mid-market manufacturers:\r\n\r\n"
            "1/ If you build custom pumps, trucks, or equipment, sales engineers spend 40% of their time manually configuring quotes on spreadsheets.\r\n\r\n"
            "2/ They think they need an agency. In 2026, you can drag your Onshape CAD files directly into Spokbee and get a live, priced 3D configurator in 5 minutes. No code.\r\n\r\n"
            "3/ Even better: our WebAssembly engine runs the rules locally. Zero latency pricing. Real AC-3 constraint propagation means impossible configurations are weeded out instantly.\r\n\r\n"
            "Stop bleeding deals to 'Request a Quote' forms. Let customers configure & checkout in seconds. ⚡"
        )
    elif "linkedin" in prompt.lower() or "article" in prompt.lower():
        text = (
            "**Is Your 'Request a Quote' Button Leaking Millions?**\r\n\r\n"
            "Every day, custom manufacturers send high-intent buyers into a black hole: the manual quoting form.\r\n\r\n"
            "They fill out 15 fields, wait 3 days for sales engineering to check CAD constraints, and receive a PDF pricing quote. By then, they've already checked out a competitor.\r\n\r\n"
            "At Spokbee, we built the definitive operating system for programmable products. We took the heavy constraint-propagation mathematics (arc-consistency AC-3 algorithms) and compiled them into Rust/WebAssembly.\r\n\r\n"
            "The result? A zero-latency, cloud-native 3D configurator that embeds on Shopify or your site with one line of code.\r\n\r\n"
            "1. Pricing updates in real time.\r\n"
            "2. The 3D model rotates and snaps perfectly based on actual CAD parameters.\r\n"
            "3. The Bill of Materials (BOM) is automatically compiled and pushed to your ERP.\r\n\r\n"
            "We cut GTM launch times from 6 months to 5 minutes, and subscription costs by 50x ($299/mo Pro vs $150,000 enterprise setup fee).\r\n\r\n"
            "Let’s stop wasting your sales engineers' time. Build a live demo of your catalog today. 👇"
        )
    else:
        text = (
            f"Here is a customized CMO GTM copy draft for Spokbee AI:\r\n\r\n"
            f"We are launching Spokbee's new outbound sequence targeting manufacturing leaders.\r\n"
            f"Core Hook: 'Move from Onshape assembly to live 3D widget in under 10 minutes.'\r\n\r\n"
            f"Why it lands: They are currently paying $15K/month to consulting agencies to build custom WebGL renderers. Spokbee does it out-of-the-box for a fraction of the cost, powered by a real-time Rust engine in the browser.\r\n"
            f"Let's deploy this campaign immediately to our Clay enriched list!"
        )

    return {"text": text, "engine": "spokbee-local-cmo-mind"}


class SyncHubspotInput(BaseModel):
    token: str
    leads: list

@app.post("/api/sync-hubspot")
async def sync_hubspot(payload: SyncHubspotInput):
    token = payload.token
    leads = payload.leads
    
    results = []
    async with httpx.AsyncClient() as client:
        for lead in leads:
            company = lead.get("company", "")
            website = lead.get("website", "")
            industry = lead.get("industry", "")
            competitor = lead.get("competitor", "")
            savings = lead.get("savings", "")
            pain = lead.get("pain", "")
            play = lead.get("play", "")
            
            # Clean email generation
            clean_domain = website.replace("https://", "").replace("http://", "").replace("www.", "") if website else ""
            if clean_domain:
                email = f"info@{clean_domain}"
            else:
                email = f"{re.sub(r'[^a-z0-9]', '', company.lower())}@spokbee-target.com"
                
            hubspot_payload = {
                "properties": {
                    "email": email,
                    "firstname": company,
                    "lastname": "CMO Target Prospect",
                    "company": company,
                    "website": website,
                    "industry": industry,
                    "description": f"Current Competitor Used: {competitor}\nProjected Savings: {savings}\n\nDetected Pain Point:\n{pain}\n\nSpokbee Attack Play:\n{play}"
                }
            }
            
            try:
                response = await client.post(
                    "https://api.hubapi.com/crm/v3/objects/contacts",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    },
                    json=hubspot_payload,
                    timeout=10.0
                )
                
                resp_data = response.json()
                results.append({
                    "company": company,
                    "status": response.status_code,
                    "success": response.status_code in [200, 201],
                    "id": resp_data.get("id") if response.status_code in [200, 201] else None,
                    "error": resp_data if response.status_code not in [200, 201] else None
                })
            except Exception as e:
                results.append({
                    "company": company,
                    "status": 500,
                    "success": False,
                    "id": None,
                    "error": str(e)
                })
                
    return {"success": True, "results": results}
