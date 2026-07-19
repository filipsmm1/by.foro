
const root=document.documentElement;root.classList.add('reveal-ready');
const header=document.querySelector('[data-header]');const toggle=document.querySelector('.menu-toggle');const nav=document.querySelector('.site-nav');
const closeMenu=()=>{if(!nav||!toggle)return;nav.classList.remove('is-open');document.body.classList.remove('menu-open');toggle.setAttribute('aria-expanded','false');toggle.querySelector('span').textContent='Menu'};
if(toggle&&nav){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('is-open');document.body.classList.toggle('menu-open',open);toggle.setAttribute('aria-expanded',String(open));toggle.querySelector('span').textContent=open?'Close':'Menu'});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));document.addEventListener('keydown',e=>{if(e.key==='Escape')closeMenu()})}
const onScroll=()=>header?.classList.toggle('is-scrolled',window.scrollY>24);onScroll();window.addEventListener('scroll',onScroll,{passive:true});
const reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;const reveals=document.querySelectorAll('[data-reveal]');if(reduce||!('IntersectionObserver'in window)){reveals.forEach(x=>x.classList.add('is-visible'))}else{const io=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -40px'});reveals.forEach(x=>io.observe(x))}
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
document.querySelectorAll('[data-copy-link]').forEach(btn=>btn.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(location.href);btn.textContent='Link copied'}catch{btn.textContent='Copy failed'}}));
async function submitForm(form){const status=form.querySelector('.form-status');const button=form.querySelector('button[type=submit]');const original=button?.textContent;if(form.querySelector('input[name=_honey]')?.value)return;button&&(button.disabled=true,button.textContent='Sending…');status&&(status.textContent='');try{const endpoint=form.action.replace('formsubmit.co/','formsubmit.co/ajax/');const response=await fetch(endpoint,{method:'POST',headers:{Accept:'application/json'},body:new FormData(form)});if(!response.ok)throw new Error('Submission failed');form.reset();status&&(status.textContent=form.dataset.formKind==='newsletter'?'You are on the request list. Check your inbox when the first letter is sent.':'Thank you. Your message has been sent.')}catch(error){status&&(status.innerHTML='The form could not send. Email <a href="mailto:hello@byforo.com">hello@byforo.com</a> instead.')}finally{button&&(button.disabled=false,button.textContent=original)}}
document.querySelectorAll('[data-ajax-form]').forEach(form=>form.addEventListener('submit',e=>{e.preventDefault();if(form.reportValidity())submitForm(form)}));

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
