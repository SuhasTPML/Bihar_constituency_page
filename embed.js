/* Bihar Constituency Dynamic Embed (no iframe)
 * Minimal runtime to derive constituency from page URL, fetch JSON, and render.
 * Global API: window.BiharEmbed.mount(elOrSelector, { constituency?, source? })
 */
(function(){
  function $(sel){ return (typeof sel==='string') ? document.querySelector(sel) : sel; }
  function slugifyName(t){
    try {
      return String(t||'')
        .replace(/\([^)]*\)/g,'')
        .normalize('NFD').replace(/[\u0300-\u036f]/g,'')
        .toLowerCase()
        .replace(/[^a-z0-9]+/g,'-')
        .replace(/-+/g,'-')
        .replace(/^-+|-+$/g,'');
    } catch(e){ return ''; }
  }
  function extractPageSlug(u){
    try {
      var url = new URL(u);
      var segs = url.pathname.split('/').filter(Boolean);
      if (!segs.length) return '';
      var last = segs[segs.length-1].toLowerCase();
      last = last.replace(/\.(html|htm)$/,'');
      last = last.replace(/-(assembly|vidhan-sabha)-(election|polls)(-by)?(-20\d{2})?(-\d+)?$/,'');
      last = last.replace(/-\d+$/,'');
      return last.replace(/[^a-z0-9-]+/g,'-').replace(/-+/g,'-').replace(/^-+|-+$/g,'');
    } catch(e){ return ''; }
  }
  function endpoints(source){
    if ((source||'').toLowerCase()==='sandbox'){
      return {
        parties: 'https://dh-sandbox-web.quintype.io/parties.json',
        consolidated: 'https://dh-sandbox-web.quintype.io/bihar_election_results_consolidated'
      };
    }
    return {
      parties: 'https://suhastpml.github.io/Bihar_constituency_page/parties.json',
      consolidated: 'https://suhastpml.github.io/Bihar_constituency_page/bihar_election_results_consolidated.json'
    };
  }
  function injectStyles(root){
    var css = ''+
    ':host, :root { --bg:#fff; --text:#000; --muted:#5B6064; --border:#E5E7EB; --card:#fff; }\n'+
    '.container{max-width:1120px;margin:0 auto;padding:0 16px;font-family:\'Roboto Slab\',\'Roboto Serif\',Georgia,serif;color:var(--text);}\n'+
    '.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px;margin-bottom:16px;}\n'+
    '.constituency-title{font-family:Playfair Display,serif;font-size:32px;font-weight:700;margin:0 0 8px;}\n'+
    '.constituency-info{display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;}\n'+
    '.badge{display:inline-block;padding:2px 8px;border-radius:999px;background:#eef2ff;border:1px solid #e5e7eb;font-size:12px;}\n'+
    '.election-title{font-family:Playfair Display,serif;font-size:18px;font-weight:600;margin:0 0 12px;}\n'+
    '.candidate-row{margin-bottom:16px;} .candidate-info{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;}\n'+
    '.candidate-name{font-weight:700;font-size:16px;} .candidate-party{color:var(--muted);font-size:14px;} .vote-count{font-weight:600;}\n'+
    '.bar{height:8px;border-radius:999px;background:#e5e7eb;position:relative;margin-bottom:6px;} .bar>span{position:absolute;left:0;top:0;bottom:0;border-radius:999px;}\n'+
    '.margin-text{font-weight:700;font-size:12px;} .muted{color:var(--muted);} .disclaimer-text{color:var(--muted);font-size:11px;text-align:center;}\n';
    var style = document.createElement('style');
    style.textContent = css;
    root.appendChild(style);
  }
  function fmt(n){ try { return Number(n).toLocaleString('en-IN'); } catch(_) { return String(n); } }
  function enrichParty(code, partiesIdx){ var c=(code||'').trim(); var meta=partiesIdx[c]||null; return { code: c||null, name: meta? meta.name:null, color: meta? meta.color:'#888' }; }
  function recFromRow(row, year){ if(!row) return null; var y=String(year); var wN=row['y'+y+'_winner_name']; var wP=row['y'+y+'_winner_party']; var wV=row['y'+y+'_winner_votes']; var rN=row['y'+y+'_runner_name']; var rP=row['y'+y+'_runner_party']; var rV=row['y'+y+'_runner_votes']; var m=row['y'+y+'_margin']; if(!wN && !wP && !wV && !m) return null; return { 'Winner': { Candidate: wN||'-', Party: wP||'-', Votes: wV||'0' }, 'Runner up': { Candidate: rN||'-', Party: rP||'-', Votes: rV||'0' }, 'Margin': m||'0' }; }
  function renderYearBlock(year, rec, partiesIdx){ if(!rec){ return '<div class="card election-result"><h3 class="election-title">Bihar Elections '+year+' Results</h3><div class="muted">Not available</div></div>'; } var w=rec['Winner']||{}, ru=rec['Runner up']||{}; var wP=enrichParty(w.Party, partiesIdx), ruP=enrichParty(ru.Party, partiesIdx); var wVotes=parseInt(String(w.Votes||'').replace(/,/g,''),10)||0; var ruVotes=parseInt(String(ru.Votes||'').replace(/,/g,''),10)||0; var margin=parseInt(String(rec.Margin||'').replace(/,/g,''),10)||Math.max(0,wVotes-ruVotes); var maxV=Math.max(wVotes,ruVotes,1); var wPct=Math.round((wVotes/maxV)*100); var ruPct=Math.round((ruVotes/maxV)*100); return '<div class="card election-result">'+
    '<h3 class="election-title">Bihar Elections '+year+' Results</h3>'+
    '<div class="candidate-row">'+
    '<div class="candidate-info"><div><div class="candidate-name">WINNER: '+(w.Candidate||'-')+'</div><div class="candidate-party">'+(wP.name||wP.code||'-')+' · <span class="vote-count">'+fmt(wVotes)+' votes</span></div></div></div>'+
    '<div class="bar"><span style="width:'+wPct+'%; background:'+wP.color+'"></span></div>'+
    '</div>'+
    '<div class="candidate-row">'+
    '<div class="candidate-info"><div><div class="candidate-name">Runner-up: '+(ru.Candidate||'-')+'</div><div class="candidate-party">'+(ruP.name||ruP.code||'-')+' · <span class="vote-count">'+fmt(ruVotes)+' votes</span></div></div></div>'+
    '<div class="bar"><span style="width:'+ruPct+'%; background:'+ruP.color+'"></span></div>'+
    '</div>'+
    '<div class="margin-info"><span class="margin-text">MARGIN: '+fmt(margin)+' votes</span></div>'+
    '</div>'; }

  function mount(elOrSelector, options){
    var host = $(elOrSelector);
    if (!host) return;
    // Shadow DOM to scope styles
    var shadow = host.attachShadow ? host.attachShadow({mode:'open'}) : host;
    injectStyles(shadow);
    var wrap = document.createElement('div');
    wrap.className = 'container';
    shadow.appendChild(wrap);
    wrap.innerHTML = '<div class="muted">Loading constituency widget...</div>';

    var source = (host.getAttribute('data-source')|| (options && options.source) || 'gh');
    var ep = endpoints(source);
    var override = (host.getAttribute('data-constituency') || (options && options.constituency) || '').toLowerCase();
    if (!override){ try{ var qp = new URLSearchParams(location.search||''); override = (qp.get('constituency')||'').toLowerCase(); } catch(_){} }
    var slug = override || extractPageSlug(window.location.href);

    Promise.all([ fetch(ep.parties).then(r=>r.json()), fetch(ep.consolidated).then(r=>r.json()) ]).then(function(res){
      var parties = res[0]||[]; var consolidated = res[1]||[];
      var partiesIdx = {}; (parties||[]).forEach(function(p){ partiesIdx[p.code]=p; });
      var byNo = new Map(); var slugMap = new Map();
      (consolidated||[]).forEach(function(row){ var no=parseInt(String(row.no||''),10); if(Number.isFinite(no)){ byNo.set(no,row); var s=slugifyName(row.constituency_name||row.name||''); if(s) slugMap.set(s,no); }});
      var seatNo = null;
      if (slug && slugMap.has(slug)) seatNo = slugMap.get(slug); else if (slug) {
        var relaxed=slug.replace(/-/g,''); for (var it of slugMap.keys()){ if (it.replace(/-/g,'')===relaxed){ seatNo = slugMap.get(it); break; } }
      }
      if (!seatNo){ wrap.innerHTML = '<div class="card"><div class="error">Could not infer constituency from URL. Set data-constituency on container.</div></div>'; return; }
      var row = byNo.get(seatNo);
      var base = row ? { name: row.constituency_name, district: row.district, reserved: row.reserved || 'General' } : null;
      if (!base){ wrap.innerHTML = '<div class="card"><div class="error">Seat #'+seatNo+' not found.</div></div>'; return; }
      var r2010=recFromRow(row,2010), r2015=recFromRow(row,2015), r2020=recFromRow(row,2020), r2025=recFromRow(row,2025);
      var html = ''+
        '<div class="card constituency-header">'+
        '<h2 class="constituency-title">'+base.name+' Assembly Election 2025</h2>'+ 
        '<div class="constituency-info">'+
          '<div><strong>District:</strong> '+(base.district||'-')+'</div>'+ 
          '<div><strong>Seat Type:</strong> <span class="badge">'+(base.reserved||'General')+'</span></div>'+ 
        '</div></div>'+
        (r2025? renderYearBlock(2025, r2025, partiesIdx) : '')+
        '<div class="card"><div class="cms-content-body"><div id="mapEmbed" style="width:100%;"></div></div></div>'+
        '<div class="card">'+
          '<h3 class="past-results-title">Bihar Assembly Elections '+base.name+' Past Results</h3>'+ 
          renderYearBlock(2020, r2020, partiesIdx)+
          renderYearBlock(2015, r2015, partiesIdx)+
          renderYearBlock(2010, r2010, partiesIdx)+
        '</div>'+
        '<div class="disclaimer-footer"><div class="disclaimer-text">This page incorporates information from Wikipedia and ECI data.</div></div>';
      wrap.innerHTML = html;
      try {
        var el = (shadow.getElementById ? shadow.getElementById('mapEmbed') : document.getElementById('mapEmbed')) || wrap.querySelector('#mapEmbed');
        if (el){
          var ac = String(seatNo).padStart(3,'0');
          var iframe = document.createElement('iframe');
          iframe.className = 'embed-map';
          iframe.loading = 'lazy';
          iframe.referrerPolicy = 'no-referrer';
          iframe.style.width = '100%';
          iframe.style.height = '600px';
          iframe.style.border = '0';
          iframe.style.borderRadius = '8px';
          iframe.src = 'https://suhastpml.github.io/Bihar_constituency_page/map.html?ac='+ac+'&enable2025='+(r2025? '1':'0');
          el.innerHTML = '';
          el.appendChild(iframe);
        }
      } catch(_){}
    }).catch(function(e){ wrap.innerHTML = '<div class="card"><div class="error">Failed to load data for dynamic embed.</div></div>'; console && console.error && console.error(e); });
  }

  window.BiharEmbed = { mount: mount };
})();

