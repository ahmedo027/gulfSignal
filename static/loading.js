const matchButton=document.querySelector('#search');
if(matchButton){matchButton.onclick=async()=>{matchButton.disabled=true;matchButton.innerHTML='<span class="spinner"></span> Matching';await load();matchButton.disabled=false;matchButton.textContent='Match ↗';};}
setTimeout(()=>{if(!document.querySelector('.card')&&document.querySelector('#jobs'))document.querySelector('#jobs').innerHTML='<div class="empty">No matching jobs found for this location yet.</div>';},800);
