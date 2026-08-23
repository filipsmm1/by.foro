(() => {
  const app = document.querySelector('[data-finder-app]');
  const form = document.querySelector('[data-finder-form]');
  if (!app || !form) return;

  const steps = [...form.querySelectorAll('[data-step]')];
  const progressSteps = [...document.querySelectorAll('[data-progress-step]')];
  const back = form.querySelector('[data-back]');
  const next = form.querySelector('[data-next]');
  const note = form.querySelector('[data-selection-note]');
  const status = form.querySelector('[data-form-status]');
  const progressNumber = document.querySelector('[data-progress-number]');
  const progressBar = document.querySelector('[data-progress-bar]');
  const results = document.querySelector('[data-results]');
  const resultGrid = document.querySelector('[data-results-grid]');
  const resultSummary = document.querySelector('[data-results-summary]');
  const compareHead = document.querySelector('[data-compare-head]');
  const compareBody = document.querySelector('[data-compare-body]');
  const sourceList = document.querySelector('[data-source-list]');

  const familyLabels = {
    'skin-musk': 'skin musk',
    'fresh-citrus': 'fresh citrus',
    'floral-powdery': 'floral and powdery',
    'green-woody': 'green and woody',
    'gourmand-vanilla': 'gourmand vanilla',
    'amber-spicy': 'amber and spice'
  };
  const intensityLabels = { intimate: 'intimate', balanced: 'balanced', noticeable: 'noticeable' };
  const occasionLabels = {
    everyday: 'everyday wear', office: 'the office', date: 'dates', evening: 'evenings',
    'warm-weather': 'warm weather', 'cold-weather': 'cold weather', versatile: 'mixed settings'
  };
  const textureLabels = { clean: 'clean', creamy: 'creamy', dry: 'dry', juicy: 'juicy', powdery: 'powdery', smoky: 'smoky' };
  const priorityLabels = {
    longevity: 'longevity', subtlety: 'subtlety', uniqueness: 'distinctiveness', versatility: 'versatility',
    compliments: 'presence', layering: 'layering', comfort: 'comfort'
  };

  let products = [];
  let current = 0;

  const escapeHtml = value => String(value).replace(/[&<>'"]/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  })[character]);
  const selected = name => [...form.querySelectorAll(`input[name="${name}"]:checked`)].map(input => input.value);
  const one = name => form.querySelector(`input[name="${name}"]:checked`)?.value || '';
  const answers = () => ({
    budget: Number(one('budget')),
    families: selected('families'),
    intensity: one('intensity'),
    occasions: selected('occasions'),
    textures: selected('textures'),
    avoid: selected('avoid').filter(value => value !== 'nothing'),
    priorities: selected('priorities')
  });

  const stepSelection = index => {
    const fieldset = steps[index];
    return [...fieldset.querySelectorAll('input:checked')];
  };

  const updateControls = () => {
    const count = stepSelection(current).length;
    next.disabled = count === 0 || products.length === 0;
    back.hidden = current === 0;
    next.innerHTML = current === steps.length - 1
      ? 'Build my shortlist <span aria-hidden="true">→</span>'
      : 'Continue <span aria-hidden="true">→</span>';
    const max = Number(steps[current].querySelector('[data-max]')?.dataset.max || 0);
    note.textContent = count
      ? `${count} selected${max ? ` · up to ${max}` : ''}`
      : `Choose ${steps[current].querySelector('input[type="radio"]') ? 'one answer' : 'at least one'} to continue.`;
    progressNumber.textContent = String(current + 1).padStart(2, '0');
    progressBar.style.width = `${((current + 1) / steps.length) * 100}%`;
    progressSteps.forEach((item, index) => {
      item.classList.toggle('is-current', index === current);
      item.classList.toggle('is-complete', index < current);
    });
  };

  const showStep = (index, focus = true) => {
    current = Math.max(0, Math.min(index, steps.length - 1));
    steps.forEach((step, stepIndex) => {
      const active = stepIndex === current;
      step.hidden = !active;
      step.classList.toggle('is-active', active);
    });
    status.textContent = '';
    updateControls();
    if (focus) steps[current].querySelector('legend')?.focus?.();
  };

  const enforceChoiceRules = input => {
    const grid = input.closest('[data-max], [data-exclusive]');
    if (!grid) return;
    if (grid.dataset.exclusive) {
      const options = [...grid.querySelectorAll('input')];
      const exclusive = options.find(option => option.value === grid.dataset.exclusive);
      if (input === exclusive && input.checked) options.filter(option => option !== input).forEach(option => { option.checked = false; });
      if (input !== exclusive && input.checked && exclusive) exclusive.checked = false;
    }
    const max = Number(grid.dataset.max || 0);
    const checked = [...grid.querySelectorAll('input:checked')];
    if (max && checked.length > max) {
      input.checked = false;
      status.textContent = `Choose up to ${max} answers for this question.`;
      window.setTimeout(() => { if (status.textContent.startsWith('Choose up to')) status.textContent = ''; }, 2200);
    }
  };

  form.addEventListener('change', event => {
    if (!(event.target instanceof HTMLInputElement)) return;
    enforceChoiceRules(event.target);
    updateControls();
  });
  form.addEventListener('submit', event => event.preventDefault());
  back.addEventListener('click', () => showStep(current - 1));
  next.addEventListener('click', () => {
    if (!stepSelection(current).length) {
      status.textContent = 'Choose an answer before continuing.';
      return;
    }
    if (current < steps.length - 1) showStep(current + 1);
    else renderResults();
  });

  const overlap = (left, right) => left.filter(value => right.includes(value));
  const scoreProduct = (product, profile) => {
    let score = 8;
    const matches = {
      families: overlap(profile.families, product.families),
      occasions: overlap(profile.occasions, product.occasions),
      textures: overlap(profile.textures, product.textures),
      priorities: overlap(profile.priorities, product.priorities),
      conflicts: overlap(profile.avoid, product.traits)
    };

    if (profile.budget === 0) score += 2;
    else if (product.priceTier <= profile.budget) score += 4 - Math.max(0, profile.budget - product.priceTier) * .35;
    else score -= (product.priceTier - profile.budget) * 4;

    score += matches.families.length * 4;
    const intensityDistance = Math.abs(['intimate', 'balanced', 'noticeable'].indexOf(profile.intensity) - ['intimate', 'balanced', 'noticeable'].indexOf(product.intensity));
    score += intensityDistance === 0 ? 3.5 : intensityDistance === 1 ? 1 : -2;
    score += matches.occasions.length * 1.7;
    if (profile.occasions.includes('versatile') && product.occasions.includes('versatile')) score += 2;
    score += matches.textures.length * 1.5;
    score += matches.priorities.length * 1.6;
    score -= matches.conflicts.length * 7;
    return { product, score, matches, overBudget: profile.budget > 0 && product.priceTier > profile.budget };
  };

  const reasonsFor = item => {
    const profile = answers();
    const reasons = [];
    if (item.matches.families.length) reasons.push(`Your ${item.matches.families.slice(0, 2).map(value => familyLabels[value]).join(' + ')} direction`);
    if (item.product.intensity === profile.intensity) reasons.push(`${intensityLabels[profile.intensity]} projection`);
    if (item.matches.occasions.length) reasons.push(`Suited to ${item.matches.occasions.slice(0, 2).map(value => occasionLabels[value]).join(' and ')}`);
    if (item.matches.textures.length) reasons.push(`${item.matches.textures.slice(0, 2).map(value => textureLabels[value]).join(', ')} texture`);
    if (item.matches.priorities.length) reasons.push(`Supports ${item.matches.priorities.slice(0, 2).map(value => priorityLabels[value]).join(' and ')}`);
    if (!item.matches.conflicts.length) reasons.push('No selected deal-breakers detected');
    if (item.overBudget) reasons.push('A stretch above your full-bottle budget');
    return reasons.slice(0, 4);
  };

  const productCard = (item, index) => {
    const product = item.product;
    const destination = product.affiliateUrl || product.productUrl;
    const affiliate = Boolean(product.affiliateUrl);
    const rel = affiliate ? 'sponsored nofollow noopener' : 'nofollow noopener';
    const label = affiliate ? 'Shop via partner' : 'View official product';
    const reasons = reasonsFor(item);
    return `
      <article class="result-card${index === 0 ? ' result-card--first' : ''}">
        <div class="result-image">
          <picture><source srcset="/find/assets/products/${escapeHtml(product.image)}.webp" type="image/webp"><img src="/find/assets/products/${escapeHtml(product.image)}.jpg" width="900" height="900" loading="${index ? 'lazy' : 'eager'}" alt="${escapeHtml(product.brand)} ${escapeHtml(product.name)} perfume bottle in official product photography"></picture>
          <span class="result-rank">0${index + 1}</span><span class="result-fit">${item.fit}% fit</span>
        </div>
        <div class="result-copy">
          <p class="brand">${escapeHtml(product.brand)}${index === 0 ? ' · Closest match' : ''}</p>
          <h3>${escapeHtml(product.name)}</h3>
          <div class="result-meta"><span>${escapeHtml(product.concentration)}</span><span>·</span><span>${escapeHtml(product.priceLabel)}</span></div>
          <p class="result-summary">${escapeHtml(product.summary)}</p>
          <div class="match-reasons"><strong>Why it matched</strong><ul>${reasons.map(reason => `<li>${escapeHtml(reason)}</li>`).join('')}</ul></div>
          <ul class="result-notes" aria-label="Key notes">${product.notes.slice(0, 5).map(note => `<li>${escapeHtml(note)}</li>`).join('')}</ul>
          <p class="sample-advice"><strong>Before buying:</strong> ${escapeHtml(product.sampleAdvice)}</p>
          <a class="button button--wine result-shop" href="${escapeHtml(destination)}" target="_blank" rel="${rel}" data-product-link data-product-id="${escapeHtml(product.id)}" data-affiliate="${affiliate}">${label} <span aria-hidden="true">↗</span></a>
          <p class="result-source">Photo: ${escapeHtml(product.imageCredit)} · <a href="${escapeHtml(product.sourceImageUrl)}" target="_blank" rel="nofollow noopener">source</a></p>
        </div>
      </article>`;
  };

  const compare = shortlist => {
    compareHead.innerHTML = `<tr><th scope="col">Compare</th>${shortlist.map(item => `<th scope="col">${escapeHtml(item.product.brand)}<br>${escapeHtml(item.product.name)}</th>`).join('')}</tr>`;
    const rows = [
      ['Fit', ...shortlist.map(item => `${item.fit}% questionnaire fit`)],
      ['Price', ...shortlist.map(item => item.product.priceLabel)],
      ['Direction', ...shortlist.map(item => item.product.families.map(value => familyLabels[value]).join(', '))],
      ['Projection', ...shortlist.map(item => intensityLabels[item.product.intensity])],
      ['Best reason', ...shortlist.map(item => reasonsFor(item)[0] || 'Balanced overall fit')],
      ['Watch for', ...shortlist.map(item => item.matches.conflicts.length ? `Contains ${item.matches.conflicts.join(', ')}` : item.overBudget ? 'Above chosen budget' : 'No selected deal-breakers')]
    ];
    compareBody.innerHTML = rows.map(row => `<tr><td>${escapeHtml(row[0])}</td>${row.slice(1).map(value => `<td>${escapeHtml(value)}</td>`).join('')}</tr>`).join('');
  };

  const encodeProfile = profile => {
    const compact = [profile.budget, profile.families, profile.intensity, profile.occasions, profile.textures, profile.avoid, profile.priorities];
    const bytes = new TextEncoder().encode(JSON.stringify(compact));
    let binary = '';
    bytes.forEach(byte => { binary += String.fromCharCode(byte); });
    return btoa(binary).replaceAll('+', '-').replaceAll('/', '_').replaceAll('=', '');
  };
  const decodeProfile = value => {
    try {
      const normalised = value.replaceAll('-', '+').replaceAll('_', '/');
      const binary = atob(normalised + '='.repeat((4 - normalised.length % 4) % 4));
      const bytes = Uint8Array.from(binary, character => character.charCodeAt(0));
      const data = JSON.parse(new TextDecoder().decode(bytes));
      return { budget: Number(data[0]), families: data[1], intensity: data[2], occasions: data[3], textures: data[4], avoid: data[5], priorities: data[6] };
    } catch { return null; }
  };

  const renderResults = (scroll = true) => {
    const profile = answers();
    const ranked = products.map(product => scoreProduct(product, profile)).sort((a, b) => b.score - a.score || a.product.id.localeCompare(b.product.id));
    const scores = ranked.map(item => item.score);
    const low = Math.min(...scores);
    const high = Math.max(...scores);
    ranked.forEach(item => {
      item.fit = Math.round(72 + ((item.score - low) / Math.max(1, high - low)) * 24);
      if (item.matches.conflicts.length) item.fit = Math.min(item.fit, 84);
    });
    const shortlist = ranked.slice(0, 3);
    resultGrid.innerHTML = shortlist.map(productCard).join('');
    compare(shortlist);
    resultSummary.textContent = `Built from ${profile.families.map(value => familyLabels[value]).join(', ')}, ${intensityLabels[profile.intensity]} projection and ${profile.avoid.length ? `${profile.avoid.length} deal-breaker${profile.avoid.length === 1 ? '' : 's'}` : 'no scent exclusions'}.`;
    app.hidden = true;
    results.hidden = false;
    history.replaceState(null, '', `${location.pathname}${location.search}#profile=${encodeProfile(profile)}`);
    if (scroll) results.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
    results.querySelector('h2')?.setAttribute('tabindex', '-1');
    results.querySelector('h2')?.focus({ preventScroll: true });
  };

  const applyProfile = profile => {
    form.reset();
    const setOne = (name, value) => { const input = form.querySelector(`input[name="${name}"][value="${CSS.escape(String(value))}"]`); if (input) input.checked = true; };
    const setMany = (name, values) => (Array.isArray(values) ? values : []).forEach(value => setOne(name, value));
    setOne('budget', profile.budget);
    setMany('families', profile.families);
    setOne('intensity', profile.intensity);
    setMany('occasions', profile.occasions);
    setMany('textures', profile.textures);
    setMany('avoid', profile.avoid?.length ? profile.avoid : ['nothing']);
    setMany('priorities', profile.priorities);
  };

  document.querySelector('[data-refine]')?.addEventListener('click', () => {
    results.hidden = true;
    app.hidden = false;
    showStep(0, false);
    app.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  document.querySelector('[data-restart]')?.addEventListener('click', () => {
    form.reset();
    results.hidden = true;
    app.hidden = false;
    history.replaceState(null, '', `${location.pathname}${location.search}#finder`);
    showStep(0, false);
    app.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
  document.querySelector('[data-copy-results]')?.addEventListener('click', async event => {
    const button = event.currentTarget;
    const original = button.textContent;
    try {
      await navigator.clipboard.writeText(location.href);
      button.textContent = 'Result link copied';
    } catch { button.textContent = 'Copy unavailable'; }
    window.setTimeout(() => { button.textContent = original; }, 2200);
  });
  document.addEventListener('click', event => {
    const link = event.target.closest('[data-product-link]');
    if (!link) return;
    const product = products.find(item => item.id === link.dataset.productId);
    if (typeof window.gtag === 'function' && product) {
      window.gtag('event', link.dataset.affiliate === 'true' ? 'affiliate_click' : 'product_click', {
        item_name: product.name,
        item_brand: product.brand,
        destination_type: link.dataset.affiliate === 'true' ? 'affiliate' : 'official'
      });
    }
  });

  const load = async () => {
    try {
      const response = await fetch('/find/products.json', { cache: 'no-cache' });
      if (!response.ok) throw new Error(`Product database returned ${response.status}`);
      products = await response.json();
      sourceList.innerHTML = products.map(product => `<a href="${escapeHtml(product.sourceImageUrl)}" target="_blank" rel="nofollow noopener">${escapeHtml(product.brand)} ${escapeHtml(product.name)} · ${escapeHtml(product.imageCredit)}</a>`).join('');
      updateControls();
      const profilePart = location.hash.startsWith('#profile=') ? location.hash.slice(9) : '';
      const profile = profilePart ? decodeProfile(profilePart) : null;
      if (profile) {
        applyProfile(profile);
        renderResults(false);
      }
    } catch (error) {
      status.textContent = 'The product edit could not load. Please refresh the page.';
      next.disabled = true;
      console.error(error);
    }
  };

  showStep(0, false);
  load();
})();
