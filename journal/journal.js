(()=>{
  const library=document.querySelector('[data-journal-library]');
  if(!library)return;

  const search=library.querySelector('[data-journal-search]');
  const clear=library.querySelector('[data-journal-clear]');
  const sort=library.querySelector('[data-journal-sort]');
  const status=library.querySelector('[data-journal-status]');
  const results=document.querySelector('[data-journal-results]');
  const cards=[...results.querySelectorAll('.story-card')];
  const empty=document.querySelector('[data-journal-empty]');
  const reset=document.querySelector('[data-journal-reset]');
  const departmentButtons=[...library.querySelectorAll('[data-department]')];
  const topicButtons=[...library.querySelectorAll('[data-topic]')];
  const queryButtons=[...library.querySelectorAll('[data-journal-query]')];
  const topicDisclosure=library.querySelector('.journal-topic-disclosure');
  const allowedDepartments=new Set(departmentButtons.map(button=>button.dataset.department));
  const allowedTopics=new Set(topicButtons.map(button=>button.dataset.topic));
  const params=new URLSearchParams(location.search);
  let department=allowedDepartments.has(params.get('department'))?params.get('department'):'all';
  let topic=allowedTopics.has(params.get('topic'))?params.get('topic'):'all';
  if(topic!=='all'&&topicDisclosure)topicDisclosure.open=true;
  search.value=params.get('q')||'';
  if(sort&&['newest','longest','shortest','az'].includes(params.get('sort')))sort.value=params.get('sort');

  const normalise=value=>value.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').trim();
  const topicFitsDepartment=value=>{
    if(value==='all')return true;
    const button=topicButtons.find(item=>item.dataset.topic===value);
    return department==='all'||button?.dataset.departments?.split(' ').includes(department);
  };
  const syncTopicVisibility=()=>{
    topicButtons.forEach(button=>{
      if(button.dataset.topic==='all'){button.hidden=false;return}
      const belongs=button.dataset.departments?.split(' ').includes(department);
      button.hidden=department==='all'?button.dataset.hasStories!=='true':!belongs;
    });
    if(!topicFitsDepartment(topic))topic='all';
  };
  const orderedCards=()=>{
    const mode=sort?.value||'newest';
    return [...cards].sort((a,b)=>{
      if(mode==='longest')return Number(b.dataset.minutes||0)-Number(a.dataset.minutes||0);
      if(mode==='shortest')return Number(a.dataset.minutes||0)-Number(b.dataset.minutes||0);
      if(mode==='az')return (a.dataset.title||'').localeCompare(b.dataset.title||'');
      return (b.dataset.date||'').localeCompare(a.dataset.date||'');
    });
  };
  const updateUrl=()=>{
    const next=new URLSearchParams();
    const query=search.value.trim();
    if(department!=='all')next.set('department',department);
    if(topic!=='all')next.set('topic',topic);
    if(query)next.set('q',query);
    if(sort?.value&&sort.value!=='newest')next.set('sort',sort.value);
    const suffix=next.toString()?`?${next}`:'';
    history.replaceState(null,'',`${location.pathname}${suffix}`);
  };
  const apply=()=>{
    syncTopicVisibility();
    orderedCards().forEach(card=>results.append(card));
    const query=normalise(search.value);
    let visible=0;
    cards.forEach(card=>{
      const matchesDepartment=department==='all'||card.dataset.department===department;
      const matchesTopic=topic==='all'||card.dataset.topic===topic;
      const haystack=normalise(`${card.dataset.search||''} ${card.textContent||''}`);
      const matchesSearch=!query||query.split(/\s+/).every(term=>haystack.includes(term));
      const show=matchesDepartment&&matchesTopic&&matchesSearch;
      card.hidden=!show;
      if(show)visible+=1;
    });
    departmentButtons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.department===department)));
    topicButtons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.topic===topic)));
    queryButtons.forEach(button=>button.setAttribute('aria-pressed',String(search.value.trim().toLowerCase()===button.dataset.journalQuery)));
    clear.hidden=!search.value;
    empty.hidden=visible!==0;
    const detail=[];
    if(department!=='all')detail.push(department.charAt(0).toUpperCase()+department.slice(1));
    if(topic!=='all')detail.push(topicButtons.find(button=>button.dataset.topic===topic)?.childNodes[0]?.textContent?.trim()||topic);
    if(query)detail.push(`"${search.value.trim()}"`);
    if(sort?.value&&sort.value!=='newest')detail.push(sort.options[sort.selectedIndex].text);
    status.textContent=`Showing ${visible} of ${cards.length} ${cards.length===1?'story':'stories'}${detail.length?` · ${detail.join(' · ')}`:''}`;
    updateUrl();
  };
  departmentButtons.forEach(button=>button.addEventListener('click',()=>{department=button.dataset.department;apply()}));
  topicButtons.forEach(button=>button.addEventListener('click',()=>{topic=button.dataset.topic;if(topic!=='all'&&topicDisclosure)topicDisclosure.open=true;apply()}));
  queryButtons.forEach(button=>button.addEventListener('click',()=>{search.value=button.dataset.journalQuery;search.focus();apply()}));
  search.addEventListener('input',apply);
  sort?.addEventListener('change',apply);
  clear.addEventListener('click',()=>{search.value='';search.focus();apply()});
  reset?.addEventListener('click',()=>{department='all';topic='all';search.value='';if(sort)sort.value='newest';apply();library.scrollIntoView({behavior:'smooth',block:'start'})});
  apply();
})();
