import json, sys, os

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else '/tmp/final_all_data.json'
OUT_PATH = sys.argv[2] if len(sys.argv) > 2 else '/tmp/Writers Thesaurus.html'

with open(DATA_PATH, encoding='utf-8') as f:
    data = json.load(f)

data_json = json.dumps(data, ensure_ascii=False)
data_json_safe = data_json.replace('</', '<\\/')

HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Writer's Thesaurus</title>
<style>
  :root{
    --paper: #faf6ee;
    --paper-raised: #ffffff;
    --ink: #2b2620;
    --ink-soft: #6b6255;
    --ink-faint: #9a917f;
    --accent: #8a4a3b;
    --accent-soft: #c98f7a;
    --line: #e5dcc9;
    --highlight: #f3dfa4;
    --danger: #b3492f;
  }
  @media (prefers-color-scheme: dark){
    :root{
      --paper: #1c1a16;
      --paper-raised: #242019;
      --ink: #ece5d6;
      --ink-soft: #b8ae99;
      --ink-faint: #7d7566;
      --accent: #e0a08c;
      --accent-soft: #a9695a;
      --line: #3a352b;
      --highlight: #4a3d1d;
      --danger: #e0836a;
    }
  }
  *{ box-sizing: border-box; }
  html,body{ height:100%; }
  body{
    margin:0;
    background:var(--paper);
    color:var(--ink);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    display:flex;
    flex-direction:column;
  }
  .brand{ font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif; }
  header{
    padding: 18px 28px 14px;
    border-bottom: 1px solid var(--line);
    background: var(--paper);
    position: sticky;
    top:0;
    z-index: 5;
  }
  .top-row{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:16px;
    flex-wrap:wrap;
  }
  h1{
    margin:0;
    font-size: 1.4rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    white-space: nowrap;
  }
  .controls{
    display:flex;
    gap:10px;
    flex:1;
    flex-wrap:wrap;
    justify-content:flex-end;
  }
  select#notebookSelect{
    padding: 9px 12px;
    border-radius: 10px;
    border: 1px solid var(--line);
    background: var(--paper-raised);
    color: var(--ink);
    font-size: 0.92rem;
    font-family: inherit;
    max-width: 220px;
  }
  .search-wrap{
    flex: 1 1 280px;
    max-width: 420px;
    position: relative;
  }
  #search{
    width:100%;
    padding: 9px 14px 9px 34px;
    border-radius: 10px;
    border: 1px solid var(--line);
    background: var(--paper-raised);
    color: var(--ink);
    font-size: 0.92rem;
    outline: none;
  }
  #search:focus{ border-color: var(--accent-soft); }
  .search-wrap::before{
    content: "";
    position:absolute;
    left: 12px;
    top: 50%;
    transform: translateY(-50%);
    width: 13px; height:13px;
    border: 2px solid var(--ink-faint);
    border-radius: 50%;
    pointer-events:none;
  }
  .search-wrap::after{
    content:"";
    position:absolute;
    left: 23px;
    top: 62%;
    width: 6px;
    height: 2px;
    background: var(--ink-faint);
    transform: rotate(45deg);
    pointer-events:none;
  }
  main{ flex:1; display:flex; min-height:0; }
  nav.index{
    width: 250px;
    flex-shrink:0;
    border-right: 1px solid var(--line);
    overflow-y: auto;
    padding: 0 0 40px;
    display:flex;
    flex-direction:column;
  }
  nav.index .filter-wrap{
    padding: 12px 16px 6px;
    position: sticky;
    top: 0;
    background: var(--paper);
  }
  nav.index .filter-wrap input{
    width:100%;
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid var(--line);
    background: var(--paper-raised);
    color: var(--ink);
    font-size: 0.82rem;
  }
  nav.index .count{
    padding: 8px 20px 6px;
    font-size: 0.7rem;
    color: var(--ink-faint);
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }
  nav.index ul{ list-style:none; margin:0; padding:0; }
  nav.index li{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:8px;
    padding: 8px 20px;
    cursor:pointer;
    font-size: 0.92rem;
    border-left: 3px solid transparent;
  }
  nav.index li:hover{ background: var(--paper-raised); }
  nav.index li.active{
    background: var(--paper-raised);
    border-left-color: var(--accent);
    font-weight: 600;
  }
  nav.index li .n{
    font-size: 0.7rem;
    color: var(--ink-faint);
    background: var(--line);
    border-radius: 10px;
    padding: 1px 7px;
    flex-shrink:0;
  }
  nav.index .empty-hint{
    padding: 8px 20px;
    font-size: 0.85rem;
    color: var(--ink-faint);
    font-style: italic;
  }
  nav.index .new-hw-wrap{
    padding: 14px 16px 16px;
    margin-top: 10px;
    border-top: 1px solid var(--line);
    display:flex;
    flex-direction:column;
    gap:6px;
  }
  nav.index .new-hw-wrap input{
    width:100%;
    padding: 6px 10px;
    border-radius: 8px;
    border: 1px solid var(--line);
    background: var(--paper-raised);
    color: var(--ink);
    font-size: 0.82rem;
  }
  nav.index .new-hw-wrap button{
    align-self:flex-start;
    padding: 6px 12px;
    border-radius: 8px;
    border: none;
    background: var(--accent);
    color: #fff;
    font-size: 0.78rem;
    font-weight: 600;
    cursor:pointer;
  }
  nav.index .new-hw-wrap button:hover{ background: var(--accent-soft); }
  nav.index .new-hw-error{
    font-size: 0.75rem;
    color: var(--danger);
  }
  section.content{ flex:1; overflow-y:auto; padding: 30px 40px 80px; }
  .content-inner{ max-width: 700px; }
  .crumb{
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--accent);
    margin-bottom: 6px;
  }
  h2.headword{
    font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
    font-size: 2rem;
    margin: 0 0 4px;
    color: var(--ink);
  }
  .headword-meta{ color: var(--ink-faint); font-size: 0.85rem; margin-bottom: 24px; }
  ul.beats{ list-style:none; margin: 0 0 30px; padding:0; }
  li.beat{ padding: 16px 0; border-bottom: 1px solid var(--line); position: relative; }
  li.beat:last-child{ border-bottom:none; }
  li.beat .text{
    font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
    font-size: 1.08rem;
    line-height: 1.6;
    color: var(--ink);
  }
  li.beat .source{ margin-top: 6px; font-size: 0.8rem; color: var(--ink-faint); font-style: italic; }
  li.beat img.beat-photo{
    display:block;
    max-width: 260px;
    max-height: 260px;
    width:auto; height:auto;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 1px solid var(--line);
  }
  li.beat .tag-mine{
    display:inline-block;
    margin-left: 8px;
    font-size: 0.66rem;
    font-style: normal;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent);
    background: color-mix(in srgb, var(--accent) 12%, transparent);
    padding: 2px 6px;
    border-radius: 6px;
    vertical-align: middle;
  }
  li.beat .del{
    position:absolute; right:0; top:14px;
    border:none; background:none; color: var(--ink-faint);
    cursor:pointer; font-size:1.1rem; line-height:1; padding:4px 6px;
    opacity:0; transition:opacity .15s;
  }
  li.beat:hover .del{ opacity:1; }
  li.beat .del:hover{ color: var(--danger); }
  mark{ background: var(--highlight); color: inherit; border-radius: 3px; padding: 0 1px; }
  .add-form{
    margin-top: 8px;
    padding: 18px 20px;
    background: var(--paper-raised);
    border: 1px dashed var(--line);
    border-radius: 12px;
  }
  .add-form summary{ cursor:pointer; font-size: 0.88rem; color: var(--accent); font-weight: 600; list-style: none; }
  .add-form summary::-webkit-details-marker{ display:none; }
  .add-form summary::before{ content: "+ "; }
  .add-form[open] summary::before{ content: "\2212 "; }
  .fields{ margin-top: 14px; display:flex; flex-direction:column; gap: 10px; }
  .fields input, .fields textarea{
    width:100%; padding: 9px 12px; border-radius: 8px;
    border: 1px solid var(--line); background: var(--paper); color: var(--ink);
    font-size: 0.92rem; font-family: inherit; resize: vertical;
  }
  .fields button{
    align-self:flex-start; padding: 8px 18px; border-radius: 8px; border: none;
    background: var(--accent); color: #fff; font-size: 0.88rem; font-weight: 600; cursor:pointer;
  }
  .image-attach{ display:flex; align-items:center; gap:10px; flex-wrap:wrap; }
  .image-attach-btn{
    padding: 7px 14px; border-radius: 8px; border: 1px solid var(--line);
    background: var(--paper); color: var(--ink-soft); font-size: 0.85rem;
    cursor:pointer; user-select:none;
  }
  .image-attach-btn:hover{ border-color: var(--accent-soft); color: var(--accent); }
  .image-attach-name{ font-size: 0.8rem; color: var(--ink-faint); }
  .image-attach-preview{
    max-width: 90px; max-height: 90px; border-radius: 8px; border: 1px solid var(--line); display:block;
  }
  .fields button:hover{ background: var(--accent-soft); }
  .search-results .result-crumb{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em;
    color: var(--accent); margin-bottom: 4px;
  }
  .result-crumb-link{
    cursor: pointer;
    display: inline-block;
    text-decoration: underline;
    text-decoration-color: transparent;
    text-underline-offset: 3px;
    transition: text-decoration-color .15s;
  }
  .result-crumb-link:hover{
    text-decoration-color: var(--accent);
  }
  .empty-state{ color: var(--ink-faint); font-size: 0.95rem; padding: 40px 0; }
  footer.tools{
    padding: 14px 28px; border-top: 1px solid var(--line);
    display:flex; justify-content:space-between; align-items:center;
    font-size: 0.78rem; color: var(--ink-faint); flex-wrap:wrap; gap: 8px;
  }
  footer.tools button{
    background:none; border: 1px solid var(--line); color: var(--ink-soft);
    padding: 6px 12px; border-radius: 8px; cursor:pointer; font-size: 0.78rem;
  }
  footer.tools button:hover{ border-color: var(--accent-soft); color: var(--accent); }
  .comments-section{
    max-width: 700px;
    margin: 0 auto;
    padding: 0 40px 60px;
  }
  .comments-section h3{
    font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
    font-size: 1.1rem;
    margin: 0 0 4px;
    color: var(--ink);
  }
  .comments-section .hint{
    font-size: 0.82rem;
    color: var(--ink-faint);
    margin-bottom: 16px;
  }
  @media (max-width: 780px){
    .comments-section{ padding: 0 20px 40px; }
  }
  @media (max-width: 780px){
    main{ flex-direction:column; }
    nav.index{ width:100%; max-height: 220px; border-right:none; border-bottom: 1px solid var(--line); }
    section.content{ padding: 22px 20px 60px; }
    select#notebookSelect{ max-width: none; }
  }
</style>
</head>
<body>

<header>
  <div class="top-row">
    <h1 class="brand">Writer's Thesaurus</h1>
    <div class="controls">
      <select id="notebookSelect"></select>
      <div class="search-wrap">
        <input id="search" type="text" placeholder="Search every notebook…" autocomplete="off">
      </div>
    </div>
  </div>
</header>

<main>
  <nav class="index" id="index"></nav>
  <section class="content"><div class="content-inner" id="content"></div></section>
</main>

<footer class="tools">
  <span id="statline"></span>
  <div><button id="exportBtn" type="button">Export my additions (.json)</button></div>
</footer>

<div class="comments-section">
  <h3>Comments &amp; suggestions</h3>
  <div class="hint">Sign in with GitHub to suggest a beat, a headword, or a fix — nothing here changes the thesaurus itself until Amel folds it in.</div>
  <script src="https://giscus.app/client.js"
    data-repo="amelabrs/writers-thesaurus"
    data-repo-id="R_kgDOUTruqA"
    data-category="Announcements"
    data-category-id="DIC_kwDOUTruqM4DFRwS"
    data-mapping="pathname"
    data-strict="0"
    data-reactions-enabled="1"
    data-emit-metadata="0"
    data-input-position="bottom"
    data-theme="preferred_color_scheme"
    data-lang="en"
    crossorigin="anonymous"
    async>
  </script>
</div>

<script id="builtin-data" type="application/json">__DATA_JSON__</script>
<script>
(function(){
  "use strict";
  var BUILTIN = JSON.parse(document.getElementById('builtin-data').textContent);
  var STORE_KEY = 'writersThesaurus_v2';
  var LEGACY_KEY = 'beatsThesaurus_v1';

  function loadMine(){
    try{
      var raw = localStorage.getItem(STORE_KEY);
      var mine = raw ? JSON.parse(raw) : {};
      // one-time migration from the old single-notebook store
      if (!mine.__migrated){
        try{
          var legacyRaw = localStorage.getItem(LEGACY_KEY);
          if (legacyRaw){
            var legacy = JSON.parse(legacyRaw);
            if (legacy && Object.keys(legacy).length){
              mine['Beats'] = mine['Beats'] || {};
              Object.keys(legacy).forEach(function(hw){
                mine['Beats'][hw] = (mine['Beats'][hw] || []).concat(legacy[hw]);
              });
            }
          }
        }catch(e){}
        mine.__migrated = true;
        try{ localStorage.setItem(STORE_KEY, JSON.stringify(mine)); }catch(e){}
      }
      return mine;
    }catch(e){ return {__migrated:true}; }
  }
  function saveMine(mine){
    try{ localStorage.setItem(STORE_KEY, JSON.stringify(mine)); }catch(e){}
  }

  var mine = loadMine();

  function notebookNames(){
    var names = {};
    Object.keys(BUILTIN).forEach(function(k){ names[k] = true; });
    Object.keys(mine).forEach(function(k){ if (k.indexOf('__') !== 0) names[k] = true; });
    return Object.keys(names);
  }

  function isDeleted(notebook, headword, text){
    var d = mine.__deleted && mine.__deleted[notebook] && mine.__deleted[notebook][headword];
    return !!(d && d.indexOf(text) !== -1);
  }

  function markDeleted(notebook, headword, text){
    mine.__deleted = mine.__deleted || {};
    mine.__deleted[notebook] = mine.__deleted[notebook] || {};
    mine.__deleted[notebook][headword] = mine.__deleted[notebook][headword] || [];
    if (mine.__deleted[notebook][headword].indexOf(text) === -1){
      mine.__deleted[notebook][headword].push(text);
    }
    saveMine(mine);
  }

  function headwordNames(notebook){
    var names = {};
    var bnb = BUILTIN[notebook] || {};
    Object.keys(bnb).forEach(function(k){ names[k.toLowerCase()] = k; });
    var mnb = (mine[notebook] || {});
    Object.keys(mnb).forEach(function(k){
      var lower = k.toLowerCase();
      if (!names[lower]) names[lower] = k;
    });
    return Object.keys(names).map(function(l){ return names[l]; }).sort(function(a,b){
      return a.toLowerCase().localeCompare(b.toLowerCase());
    });
  }

  function entriesFor(notebook, headword){
    var lower = headword.toLowerCase();
    var out = [];
    var bnb = BUILTIN[notebook] || {};
    Object.keys(bnb).forEach(function(k){
      if (k.toLowerCase() === lower){
        bnb[k].forEach(function(e){
          if (isDeleted(notebook, k, e.text || '')) return;
          out.push({text:e.text||'', source:e.source||'', image:e.image||'', mine:false, notebook:notebook, headword:k});
        });
      }
    });
    var mnb = (mine[notebook] || {});
    Object.keys(mnb).forEach(function(k){
      if (k.toLowerCase() === lower){
        mnb[k].forEach(function(e, idx){ out.push({text:e.text||'', source:e.source||'', image:e.image||'', mine:true, idx:idx, notebook:notebook, headword:k}); });
      }
    });
    return out;
  }

  var state = { notebook: null, headword: null, query: '' };

  function escapeHtml(s){
    return String(s).replace(/[&<>"']/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function highlight(text, q){
    if(!q) return escapeHtml(text);
    var esc = escapeHtml(text);
    var qEsc = escapeHtml(q);
    try{
      var re = new RegExp('(' + qEsc.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
      return esc.replace(re, '<mark>$1</mark>');
    }catch(e){ return esc; }
  }

  function populateNotebookSelect(){
    var sel = document.getElementById('notebookSelect');
    var names = notebookNames();
    sel.innerHTML = names.map(function(n){
      var hwCount = headwordNames(n).length;
      return '<option value="' + escapeHtml(n) + '">' + escapeHtml(n) + ' (' + hwCount + ')</option>';
    }).join('');
    if (!state.notebook || names.indexOf(state.notebook) === -1){
      state.notebook = names[0];
    }
    sel.value = state.notebook;
  }

  function renderIndex(){
    var names = headwordNames(state.notebook);
    var filterVal = (document.getElementById('hwFilter') ? document.getElementById('hwFilter').value : '').trim().toLowerCase();
    var nav = document.getElementById('index');
    var html = '<div class="filter-wrap"><input id="hwFilter" type="text" placeholder="Filter headwords…" value="' + escapeHtml(filterVal) + '"></div>';
    html += '<div class="count">' + names.length + ' headwords</div><ul>';
    var shown = 0;
    names.forEach(function(name){
      if (filterVal && name.toLowerCase().indexOf(filterVal) === -1) return;
      shown++;
      var count = entriesFor(state.notebook, name).length;
      var cls = (name === state.headword) ? 'active' : '';
      html += '<li class="' + cls + '" data-hw="' + escapeHtml(name) + '">' +
                '<span>' + escapeHtml(name) + '</span><span class="n">' + count + '</span></li>';
    });
    html += '</ul>';
    if (shown === 0){
      html += '<div class="empty-hint">No headwords match.</div>';
    }
    html += '<div class="new-hw-wrap">' +
        '<input id="newHwInput" type="text" placeholder="New section… e.g. Vurms">' +
        '<button type="button" id="newHwBtn">+ Add section</button>' +
        '<div class="new-hw-error" id="newHwError" hidden></div>' +
      '</div>';
    nav.innerHTML = html;
    Array.prototype.forEach.call(nav.querySelectorAll('li[data-hw]'), function(li){
      li.addEventListener('click', function(){
        state.headword = li.getAttribute('data-hw');
        render();
      });
    });
    var filterInput = document.getElementById('hwFilter');
    filterInput.addEventListener('input', function(e){
      renderIndex();
      var el = document.getElementById('hwFilter');
      el.focus();
      el.selectionStart = el.selectionEnd = el.value.length;
    });

    var newHwInput = document.getElementById('newHwInput');
    var newHwBtn = document.getElementById('newHwBtn');
    var newHwError = document.getElementById('newHwError');
    function submitNewHw(){
      var name = newHwInput.value.trim();
      newHwError.hidden = true;
      if (!name) return;
      var existing = headwordNames(state.notebook);
      var dup = existing.some(function(n){ return n.toLowerCase() === name.toLowerCase(); });
      if (dup){
        newHwError.textContent = '"' + name + '" already exists in this notebook.';
        newHwError.hidden = false;
        return;
      }
      mine[state.notebook] = mine[state.notebook] || {};
      mine[state.notebook][name] = mine[state.notebook][name] || [];
      saveMine(mine);
      state.headword = name;
      state.query = '';
      document.getElementById('search').value = '';
      render();
    }
    newHwBtn.addEventListener('click', submitNewHw);
    newHwInput.addEventListener('keydown', function(e){
      if (e.key === 'Enter'){ e.preventDefault(); submitNewHw(); }
    });
  }

  function renderEntry(e, opts){
    opts = opts || {};
    var out = '<li class="beat">';
    if (e.mine){
      out += '<button class="del" data-mode="mine" data-notebook="' + escapeHtml(e.notebook) + '" data-hw="' + escapeHtml(e.headword) + '" data-idx="' + e.idx + '" title="Remove">&times;</button>';
    } else {
      out += '<button class="del" data-mode="builtin" data-notebook="' + escapeHtml(e.notebook) + '" data-hw="' + escapeHtml(e.headword) + '" data-text="' + escapeHtml(e.text) + '" title="Remove">&times;</button>';
    }
    if (opts.crumb){
      if (opts.crumbNb){
        out += '<div class="result-crumb result-crumb-link" data-nb="' + escapeHtml(opts.crumbNb) + '" data-hw="' + escapeHtml(opts.crumbHw) + '" title="Go to this headword">' + escapeHtml(opts.crumb) + '</div>';
      } else {
        out += '<div class="result-crumb">' + escapeHtml(opts.crumb) + '</div>';
      }
    }
    if (e.image){
      out += '<img class="beat-photo" src="' + e.image + '" alt="' + escapeHtml(e.text) + '">';
    }
    if (e.text){
      out += '<div class="text">' + highlight(e.text, opts.q || '') + (e.mine ? '<span class="tag-mine">yours</span>' : '') + '</div>';
    }
    if (e.source){
      out += '<div class="source">' + escapeHtml(e.source) + '</div>';
    }
    out += '</li>';
    return out;
  }

  function renderAddForm(notebook, headword){
    return '' +
      '<details class="add-form" id="addForm">' +
        '<summary>Add a beat to "' + escapeHtml(headword) + '"</summary>' +
        '<div class="fields">' +
          '<textarea id="newBeatText" rows="2" placeholder="type a new beat… (optional if you attach an image)"></textarea>' +
          '<input id="newBeatSource" type="text" placeholder="Source (optional) — book, author, page">' +
          '<div class="image-attach">' +
            '<label class="image-attach-btn" for="newBeatImage">Attach an image (optional)</label>' +
            '<input id="newBeatImage" type="file" accept="image/*" hidden>' +
            '<span id="newBeatImageName" class="image-attach-name"></span>' +
            '<img id="newBeatImagePreview" class="image-attach-preview" hidden>' +
          '</div>' +
          '<button type="button" id="addBeatBtn">Add beat</button>' +
        '</div>' +
      '</details>';
  }

  function resizeImageFile(file, maxDim, quality){
    return new Promise(function(resolve, reject){
      var reader = new FileReader();
      reader.onerror = reject;
      reader.onload = function(){
        var img = new Image();
        img.onerror = reject;
        img.onload = function(){
          var w = img.width, h = img.height;
          var scale = Math.min(1, maxDim / Math.max(w, h));
          var cw = Math.round(w * scale), ch = Math.round(h * scale);
          var canvas = document.createElement('canvas');
          canvas.width = cw; canvas.height = ch;
          var ctx = canvas.getContext('2d');
          ctx.drawImage(img, 0, 0, cw, ch);
          var mime = (file.type === 'image/png') ? 'image/png' : 'image/jpeg';
          resolve(canvas.toDataURL(mime, quality));
        };
        img.src = reader.result;
      };
      reader.readAsDataURL(file);
    });
  }

  function wireDeleteButtons(container){
    Array.prototype.forEach.call(container.querySelectorAll('.del'), function(btn){
      btn.addEventListener('click', function(){
        var nb = btn.getAttribute('data-notebook');
        var hw = btn.getAttribute('data-hw');
        var mode = btn.getAttribute('data-mode');
        if (mode === 'mine'){
          var idx = parseInt(btn.getAttribute('data-idx'), 10);
          if (mine[nb] && mine[nb][hw]){
            mine[nb][hw].splice(idx, 1);
            if (mine[nb][hw].length === 0) delete mine[nb][hw];
            saveMine(mine);
            render();
          }
        } else {
          var text = btn.getAttribute('data-text');
          markDeleted(nb, hw, text);
          render();
        }
      });
    });
  }

  function renderHeadword(){
    var notebook = state.notebook, headword = state.headword;
    var entries = entriesFor(notebook, headword);
    var content = document.getElementById('content');
    var html = '<div class="crumb">' + escapeHtml(notebook) + '</div>' +
      '<h2 class="headword">' + escapeHtml(headword) + '</h2>' +
      '<div class="headword-meta">' + entries.length + (entries.length === 1 ? ' entry' : ' entries') + '</div>';
    if (entries.length === 0){
      html += '<div class="empty-state">Nothing here yet — add the first one below.</div>';
    } else {
      html += '<ul class="beats">';
      entries.forEach(function(e){ html += renderEntry(e); });
      html += '</ul>';
    }
    html += renderAddForm(notebook, headword);
    content.innerHTML = html;
    wireDeleteButtons(content);

    var imageInput = document.getElementById('newBeatImage');
    var imageNameEl = document.getElementById('newBeatImageName');
    var imagePreview = document.getElementById('newBeatImagePreview');
    var pendingImage = null;
    if (imageInput){
      imageInput.addEventListener('change', function(){
        var file = imageInput.files && imageInput.files[0];
        pendingImage = null;
        if (!file){
          imageNameEl.textContent = '';
          imagePreview.hidden = true;
          return;
        }
        imageNameEl.textContent = 'Processing…';
        resizeImageFile(file, 900, 0.85).then(function(dataUrl){
          pendingImage = dataUrl;
          imageNameEl.textContent = file.name;
          imagePreview.src = dataUrl;
          imagePreview.hidden = false;
        }).catch(function(){
          imageNameEl.textContent = 'Could not read that image.';
        });
      });
    }

    var addBtn = document.getElementById('addBeatBtn');
    if (addBtn){
      addBtn.addEventListener('click', function(){
        var textEl = document.getElementById('newBeatText');
        var sourceEl = document.getElementById('newBeatSource');
        var text = textEl.value.trim();
        var source = sourceEl.value.trim();
        if (!text && !pendingImage) return;
        mine[notebook] = mine[notebook] || {};
        mine[notebook][headword] = mine[notebook][headword] || [];
        var entry = {text: text, source: source};
        if (pendingImage) entry.image = pendingImage;
        mine[notebook][headword].push(entry);
        saveMine(mine);
        pendingImage = null;
        render();
      });
    }
  }

  function renderSearchResults(){
    var q = state.query.trim();
    var qLower = q.toLowerCase();
    var content = document.getElementById('content');
    var results = [];
    notebookNames().forEach(function(nb){
      headwordNames(nb).forEach(function(hw){
        entriesFor(nb, hw).forEach(function(e){
          if ((e.text || '').toLowerCase().indexOf(qLower) !== -1){
            results.push({nb: nb, hw: hw, entry: e});
          }
        });
      });
    });
    var html = '<h2 class="headword">Search: "' + escapeHtml(q) + '"</h2>' +
      '<div class="headword-meta">' + results.length + (results.length === 1 ? ' match' : ' matches') + ' across every notebook</div>';
    if (results.length === 0){
      html += '<div class="empty-state">Nothing found.</div>';
    } else {
      html += '<ul class="beats search-results">';
      results.slice(0, 400).forEach(function(r){
        html += renderEntry(r.entry, {crumb: r.nb + ' → ' + r.hw, crumbNb: r.nb, crumbHw: r.hw, q: q});
      });
      html += '</ul>';
      if (results.length > 400){
        html += '<div class="empty-state">' + (results.length - 400) + ' more matches not shown — narrow your search.</div>';
      }
    }
    content.innerHTML = html;
    wireDeleteButtons(content);

    Array.prototype.forEach.call(content.querySelectorAll('.result-crumb-link'), function(el){
      el.addEventListener('click', function(){
        state.notebook = el.getAttribute('data-nb');
        state.headword = el.getAttribute('data-hw');
        state.query = '';
        document.getElementById('search').value = '';
        render();
      });
    });
  }

  function updateStatline(){
    var nbs = notebookNames();
    var totalHw = 0, total = 0;
    nbs.forEach(function(n){
      var hws = headwordNames(n);
      totalHw += hws.length;
      hws.forEach(function(hw){ total += entriesFor(n, hw).length; });
    });
    document.getElementById('statline').textContent =
      nbs.length + ' notebooks · ' + totalHw + ' headwords · ' + total + ' entries';
  }

  function render(){
    populateNotebookSelect();
    if (state.query.trim()){
      renderIndex();
      updateStatline();
      renderSearchResults();
      return;
    }
    var names = headwordNames(state.notebook);
    if (!state.headword || names.indexOf(state.headword) === -1){
      state.headword = names[0] || null;
    }
    renderIndex();
    updateStatline();
    if (state.headword){
      renderHeadword();
    } else {
      document.getElementById('content').innerHTML = '<div class="empty-state">This notebook is empty.</div>';
    }
  }

  document.getElementById('notebookSelect').addEventListener('change', function(e){
    state.notebook = e.target.value;
    state.headword = null;
    state.query = '';
    document.getElementById('search').value = '';
    render();
  });

  document.getElementById('search').addEventListener('input', function(e){
    state.query = e.target.value;
    render();
  });

  document.getElementById('exportBtn').addEventListener('click', function(){
    var blob = new Blob([JSON.stringify(mine, null, 2)], {type: 'application/json'});
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'writers-thesaurus-my-additions.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function(){ URL.revokeObjectURL(url); }, 1000);
  });

  render();
})();
</script>

</body>
</html>
"""

HTML = HTML.replace('__DATA_JSON__', data_json_safe)

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(HTML)

print("Wrote", len(HTML), "bytes to", OUT_PATH)
