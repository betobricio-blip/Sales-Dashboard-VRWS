import json
import re
import html

data = json.load(open('all_data.json'))

def cls(s):
    return re.sub(r'[^a-zA-Z0-9]+', '-', str(s or ''))

# Data as JSON
data_json_str = json.dumps(data)

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VRWS 2026 Opportunity Ledger (Confidential)</title>
  
  <!-- Anti-Crawler / Anti-Indexing Directives -->
  <meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex, nocache">
  <meta name="googlebot" content="noindex, nofollow, noarchive, nosnippet">
  <meta name="bingbot" content="noindex, nofollow, noarchive, nosnippet">
  <meta name="referrer" content="no-referrer">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=Libre+Franklin:wght@700;800&display=swap" rel="stylesheet">
  
  <style>
    :root {{
      --bg: #f5f6f9;
      --panel: #ffffff;
      --panel2: #eef0f5;
      --border: #dfe3ec;
      --text: #171b26;
      --muted: #626a7d;
      --accent: #2f5fd6;
      --accent-soft: #e8eefc;
      --customer: #1c8a5a;
      --customer-bg: #e3f4ec;
      --pipeline: #a2660a;
      --pipeline-bg: #faf0dc;
      --cold: #b7402f;
      --cold-bg: #fbe9e5;
      --lead: #626a7d;
      --lead-bg: #eef0f5;
      --consistent: #1c8a5a;
      --growth: #2f5fd6;
      --outdated: #b7402f;
      --na: #8890a1;
    }}
    @media (prefers-color-scheme: dark) {{
      :root:not([data-theme="light"]) {{
        --bg: #0f1219;
        --panel: #171b26;
        --panel2: #1d2230;
        --border: #2b3142;
        --text: #e8eaf2;
        --muted: #99a1b6;
        --accent: #6f95f2;
        --accent-soft: #202a45;
        --customer: #3fcf8e;
        --customer-bg: #143128;
        --pipeline: #e8ab4a;
        --pipeline-bg: #332711;
        --cold: #ef7a68;
        --cold-bg: #351d1a;
        --lead: #99a1b6;
        --lead-bg: #1d2230;
        --consistent: #3fcf8e;
        --growth: #6f95f2;
        --outdated: #ef7a68;
        --na: #7d859a;
      }}
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0; background: var(--bg); color: var(--text);
      font-family: "IBM Plex Sans", -apple-system, BlinkMacSystemFont, sans-serif;
      padding: clamp(20px, 4vw, 40px) 20px 72px;
      min-height: 100vh;
    }}

    /* Password Gate Screen */
    #auth-screen {{
      position: fixed;
      inset: 0;
      background: var(--bg);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      z-index: 99999;
    }}
    .auth-card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 32px 28px;
      max-width: 400px;
      width: 100%;
      box-shadow: 0 20px 40px -15px rgba(0,0,0,0.15);
      text-align: center;
    }}
    .auth-icon {{
      width: 52px;
      height: 52px;
      margin: 0 auto 16px;
      background: var(--accent-soft);
      color: var(--accent);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
    }}
    .auth-title {{
      font-family: "Libre Franklin", sans-serif;
      font-size: 20px;
      font-weight: 800;
      margin: 0 0 6px;
      letter-spacing: -0.01em;
    }}
    .auth-desc {{
      color: var(--muted);
      font-size: 13px;
      margin: 0 0 22px;
      line-height: 1.5;
    }}
    .auth-form {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}
    .auth-input {{
      width: 100%;
      padding: 12px 14px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--panel2);
      color: var(--text);
      font-size: 14px;
      font-family: inherit;
      outline: none;
      transition: border-color 0.2s;
    }}
    .auth-input:focus {{
      border-color: var(--accent);
    }}
    .auth-btn {{
      width: 100%;
      padding: 12px;
      border: none;
      border-radius: 8px;
      background: var(--accent);
      color: #fff;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: opacity 0.2s;
    }}
    .auth-btn:hover {{
      opacity: 0.9;
    }}
    .auth-error {{
      color: var(--cold);
      font-size: 12px;
      margin-top: 4px;
      display: none;
      font-weight: 500;
    }}
    .auth-error.visible {{
      display: block;
    }}
    .auth-remember {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      font-size: 12px;
      color: var(--muted);
      cursor: pointer;
      margin-top: 4px;
    }}
    @keyframes shake {{
      0%, 100% {{ transform: translateX(0); }}
      20%, 60% {{ transform: translateX(-6px); }}
      40%, 80% {{ transform: translateX(6px); }}
    }}
    .shake {{
      animation: shake 0.35s ease;
    }}

    /* Main Dashboard container */
    #dashboard-content {{
      display: none;
    }}
    #dashboard-content.unlocked {{
      display: block;
    }}

    .wrap {{ max-width: 1220px; margin: 0 auto; }}
    .header-bar {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 22px;
    }}
    .lock-session-btn {{
      background: var(--panel);
      border: 1px solid var(--border);
      color: var(--muted);
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.15s;
    }}
    .lock-session-btn:hover {{
      color: var(--text);
      border-color: var(--muted);
    }}
    .eyebrow {{
      font-family: "IBM Plex Mono", monospace; font-size: 11px; letter-spacing: .08em; text-transform: uppercase;
      color: var(--accent); margin: 0 0 6px;
    }}
    h1 {{
      font-family: "Libre Franklin", sans-serif; font-weight: 800; font-size: clamp(24px, 3.2vw, 32px);
      margin: 0 0 6px; letter-spacing: -0.01em;
    }}
    .subtitle {{ color: var(--muted); font-size: 14px; margin: 0; max-width: 66ch; line-height: 1.5; }}
    
    .guide {{
      background: var(--panel); border: 1px solid var(--border); border-radius: 12px;
      padding: 16px 18px; margin-bottom: 22px;
    }}
    .guide h3 {{
      margin: 0 0 12px; font-family: "Libre Franklin", sans-serif; font-size: 13px; font-weight: 700;
      text-transform: uppercase; letter-spacing: .04em; color: var(--muted);
    }}
    .legend {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px 16px; margin-bottom: 14px; }}
    @media (max-width: 720px) {{ .legend {{ grid-template-columns: repeat(2, 1fr); }} }}
    .legend-item {{ display: flex; gap: 8px; align-items: baseline; }}
    .legend-item .swatch {{
      flex-shrink: 0; width: 10px; height: 10px; border-radius: 3px; margin-top: 3px;
    }}
    .legend-item .swatch.Customer {{ background: var(--customer); }}
    .legend-item .swatch.Pipeline {{ background: var(--pipeline); }}
    .legend-item .swatch.Cold-Lead {{ background: var(--cold); }}
    .legend-item .swatch.Potential-Lead {{ background: var(--lead); }}
    .legend-item .txt {{ font-size: 12.5px; line-height: 1.4; color: var(--text); }}
    .legend-item .txt b {{ font-weight: 600; }}
    .guide-tips {{ border-top: 1px solid var(--border); padding-top: 12px; display: flex; flex-direction: column; gap: 6px; }}
    .guide-tips p {{ margin: 0; font-size: 12.5px; color: var(--muted); line-height: 1.55; }}
    .guide-tips p b {{ color: var(--text); font-weight: 600; }}
    
    .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 18px; }}
    @media (max-width: 620px) {{ .stats {{ grid-template-columns: repeat(2, 1fr); }} }}
    .stat {{ background: var(--panel); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; }}
    .stat .n {{ font-family: "Libre Franklin", sans-serif; font-size: 28px; font-weight: 800; font-variant-numeric: tabular-nums; }}
    .stat .l {{ font-size: 12px; color: var(--muted); margin-top: 2px; }}
    .stat.customer .n {{ color: var(--customer); }}
    .stat.pipeline .n {{ color: var(--pipeline); }}
    .stat.cold .n {{ color: var(--cold); }}
    .stat.lead .n {{ color: var(--lead); }}
    
    .meta-row {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }}
    .meta-row span {{
      background: var(--panel2); border: 1px solid var(--border); border-radius: 999px; padding: 5px 12px;
      font-size: 12px; color: var(--muted);
    }}
    .filters {{ display: flex; gap: 8px; margin-bottom: 10px; flex-wrap: wrap; }}
    .filters button {{
      background: var(--panel); border: 1px solid var(--border); color: var(--text); border-radius: 999px;
      padding: 7px 14px; font-size: 13px; font-family: inherit; cursor: pointer; transition: all 0.15s;
    }}
    .filters button:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
    .filters button.active {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
    .table-scroll {{ overflow-x: auto; border-radius: 12px; border: 1px solid var(--border); }}
    table {{ width: 100%; min-width: 880px; border-collapse: collapse; background: var(--panel); }}
    thead th {{
      text-align: left; font-family: "IBM Plex Mono", monospace; font-size: 10.5px; text-transform: uppercase;
      letter-spacing: .06em; color: var(--muted); padding: 11px 12px; border-bottom: 1px solid var(--border);
      background: var(--panel2); position: sticky; top: 0;
    }}
    tbody td {{ padding: 12px; border-bottom: 1px solid var(--border); font-size: 13px; vertical-align: top; }}
    tbody tr:last-child td {{ border-bottom: none; }}
    tbody tr:hover {{ background: var(--panel2); }}
    .domain {{ font-weight: 600; }}
    .desig {{ color: var(--muted); font-size: 11.5px; margin-top: 2px; }}
    .range {{ font-family: "IBM Plex Mono", monospace; font-size: 12px; }}
    .badge {{
      display: inline-block; padding: 3px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;
    }}
    .badge.Customer {{ background: var(--customer-bg); color: var(--customer); }}
    .badge.Pipeline {{ background: var(--pipeline-bg); color: var(--pipeline); }}
    .badge.Cold-Lead {{ background: var(--cold-bg); color: var(--cold); }}
    .badge.Potential-Lead {{ background: var(--lead-bg); color: var(--lead); }}
    .cbadge {{
      display: inline-block; padding: 2px 9px; border-radius: 999px; font-size: 11px; font-weight: 600;
      white-space: nowrap;
    }}
    .cbadge.Consistent {{ background: var(--customer-bg); color: var(--consistent); }}
    .cbadge.HubSpot-indicates-growth {{ background: var(--accent-soft); color: var(--growth); }}
    .cbadge.HubSpot-outdated-or-event-overstated {{ background: var(--cold-bg); color: var(--outdated); }}
    .cbadge.N-A {{ background: var(--lead-bg); color: var(--na); }}
    .info-btn {{
      display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px;
      border-radius: 50%; background: var(--panel2); border: 1px solid var(--border); color: var(--muted);
      font-family: "IBM Plex Mono", monospace; font-size: 12px; cursor: pointer; margin-left: 6px;
    }}
    .info-btn:hover, .info-btn:focus-visible {{ background: var(--accent); color: #fff; border-color: var(--accent); outline: none; }}
    .people-btn {{
      font-family: "IBM Plex Mono", monospace; font-variant-numeric: tabular-nums; font-size: 13px;
      background: transparent; border: none; border-bottom: 1px dashed var(--muted); color: var(--text);
      cursor: pointer; padding: 0; font-weight: 600;
    }}
    .people-btn:hover, .people-btn:focus-visible {{ color: var(--accent); border-color: var(--accent); outline: none; }}
    .rationale {{
      margin-top: 10px; background: var(--panel2); border: 1px solid var(--border);
      border-radius: 8px; padding: 10px 12px; font-family: "IBM Plex Mono", monospace; font-size: 11.5px;
      color: var(--muted); white-space: pre-wrap; line-height: 1.6;
    }}
    .rationale[hidden] {{ display: none; }}
    footer {{ margin-top: 26px; font-size: 11.5px; color: var(--muted); text-align: center; }}
  </style>
</head>
<body>

  <!-- Lock Screen for Visitors & Crawlers -->
  <div id="auth-screen">
    <div class="auth-card" id="auth-card">
      <div class="auth-icon">&#128274;</div>
      <h2 class="auth-title">Protected Dashboard</h2>
      <p class="auth-desc">Enter the access passcode to view the VRWS Opportunity Ledger & HubSpot CRM analysis.</p>
      
      <form class="auth-form" id="auth-form" onsubmit="event.preventDefault(); checkPassword();">
        <input 
          type="password" 
          id="pass-input" 
          class="auth-input" 
          placeholder="Enter password..." 
          autocomplete="current-password" 
          required 
          autofocus 
        />
        <button type="submit" class="auth-btn">Unlock Dashboard</button>
        <label class="auth-remember">
          <input type="checkbox" id="remember-me" checked> Remember access on this browser
        </label>
        <div id="auth-error" class="auth-error">Incorrect password. Please try again.</div>
      </form>
    </div>
  </div>

  <!-- Dashboard Content (Rendered Dynamically Only After Auth) -->
  <div id="dashboard-content">
    <div class="wrap">
      <div class="header-bar">
        <div>
          <p class="eyebrow">Guesty &middot; Marketing / Events</p>
          <h1>VRWS 2026 Opportunity Ledger</h1>
          <p class="subtitle">Every Property Manager / Owner account from the Vacation Rental World Summit attendee list, cross-referenced against the event contact sheet and HubSpot CRM.</p>
        </div>
        <button type="button" class="lock-session-btn" onclick="lockDashboard()">
          <span>&#128274;</span> Lock Page
        </button>
      </div>

      <div class="guide">
        <h3>How to read this dashboard</h3>
        <div class="legend">
          <div class="legend-item"><span class="swatch Pipeline"></span><span class="txt"><b>Pipeline</b> &mdash; an active deal in motion (Opportunity, SQL, MQL). Follow up first.</span></div>
          <div class="legend-item"><span class="swatch Potential-Lead"></span><span class="txt"><b>Potential Lead</b> &mdash; real portfolio declared at event, but not in HubSpot yet.</span></div>
          <div class="legend-item"><span class="swatch Cold-Lead"></span><span class="txt"><b>Cold Lead</b> &mdash; CRM history but no active deal (some are past churned customers).</span></div>
          <div class="legend-item"><span class="swatch Customer"></span><span class="txt"><b>Customer</b> &mdash; active Guesty customer. Useful for account renewals.</span></div>
        </div>
        <div class="guide-tips">
          <p><b>Property-count consistency</b> compares portfolio size declared at event vs HubSpot on file.</p>
          <p><b>Click the number in “People”</b> to see who is attending.</p>
          <p><b>Click the “?”</b> to see exact HubSpot fields and rationale.</p>
        </div>
      </div>

      <div class="stats">
        <div class="stat pipeline"><div class="n" id="stat-pipeline">56</div><div class="l">Pipeline</div></div>
        <div class="stat lead"><div class="n" id="stat-lead">8</div><div class="l">Potential Lead</div></div>
        <div class="stat cold"><div class="n" id="stat-cold">9</div><div class="l">Cold Lead</div></div>
        <div class="stat customer"><div class="n" id="stat-customer">21</div><div class="l">Customer</div></div>
      </div>

      <div class="meta-row">
        <span>94 Property Manager / Owner accounts analyzed</span>
        <span>12 attendees used personal email domains</span>
        <span>Sources: event contact sheet &middot; Eventify directory &middot; HubSpot CRM</span>
      </div>

      <div class="filters" id="filters" role="group" aria-label="Filter by classification">
        <button data-f="all" class="active" aria-pressed="true">All (94)</button>
        <button data-f="Pipeline" aria-pressed="false">Pipeline (56)</button>
        <button data-f="Potential Lead" aria-pressed="false">Potential Lead (8)</button>
        <button data-f="Cold Lead" aria-pressed="false">Cold Lead (9)</button>
        <button data-f="Customer" aria-pressed="false">Customer (21)</button>
      </div>

      <div class="table-scroll">
        <table>
          <thead>
            <tr>
              <th style="width:22%">Account</th>
              <th style="width:16%">Property range</th>
              <th style="width:9%">Countries</th>
              <th style="width:9%">People</th>
              <th style="width:13%">Classification</th>
              <th style="width:16%">Property-count consistency</th>
              <th>Rationale</th>
            </tr>
          </thead>
          <tbody id="tbody">
            <!-- Populated dynamically only upon authenticated unlock -->
          </tbody>
        </table>
      </div>

      <footer>Pilot report for internal review &middot; rationale behind every classification is available via the “?” icons.</footer>
    </div>
  </div>

  <script>
    // -------------------------------------------------------------
    // CONFIGURATION: Set your desired password here
    // Default is: vrws2026
    // -------------------------------------------------------------
    const CONFIG_PASSWORD = "vrws2026";

    // 94 Analyzed Leads Dataset
    const RAW_DATA = {data_json_str};

    function escapeHtml(str) {{
      return String(str || '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }}

    function cls(s) {{
      return String(s || '').replace(/[^a-zA-Z0-9]+/g, '-');
    }}

    function renderTableRows(filter = 'all') {{
      const tbody = document.getElementById('tbody');
      if (!tbody) return;
      tbody.innerHTML = '';

      const filtered = RAW_DATA.filter(d => filter === 'all' || d.classification === filter);

      filtered.forEach((d, i) => {{
        const tr = document.createElement('tr');
        tr.setAttribute('data-classification', d.classification);

        const domain = escapeHtml(d.domain);
        const desigs = (d.designations || []).map(escapeHtml).join(' &middot; ');
        const propRange = escapeHtml(d.property_range);
        const countries = (d.countries || []).map(escapeHtml).join(', ');
        const peopleCount = d.people_count || 0;
        const classification = escapeHtml(d.classification);
        const rangeConsistency = escapeHtml(d.range_consistency);

        const rid = 'r' + i + '_' + cls(d.domain);
        const pid = 'p' + i + '_' + cls(d.domain);

        const fullRationale = 'CLASSIFICATION\\n' + (d.classification_rationale || []).join('\\n') +
          '\\n\\nPROPERTY-COUNT CONSISTENCY\\n' + (d.range_consistency_rationale || []).join('\\n');

        const peopleList = (d.people || []).map(p => {{
          let tag = ' (VRWS attendance not checked)';
          if (p.matched_in_eventify === true) tag = ' (confirmed at VRWS)';
          else if (p.matched_in_eventify === false) tag = ' (on list, not confirmed at VRWS)';
          return p.name + tag;
        }}).join('\\n');

        tr.innerHTML = `
          <td>
            <div class="domain">${{domain}}</div>
            <div class="desig">${{desigs}}</div>
          </td>
          <td class="range">${{propRange}}</td>
          <td>${{countries}}</td>
          <td>
            <button class="people-btn" data-target="${{pid}}" aria-expanded="false" aria-label="Show names">${{peopleCount}}</button>
            <div class="rationale" id="${{pid}}" hidden>${{escapeHtml(peopleList)}}</div>
          </td>
          <td><span class="badge ${{cls(classification)}}">${{classification}}</span></td>
          <td><span class="cbadge ${{cls(rangeConsistency)}}">${{rangeConsistency}}</span></td>
          <td>
            <button class="info-btn" data-target="${{rid}}" aria-expanded="false" aria-label="Show rationale">?</button>
            <div class="rationale" id="${{rid}}" hidden>${{escapeHtml(fullRationale)}}</div>
          </td>
        `;

        tbody.appendChild(tr);
      }});

      // Bind button events
      tbody.querySelectorAll('.info-btn, .people-btn').forEach(btn => {{
        btn.addEventListener('click', (e) => {{
          e.stopPropagation();
          const target = document.getElementById(btn.dataset.target);
          if (!target) return;
          const willShow = target.hidden;
          target.hidden = !willShow;
          btn.setAttribute('aria-expanded', String(willShow));
        }});
      }});
    }}

    function setupFilters() {{
      const filters = document.getElementById('filters');
      if (!filters) return;
      filters.addEventListener('click', (e) => {{
        const btn = e.target.closest('button');
        if (!btn) return;
        filters.querySelectorAll('button').forEach(b => {{
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        }});
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
        renderTableRows(btn.dataset.f);
      }});
    }}

    function unlockDashboard() {{
      document.getElementById('auth-screen').style.display = 'none';
      document.getElementById('dashboard-content').classList.add('unlocked');
      renderTableRows('all');
      setupFilters();
    }}

    function lockDashboard() {{
      localStorage.removeItem('vrws_auth');
      sessionStorage.removeItem('vrws_auth');
      document.getElementById('dashboard-content').classList.remove('unlocked');
      document.getElementById('auth-screen').style.display = 'flex';
      const input = document.getElementById('pass-input');
      if (input) {{
        input.value = '';
        input.focus();
      }}
      document.getElementById('tbody').innerHTML = '';
    }}

    function checkPassword() {{
      const input = document.getElementById('pass-input');
      const err = document.getElementById('auth-error');
      const card = document.getElementById('auth-card');
      const remember = document.getElementById('remember-me').checked;

      if (!input) return;

      if (input.value === CONFIG_PASSWORD) {{
        err.classList.remove('visible');
        if (remember) {{
          localStorage.setItem('vrws_auth', 'unlocked');
        }} else {{
          sessionStorage.setItem('vrws_auth', 'unlocked');
        }}
        unlockDashboard();
      }} else {{
        err.classList.add('visible');
        card.classList.remove('shake');
        void card.offsetWidth; // retrigger animation
        card.classList.add('shake');
        input.select();
      }}
    }}

    // Check existing session
    (function initAuth() {{
      const isAuth = localStorage.getItem('vrws_auth') === 'unlocked' || sessionStorage.getItem('vrws_auth') === 'unlocked';
      if (isAuth) {{
        unlockDashboard();
      }}
    }})();
  </script>
</body>
</html>"""

with open('/app/applet/public/full-index.html', 'w') as f:
    f.write(html_template)

with open('/app/applet/public/standalone.html', 'w') as f:
    f.write(html_template)

print("Generated protected index.html successfully!")
print("File size:", len(html_template))
