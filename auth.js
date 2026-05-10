// MedFind Auth utilities
const MFAuth = {
  getUser()  { try { return JSON.parse(localStorage.getItem('mf_user')||'null'); } catch { return null; } },
  getToken() { return localStorage.getItem('mf_token'); },
  isLoggedIn(){ return !!(this.getUser()&&this.getToken()); },
  save(u,t)  { localStorage.setItem('mf_user',JSON.stringify(u)); localStorage.setItem('mf_token',t); },
  clear()    { localStorage.removeItem('mf_user'); localStorage.removeItem('mf_token'); },
  logout()   { this.clear(); location.href=MedFindComponents.getBasePath()+'pages/login.html'; }
};
window.MFAuth = MFAuth;
