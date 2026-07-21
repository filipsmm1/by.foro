
const root=document.documentElement;root.classList.add('reveal-ready');
const header=document.querySelector('[data-header]');const toggle=document.querySelector('.menu-toggle');const nav=document.querySelector('.site-nav');
let menuReturnFocus=null;
const menuFocusable=()=>[toggle,...nav.querySelectorAll('a[href],button:not([disabled])')].filter(Boolean);
const closeMenu=(restoreFocus=false)=>{if(!nav||!toggle)return;const wasOpen=nav.classList.contains('is-open');nav.classList.remove('is-open');document.body.classList.remove('menu-open');toggle.setAttribute('aria-expanded','false');toggle.querySelector('span').textContent='Menu';if(wasOpen&&restoreFocus)(menuReturnFocus||toggle).focus()};
const openMenu=()=>{if(!nav||!toggle)return;menuReturnFocus=document.activeElement;nav.classList.add('is-open');document.body.classList.add('menu-open');toggle.setAttribute('aria-expanded','true');toggle.querySelector('span').textContent='Close';requestAnimationFrame(()=>nav.querySelector('a')?.focus())};
if(toggle&&nav){toggle.addEventListener('click',()=>nav.classList.contains('is-open')?closeMenu(true):openMenu());nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>closeMenu(false)));document.addEventListener('keydown',e=>{if(!nav.classList.contains('is-open'))return;if(e.key==='Escape'){e.preventDefault();closeMenu(true);return}if(e.key!=='Tab')return;const items=menuFocusable();const first=items[0];const last=items.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}});window.matchMedia('(min-width: 1081px)').addEventListener('change',event=>{if(event.matches)closeMenu(false)})}
const onScroll=()=>header?.classList.toggle('is-scrolled',window.scrollY>24);onScroll();window.addEventListener('scroll',onScroll,{passive:true});
const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;const reveals=document.querySelectorAll('[data-reveal]');if(reduce||!('IntersectionObserver'in window)){reveals.forEach(x=>x.classList.add('is-visible'))}else{const io=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px'});reveals.forEach(x=>io.observe(x))}
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
const setTemporaryLabel=(button,label)=>{const original=button.textContent;button.textContent=label;window.setTimeout(()=>button.textContent=original,2200)};
document.querySelectorAll('[data-copy-link]').forEach(btn=>btn.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(location.href);setTemporaryLabel(btn,'Link copied')}catch{setTemporaryLabel(btn,'Copy failed')}}));
document.querySelectorAll('[data-share-story]').forEach(btn=>btn.addEventListener('click',async()=>{const shareData={title:btn.dataset.shareTitle||document.title,url:location.href};try{if(navigator.share){await navigator.share(shareData)}else{await navigator.clipboard.writeText(location.href);setTemporaryLabel(btn,'Link copied')}}catch(error){if(error?.name!=='AbortError')setTemporaryLabel(btn,'Share unavailable')}}));
async function submitForm(form){const status=form.querySelector('.form-status');const button=form.querySelector('button[type=submit]');const original=button?.textContent;if(form.querySelector('input[name=_honey]')?.value)return;button&&(button.disabled=true,button.textContent='Sending…');status&&(status.textContent='');try{const endpoint=form.action.replace('formsubmit.co/','formsubmit.co/ajax/');const response=await fetch(endpoint,{method:'POST',headers:{Accept:'application/json'},body:new FormData(form)});if(!response.ok)throw new Error('Submission failed');form.reset();status&&(status.textContent=form.dataset.formKind==='newsletter'?"Your request is in. We'll email you when the first issue is ready.":'Thank you. Your message has been sent.')}catch(error){status&&(status.innerHTML='The form could not send. Email <a href="mailto:hello@byforo.com">hello@byforo.com</a> instead.')}finally{button&&(button.disabled=false,button.textContent=original)}}
document.querySelectorAll('[data-ajax-form]').forEach(form=>form.addEventListener('submit',e=>{e.preventDefault();if(form.reportValidity())submitForm(form)}));

// Cookie consent. Optional scripts must use type="text/plain" and
// data-cookie-category="optional"; they are activated only after acceptance.
(()=>{
  const cookieName='byforo_cookie_consent';
  const maxAge=60*60*24*180;
  const googleAnalyticsId='G-NG228C73TN';
  const readChoice=()=>document.cookie.split('; ').find(row=>row.startsWith(`${cookieName}=`))?.split('=')[1]||null;
  const writeChoice=choice=>{document.cookie=`${cookieName}=${choice}; Max-Age=${maxAge}; Path=/; SameSite=Lax; Secure`};
  const activateOptionalScripts=()=>document.querySelectorAll('script[type="text/plain"][data-cookie-category="optional"]').forEach(blocked=>{
    if(blocked.dataset.cookieActivated)return;
    const script=document.createElement('script');
    [...blocked.attributes].forEach(({name,value})=>{if(!['type','data-cookie-category'].includes(name))script.setAttribute(name,value)});
    script.text=blocked.textContent;
    blocked.dataset.cookieActivated='true';
    blocked.after(script);
  });
  const activateGoogleAnalytics=()=>{
    if(document.querySelector(`script[data-google-analytics="${googleAnalyticsId}"]`))return;
    window.dataLayer=window.dataLayer||[];
    window.gtag=window.gtag||function(){window.dataLayer.push(arguments)};
    window.gtag('js',new Date());
    window.gtag('config',googleAnalyticsId,{anonymize_ip:true});
    const script=document.createElement('script');
    script.async=true;
    script.src=`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(googleAnalyticsId)}`;
    script.dataset.googleAnalytics=googleAnalyticsId;
    document.head.append(script);
  };
  const announce=choice=>{
    document.documentElement.dataset.cookieConsent=choice;
    window.byForoConsent={choice,optional:choice==='accepted'};
    window.dispatchEvent(new CustomEvent('byforo:consent',{detail:window.byForoConsent}));
    if(choice==='accepted'){activateOptionalScripts();activateGoogleAnalytics()}
  };
  let cookieReturnFocus=null;
  const closePanel=(restoreFocus=false)=>{document.querySelector('[data-cookie-panel]')?.remove();if(restoreFocus)cookieReturnFocus?.focus()};
  const save=choice=>{writeChoice(choice);announce(choice);closePanel(true)};
  const openPanel=(opener=null)=>{
    closePanel();cookieReturnFocus=opener;
    const panel=document.createElement('section');
    panel.className='cookie-panel';panel.dataset.cookiePanel='';panel.setAttribute('role','dialog');panel.setAttribute('aria-modal','true');panel.setAttribute('aria-labelledby','cookie-title');panel.setAttribute('aria-describedby','cookie-description');
    panel.innerHTML='<div class="cookie-panel__copy"><p class="kicker">Your privacy</p><h2 id="cookie-title">Cookie preferences</h2><p id="cookie-description">We use one necessary cookie to remember your choice. With permission, Google Analytics helps us understand visits and improve the journal. Analytics stays off unless you accept optional cookies.</p><a href="/cookies/">Read the cookie policy</a></div><div class="cookie-panel__actions"><button class="button button--dark" data-cookie-accept type="button">Accept optional</button><button class="button" data-cookie-reject type="button">Reject optional</button></div>';
    document.body.append(panel);
    panel.querySelector('[data-cookie-accept]').addEventListener('click',()=>save('accepted'));
    panel.querySelector('[data-cookie-reject]').addEventListener('click',()=>save('rejected'));
    panel.addEventListener('keydown',event=>{const items=[...panel.querySelectorAll('a[href],button:not([disabled])')];const first=items[0];const last=items.at(-1);if(event.key==='Escape'&&readChoice()){event.preventDefault();closePanel(true)}else if(event.key==='Tab'&&event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus()}else if(event.key==='Tab'&&!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus()}});
    panel.querySelector('button').focus();
  };
  document.addEventListener('click',event=>{const opener=event.target.closest('[data-cookie-settings]');if(opener){event.preventDefault();openPanel(opener)}});
  const choice=readChoice();
  if(choice==='accepted'||choice==='rejected')announce(choice);else openPanel();
})();

// Dynamic editorial image interaction: cursor-position zoom and subtle parallax.
(()=>{
  const finePointer=window.matchMedia('(hover: hover) and (pointer: fine)');
  const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
  const mediaItems=document.querySelectorAll('[data-zoom-media]');
  if(!mediaItems.length)return;

  const reset=(media)=>{
    media.classList.remove('is-zooming');
    media.style.setProperty('--zoom-x','50%');
    media.style.setProperty('--zoom-y','50%');
    media.style.setProperty('--pan-x','0px');
    media.style.setProperty('--pan-y','0px');
  };

  mediaItems.forEach(media=>{
    media.addEventListener('pointerenter',()=>{
      if(!finePointer.matches||reduced.matches)return;
      media.classList.add('is-zooming');
    });
    media.addEventListener('pointermove',event=>{
      if(!finePointer.matches||reduced.matches)return;
      const rect=media.getBoundingClientRect();
      const x=Math.max(0,Math.min(1,(event.clientX-rect.left)/rect.width));
      const y=Math.max(0,Math.min(1,(event.clientY-rect.top)/rect.height));
      media.style.setProperty('--zoom-x',`${(x*100).toFixed(2)}%`);
      media.style.setProperty('--zoom-y',`${(y*100).toFixed(2)}%`);
      media.style.setProperty('--pan-x',`${((.5-x)*7).toFixed(2)}px`);
      media.style.setProperty('--pan-y',`${((.5-y)*7).toFixed(2)}px`);
    });
    media.addEventListener('pointerleave',()=>reset(media));
    media.addEventListener('blur',()=>reset(media));
  });
})();
