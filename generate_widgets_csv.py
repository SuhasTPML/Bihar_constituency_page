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
    """Generate headline for CMS."""
    name = constituency.get('constituency_name', '')
    return f"{name} Assembly Election 2025 - Results, Winner, Runner-up"


def generate_body_text(constituency):
    """Generate body text for article."""
    name = constituency.get('constituency_name', '')
    district = constituency.get('district', '')
    reserved = constituency.get('reserved', '')
    seat_type = "General" if reserved == "" else reserved
    lok_sabha = constituency.get('lok_sabha', '')

    body = f"The {name} constituency is in {district} district of Bihar. This is a {seat_type} seat under the {lok_sabha} Lok Sabha constituency.\n\n"

    # Add 2020 results
    w2020 = constituency.get('y2020_winner_name', '')
    p2020 = constituency.get('y2020_winner_party', '')
    v2020 = constituency.get('y2020_winner_votes', 0)
    r2020 = constituency.get('y2020_runner_name', '')
    rp2020 = constituency.get('y2020_runner_party', '')
    rv2020 = constituency.get('y2020_runner_votes', 0)
    m2020 = constituency.get('y2020_margin', 0)

    try:
        v2020_fmt = f"{int(v2020):,}"
        rv2020_fmt = f"{int(rv2020):,}"
        m2020_fmt = f"{int(m2020):,}"
    except:
        v2020_fmt = str(v2020)
        rv2020_fmt = str(rv2020)
        m2020_fmt = str(m2020)

    body += f"In the 2020 Bihar Assembly elections, {w2020} ({p2020}) won the seat with {v2020_fmt} votes. {r2020} ({rp2020}) was the runner-up with {rv2020_fmt} votes. The victory margin was {m2020_fmt} votes."

    return body


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
                'widget_2025_results': generate_2025_widget(constituency),
                'widget_current_mla': generate_mla_widget(constituency),
                'widget_timeline': generate_timeline_widget(constituency),
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
