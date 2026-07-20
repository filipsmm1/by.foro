(()=>{
  const library=document.querySelector('[data-journal-library]');
  if(!library)return;
  const search=library.querySelector('[data-journal-search]');
  const clear=library.querySelector('[data-journal-clear]');
  const status=library.querySelector('[data-journal-status]');
  const cards=[...document.querySelectorAll('[data-journal-results] .story-card')];
  const empty=document.querySelector('[data-journal-empty]');
  const reset=document.querySelector('[data-journal-reset]');
  const departmentButtons=[...library.querySelectorAll('[data-department]')];
  const topicButtons=[...library.querySelectorAll('[data-topic]')];
  const allowedDepartments=new Set(departmentButtons.map(button=>button.dataset.department));
  const allowedTopics=new Set(topicButtons.map(button=>button.dataset.topic));
  const params=new URLSearchParams(location.search);
  let department=allowedDepartments.has(params.get('department'))?params.get('department'):'all';
  let topic=allowedTopics.has(params.get('topic'))?params.get('topic'):'all';
  search.value=params.get('q')||'';

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
  const updateUrl=()=>{
    const next=new URLSearchParams();
    const query=search.value.trim();
    if(department!=='all')next.set('department',department);
    if(topic!=='all')next.set('topic',topic);
    if(query)next.set('q',query);
    const suffix=next.toString()?`?${next}`:'';
    history.replaceState(null,'',`${location.pathname}${suffix}`);
  };
  const apply=()=>{
    syncTopicVisibility();
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
    clear.hidden=!search.value;
    empty.hidden=visible!==0;
    const detail=[];
    if(department!=='all')detail.push(department.charAt(0).toUpperCase()+department.slice(1));
    if(topic!=='all')detail.push(topicButtons.find(button=>button.dataset.topic===topic)?.childNodes[0]?.textContent?.trim()||topic);
    if(query)detail.push(`“${search.value.trim()}”`);
    status.textContent=`Showing ${visible} of ${cards.length} ${cards.length===1?'story':'stories'}${detail.length?` · ${detail.join(' · ')}`:''}`;
    updateUrl();
  };
  departmentButtons.forEach(button=>button.addEventListener('click',()=>{department=button.dataset.department;apply()}));
  topicButtons.forEach(button=>button.addEventListener('click',()=>{topic=button.dataset.topic;apply()}));
  search.addEventListener('input',apply);
  clear.addEventListener('click',()=>{search.value='';search.focus();apply()});
  reset?.addEventListener('click',()=>{department='all';topic='all';search.value='';apply();library.scrollIntoView({behavior:'smooth',block:'start'})});
  apply();
})();
