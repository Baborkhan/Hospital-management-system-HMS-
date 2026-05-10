/**
 * MedFind Admin Auth Guard v3.0
 * Owner: direct email+phone+OTP login
 * Team Members: email+phone → Owner Gmail Approval → OTP → enter
 */

const ADMIN_AUTH = {
  // ── OWNER CREDENTIALS ──────────────────────────────────────
  OWNER_EMAILS: [
    'ahsanulyaminbabor@gmail.com',
    'baborkhan117085@gmail.com'
  ],
  OWNER_PHONES: [
    '01772172829',
    '01516550217'
  ],

  // Notification email (owner's primary Gmail for approval alerts)
  OWNER_NOTIFY_EMAIL: 'ahsanulyaminbabor@gmail.com',

  ROLES: {
    superadmin:    { label: 'Super Admin',    color: '#10b981', canAccessAdmin: true,  canAccessAnalytics: true,  canManageUsers: true,  canManagePayments: true  },
    developer:     { label: 'Developer',      color: '#6366f1', canAccessAdmin: true,  canAccessAnalytics: true,  canManageUsers: false, canManagePayments: false },
    hospital_admin:{ label: 'Hospital Admin', color: '#f59e0b', canAccessAdmin: false, canAccessAnalytics: false, canManageUsers: false, canManagePayments: false },
    doctor:        { label: 'Doctor',         color: '#3b82f6', canAccessAdmin: false, canAccessAnalytics: false, canManageUsers: false, canManagePayments: false },
    patient:       { label: 'Patient',        color: '#94a3b8', canAccessAdmin: false, canAccessAnalytics: false, canManageUsers: false, canManagePayments: false },
  },

  // ── SESSION ─────────────────────────────────────────────────
  getSession()  { try { return JSON.parse(sessionStorage.getItem('mf_admin_session') || 'null'); } catch { return null; } },
  setSession(d) { sessionStorage.setItem('mf_admin_session', JSON.stringify({ ...d, timestamp: Date.now(), expires: Date.now() + 2*60*60*1000 })); },
  clearSession(){ sessionStorage.removeItem('mf_admin_session'); localStorage.removeItem('mf_token'); localStorage.removeItem('mf_user'); },
  isSessionValid(){ const s=this.getSession(); if(!s) return false; if(Date.now()>s.expires){this.clearSession();return false;} return s.verified===true; },

  canAccess(page='admin'){
    if(!this.isSessionValid()) return false;
    const s=this.getSession(); const role=this.ROLES[s.role]||{};
    if(page==='analytics') return role.canAccessAnalytics===true;
    if(page==='admin')     return role.canAccessAdmin===true;
    return false;
  },

  protect(page='admin'){
    if(!this.isSessionValid()||!this.canAccess(page)){ this.showLoginGate(page); return false; }
    this.injectUserInfo(); this.logAccess(page); return true;
  },

  injectUserInfo(){
    const s=this.getSession(); if(!s) return;
    document.querySelectorAll('#sbUserName,.sb-uname,.admin-username').forEach(el=>el&&(el.textContent=s.name||'Admin'));
    const ri=this.ROLES[s.role]||{label:'Admin',color:'#94a3b8'};
    document.querySelectorAll('#sbUserRole,.sb-urole,.admin-role').forEach(el=>{if(el){el.textContent=ri.label;el.style.color=ri.color;}});
  },

  logAccess(page){
    const s=this.getSession();
    const logs=JSON.parse(localStorage.getItem('mf_access_logs')||'[]');
    logs.unshift({user:s?.email,page,time:new Date().toISOString()});
    if(logs.length>100) logs.splice(100);
    localStorage.setItem('mf_access_logs',JSON.stringify(logs));
  },

  // ── LOGIN GATE UI ────────────────────────────────────────────
  showLoginGate(page){
    document.body.style.overflow='hidden';
    const gate=document.createElement('div');
    gate.id='adminGate';
    gate.innerHTML=`
<style>
  #adminGate{position:fixed;inset:0;z-index:99999;background:linear-gradient(135deg,#030810,#0a1628);
    display:flex;align-items:center;justify-content:center;font-family:'Inter',sans-serif;}
  .gate-box{background:rgba(15,23,42,.97);border:1px solid rgba(37,99,235,.25);border-radius:22px;
    padding:28px 24px;max-width:420px;width:calc(100vw - 32px);box-shadow:0 28px 70px rgba(0,0,0,.65);position:relative;overflow:hidden;}
  .gate-box::before{content:'';position:absolute;top:-60px;right:-60px;width:180px;height:180px;
    background:radial-gradient(circle,rgba(37,99,235,.12),transparent 70%);pointer-events:none;}
  .gate-logo{display:flex;align-items:center;gap:11px;margin-bottom:6px;}
  .gate-icon{width:46px;height:46px;background:linear-gradient(135deg,#1d4ed8,#7c3aed);border-radius:13px;
    display:flex;align-items:center;justify-content:center;font-size:20px;color:#fff;
    box-shadow:0 6px 20px rgba(37,99,235,.35);}
  .gate-title{font-size:1.35rem;font-weight:800;color:#f1f5f9;}
  .gate-sub{font-size:.72rem;color:#475569;margin-top:2px;}
  .gate-step{display:none;} .gate-step.active{display:block;}
  .gate-label{font-size:.76rem;font-weight:600;color:#94a3b8;margin-bottom:6px;display:flex;align-items:center;gap:5px;}
  .gate-input{width:100%;background:rgba(255,255,255,.05);border:1.5px solid rgba(255,255,255,.1);
    border-radius:12px;padding:.72rem 1rem;color:#f1f5f9;font-size:.9rem;
    font-family:'Inter',sans-serif;outline:none;transition:.2s;margin-bottom:12px;}
  .gate-input:focus{border-color:#2563eb;background:rgba(37,99,235,.1);}
  .gate-btn{width:100%;padding:.8rem;background:linear-gradient(135deg,#1d4ed8,#7c3aed);
    border:none;border-radius:13px;color:#fff;font-size:.9rem;font-weight:700;
    cursor:pointer;font-family:'Inter',sans-serif;transition:.2s;margin-top:2px;}
  .gate-btn:hover{opacity:.9;transform:translateY(-1px);box-shadow:0 8px 24px rgba(37,99,235,.3);}
  .gate-btn:disabled{opacity:.4;cursor:default;transform:none;}
  .gate-btn-ghost{width:100%;padding:.72rem;background:rgba(255,255,255,.05);
    border:1.5px solid rgba(255,255,255,.1);border-radius:13px;color:#94a3b8;font-size:.88rem;
    font-weight:600;cursor:pointer;font-family:'Inter',sans-serif;transition:.2s;margin-top:8px;}
  .gate-btn-ghost:hover{background:rgba(255,255,255,.08);color:#f1f5f9;}
  .gate-err{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);
    border-radius:10px;padding:9px 13px;color:#fca5a5;font-size:.78rem;margin-bottom:12px;display:none;}
  .gate-err.show{display:block;}
  .gate-ok{background:rgba(16,185,129,.1);border:1px solid rgba(16,185,129,.25);
    border-radius:10px;padding:9px 13px;color:#6ee7b7;font-size:.78rem;margin-bottom:12px;display:none;}
  .gate-ok.show{display:block;}
  .gate-info{font-size:.68rem;color:#475569;text-align:center;margin-top:10px;line-height:1.6;}
  .step-bar{display:flex;gap:5px;margin-bottom:22px;}
  .step-seg{height:3px;flex:1;border-radius:3px;background:rgba(255,255,255,.08);transition:.35s;}
  .step-seg.done{background:linear-gradient(90deg,#1d4ed8,#7c3aed);}
  .otp-row{display:flex;gap:6px;margin-bottom:12px;justify-content:center;}
  .otp-box{flex:1;min-width:0;max-width:52px;background:rgba(255,255,255,.05);border:1.5px solid rgba(255,255,255,.1);
    border-radius:10px;padding:.55rem .25rem;text-align:center;font-size:1.15rem;font-weight:700;
    color:#f1f5f9;font-family:'JetBrains Mono',monospace;outline:none;transition:.2s;width:100%;}
  .otp-box:focus{border-color:#2563eb;background:rgba(37,99,235,.08);}
  .otp-box.filled{border-color:#10b981;}
  .back-link{text-align:center;margin-top:12px;font-size:.75rem;color:#475569;cursor:pointer;transition:.2s;}
  .back-link:hover{color:#94a3b8;}
  .shield-badge{display:inline-flex;align-items:center;gap:5px;background:rgba(16,185,129,.1);
    border:1px solid rgba(16,185,129,.2);border-radius:20px;padding:5px 13px;
    font-size:.66rem;font-weight:700;color:#34d399;margin-bottom:18px;}
  /* Approval waiting screen */
  .appr-box{background:rgba(245,158,11,.06);border:1px solid rgba(245,158,11,.2);
    border-radius:14px;padding:16px;margin-bottom:14px;}
  .appr-code{font-family:'JetBrains Mono',monospace;font-size:2rem;font-weight:900;
    letter-spacing:.2em;color:#fbbf24;text-align:center;padding:14px 0 8px;
    background:rgba(245,158,11,.08);border-radius:10px;margin:10px 0;}
  .appr-steps{list-style:none;display:flex;flex-direction:column;gap:6px;margin-bottom:12px;}
  .appr-steps li{display:flex;align-items:flex-start;gap:8px;font-size:.78rem;color:#94a3b8;line-height:1.5;}
  .appr-steps li .n{background:rgba(37,99,235,.2);color:#93c5fd;border-radius:50%;width:18px;height:18px;
    display:flex;align-items:center;justify-content:center;font-size:.65rem;font-weight:700;flex-shrink:0;margin-top:1px;}
  .gmail-btn{display:flex;align-items:center;justify-content:center;gap:7px;width:100%;
    padding:.65rem;background:rgba(234,67,53,.12);border:1px solid rgba(234,67,53,.25);
    border-radius:10px;color:#fca5a5;font-size:.82rem;font-weight:700;cursor:pointer;
    font-family:'Inter',sans-serif;transition:.2s;text-decoration:none;margin-bottom:10px;}
  .gmail-btn:hover{background:rgba(234,67,53,.2);color:#fff;}
  .timer-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;}
</style>

<div class="gate-box">
  <div class="gate-logo">
    <div class="gate-icon">🔐</div>
    <div><div class="gate-title">Admin Access</div><div class="gate-sub">MedFind Secure Zone</div></div>
  </div>
  <div class="shield-badge">🛡️ Owner-Level Authentication Required</div>

  <div class="step-bar">
    <div class="step-seg done" id="ss1"></div>
    <div class="step-seg" id="ss2"></div>
    <div class="step-seg" id="ss3"></div>
    <div class="step-seg" id="ss4"></div>
  </div>

  <!-- STEP 1: Credentials -->
  <div class="gate-step active" id="gStep1">
    <div class="gate-label"><i class="fas fa-envelope" style="color:#6366f1"></i> Authorized Email Address</div>
    <input class="gate-input" type="email" id="gEmail" placeholder="your@email.com" autocomplete="off">
    <div class="gate-label"><i class="fas fa-phone" style="color:#10b981"></i> Registered Phone Number</div>
    <input class="gate-input" type="tel" id="gPhone" placeholder="01XXXXXXXXX" maxlength="11">
    <div class="gate-err" id="gErr1"></div>
    <button class="gate-btn" id="gBtn1" onclick="ADMIN_AUTH._step1()">
      <i class="fas fa-arrow-right"></i> Verify Identity
    </button>
    <div class="gate-info">Only authorized team members can access this area.</div>
  </div>

  <!-- STEP 2 (TEAM ONLY): Owner Approval Required -->
  <div class="gate-step" id="gStep2">
    <div class="appr-box">
      <div style="font-size:.75rem;font-weight:700;color:#fbbf24;margin-bottom:4px;display:flex;align-items:center;gap:5px;">
        <i class="fas fa-clock"></i> Owner Approval Required
      </div>
      <div style="font-size:.72rem;color:#94a3b8;margin-bottom:2px;">
        Your login request needs admin approval. Your Request Code:
      </div>
      <div class="appr-code" id="gApprCode">------</div>
    </div>
    <ul class="appr-steps">
      <li><span class="n">1</span> Click the button below to send approval request to admin's Gmail</li>
      <li><span class="n">2</span> Wait for admin to share the <strong style="color:#fbbf24">6-digit Approval Code</strong> with you</li>
      <li><span class="n">3</span> Enter the code below to continue</li>
    </ul>
    <a class="gmail-btn" id="gGmailBtn" href="#" onclick="ADMIN_AUTH._openGmail(); return false;">
      <i class="fab fa-google"></i> Send Approval Request to Admin Gmail
    </a>
    <div class="gate-label" style="margin-top:4px"><i class="fas fa-key" style="color:#f59e0b"></i> Enter Approval Code from Admin</div>
    <input class="gate-input" type="text" id="gApprInput" placeholder="Enter 6-digit code" maxlength="6" style="letter-spacing:.2em;font-family:'JetBrains Mono',monospace;font-size:1.1rem;text-align:center;">
    <div class="gate-err" id="gErr2"></div>
    <button class="gate-btn" onclick="ADMIN_AUTH._verifyApproval()">
      <i class="fas fa-unlock"></i> Submit Approval Code
    </button>
    <div class="back-link" onclick="ADMIN_AUTH._goStep(1)">← Back</div>
  </div>

  <!-- STEP 3: OTP -->
  <div class="gate-step" id="gStep3">
    <div class="gate-label"><i class="fas fa-key" style="color:#f59e0b"></i> 6-Digit Verification Code</div>
    <div style="font-size:.78rem;color:#64748b;margin-bottom:12px;">
      Enter the OTP sent to your registered email/phone.
    </div>
    <div class="otp-row" id="otpRow"></div>
    <div class="timer-row">
      <span style="font-size:.72rem;color:#475569;"><i class="fas fa-clock"></i> <span id="gTimer">2:00</span></span>
      <button style="background:none;border:none;color:#6366f1;font-size:.72rem;cursor:pointer;font-family:inherit;" onclick="ADMIN_AUTH._resendOTP()">Resend OTP</button>
    </div>
    <div class="gate-err" id="gErr3"></div>
    <div class="back-link" onclick="ADMIN_AUTH._goStep(ADMIN_AUTH._pendingUser?.isOwner ? 1 : 2)">← Back</div>
  </div>

  <!-- STEP 4: Welcome -->
  <div class="gate-step" id="gStep4">
    <div style="text-align:center;padding:20px 0;">
      <div style="font-size:2.4rem;margin-bottom:12px;">✅</div>
      <div style="font-size:1.15rem;font-weight:800;color:#f1f5f9;margin-bottom:6px;">Identity Verified</div>
      <div style="font-size:.83rem;color:#64748b;margin-bottom:24px;">
        Welcome back, <strong id="gWelcomeName" style="color:#10b981"></strong>
      </div>
      <button class="gate-btn" onclick="ADMIN_AUTH._enterAdmin()">
        <i class="fas fa-shield-halved"></i> Enter Admin Panel
      </button>
    </div>
  </div>
</div>`;
    document.body.appendChild(gate);
    this._initGate();
  },

  _initGate(){
    const row=document.getElementById('otpRow');
    if(!row) return;
    row.innerHTML='';
    for(let i=0;i<6;i++){
      const b=document.createElement('input');
      b.className='otp-box'; b.maxLength=1; b.dataset.i=i;
      b.addEventListener('input',e=>{
        const v=e.target.value;
        if(!/^\d*$/.test(v)){e.target.value='';return;}
        e.target.classList.toggle('filled',!!v);
        if(v&&i<5) row.children[i+1].focus();
        const code=Array.from(row.children).map(x=>x.value).join('');
        if(code.length===6) this._verifyOTP(code);
      });
      b.addEventListener('keydown',e=>{
        if(e.key==='Backspace'&&!e.target.value&&i>0) row.children[i-1].focus();
      });
      row.appendChild(b);
    }
    document.getElementById('gEmail')?.addEventListener('keydown',e=>{if(e.key==='Enter')this._step1();});
    document.getElementById('gPhone')?.addEventListener('keydown',e=>{if(e.key==='Enter')this._step1();});
    document.getElementById('gApprInput')?.addEventListener('keydown',e=>{if(e.key==='Enter')this._verifyApproval();});
  },

  _otpCode:null, _otpTimer:null, _pendingUser:null, _approvalCode:null,

  _step1(){
    const email=(document.getElementById('gEmail')?.value||'').trim().toLowerCase();
    const phone=(document.getElementById('gPhone')?.value||'').trim().replace(/[-\s]/g,'');
    const err=document.getElementById('gErr1');

    if(!email||!phone){err.textContent='Both email and phone are required.';err.classList.add('show');return;}

    const isOwner=this.OWNER_EMAILS.includes(email)&&this.OWNER_PHONES.includes(phone);
    const teamMembers=JSON.parse(localStorage.getItem('mf_team_members')||'[]');
    const teamMember=teamMembers.find(m=>m.email.toLowerCase()===email&&m.phone===phone&&m.active);

    if(!isOwner&&!teamMember){
      err.textContent='⛔ Access denied. This email or phone is not authorized.';err.classList.add('show');return;
    }
    err.classList.remove('show');

    this._pendingUser={
      email, phone,
      role: isOwner ? 'superadmin' : (teamMember?.role||'developer'),
      name: isOwner ? (email.split('@')[0]) : (teamMember?.name||'Team Member'),
      isOwner
    };

    if(isOwner){
      // Owner: skip approval step, go straight to OTP
      this._sendOTP();
      this._goStep(3);
    } else {
      // Team member: need owner approval first
      this._approvalCode=Math.floor(100000+Math.random()*900000).toString();
      document.getElementById('gApprCode').textContent=this._approvalCode;
      this._buildGmailLink();
      this._goStep(2);
    }
  },

  _buildGmailLink(){
    const u=this._pendingUser;
    const now=new Date().toLocaleString('en-BD',{timeZone:'Asia/Dhaka'});
    const subject=encodeURIComponent(`[MedFind] Admin Access Request — ${u.name}`);
    const body=encodeURIComponent(
`MedFind Admin Panel — Access Request Alert
===========================================

A team member is requesting access to the Admin Panel.

Requester  : ${u.name}
Email      : ${u.email}
Phone      : ${u.phone}
Role       : ${u.role}
Time       : ${now}
Page       : ${document.title}

APPROVAL CODE : ${this._approvalCode}

─────────────────────────────────────
If you authorize this login, share the APPROVAL CODE above with the team member.
If this request is unauthorized, ignore this email.

— MedFind Security System`
    );
    const link=`https://mail.google.com/mail/?view=cm&to=${encodeURIComponent(this.OWNER_NOTIFY_EMAIL)}&su=${subject}&body=${body}`;
    document.getElementById('gGmailBtn').href=link;
    document.getElementById('gGmailBtn').onclick=null;
    document.getElementById('gGmailBtn').target='_blank';
    document.getElementById('gGmailBtn').rel='noopener';
  },

  _openGmail(){
    // fallback if href not set yet
    const btn=document.getElementById('gGmailBtn');
    if(btn&&btn.href&&btn.href!=='#') window.open(btn.href,'_blank');
  },

  _verifyApproval(){
    const entered=(document.getElementById('gApprInput')?.value||'').trim();
    const err=document.getElementById('gErr2');
    if(!entered){err.textContent='Please enter the approval code from admin.';err.classList.add('show');return;}
    if(entered!==this._approvalCode){
      err.textContent='❌ Invalid approval code. Ask admin for the correct code.';err.classList.add('show');
      document.getElementById('gApprInput').value='';
      return;
    }
    err.classList.remove('show');
    this._sendOTP();
    this._goStep(3);
  },

  _sendOTP(){
    this._otpCode=Math.floor(100000+Math.random()*900000).toString();
    this._startTimer();
    // In production: call backend to email/SMS the OTP
    // For dev/demo: show in console (remove in production)
    if(location.hostname==='localhost'||location.hostname==='127.0.0.1'){
      console.log('%c[DEV] OTP Code: '+this._otpCode,'background:#1d4ed8;color:#fff;padding:4px 12px;border-radius:4px;font-weight:700;');
    }
  },

  _startTimer(){
    let t=120; clearInterval(this._otpTimer);
    this._otpTimer=setInterval(()=>{
      t--;
      const el=document.getElementById('gTimer');
      if(el) el.textContent=`${Math.floor(t/60)}:${(t%60).toString().padStart(2,'0')}`;
      if(t<=0) clearInterval(this._otpTimer);
    },1000);
  },

  _resendOTP(){
    this._sendOTP();
    const row=document.getElementById('otpRow');
    Array.from(row.children).forEach(b=>{b.value='';b.classList.remove('filled');});
  },

  _verifyOTP(code){
    if(code!==this._otpCode){
      const err=document.getElementById('gErr3');
      if(err){err.textContent='❌ Invalid OTP. Please try again.';err.classList.add('show');}
      const row=document.getElementById('otpRow');
      Array.from(row.children).forEach(b=>{b.value='';b.classList.remove('filled');});
      row.children[0]?.focus();
      return;
    }
    clearInterval(this._otpTimer);
    const nameEl=document.getElementById('gWelcomeName');
    if(nameEl) nameEl.textContent=this._pendingUser?.name||this._pendingUser?.email;
    this._goStep(4);
  },

  _enterAdmin(){
    this.setSession({...this._pendingUser,verified:true});
    document.getElementById('adminGate')?.remove();
    document.body.style.overflow='';
    this.injectUserInfo();
    this.logAccess('admin_login');
    setTimeout(()=>{
      const t=document.createElement('div');
      t.style.cssText='position:fixed;top:20px;right:20px;z-index:9999;background:linear-gradient(135deg,#10b981,#059669);color:#fff;padding:12px 20px;border-radius:13px;font-family:Inter,sans-serif;font-size:.85rem;font-weight:600;box-shadow:0 8px 24px rgba(0,0,0,.3);';
      t.innerHTML=`<i class="fas fa-check-circle"></i> Welcome, ${this._pendingUser?.name}! Admin access granted.`;
      document.body.appendChild(t);
      setTimeout(()=>t.remove(),3500);
    },300);
  },

  _goStep(n){
    const total=4;
    for(let i=1;i<=total;i++){
      document.getElementById(`gStep${i}`)?.classList.toggle('active',i===n);
      const seg=document.getElementById(`ss${i}`);
      if(seg) seg.classList.toggle('done',i<=n);
    }
    if(n===3) setTimeout(()=>document.querySelector('.otp-box')?.focus(),100);
    if(n===2) setTimeout(()=>document.getElementById('gApprInput')?.focus(),100);
  },

  logout(){
    this.clearSession();
    window.location.href=window.location.pathname.includes('/pages/')? '../login.html':'pages/login.html';
  }
};

// Auto-protect
document.addEventListener('DOMContentLoaded',()=>{
  const page=document.body.dataset.adminPage||'admin';
  ADMIN_AUTH.protect(page);
});
