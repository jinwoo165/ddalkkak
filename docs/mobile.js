/* Reuse the existing controls and listeners in compact mobile sheets. */
(()=>{
 const $=s=>document.querySelector(s), mq=matchMedia('(max-width: 850px)');
 const nav=document.createElement('nav');nav.className='mobile-dock';nav.setAttribute('aria-label','키캡 설정');
 nav.innerHTML='<button data-panel="shape"><small>모양</small><b id="mobileShape"></b></button><button data-panel="sound"><small>스위치</small><b id="mobileSound"></b></button><button data-panel="settings"><small>음량 · 테마</small><b>설정</b></button>';
 $('.left-column').append(nav);
 const sheet=document.createElement('dialog');sheet.className='mobile-sheet';sheet.setAttribute('aria-labelledby','sheetTitle');sheet.innerHTML='<div class="sheet-header"><h2 id="sheetTitle"></h2><button class="btn small" id="sheetClose">완료</button></div><div class="sheet-body"></div>';document.body.append(sheet);
 const groups={shape:[$('.shape-section')],sound:[$('.sound-section')],settings:[$('.side-column'),$('.install-strip'),$('.page-footer')]};
 const homes=new Map();Object.values(groups).flat().forEach(el=>{const marker=document.createComment('control home');el.before(marker);homes.set(el,marker)});
 function restore(){for(const [el,marker] of homes)marker.after(el)}
 function close(){sheet.close();restore()}
 $('#sheetClose').onclick=close;sheet.addEventListener('close',restore);
 sheet.addEventListener('click',e=>{if(e.target===sheet){const r=sheet.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)close()}});
 nav.addEventListener('click',e=>{const b=e.target.closest('[data-panel]');if(!b)return;restore();$('#sheetTitle').textContent={shape:'누르고 싶은 모양',sound:'오늘의 스위치',settings:'나만의 설정'}[b.dataset.panel];groups[b.dataset.panel].forEach(el=>$('.sheet-body').append(el));sheet.showModal();$('.sheet-body').scrollTop=0;});
 // Shape choice returns straight to the instrument. Sound choices stay open to compare.
 $('#shapeList').addEventListener('click',e=>{if(e.target.closest('[data-shape]')&&sheet.open)close()});
 const save=$('#savePreset'),saveHome=document.createComment('save home');save.before(saveHome);
 function layout(){if(!mq.matches&&sheet.open)close();if(mq.matches)$('.header-right').prepend(save);else saveHome.after(save);fit()}
 function fit(){if(!mq.matches)return;const r=$('#playfield').getBoundingClientRect();$('#playfield').style.setProperty('--play-size',Math.max(24,Math.min(r.width-8,r.height-12,360))+'px')}
 new ResizeObserver(fit).observe($('#playfield'));mq.addEventListener('change',layout);
 function labels(){$('#mobileShape').textContent=$('#shapeName').textContent;$('#mobileSound').textContent=$('#currentSound').textContent}
 for(const s of ['#shapeName','#currentSound'])new MutationObserver(labels).observe($(s),{childList:true,subtree:true,characterData:true});labels();layout();
})();
