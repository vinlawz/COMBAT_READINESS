(function(){
  if(window._tactical_ui_loaded) return; 
  window._tactical_ui_loaded = true;
  
  document.addEventListener('DOMContentLoaded', function() {
    // Inject scanlines and grid only if not present
    if(!document.querySelector('.tactical-scanlines')){
      const s = document.createElement('div'); 
      s.className = 'tactical-scanlines'; 
      document.body.appendChild(s);
    }
    
    if(!document.querySelector('.tactical-grid')){
      const g = document.createElement('div'); 
      g.className = 'tactical-grid'; 
      document.body.appendChild(g);
    }
    
    // Update mission time
    function updateMissionTime() {
      const timeElement = document.getElementById('mission-time');
      if (timeElement) {
        const now = new Date();
        const hours = now.getUTCHours().toString().padStart(2, '0');
        const minutes = now.getUTCMinutes().toString().padStart(2, '0');
        const seconds = now.getUTCSeconds().toString().padStart(2, '0');
        timeElement.textContent = `${hours}:${minutes}:${seconds}Z`;
      }
    }
    
    // Update time immediately and then every second
    updateMissionTime();
    setInterval(updateMissionTime, 1000);
    
    // Animate counters if present
    document.querySelectorAll('.tactical-counter').forEach(el => {
      const target = parseInt(el.dataset.target || el.innerText || 0, 10);
      if (isNaN(target)) return;
      
      el.innerText = '0';
      let val = 0;
      const step = Math.max(1, Math.floor(target / 40));
      
      const t = setInterval(() => {
        val += step;
        if (val >= target) {
          el.innerText = String(target);
          clearInterval(t);
        } else {
          el.innerText = String(val);
        }
      }, 20);
    });
  });
})();
