// profile.js — modal logic, persistence
document.addEventListener('DOMContentLoaded', () => {
    const verifyBtn = document.getElementById('verifyBtn');
    const modal = document.getElementById('verifyModal');
    const confirmBtn = document.getElementById('confirmVerify');
    const cancelBtn = document.getElementById('cancelVerify');
  
    function setRequestedState() {
      verifyBtn.textContent = 'Requested ✓';
      verifyBtn.disabled = true;
      verifyBtn.style.background = 'linear-gradient(90deg,var(--secondary),#18b37b)';
      verifyBtn.style.cursor = 'default';
    }
  
    // restore
    if (localStorage.getItem('credify_verification_requested') === 'true') {
      setRequestedState();
    }
  
    verifyBtn && verifyBtn.addEventListener('click', () => {
      modal.classList.add('show');
      modal.setAttribute('aria-hidden','false');
    });
  
    cancelBtn && cancelBtn.addEventListener('click', () => {
      modal.classList.remove('show');
      modal.setAttribute('aria-hidden','true');
    });
  
    confirmBtn && confirmBtn.addEventListener('click', () => {
      localStorage.setItem('credify_verification_requested','true');
      setRequestedState();
      modal.classList.remove('show');
      modal.setAttribute('aria-hidden','true');
      setTimeout(()=> alert('Verification request submitted. We will review and notify you via email.'), 150);
    });
  });
  