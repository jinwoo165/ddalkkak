'use strict';
(()=>{
const $=id=>document.getElementById(id);
const actualIOS=/iPad|iPhone|iPod/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
const platform=new URLSearchParams(location.search).get('platform')||(actualIOS?'ios':'android');
$('platformLabel').textContent=platform==='ios'?'딸깍 · 아이폰':'딸깍 · 안드로이드';
document.querySelectorAll('.install-strip a').forEach(a=>{if(a.href.includes('platform='+platform))a.setAttribute('aria-current','page')});
let prompt;
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();prompt=e});
$('installBtn').addEventListener('click',async()=>{
 if(prompt){await prompt.prompt();prompt=null;return}
 $('installHelp').hidden=!$('installHelp').hidden;
 $('installHelp').textContent=platform==='ios'?'Safari에서 열기 → 공유 버튼 → 홈 화면에 추가. 첫 실행 후 키캡을 눌러 소리를 시작하세요. 아이폰 웹에서는 진동을 지원하지 않습니다.':'Chrome에서 열기 → 메뉴 ⋮ → 홈 화면에 추가 또는 앱 설치. 카카오톡 안에서 열었다면 외부 브라우저로 열어주세요.';
});
$('shareWav').addEventListener('click',async()=>{if(!window.lastRhythmFile)return;try{await navigator.share({files:[window.lastRhythmFile],title:'딸깍 내 리듬'})}catch(e){if(e.name!=='AbortError')$('recordInfo').textContent='공유를 실행하지 못했어요. WAV 저장 버튼으로 다운로드해주세요.'}});
if(actualIOS){$('hapticStatus').textContent='아이폰 웹은 진동을 지원하지 않아요. 소리와 눌림 효과로 즐겨주세요.'}
const status=$('offlineStatus');
if('serviceWorker' in navigator&&location.protocol!=='file:'){
 navigator.serviceWorker.register('./sw.js',{updateViaCache:'none'}).then(reg=>{
 const show=()=>{if(reg.active)status.textContent='오프라인 사용 준비 완료';else status.textContent='음원 저장 중 · 잠시 기다려주세요'};
 show();reg.addEventListener('updatefound',()=>{const w=reg.installing;w?.addEventListener('statechange',()=>{if(w.state==='activated')show();if(w.state==='installed'&&navigator.serviceWorker.controller){status.textContent='새 버전 준비됨 · 앱을 모두 닫고 다시 여세요'}})});
 navigator.serviceWorker.ready.then(()=>{status.textContent='오프라인 사용 준비 완료'});
 }).catch(()=>{status.textContent='오프라인 저장 실패 · 온라인 사용 가능'});
}else status.textContent='온라인 모드';
})();
