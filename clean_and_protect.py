import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Extract DATA
data_match = re.search(r'const DATA = (\[[\s\S]*?\]);\s*function cls', content)
if not data_match:
    # Try alternate match
    data_match = re.search(r'const DATA = (\[[\s\S]*?\]);', content)

if data_match:
    print("Found DATA, length:", len(data_match.group(1)))
    raw_data_json = data_match.group(1)
else:
    print("ERROR: DATA not found")
    exit(1)

# 2. Extract CSS inside <style> ... </style>
css_match = re.search(r'<style>([\s\S]*?)</style>', content)
original_css = css_match.group(1) if css_match else ""

# 3. Build the clean, protected HTML
lock_screen_css = """
  /* Password Gate Styles */
  #auth-screen {
    position: fixed;
    inset: 0;
    background: var(--bg);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    z-index: 99999;
  }
  .auth-card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 28px;
    max-width: 400px;
    width: 100%;
    box-shadow: 0 20px 40px -15px rgba(0,0,0,0.15);
    text-align: center;
  }
  .auth-icon {
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
  }
  .auth-title {
    font-family: "Libre Franklin", sans-serif;
    font-size: 20px;
    font-weight: 800;
    margin: 0 0 6px;
    letter-spacing: -0.01em;
  }
  .auth-desc {
    color: var(--muted);
    font-size: 13px;
    margin: 0 0 22px;
    line-height: 1.5;
  }
  .auth-form {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }
  .auth-input {
    width: 100%;
    padding: 12px 14px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--panel2);
    color: var(--text);
    font-size: 14px;
    font-family: inherit;
    outline: none;
    box-sizing: border-box;
    transition: border-color 0.2s;
  }
  .auth-input:focus {
    border-color: var(--accent);
  }
  .auth-btn {
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
  }
  .auth-btn:hover {
    opacity: 0.9;
  }
  .auth-error {
    color: var(--cold);
    font-size: 12px;
    margin-top: 4px;
    display: none;
    font-weight: 500;
  }
  .auth-error.visible {
    display: block;
  }
  .auth-remember {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    font-size: 12px;
    color: var(--muted);
    cursor: pointer;
    margin-top: 4px;
  }
  @keyframes shake {
    0%, 100% { transform: translateX(0); }
    20%, 60% { transform: translateX(-6px); }
    40%, 80% { transform: translateX(6px); }
  }
  .shake {
    animation: shake 0.35s ease;
  }

  /* Conceal dashboard until unlocked */
  #dashboard-content {
    display: none;
  }
  #dashboard-content.unlocked {
    display: block;
  }
  .lock-session-btn {
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
    float: right;
  }
  .lock-session-btn:hover {
    color: var(--text);
    border-color: var(--muted);
  }
"""

clean_html = f"""<!DOCTYPE html>
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
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=Libre+Franklin:wght@700;800&display=swap">

  <style>
{original_css}
{lock_screen_css}
  </style>
</head>
<body>

  <!-- Password Gate Lock Screen -->
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

  <!-- Dashboard Content (Revealed Only Upon Authenticated Unlock) -->
  <div id="dashboard-content">
    <div class="wrap">
      <button type="button" class="lock-session-btn" onclick="lockDashboard()">
        <span>&#128274;</span> Lock Page
      </button>

      <p class="eyebrow">Guesty &middot; Marketing / Events</p>
      <h1>VRWS 2026 Opportunity Ledger</h1>
      <p class="subtitle">Every Property Manager / Owner account from the Vacation Rental World Summit attendee list, cross-referenced against the event contact sheet and HubSpot CRM — pilot run for sales-team review.</p>

      <div class="guide">
        <h3>How to read this dashboard</h3>
        <div class="legend">
          <div class="legend-item"><span class="swatch Pipeline"></span><span class="txt"><b>Pipeline</b> &mdash; an active deal in motion (Opportunity, SQL, MQL or similar stage in HubSpot). Follow up on these first.</span></div>
          <div class="legend-item"><span class="swatch Potential-Lead"></span><span class="txt"><b>Potential Lead</b> &mdash; a real property portfolio (from the event badge), but nothing in HubSpot yet. Likely a genuinely fresh prospect.</span></div>
          <div class="legend-item"><span class="swatch Cold-Lead"></span><span class="txt"><b>Cold Lead</b> &mdash; has a HubSpot history but no active deal. Some of these are past customers who churned — the “?” on that row says so; approach as a win-back, not a cold call.</span></div>
          <div class="legend-item"><span class="swatch Customer"></span><span class="txt"><b>Customer</b> &mdash; already a Guesty customer (HubSpot Lifecycle Stage = Customer). Not a sales target; useful for account management or renewal context.</span></div>
        </div>
        <div class="guide-tips">
          <p><b>Property-count consistency</b> compares the portfolio size the person declared at the event against what HubSpot has on file for that account — useful for sanity-checking pitch size before reaching out.</p>
          <p><b>Click the number in “People”</b> to see who’s behind an account, and whether they were confirmed as attending VRWS.</p>
          <p><b>Click the “?”</b> next to any classification or consistency badge to see the exact HubSpot field values behind that call.</p>
          <p><b>Coverage:</b> built from the event contact sheet as of Sept 2, 2026. The Eventify app keeps registering attendees after that date, so some Property Managers at VRWS may not appear here yet — treat this as a strong starting list, not the final one.</p>
          <p><b>Default order:</b> rows are ranked for outreach, not alphabetically — Pipeline and Potential Lead accounts come first, then Cold Lead, then Customer; within each group, the accounts where HubSpot confirms the portfolio size and the largest portfolios are ranked highest.</p>
        </div>
      </div>

      <div class="stats">
        <div class="stat pipeline"><div class="n">56</div><div class="l">Pipeline</div></div>
        <div class="stat lead"><div class="n">8</div><div class="l">Potential Lead</div></div>
        <div class="stat cold"><div class="n">9</div><div class="l">Cold Lead</div></div>
        <div class="stat customer"><div class="n">21</div><div class="l">Customer</div></div>
      </div>

      <div class="meta-row">
        <span>94 Property Manager / Owner accounts analyzed — suppliers, OTAs and other non-PM designations are excluded from this report</span>
        <span>12 attendees used personal email domains — excluded from company aggregation</span>
        <span>Sources: event contact sheet (355 rows) &middot; Eventify attendee directory (600 records) &middot; HubSpot CRM</span>
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
            <!-- Dynamically populated only when unlocked -->
          </tbody>
        </table>
      </div>

      <footer>Pilot report for internal review &middot; rationale behind every classification is available via the “?” icons.</footer>
    </div>
  </div>

  <script>
    // ACCESS PASSWORD (default: vrws2026)
    const CONFIG_PASSWORD = "vrws2026";

    // 94 Analyzed Accounts
    const DATA = {raw_data_json};

    function cls(s) {{
      return String(s || '').replace(/[^a-zA-Z0-9]+/g, '-');
    }}

    let currentFilter = 'all';

    function render() {{
      const tbody = document.getElementById('tbody');
      if (!tbody) return;
      tbody.innerHTML = '';

      const filtered = DATA.filter(d => currentFilter === 'all' || d.classification === currentFilter);

      filtered.forEach((d, i) => {{
        const tr = document.createElement('tr');
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
            <div class="domain">${{d.domain}}</div>
            <div class="desig">${{(d.designations || []).join(' &middot; ')}}</div>
          </td>
          <td class="range">${{d.property_range}}</td>
          <td>${{(d.countries || []).join(', ')}}</td>
          <td>
            <button class="people-btn" data-target="${{pid}}" aria-expanded="false" aria-label="Show names">${{d.people_count}}</button>
            <div class="rationale" id="${{pid}}" hidden></div>
          </td>
          <td><span class="badge ${{cls(d.classification)}}">${{d.classification}}</span></td>
          <td><span class="cbadge ${{cls(d.range_consistency)}}">${{d.range_consistency}}</span></td>
          <td>
            <button class="info-btn" data-target="${{rid}}" aria-expanded="false" aria-label="Show rationale">?</button>
            <div class="rationale" id="${{rid}}" hidden></div>
          </td>
        `;

        tbody.appendChild(tr);
        tr.querySelector('#' + rid).textContent = fullRationale;
        tr.querySelector('#' + pid).textContent = peopleList;
      }});

      tbody.querySelectorAll('.info-btn, .people-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
          const target = document.getElementById(btn.dataset.target);
          const willShow = target.hidden;
          target.hidden = !willShow;
          btn.setAttribute('aria-expanded', String(willShow));
        }});
      }});
    }}

    function setupFilters() {{
      const filters = document.getElementById('filters');
      if (!filters) return;
      filters.onclick = (e) => {{
        const btn = e.target.closest('button');
        if (!btn) return;
        document.querySelectorAll('#filters button').forEach(b => {{
          b.classList.remove('active');
          b.setAttribute('aria-pressed', 'false');
        }});
        btn.classList.add('active');
        btn.setAttribute('aria-pressed', 'true');
        currentFilter = btn.dataset.f;
        render();
      }};
    }}

    function unlockDashboard() {{
      document.getElementById('auth-screen').style.display = 'none';
      document.getElementById('dashboard-content').classList.add('unlocked');
      render();
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
        void card.offsetWidth;
        card.classList.add('shake');
        input.select();
      }}
    }}

    // Check existing authenticated session
    (function initAuth() {{
      const isAuth = localStorage.getItem('vrws_auth') === 'unlocked' || sessionStorage.getItem('vrws_auth') === 'unlocked';
      if (isAuth) {{
        unlockDashboard();
      }}
    }})();
  </script>
</body>
</html>"""

# Write out to public/index.html, dist/index.html, and a copy at ready_for_github/index.html
with open('public/index.html', 'w', encoding='utf-8') as f:
    f.write(clean_html)

with open('public/full-index.html', 'w', encoding='utf-8') as f:
    f.write(clean_html)

with open('public/standalone.html', 'w', encoding='utf-8') as f:
    f.write(clean_html)

print("Saved clean, protected index.html successfully! Size:", len(clean_html))
