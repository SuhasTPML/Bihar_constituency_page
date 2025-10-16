"""
Generate CSV export with hardcoded widgets for CMS import.
Creates one row per constituency with all widgets embedded.
"""

import json
import csv
import os


def generate_2025_widget(constituency):
    """
    Generate 2025 Results widget.
    Always displays - shows placeholder before results, actual results after.
    """
    slug = constituency.get('slug', '')
    const_id = f"bihar-2025-{slug}"

    widget_html = f'''<div id="{const_id}" class="widget-2025">
<style>
#{const_id} .card {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin: 16px 0; background: white; }}
#{const_id} .election-title {{ font-size: 20px; font-weight: 600; margin-bottom: 16px; color: #1f2937; }}
#{const_id} .placeholder-message {{ text-align: center; padding: 40px 20px; color: #6b7280; }}
#{const_id} .candidate-row {{ margin: 12px 0; }}
#{const_id} .candidate-name {{ font-weight: 600; color: #1f2937; }}
#{const_id} .candidate-party {{ color: #6b7280; font-size: 14px; }}
#{const_id} .bar {{ height: 8px; background: #f3f4f6; border-radius: 4px; margin-top: 8px; overflow: hidden; }}
#{const_id} .bar span {{ display: block; height: 100%; }}
#{const_id} .margin-info {{ margin-top: 16px; padding-top: 16px; border-top: 1px solid #e5e7eb; text-align: center; font-weight: 600; }}
</style>
<div class="card">
<h3 class="election-title">Bihar Elections 2025 Results</h3>
<div class="placeholder-message">
<p>Results will be updated here after announcement. Please check on the result day.</p>
</div>
</div>
</div>
<script>
(function(){{
  var el = document.getElementById('{const_id}');
  if (!el) return;

  function detectDataSource() {{
    var host = window.location.hostname.toLowerCase();
    if (host.includes('quintype.io') || host.includes('sandbox')) return 'sandbox';
    return 'github';
  }}

  var dataSource = detectDataSource();
  var url = dataSource === 'sandbox'
    ? 'https://dh-sandbox-web.quintype.io/bihar_election_results_consolidated'
    : 'https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json';

  fetch(url)
    .then(function(r){{ return r.json(); }})
    .then(function(data){{
      var c = data.find(function(x){{ return x.slug === '{slug}'; }});
      if (!c || (!c.y2025_winner_name && !c.y2025_winner_party)) return;

      var wVotes = parseInt(c.y2025_winner_votes) || 0;
      var ruVotes = parseInt(c.y2025_runner_votes) || 0;
      var margin = parseInt(c.y2025_margin) || 0;
      var maxV = Math.max(wVotes, ruVotes, 1);
      var wPct = Math.round((wVotes / maxV) * 100);
      var ruPct = Math.round((ruVotes / maxV) * 100);

      var html = '<div class="card">' +
        '<h3 class="election-title">Bihar Elections 2025 Results</h3>' +
        '<div class="candidate-row">' +
        '<div class="candidate-name">WINNER: ' + (c.y2025_winner_name || '—') + '</div>' +
        '<div class="candidate-party">' + (c.y2025_winner_party || '—') + ' • ' + wVotes.toLocaleString('en-IN') + ' votes</div>' +
        '<div class="bar"><span style="width:' + wPct + '%;background:#16a34a"></span></div>' +
        '</div>' +
        '<div class="candidate-row">' +
        '<div class="candidate-name">Runner-up: ' + (c.y2025_runner_name || '—') + '</div>' +
        '<div class="candidate-party">' + (c.y2025_runner_party || '—') + ' • ' + ruVotes.toLocaleString('en-IN') + ' votes</div>' +
        '<div class="bar"><span style="width:' + ruPct + '%;background:#dc2626"></span></div>' +
        '</div>' +
        '<div class="margin-info">MARGIN: ' + margin.toLocaleString('en-IN') + ' votes</div>' +
        '</div>';

      el.innerHTML = html;
    }})
    .catch(function(e){{ console.error('2025 widget error:', e); }});
}})();
</script>'''

    return widget_html


def generate_mla_widget(constituency):
    """
    Generate Current MLA widget with hardcoded data.
    Collapses if 2025 results exist.
    """
    slug = constituency.get('slug', '')
    mla_name = constituency.get('current_mla_name', '')
    mla_party = constituency.get('current_mla_party', '')
    mla_alliance = constituency.get('current_mla_alliance', '')
    const_id = f"bihar-mla-{slug}"

    widget_html = f'''<div id="{const_id}" class="widget-mla">
<style>
#{const_id} .card {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; margin: 16px 0; background: white; }}
#{const_id} h3 {{ font-size: 20px; font-weight: 600; margin-bottom: 16px; color: #1f2937; }}
#{const_id} .mla-name {{ font-size: 18px; font-weight: 600; color: #1f2937; margin-bottom: 8px; }}
#{const_id} .mla-party {{ color: #6b7280; font-size: 14px; }}
</style>
<div class="card">
<h3>Current MLA</h3>
<div class="mla-name">{mla_name}</div>
<div class="mla-party">{mla_party} • {mla_alliance}</div>
</div>
</div>
<script>
(function(){{
  var el = document.getElementById('{const_id}');
  if (!el) return;

  function detectDataSource() {{
    var host = window.location.hostname.toLowerCase();
    if (host.includes('quintype.io') || host.includes('sandbox')) return 'sandbox';
    return 'github';
  }}

  var dataSource = detectDataSource();
  var url = dataSource === 'sandbox'
    ? 'https://dh-sandbox-web.quintype.io/bihar_election_results_consolidated'
    : 'https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json';

  fetch(url)
    .then(function(r){{ return r.json(); }})
    .then(function(data){{
      var c = data.find(function(x){{ return x.slug === '{slug}'; }});
      if (c && (c.y2025_winner_name || c.y2025_winner_party)) {{
        el.style.display = 'none';
      }}
    }})
    .catch(function(e){{ console.error('MLA widget error:', e); }});
}})();
</script>'''

    return widget_html


def generate_timeline_widget(constituency):
    """
    Generate Timeline widget with hardcoded 2010/2015/2020.
    Checks for 2025 and adds it + reverses order if exists.
    """
    slug = constituency.get('slug', '')
    const_id = f"bihar-timeline-{slug}"

    w2020 = constituency.get('y2020_winner_name', '')
    p2020 = constituency.get('y2020_winner_party', '')
    w2015 = constituency.get('y2015_winner_name', '')
    p2015 = constituency.get('y2015_winner_party', '')
    w2010 = constituency.get('y2010_winner_name', '')
    p2010 = constituency.get('y2010_winner_party', '')

    widget_html = f'''<div id="{const_id}" class="widget-timeline">
<style>
#{const_id} {{ margin: 16px 0; }}
#{const_id} .timeline-title {{ font-size: 20px; font-weight: 600; margin-bottom: 16px; color: #1f2937; }}
#{const_id} .timeline-item {{ display: flex; padding: 12px 0; border-left: 2px solid #e5e7eb; padding-left: 20px; margin-left: 20px; position: relative; }}
#{const_id} .timeline-item:before {{ content: ''; position: absolute; left: -6px; top: 20px; width: 10px; height: 10px; border-radius: 50%; background: #3b82f6; }}
#{const_id} .year {{ font-weight: 600; color: #3b82f6; min-width: 80px; }}
#{const_id} .winner {{ color: #1f2937; }}
#{const_id}.reverse .timeline-item {{ flex-direction: row-reverse; border-left: none; border-right: 2px solid #e5e7eb; padding-left: 0; padding-right: 20px; margin-left: 0; margin-right: 20px; }}
#{const_id}.reverse .timeline-item:before {{ left: auto; right: -6px; }}
</style>
<h3 class="timeline-title">Election History</h3>
<div class="timeline-item" data-year="2020">
<div class="year">2020 →</div>
<div class="winner">{w2020} ({p2020})</div>
</div>
<div class="timeline-item" data-year="2015">
<div class="year">2015 →</div>
<div class="winner">{w2015} ({p2015})</div>
</div>
<div class="timeline-item" data-year="2010">
<div class="year">2010 →</div>
<div class="winner">{w2010} ({p2010})</div>
</div>
</div>
<script>
(function(){{
  var el = document.getElementById('{const_id}');
  if (!el) return;

  function detectDataSource() {{
    var host = window.location.hostname.toLowerCase();
    if (host.includes('quintype.io') || host.includes('sandbox')) return 'sandbox';
    return 'github';
  }}

  var dataSource = detectDataSource();
  var url = dataSource === 'sandbox'
    ? 'https://dh-sandbox-web.quintype.io/bihar_election_results_consolidated'
    : 'https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json';

  fetch(url)
    .then(function(r){{ return r.json(); }})
    .then(function(data){{
      var c = data.find(function(x){{ return x.slug === '{slug}'; }});
      if (!c || !c.y2025_winner_name) return;

      // Add 2025 item at the top
      var item2025 = document.createElement('div');
      item2025.className = 'timeline-item';
      item2025.setAttribute('data-year', '2025');
      item2025.innerHTML = '<div class="year">← 2025</div><div class="winner">' + c.y2025_winner_name + ' (' + c.y2025_winner_party + ')</div>';
      el.insertBefore(item2025, el.querySelector('.timeline-item'));

      // Reverse order and flip arrows
      el.classList.add('reverse');
      el.querySelectorAll('.year').forEach(function(yearEl){{
        yearEl.textContent = yearEl.textContent.replace('→', '←');
      }});
    }})
    .catch(function(e){{ console.error('Timeline widget error:', e); }});
}})();
</script>'''

    return widget_html


def generate_grid_widget(constituency):
    """
    Generate Historical Grid widget with hardcoded 2020/2015/2010.
    Pure static HTML, no JavaScript.
    """
    const_id = f"bihar-grid-{constituency.get('slug', '')}"

    def format_votes(votes):
        try:
            return f"{int(votes):,}"
        except:
            return str(votes)

    w2020 = constituency.get('y2020_winner_name', '')
    p2020 = constituency.get('y2020_winner_party', '')
    v2020 = format_votes(constituency.get('y2020_winner_votes', 0))
    r2020 = constituency.get('y2020_runner_name', '')
    rp2020 = constituency.get('y2020_runner_party', '')
    rv2020 = format_votes(constituency.get('y2020_runner_votes', 0))
    m2020 = format_votes(constituency.get('y2020_margin', 0))

    w2015 = constituency.get('y2015_winner_name', '')
    p2015 = constituency.get('y2015_winner_party', '')
    v2015 = format_votes(constituency.get('y2015_winner_votes', 0))
    r2015 = constituency.get('y2015_runner_name', '')
    rp2015 = constituency.get('y2015_runner_party', '')
    rv2015 = format_votes(constituency.get('y2015_runner_votes', 0))
    m2015 = format_votes(constituency.get('y2015_margin', 0))

    w2010 = constituency.get('y2010_winner_name', '')
    p2010 = constituency.get('y2010_winner_party', '')
    v2010 = format_votes(constituency.get('y2010_winner_votes', 0))
    r2010 = constituency.get('y2010_runner_name', '')
    rp2010 = constituency.get('y2010_runner_party', '')
    rv2010 = format_votes(constituency.get('y2010_runner_votes', 0))
    m2010 = format_votes(constituency.get('y2010_margin', 0))

    widget_html = f'''<div id="{const_id}" class="widget-grid">
<style>
#{const_id} {{ margin: 16px 0; }}
#{const_id} .grid-title {{ font-size: 20px; font-weight: 600; margin-bottom: 16px; color: #1f2937; }}
#{const_id} .grid-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
#{const_id} .year-card {{ border: 1px solid #e5e7eb; border-radius: 8px; padding: 16px; background: white; }}
#{const_id} .year-card h4 {{ margin: 0 0 12px 0; color: #3b82f6; font-size: 18px; }}
#{const_id} .result-line {{ margin: 8px 0; font-size: 14px; color: #4b5563; }}
#{const_id} .result-line strong {{ color: #1f2937; }}
</style>
<h3 class="grid-title">Past Election Results</h3>
<div class="grid-container">
<div class="year-card">
<h4>2020 Results</h4>
<div class="result-line"><strong>Winner:</strong> {w2020} ({p2020}) - {v2020} votes</div>
<div class="result-line"><strong>Runner-up:</strong> {r2020} ({rp2020}) - {rv2020} votes</div>
<div class="result-line"><strong>Margin:</strong> {m2020} votes</div>
</div>
<div class="year-card">
<h4>2015 Results</h4>
<div class="result-line"><strong>Winner:</strong> {w2015} ({p2015}) - {v2015} votes</div>
<div class="result-line"><strong>Runner-up:</strong> {r2015} ({rp2015}) - {rv2015} votes</div>
<div class="result-line"><strong>Margin:</strong> {m2015} votes</div>
</div>
<div class="year-card">
<h4>2010 Results</h4>
<div class="result-line"><strong>Winner:</strong> {w2010} ({p2010}) - {v2010} votes</div>
<div class="result-line"><strong>Runner-up:</strong> {r2010} ({rp2010}) - {rv2010} votes</div>
<div class="result-line"><strong>Margin:</strong> {m2010} votes</div>
</div>
</div>
</div>'''

    return widget_html


def generate_map_widget():
    """
    Generate universal map iframe (same for all constituencies).
    Map auto-detects constituency from parent URL.
    """
    widget_html = '''<iframe
  src="https://suhastpml.github.io/Bihar_constituency_page/map.html"
  style="width:100%;height:600px;border:0;border-radius:8px;"
  loading="lazy"
  referrerpolicy="no-referrer"
  title="Bihar Constituency Map">
</iframe>'''

    return widget_html


def generate_headline(constituency):
    """Generate headline in the same format as generator files."""
    name = constituency.get('constituency_name', '')
    return f"{name} Assembly Election 2025"


def generate_body_text(constituency):
    """Generate body text using generate_constituency_writeups.py as reference."""
    def seat_type(res):
        return "General" if res == "" else res

    def fmt(n):
        try:
            return f"{int(n):,}"
        except Exception:
            return str(n)

    def result_para(data, year):
        y = str(year)
        wname = data.get(f'y{y}_winner_name', '')
        wparty = data.get(f'y{y}_winner_party', '')
        wvotes = data.get(f'y{y}_winner_votes', 0)
        rname = data.get(f'y{y}_runner_name', '')
        rparty = data.get(f'y{y}_runner_party', '')
        rvotes = data.get(f'y{y}_runner_votes', 0)
        margin = data.get(f'y{y}_margin', 0)
        return (
            f"In the {year} Bihar Assembly elections, {wname} ({wparty}) won the seat with {fmt(wvotes)} votes. "
            f"{rname} ({rparty}) was the runner-up with {fmt(rvotes)} votes. The victory margin was {fmt(margin)} votes."
        )

    # Opening
    name = constituency.get('constituency_name', '')
    no = constituency.get('no', '')
    district = constituency.get('district', '')
    reserved = constituency.get('reserved', '')
    lok_sabha = constituency.get('lok_sabha', '')
    current_mla = constituency.get('current_mla_name', '')
    current_party = constituency.get('current_mla_party', '')

    opening = (
        f"The {name} assembly constituency (No. {no}) is located in the {district} district of Bihar. "
        f"It is a {seat_type(reserved)} seat under the {lok_sabha} Lok Sabha constituency. "
        f"{current_mla} of the {current_party} currently represents this constituency."
    )

    # Yearly result paragraphs
    p2020 = result_para(constituency, 2020)
    p2015 = result_para(constituency, 2015)
    p2010 = result_para(constituency, 2010)

    # Pattern summary
    w2010 = constituency.get('y2010_winner_name', '')
    w2015 = constituency.get('y2015_winner_name', '')
    w2020 = constituency.get('y2020_winner_name', '')
    p10 = constituency.get('y2010_winner_party', '')
    p15 = constituency.get('y2015_winner_party', '')
    p20 = constituency.get('y2020_winner_party', '')
    same_candidate = (w2010 == w2015 == w2020) and bool(w2020)
    same_party = (p10 == p15 == p20) and bool(p20)
    if same_candidate:
        pattern = f"{w2020} has won this constituency in all three elections between 2010 and 2020"
        pattern += f", representing {p20} in each election" if same_party else f", representing {p10} in 2010, {p15} in 2015, and {p20} in 2020"
    else:
        pattern = f"The constituency has seen victories by {w2010} in 2010, {w2015} in 2015, and {w2020} in 2020"
    m2010 = constituency.get('y2010_margin', 0)
    m2015 = constituency.get('y2015_margin', 0)
    m2020 = constituency.get('y2020_margin', 0)
    margins = f". The victory margins were {fmt(m2010)} votes in 2010, {fmt(m2015)} votes in 2015, and {fmt(m2020)} votes in 2020"
    v2010 = constituency.get('y2010_winner_votes', 0)
    v2015 = constituency.get('y2015_winner_votes', 0)
    v2020 = constituency.get('y2020_winner_votes', 0)
    votes = f". The winning candidate's vote count was {fmt(v2010)} in 2010, {fmt(v2015)} in 2015, and {fmt(v2020)} in 2020."

    pattern_summary = pattern + margins + votes

    body = f"{opening}\n\n{p2020}\n\n{p2015}\n\n{p2010}\n\n{pattern_summary}"
    return body


def generate_2025_widget_v2(constituency):
    """2025 Results widget (aligned with CMS classes and layout)."""
    slug = constituency.get('slug', '')
    const_id = f"bihar-2025-{slug}"

    template = '''<div id="__CONST_ID__" class="widget-2025">
<style>
/* Scoped styles to match page tokens */
#__CONST_ID__ .card { background:#fff; border:1px solid #E5E7EB; border-radius:12px; padding:20px; margin:16px 0; }
#__CONST_ID__ .election-title { font-family:'Playfair Display', serif; font-size:18px; font-weight:600; line-height:36px; margin:0 0 12px; color:#000; }
#__CONST_ID__ .candidate-row { margin-bottom:16px; }
#__CONST_ID__ .candidate-name { font-family:'Roboto Slab', serif; font-weight:700; font-size:16px; color:#000; }
#__CONST_ID__ .candidate-party { color:#5B6064; font-size:14px; }
#__CONST_ID__ .bar { height:8px; border-radius:999px; background:#e5e7eb; position:relative; margin-top:8px; overflow:hidden; }
#__CONST_ID__ .bar span { position:absolute; left:0; top:0; bottom:0; border-radius:999px; display:block; }
#__CONST_ID__ .margin-info { margin-top:16px; padding-top:16px; border-top:1px solid #E5E7EB; }
#__CONST_ID__ .margin-text { font-family:'Roboto Slab', serif; font-weight:700; font-size:12px; }
#__CONST_ID__ .placeholder-message { text-align:center; padding:40px 20px; color:#6b7280; }
</style>
<div class="card">
  <h3 class="election-title">Bihar Elections 2025 Results</h3>
  <div class="placeholder-message">Results will be updated here after announcement.</div>
</div>
</div>
<script>
(function(){
  var el = document.getElementById('__CONST_ID__');
  if (!el) return;
  function detectDataSource(){ var h=(location.hostname||'').toLowerCase(); return (h.includes('quintype.io')||h.includes('sandbox'))?'sandbox':'github'; }
  var FILE = detectDataSource()==='sandbox' ? 'https://dh-sandbox-web.quintype.io/bihar_election_results_consolidated' : 'https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json';
  fetch(FILE).then(function(r){return r.json();}).then(function(data){
    var c=(data||[]).find(function(x){return x.slug=='__SLUG__';});
    var has2025 = c && (c.y2025_winner_name || c.y2025_winner_party || c.y2025_winner_votes || c.y2025_margin);
    if(!has2025) return;
    var wVotes = parseInt(c.y2025_winner_votes)||0, ruVotes=parseInt(c.y2025_runner_votes)||0, margin=parseInt(c.y2025_margin)||Math.max(0,(parseInt(c.y2025_winner_votes)||0)-(parseInt(c.y2025_runner_votes)||0));
    var maxV = Math.max(wVotes, ruVotes, 1);
    var wPct = Math.round((wVotes/maxV)*100), ruPct=Math.round((ruVotes/maxV)*100);
    var html = ''+
    '<div class="card">'+
      '<h3 class="election-title">Bihar Elections 2025 Results</h3>'+
      '<div class="candidate-row">'+
        '<div class="candidate-name">WINNER: '+(c.y2025_winner_name||'—')+'</div>'+
        '<div class="candidate-party">'+(c.y2025_winner_party||'—')+' • <span class="vote-count">'+wVotes.toLocaleString('en-IN')+' votes</span></div>'+
        '<div class="bar"><span style="width:'+wPct+'%; background:#16a34a"></span></div>'+
      '</div>'+
      '<div class="candidate-row">'+
        '<div class="candidate-name">Runner-up: '+(c.y2025_runner_name||'—')+'</div>'+
        '<div class="candidate-party">'+(c.y2025_runner_party||'—')+' • <span class="vote-count">'+ruVotes.toLocaleString('en-IN')+' votes</span></div>'+
        '<div class="bar"><span style="width:'+ruPct+'%; background:#dc2626"></span></div>'+
      '</div>'+
      '<div class="margin-info"><span class="margin-text">MARGIN: '+margin.toLocaleString('en-IN')+' votes</span></div>'+
    '</div>';
    el.innerHTML = html;
  }).catch(function(){});
})();
</script>'''

    widget_html = template.replace('__CONST_ID__', const_id).replace('__SLUG__', slug)
    return widget_html


def generate_mla_widget_v2(constituency):
    """Current MLA widget (matches page classes; hides if 2025 exists)."""
    slug = constituency.get('slug', '')
    const_id = f"bihar-mla-{slug}"
    name = constituency.get('constituency_name', '')
    mla_name = constituency.get('current_mla_name', '')
    mla_party = constituency.get('current_mla_party', '')
    mla_alliance = constituency.get('current_mla_alliance', '')

    template = '''<div id="__CONST_ID__" class="widget-mla">
<style>
#__CONST_ID__ .card { background:#fff; border:1px solid #E5E7EB; border-radius:12px; padding:20px; margin:16px 0; }
#__CONST_ID__ .current-mla-title { font-family:'Roboto Slab', serif; font-size:16px; font-weight:400; line-height:21px; color:#000; margin:0 0 6px; }
#__CONST_ID__ .mla-name { font-family:'Roboto Slab', serif; font-size:16px; font-weight:400; line-height:21px; color:#000; margin:0; }
#__CONST_ID__ .current-mla-meta { font-family:'Roboto Slab', serif; font-size:14px; line-height:18px; color:#5B6064; margin:4px 0 0; }
</style>
<div class="card current-mla-card">
  <h3 class="current-mla-title">__NAME__ Current MLA</h3>
  <p class="mla-name">__MLA_NAME__</p>
  <p class="current-mla-meta">__MLA_META__</p>
</div>
</div>
<script>
(function(){
  var root = document.getElementById('__CONST_ID__'); if (!root) return;
  function ds(){ var h=(location.hostname||'').toLowerCase(); return (h.includes('quintype.io')||h.includes('sandbox'))?'sandbox':'github'; }
  var URLc = ds()==='sandbox' ? 'https://dh-sandbox-web.quintype.io/bihar_election_results_consolidated' : 'https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json';
  fetch(URLc).then(function(r){return r.json();}).then(function(data){
    var c=(data||[]).find(function(x){return x.slug=='__SLUG__';});
    var has2025 = c && (c.y2025_winner_name || c.y2025_winner_party || c.y2025_winner_votes || c.y2025_margin);
    if (has2025) { root.style.display='none'; }
  }).catch(function(){});
})();
</script>'''

    meta = (mla_party or '-') + ((' • Alliance: ' + (mla_alliance or '')) if mla_alliance else '')
    widget_html = (template
                   .replace('__CONST_ID__', const_id)
                   .replace('__SLUG__', slug)
                   .replace('__NAME__', name)
                   .replace('__MLA_NAME__', (mla_name or '-'))
                   .replace('__MLA_META__', meta))
    return widget_html


def generate_timeline_widget_v2(constituency):
    """Past results widget using three result cards (2020/2015/2010), matching CMS markup."""
    slug = constituency.get('slug', '')
    const_id = f"bihar-pastresults-{slug}"

    template = '''<div id="__CONST_ID__" class="widget-past-results">
<style>
#__CONST_ID__ .results-container { display:grid; grid-template-columns:1fr; gap:16px; }
#__CONST_ID__ .card { background:#fff; border:1px solid #E5E7EB; border-radius:12px; padding:20px; }
#__CONST_ID__ .election-title { font-family:'Playfair Display', serif; font-size:18px; font-weight:600; line-height:36px; margin:0 0 12px; color:#000; }
#__CONST_ID__ .candidate-row { margin-bottom:16px; }
#__CONST_ID__ .candidate-name { font-family:'Roboto Slab', serif; font-weight:700; font-size:16px; color:#000; }
#__CONST_ID__ .candidate-party { color:#5B6064; font-size:14px; }
#__CONST_ID__ .bar { height:8px; border-radius:999px; background:#e5e7eb; position:relative; margin-top:8px; overflow:hidden; }
#__CONST_ID__ .bar span { position:absolute; left:0; top:0; bottom:0; border-radius:999px; display:block; }
#__CONST_ID__ .margin-info { margin-top:16px; padding-top:16px; border-top:1px solid #E5E7EB; }
#__CONST_ID__ .margin-text { font-family:'Roboto Slab', serif; font-weight:700; font-size:12px; }
@media (min-width:768px) { #__CONST_ID__ .results-container { grid-template-columns:1fr 1fr; gap:20px; } }
</style>
<div class="results-container">
  <div class="card"><h3 class="election-title">Loading past results…</h3></div>
</div>
<script>
(function(){
  var root=document.getElementById('__CONST_ID__'); if(!root) return;
  function ds(){ var h=(location.hostname||'').toLowerCase(); return (h.includes('quintype.io')||h.includes('sandbox'))?'sandbox':'github'; }
  var URLc = ds()==='sandbox' ? 'https://dh-sandbox-web.quintype.io/bihar_election_results_consolidated' : 'https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json';
  function rec(row, y){ if(!row) return null; var yy=String(y); var wN=row['y'+yy+'_winner_name'], wP=row['y'+yy+'_winner_party'], wV=row['y'+yy+'_winner_votes']; var rN=row['y'+yy+'_runner_name'], rP=row['y'+yy+'_runner_party'], rV=row['y'+yy+'_runner_votes']; var m=row['y'+yy+'_margin']; if(!wN&&!wP&&!wV&&!m) return null; return {wN:wN||'—', wP:wP||'—', wV:parseInt(wV)||0, rN:rN||'—', rP:rP||'—', rV:parseInt(rV)||0, m: (parseInt(m)||Math.max(0,(parseInt(wV)||0)-(parseInt(rV)||0)))}; }
  function cardHTML(year, r){ if(!r) return '<div class="card election-result"><h3 class="election-title">Bihar Elections '+year+' Results</h3><div class="muted">Not available</div></div>'; var maxV=Math.max(r.wV,r.rV,1), wPct=Math.round((r.wV/maxV)*100), rPct=Math.round((r.rV/maxV)*100); return ''+
    '<div class="card election-result">'+
      '<h3 class="election-title">Bihar Elections '+year+' Results</h3>'+
      '<div class="candidate-row">'+
        '<div class="candidate-name">WINNER: '+r.wN+'</div>'+
        '<div class="candidate-party">'+r.wP+' • <span class="vote-count">'+r.wV.toLocaleString('en-IN')+' votes</span></div>'+
        '<div class="bar"><span style="width:'+wPct+'%; background:#16a34a"></span></div>'+
      '</div>'+
      '<div class="candidate-row">'+
        '<div class="candidate-name">Runner-up: '+r.rN+'</div>'+
        '<div class="candidate-party">'+r.rP+' • <span class="vote-count">'+r.rV.toLocaleString('en-IN')+' votes</span></div>'+
        '<div class="bar"><span style="width:'+rPct+'%; background:#dc2626"></span></div>'+
      '</div>'+
      '<div class="margin-info"><span class="margin-text">MARGIN: '+r.m.toLocaleString('en-IN')+' votes</span></div>'+
    '</div>'; }
  fetch(URLc).then(function(r){return r.json();}).then(function(data){
    var row=(data||[]).find(function(x){return x.slug=='__SLUG__';});
    if(!row){ root.querySelector('.results-container').innerHTML='<div class="card"><div class="muted">Constituency not found</div></div>'; return; }
    var r2020=rec(row,2020), r2015=rec(row,2015), r2010=rec(row,2010);
    var html = cardHTML(2020,r2020)+cardHTML(2015,r2015)+cardHTML(2010,r2010);
    root.querySelector('.results-container').innerHTML = html;
  }).catch(function(){ root.querySelector('.results-container').innerHTML='<div class="card"><div class="muted">Error loading data</div></div>'; });
})();
</script>'''

    widget_html = template.replace('__CONST_ID__', const_id).replace('__SLUG__', slug)
    return widget_html


def main():
    """Main function to generate CSV export."""
    json_file = 'bihar_election_results_consolidated.json'

    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        constituencies = json.load(f)

    print(f"Loaded {len(constituencies)} constituencies")

    # Output CSV file
    output_file = 'constituency_widgets_export.csv'

    # CSV columns
    fieldnames = [
        'constituency_no',
        'slug',
        'name',
        'headline',
        'body_text',
        'widget_2025_results',
        'widget_current_mla',
        'widget_timeline',
        'widget_grid',
        'widget_map'
    ]

    # Generate universal map widget once
    universal_map = generate_map_widget()

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        for constituency in constituencies:
            no = constituency.get('no', 0)
            slug = constituency.get('slug', '')
            name = constituency.get('constituency_name', '')

            row = {
                'constituency_no': no,
                'slug': slug,
                'name': name,
                'headline': generate_headline(constituency),
                'body_text': generate_body_text(constituency),
                'widget_2025_results': generate_2025_widget_v2(constituency),
                'widget_current_mla': generate_mla_widget_v2(constituency),
                'widget_timeline': generate_timeline_widget_v2(constituency),
                'widget_grid': generate_grid_widget(constituency),
                'widget_map': universal_map
            }

            writer.writerow(row)
            print(f"Generated: {no} - {name}")

    print(f"\nSuccessfully generated {output_file}")
    print(f"Total rows: {len(constituencies)}")
    print(f"File size: {os.path.getsize(output_file) / 1024:.2f} KB")


if __name__ == "__main__":
    main()
