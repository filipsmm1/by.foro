(() => {
  const configs = {
    perfume: {
      name: 'Perfume', plural: 'perfumes', kicker: 'Beauty · Perfume', search: 'Try vanilla, musk or Burberry', typeName: 'Scent direction',
      types: {'skin-musk':'Skin musk','fresh-citrus':'Fresh citrus','floral-powdery':'Floral & powdery','green-woody':'Green & woody','gourmand-vanilla':'Gourmand vanilla','amber-spicy':'Amber & spice'},
      priorities: {longevity:'Long wear',subtlety:'Subtle',uniqueness:'Distinctive',versatility:'Versatile',compliments:'Noticeable',layering:'Easy to layer',comfort:'Comforting'},
      avoid: {sweet:'Too sweet',powdery:'Powdery',floral:'Floral',citrus:'Citrus',musk:'Musk',vanilla:'Vanilla',woody:'Very woody',smoky:'Smoky',strong:'Very strong'},
      budgets: ['Under $75','$75 to $150','$150 to $250','$250+']
    },
    makeup: {
      name: 'Makeup', plural: 'makeup products', kicker: 'Beauty · Makeup', search: 'Try mascara, lipstick or e.l.f.', typeName: 'Product type',
      types: {complexion:'Complexion',lips:'Lips',eyes:'Eyes',cheeks:'Cheeks',brows:'Brows',tools:'Tools'},
      priorities: {natural:'Natural finish','long-wear':'Long wear',sensitive:'Sensitive skin',travel:'Travel friendly',beginner:'Easy to use',bold:'Bold colour'},
      avoid: {fragrance:'Fragrance',shimmer:'Shimmer','full-coverage':'Full coverage',waterproof:'Waterproof',cream:'Cream textures',powder:'Powder textures'},
      budgets: ['Under $15','$15 to $30','$30 to $60','$60+']
    },
    skincare: {
      name: 'Skincare', plural: 'skincare products', kicker: 'Beauty · Skincare', search: 'Try cleanser, SPF or CeraVe', typeName: 'Product type',
      types: {cleanser:'Cleanser',moisturizer:'Moisturizer',sunscreen:'Sunscreen',serum:'Serum',exfoliant:'Exfoliant',mask:'Mask & patches',body:'Body care'},
      priorities: {hydration:'Hydration',sensitive:'Sensitive skin',acne:'Blemish care',brightening:'Brightening',barrier:'Barrier support','anti-aging':'Firming & lines'},
      avoid: {fragrance:'Fragrance','active-heavy':'Strong actives',rich:'Rich textures',oil:'Facial oils',exfoliating:'Exfoliation'},
      budgets: ['Under $20','$20 to $40','$40 to $80','$80+']
    },
    kitchen: {
      name: 'Kitchen appliances', plural: 'kitchen appliances', kicker: 'Home · Kitchen', search: 'Try air fryer, blender or Ninja', typeName: 'Appliance type',
      types: {coffee:'Coffee', 'air-frying':'Air frying', blending:'Blending', baking:'Baking', 'meal-prep':'Meal prep', breakfast:'Breakfast'},
      priorities: {compact:'Compact','easy-clean':'Easy to clean',speed:'Fast',quiet:'Quiet','family-size':'Family size','multi-use':'Multi-use'},
      avoid: {plastic:'Plastic','hand-wash':'Hand washing',large:'Large footprint','single-use':'One job only',noisy:'High noise'},
      budgets: ['Under $50','$50 to $120','$120 to $250','$250+']
    },
    home: {
      name: 'Home essentials', plural: 'home products', kicker: 'Home · Essentials', search: 'Try storage, rug or frame', typeName: 'Product type',
      types: {lighting:'Lighting',textiles:'Textiles',storage:'Storage',tabletop:'Tabletop','wall-decor':'Wall decor',scent:'Home scent'},
      priorities: {'small-space':'Small space',washable:'Washable',neutral:'Neutral',statement:'Statement',durable:'Durable','renter-friendly':'Renter friendly'},
      avoid: {glass:'Glass',scented:'Scented',synthetic:'Synthetic materials',assembly:'Assembly',oversized:'Oversized'},
      budgets: ['Under $25','$25 to $60','$60 to $150','$150+']
    },
    accessories: {
      name: 'Fashion accessories', plural: 'fashion accessories', kicker: 'Fashion · Accessories', search: 'Try sunglasses, belt or necklace', typeName: 'Accessory type',
      types: {jewelry:'Jewellery',handbags:'Bags & wallets',hair:'Hair accessories',belts:'Belts',scarves:'Scarves',eyewear:'Eyewear',hats:'Hats'},
      priorities: {everyday:'Everyday',statement:'Statement',travel:'Travel friendly',adjustable:'Adjustable',giftable:'Giftable',minimal:'Minimal'},
      avoid: {'gold-tone':'Gold tone','silver-tone':'Silver tone',logo:'Visible logos',synthetic:'Synthetic materials',delicate:'Delicate pieces'},
      budgets: ['Under $20','$20 to $50','$50 to $120','$120+']
    }
  };

  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  const escapeHtml = value => String(value ?? '').replace(/[&<>'"]/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[character]));
  const labelFor = (map, value) => map[value] || value.replaceAll('-', ' ');
  const overlap = (wanted = [], offered = []) => wanted.filter(value => offered.includes(value));

  const queryDepartment = new URLSearchParams(location.search).get('department');
  let department = configs[queryDepartment] ? queryDepartment : 'perfume';
  let products = [];
  let step = 0;
  let catalogueVisible = 24;
  let profile = {budget:null, types:[], priorities:[], avoid:[]};

  const categoryButtons = $$('[data-department]');
  const catalogueGrid = $('[data-catalogue-grid]');
  const catalogueSearch = $('[data-catalogue-search]');
  const catalogueType = $('[data-catalogue-family]');
  const cataloguePrice = $('[data-catalogue-price]');
  const catalogueCount = $('[data-catalogue-count]');
  const catalogueMore = $('[data-catalogue-more]');
  const form = $('[data-finder-form]');
  const host = $('[data-question-host]');
  const app = $('[data-finder-app]');
  const results = $('[data-results]');
  const resultGrid = $('[data-results-grid]');
  const resultSummary = $('[data-results-summary]');
  const compareHead = $('[data-compare-head]');
  const compareBody = $('[data-compare-body]');
  const status = $('[data-form-status]');
  const back = $('[data-back]');
  const next = $('[data-next]');
  const selectionNote = $('[data-selection-note]');

  const departmentProducts = () => products.filter(product => product.department === department);
  const imageMarkup = (product, eager = false) => {
    const alt = `${product.brand} ${product.name} product on a white background`;
    if (product.imageUrl) {
      return `<img src="${escapeHtml(product.imageUrl)}" width="300" height="300" loading="${eager ? 'eager' : 'lazy'}" decoding="async" alt="${escapeHtml(alt)}">`;
    }
    return `<picture><source srcset="/find/assets/products/${escapeHtml(product.image)}.webp" type="image/webp"><img src="/find/assets/products/${escapeHtml(product.image)}.jpg" width="900" height="900" loading="${eager ? 'eager' : 'lazy'}" decoding="async" alt="${escapeHtml(alt)}"></picture>`;
  };

  const filteredCatalogue = () => {
    const query = (catalogueSearch.value || '').trim().toLowerCase();
    const type = catalogueType.value || '';
    const budget = Number(cataloguePrice.value || 0);
    return departmentProducts().filter(product => {
      const haystack = [product.brand, product.name, ...(product.tags || []), ...(product.types || [])].join(' ').toLowerCase();
      return (!query || haystack.includes(query))
        && (!type || (product.types || []).includes(type))
        && (!budget || !product.priceTier || product.priceTier <= budget);
    });
  };

  const catalogueCard = product => `
    <article class="catalogue-card">
      <a href="${escapeHtml(product.affiliateUrl || product.productUrl)}" target="_blank" rel="sponsored nofollow noopener" data-product-link data-product-id="${escapeHtml(product.id)}">
        <div class="catalogue-image">${imageMarkup(product)}</div>
        <div class="catalogue-copy"><p class="catalogue-brand">${escapeHtml(product.brand)}</p><h3>${escapeHtml(product.name)}</h3><p class="catalogue-meta">View on Amazon ↗</p><ul class="catalogue-notes">${(product.tags || []).slice(0, 2).map(tag => `<li>${escapeHtml(labelFor(configs[department].types, tag))}</li>`).join('')}</ul></div>
      </a>
    </article>`;

  const renderCatalogue = (reset = false) => {
    if (reset) catalogueVisible = 24;
    const filtered = filteredCatalogue();
    const visible = filtered.slice(0, catalogueVisible);
    catalogueGrid.innerHTML = visible.length ? visible.map(catalogueCard).join('') : '<div class="catalogue-empty"><h3>No exact match.</h3><p>Try one fewer filter.</p></div>';
    catalogueCount.textContent = `${filtered.length} products · showing ${visible.length}`;
    catalogueMore.hidden = visible.length >= filtered.length;
    catalogueMore.textContent = `Show ${Math.min(24, filtered.length - visible.length)} more`;
  };

  const choice = (name, value, label, type, checked = false) => `<label><input type="${type}" name="${name}" value="${escapeHtml(value)}"${checked ? ' checked' : ''}><span><b>${escapeHtml(label)}</b></span></label>`;

  const questions = () => {
    const config = configs[department];
    return [
      {key:'budget', eyebrow:'01 · Budget', title:'What feels comfortable?', type:'radio', options:[...config.budgets.map((label,index)=>[String(index+1),label]),['0','Flexible']]},
      {key:'types', eyebrow:`02 · ${config.typeName}`, title:'What are you looking for?', type:'checkbox', max:2, options:Object.entries(config.types)},
      {key:'priorities', eyebrow:'03 · Priorities', title:'What matters most?', type:'checkbox', max:2, options:Object.entries(config.priorities)},
      {key:'avoid', eyebrow:'04 · Avoid', title:'Anything you do not want?', type:'checkbox', exclusive:'nothing', options:[...Object.entries(config.avoid),['nothing','Nothing here']]}
    ];
  };

  const selectedFor = key => key === 'budget' ? profile.budget : profile[key];
  const renderQuestion = () => {
    const question = questions()[step];
    const selected = selectedFor(question.key);
    host.innerHTML = `<fieldset class="finder-step is-active" data-max="${question.max || ''}" data-exclusive="${question.exclusive || ''}"><legend><span>${escapeHtml(question.eyebrow)}</span>${escapeHtml(question.title)}</legend><div class="choice-grid choice-grid--compact">${question.options.map(([value,label]) => choice(question.key, value, label, question.type, question.type === 'radio' ? String(selected) === value : selected.includes(value))).join('')}</div></fieldset>`;
    $$('[data-progress-step]').forEach((item,index)=>item.classList.toggle('is-current',index===step));
    $('[data-progress-number]').textContent = String(step + 1).padStart(2, '0');
    $('[data-progress-bar]').style.width = `${((step + 1) / 4) * 100}%`;
    back.hidden = step === 0;
    next.innerHTML = step === 3 ? 'Show my three <span aria-hidden="true">→</span>' : 'Continue <span aria-hidden="true">→</span>';
    updateControls();
  };

  const currentIsValid = () => {
    const key = questions()[step].key;
    return key === 'budget' ? profile.budget !== null : profile[key].length > 0;
  };

  const updateControls = () => {
    next.disabled = !currentIsValid();
    selectionNote.textContent = next.disabled ? 'Choose an answer.' : step === 3 ? 'Ready.' : 'Good. Continue.';
  };

  form.addEventListener('change', event => {
    const input = event.target.closest('input');
    if (!input) return;
    const question = questions()[step];
    if (question.type === 'radio') {
      profile[question.key] = Number(input.value);
    } else {
      const values = $$(`input[name="${question.key}"]:checked`).map(item=>item.value);
      if (question.exclusive && input.value === question.exclusive && input.checked) {
        profile[question.key] = [question.exclusive];
      } else {
        profile[question.key] = values.filter(value=>value !== question.exclusive).slice(0, question.max || values.length);
      }
      renderQuestion();
      return;
    }
    updateControls();
  });

  const scoreProduct = product => {
    const typeMatches = overlap(profile.types, product.types || []);
    const priorityMatches = overlap(profile.priorities, product.priorities || []);
    const conflicts = overlap(profile.avoid.filter(value=>value!=='nothing'), product.avoid || product.traits || []);
    let score = 10 + typeMatches.length * 6 + priorityMatches.length * 3 - conflicts.length * 9;
    if (profile.budget === 0 || !product.priceTier) score += 1;
    else if (product.priceTier <= profile.budget) score += 4 - Math.max(0, profile.budget - product.priceTier) * .4;
    else score -= (product.priceTier - profile.budget) * 4;
    return {product,score,typeMatches,priorityMatches,conflicts};
  };

  const reasonsFor = item => {
    const config = configs[department];
    const parts = [];
    if (item.typeMatches.length) parts.push(labelFor(config.types,item.typeMatches[0]));
    if (item.priorityMatches.length) parts.push(labelFor(config.priorities,item.priorityMatches[0]));
    if (!item.conflicts.length) parts.push('no selected deal-breaker');
    return `Matched for ${parts.slice(0,2).join(' and ') || 'overall fit'}.`;
  };

  const resultCard = (item,index) => {
    const product = item.product;
    return `<article class="result-card${index===0?' result-card--first':''}"><div class="result-image">${imageMarkup(product,index===0)}<span class="result-rank">0${index+1}</span><span class="result-fit">${item.fit}% fit</span></div><div class="result-copy"><p class="brand">${escapeHtml(product.brand)}${index===0?' · Closest match':''}</p><h3>${escapeHtml(product.name)}</h3><p class="result-summary">${escapeHtml(reasonsFor(item))}</p><ul class="result-notes">${(product.tags||[]).slice(0,3).map(tag=>`<li>${escapeHtml(labelFor(configs[department].types,tag))}</li>`).join('')}</ul><a class="button button--wine result-shop" href="${escapeHtml(product.affiliateUrl || product.productUrl)}" target="_blank" rel="sponsored nofollow noopener" data-product-link data-product-id="${escapeHtml(product.id)}">View on Amazon <span aria-hidden="true">↗</span></a></div></article>`;
  };

  const renderResults = (scroll = true) => {
    const ranked = departmentProducts().map(scoreProduct).sort((a,b)=>b.score-a.score || (b.product.reviewCount||0)-(a.product.reviewCount||0));
    const low = Math.min(...ranked.map(item=>item.score));
    const high = Math.max(...ranked.map(item=>item.score));
    ranked.forEach(item=>{ item.fit=Math.round(72+((item.score-low)/Math.max(1,high-low))*24); if(item.conflicts.length)item.fit=Math.min(item.fit,82); });
    const shortlist=[];
    for(const item of ranked){ if(!shortlist.some(chosen=>chosen.product.brand.toLowerCase()===item.product.brand.toLowerCase()))shortlist.push(item); if(shortlist.length===3)break; }
    resultGrid.innerHTML=shortlist.map(resultCard).join('');
    const config=configs[department];
    $('[data-results-title]').textContent=`Three ${config.plural} to consider.`;
    resultSummary.textContent=`Based on ${profile.types.map(value=>labelFor(config.types,value)).join(' and ')}.`;
    compareHead.innerHTML=`<tr><th scope="col">Compare</th>${shortlist.map(item=>`<th scope="col">${escapeHtml(item.product.brand)}<br>${escapeHtml(item.product.name)}</th>`).join('')}</tr>`;
    const rows=[['Fit',...shortlist.map(item=>`${item.fit}% match`)],['Type',...shortlist.map(item=>(item.product.types||[]).map(value=>labelFor(config.types,value)).join(', '))],['Price',...shortlist.map(item=>item.product.priceLabel)],['Watch for',...shortlist.map(item=>item.conflicts.length?item.conflicts.map(value=>labelFor(config.avoid,value)).join(', '):'No selected conflict')]];
    compareBody.innerHTML=rows.map(row=>`<tr><td>${escapeHtml(row[0])}</td>${row.slice(1).map(value=>`<td>${escapeHtml(value)}</td>`).join('')}</tr>`).join('');
    app.hidden=true; results.hidden=false;
    const encoded=btoa(unescape(encodeURIComponent(JSON.stringify({department,profile})))).replaceAll('+','-').replaceAll('/','_').replaceAll('=','');
    history.replaceState(null,'',`${location.pathname}?department=${department}#profile=${encoded}`);
    if(scroll)results.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
  };

  const resetFinder = () => {
    step=0; profile={budget:null,types:[],priorities:[],avoid:[]}; results.hidden=true; app.hidden=false; renderQuestion();
  };

  const setDepartment = (nextDepartment, scroll = true) => {
    if(!configs[nextDepartment])return;
    department=nextDepartment; catalogueSearch.value=''; cataloguePrice.value=''; catalogueVisible=24;
    const config=configs[department];
    categoryButtons.forEach(button=>{ const active=button.dataset.department===department; button.classList.toggle('category-card--active',active); button.setAttribute('aria-pressed',String(active)); });
    $('[data-catalogue-kicker]').textContent=`The ${config.name.toLowerCase()} library`;
    $('[data-catalogue-title]').textContent=`Browse ${departmentProducts().length} ${config.plural}.`;
    $('[data-catalogue-deck]').textContent='Search or filter, then open any product on Amazon.';
    catalogueSearch.placeholder=config.search;
    $('[data-type-filter-label]').textContent=config.typeName;
    catalogueType.innerHTML=`<option value="">All types</option>${Object.entries(config.types).map(([value,label])=>`<option value="${escapeHtml(value)}">${escapeHtml(label)}</option>`).join('')}`;
    $('[data-finder-kicker]').textContent=`${config.kicker} · Quick edit`;
    $('[data-finder-title]').textContent=`Find your three ${config.plural}.`;
    $('[data-finder-deck]').textContent='Four simple choices. About one minute.';
    history.replaceState(null,'',`${location.pathname}?department=${department}`);
    resetFinder(); renderCatalogue(true);
    if(scroll)$('#product-database').scrollIntoView({behavior:'smooth',block:'start'});
  };

  categoryButtons.forEach(button=>button.addEventListener('click',()=>setDepartment(button.dataset.department)));
  [catalogueSearch,catalogueType,cataloguePrice].forEach(control=>control.addEventListener(control===catalogueSearch?'input':'change',()=>renderCatalogue(true)));
  catalogueMore.addEventListener('click',()=>{catalogueVisible+=24;renderCatalogue();});
  next.addEventListener('click',()=>{ if(!currentIsValid())return; if(step<3){step+=1;renderQuestion();}else renderResults(); });
  back.addEventListener('click',()=>{if(step>0){step-=1;renderQuestion();}});
  $('[data-refine]')?.addEventListener('click',()=>{results.hidden=true;app.hidden=false;step=0;renderQuestion();app.scrollIntoView({behavior:'smooth',block:'start'});});
  $('[data-restart]')?.addEventListener('click',()=>{resetFinder();history.replaceState(null,'',`${location.pathname}?department=${department}#finder`);app.scrollIntoView({behavior:'smooth',block:'start'});});
  $('[data-copy-results]')?.addEventListener('click',async event=>{const button=event.currentTarget,original=button.textContent;try{await navigator.clipboard.writeText(location.href);button.textContent='Link copied';}catch{button.textContent='Copy unavailable';}setTimeout(()=>button.textContent=original,1800);});
  document.addEventListener('click',event=>{const link=event.target.closest('[data-product-link]');if(!link)return;const product=products.find(item=>item.id===link.dataset.productId);if(typeof window.gtag==='function'&&product)window.gtag('event','amazon_product_click',{item_name:product.name,item_brand:product.brand,item_category:product.department});});

  const restoreProfile = () => {
    if(!location.hash.startsWith('#profile='))return false;
    try {
      const value=location.hash.slice(9).replaceAll('-','+').replaceAll('_','/');
      const decoded=decodeURIComponent(escape(atob(value+'='.repeat((4-value.length%4)%4))));
      const saved=JSON.parse(decoded);
      if(!configs[saved.department])return false;
      department=saved.department; profile=saved.profile; return true;
    } catch { return false; }
  };

  const load = async () => {
    try {
      const response=await fetch('/find/products.json',{cache:'no-cache'});
      if(!response.ok)throw new Error(`Product database returned ${response.status}`);
      products=await response.json();
      const restored=restoreProfile();
      const restoredProfile=restored?profile:null;
      setDepartment(department,false);
      if(restored){profile=restoredProfile;renderQuestion();renderResults(false);}
      $('[data-source-list]').innerHTML='<p>Perfume images use credited brand photography. Other product images are served by Amazon for identification.</p>';
    } catch(error){status.textContent='The product finder could not load. Please refresh the page.';next.disabled=true;console.error(error);}
  };

  load();
})();
