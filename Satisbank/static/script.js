// Accordion behavior with smooth animation and single-open optional
document.addEventListener('DOMContentLoaded', function () {
    const items = document.querySelectorAll('.accordion-item');
  
    items.forEach(item => {
      const btn = item.querySelector('.accordion-btn');
      const panel = item.querySelector('.accordion-panel');
  
      btn.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');
  
        // If you want only one open at a time, uncomment the next block
        // items.forEach(i => { i.classList.remove('open'); i.querySelector('.accordion-panel').style.maxHeight = null; });
  
        if (isOpen) {
          item.classList.remove('open');
          panel.style.maxHeight = null;
        } else {
          item.classList.add('open');
          panel.style.maxHeight = panel.scrollHeight + 'px';
        }
      });
  
      // if panel has content expanded by server-side, set maxHeight
      if (item.classList.contains('open')) {
        panel.style.maxHeight = panel.scrollHeight + 'px';
      }
    });
  });
  