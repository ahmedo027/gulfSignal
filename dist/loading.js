const matchButton=document.querySelector('#search');
if(matchButton){matchButton.onclick=async()=>{matchButton.disabled=true;matchButton.innerHTML='<span class="spinner"></span> Matching';await load();matchButton.disabled=false;matchButton.textContent='Match ↗';};}
