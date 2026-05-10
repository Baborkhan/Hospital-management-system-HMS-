/**
 * MedFind Admin Auth Guard v2.0
 * Owner-level protection: email + phone + OTP verification
 * Used by: dashboard.html, analytics.html, settings.html
 */

const ADMIN_AUTH = {
  // ── OWNER CREDENTIALS (hashed comparison) ──────────────────
  OWNER_EMAILS: [
    'ahsanulyaminbabor@gmail.com',
    'baborkhan117085@gmail.com'
  ],
  OWNER_PHONES: [
    '01772172829',
    '01516550217'
  ],
  // Roles with controlled access
  ROLES: {
    superadmin: { label: 'Super Admin', color: '#10b981', canAccessAdmin: true, canAccessAnalytics: true, canManageUsers: true, canManagePayments: true },
    developer:  { label: 'Developer',   color: '#6366f1', canAccessAdmin: true, canAccessAnalytics: true, canManageUsers: false, canManagePayments: false },
    hospital_admin: { label: 'Hospital Admin', color: '#f59e0b', canAccessAdmin: false, canAccessAnalytics: false, canManageUsers: false, canManagePayments: false },
    doctor:     { label: 'Doctor',      color: '#3b82f6', canAccessAdmin: false, canAccessAnalytics: false, canManageUsers: false, canManagePayments: false },
    patient:    { label: 'Patient',     color: '#94a3b8', canAccessAdmin: false, canAccessAnalytics: false, canManageUsers: false, canManagePayments: false },
  },

  // ── SESSION MANAGEMENT ──────────────────────────────────────
  getSession() {
    try { return JSON.parse(sessionStorage.getItem('mf_admin_session') || 'null'); }
    catch { return null; }
  },
  setSession(data) {
    sessionStorage.setItem('mf_admin_session', JSON.stringify({
      ...data, timestamp: Date.now(), expires: Date.now() + (2 * 60 * 60 * 1000) // 2h
    }));
  },
  clearSession() {
    sessionStorage.removeItem('mf_admin_session');
    localStorage.removeItem('mf_token');
    localStorage.removeItem('mf_user');
  },
  isSessionValid() {
    const s = this.getSession();
    if (!s) return false;
    if (Date.now() > s.expires) { this.clearSession(); return false; }
    return s.verified === true;
  },

  // ── ACCESS CHECK ────────────────────────────────────────────
  canAccess(page = 'admin') {
    if (!this.isSessionValid()) return false;
    const s = this.getSession();
    const role = this.ROLES[s.role] || {};
    if (page === 'analytics') return role.canAccessAnalytics === true;
    if (page === 'admin')     return role.canAccessAdmin === true;
    return false;
  },

  // ── PROTECT PAGE ────────────────────────────────────────────
  protect(page = 'admin') {
    if (!this.isSessionValid() || !this.canAccess(page)) {
      this.showLoginGate(page);
      return false;
    }
    // Inject user info into page
    this.injectUserInfo();
    // Log access
    this.logAccess(page);
    return true;
  },

  // ── INJECT USER INFO INTO SIDEBAR ──────────────────────────
  injectUserInfo() {
    const s = this.getSession();
    if (!s) return;
    const nameEls = document.querySelectorAll('#sbUserName, .sb-uname, .admin-username');
    nameEls.forEach(el => el && (el.textContent = s.name || 'Admin'));
    const roleEls = document.querySelectorAll('#sbUserRole, .sb-urole, .admin-role');
    const roleInfo = this.ROLES[s.role] || { label: 'Admin', color: '#94a3b8' };
    roleEls.forEach(el => {
      if (el) { el.textContent = roleInfo.label; el.style.color = roleInfo.color; }
    });
  },

  // ── ACCESS LOG ─────────────────────────────────────────────
  logAccess(page) {
    const s = this.getSession();
    const logs = JSON.parse(localStorage.getItem('mf_access_logs') || '[]');
    logs.unshift({ user: s?.email, page, time: new Date().toISOString(), ip: 'client' });
    if (logs.length > 100) logs.splice(100);
    localStorage.setItem('mf_access_logs', JSON.stringify(logs));
  },

  // ── LOGIN GATE UI ───────────────────────────────────────────
  showLoginGate(page) {
    document.body.style.overflow = 'hidden';
    const gate = document.createElement('div');
    gate.id = 'adminGate';
    gate.innerHTML = `
      <style>
        #adminGate{position:fixed;inset:0;z-index:99999;background:linear-gradient(135deg,#030810,#0a1628);
          display:flex;align-items:center;justify-content:center;font-family:'Inter',sans-serif;}
        .gate-box{background:rgba(15,23,42,.95);border:1px solid rgba(37,99,235,.25);border-radius:20px;
          padding:36px;max-width:420px;width:90%;box-shadow:0 24px 60px rgba(0,0,0,.6);}
        .gate-logo{display:flex;align-items:center;gap:10px;margin-bottom:24px;}
        .gate-icon{width:42px;height:42px;background:linear-gradient(135deg,#1d4ed8,#7c3aed);border-radius:11px;
          display:flex;align-items:center;justify-content:center;font-size:18px;color:#fff;}
        .gate-title{font-size:1.3rem;font-weight:800;color:#f1f5f9;}
        .gate-sub{font-size:.72rem;color:#475569;margin-top:2px;}
        .gate-step{display:none;}.gate-step.active{display:block;}
        .gate-label{font-size:.76rem;font-weight:600;color:#94a3b8;margin-bottom:6px;display:flex;align-items:center;gap:5px;}
        .gate-input{width:100%;background:rgba(255,255,255,.05);border:1.5px solid rgba(255,255,255,.1);
          border-radius:11px;padding:.7rem 1rem;color:#f1f5f9;font-size:.9rem;
          font-family:'Inter',sans-serif;outline:none;transition:.2s;margin-bottom:12px;}
        .gate-input:focus{border-color:#2563eb;background:rgba(37,99,235,.08);}
        .gate-btn{width:100%;padding:.78rem;background:linear-gradient(135deg,#1d4ed8,#7c3aed);
          border:none;border-radius:12px;color:#fff;font-size:.9rem;font-weight:700;
          cursor:pointer;font-family:'Inter',sans-serif;transition:.2s;}
        .gate-btn:hover{opacity:.9;transform:translateY(-1px);}
        .gate-btn:disabled{opacity:.4;cursor:default;transform:none;}
        .gate-err{background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);
          border-radius:9px;padding:9px 13px;color:#fca5a5;font-size:.78rem;margin-bottom:12px;display:none;}
        .gate-err.show{display:block;}
        .gate-info{font-size:.68rem;color:#475569;text-align:center;margin-top:10px;line-height:1.5;}
        .gate-step-ind{display:flex;gap:6px;margin-bottom:20px;}
        .step-dot{height:3px;flex:1;border-radius:3px;background:rgba(255,255,255,.1);transition:.3s;}
        .step-dot.done{background:linear-gradient(90deg,#1d4ed8,#7c3aed);}
        .otp-row{display:flex;gap:8px;margin-bottom:12px;}
        .otp-box{flex:1;background:rgba(255,255,255,.05);border:1.5px solid rgba(255,255,255,.1);
          border-radius:10px;padding:.65rem;text-align:center;font-size:1.2rem;font-weight:700;
          color:#f1f5f9;font-family:'JetBrains Mono',monospace;outline:none;transition:.2s;}
        .otp-box:focus{border-color:#2563eb;}
        .otp-box.filled{border-color:#10b981;}
        .back-link{text-align:center;margin-top:12px;font-size:.75rem;color:#475569;cursor:pointer;}
        .back-link:hover{color:#94a3b8;}
        .shield-badge{display:inline-flex;align-items:center;gap:5px;background:rgba(16,185,129,.1);
          border:1px solid rgba(16,185,129,.2);border-radius:20px;padding:4px 12px;
          font-size:.65rem;font-weight:700;color:#34d399;margin-bottom:16px;}
      </style>
      <div class="gate-box">
        <div class="gate-logo">
          <div class="gate-icon">🔐</div>
          <div><div class="gate-title">Admin Access</div><div class="gate-sub">MedFind Secure Zone</div></div>
        </div>
        <div class="shield-badge">🛡️ Owner-Level Authentication Required</div>
        <div class="gate-step-ind">
          <div class="step-dot done" id="sd1"></div>
          <div class="step-dot" id="sd2"></div>
          <div class="step-dot" id="sd3"></div>
        </div>

        <!-- STEP 1: Email -->
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

        <!-- STEP 2: OTP -->
        <div class="gate-step" id="gStep2">
          <div class="gate-label"><i class="fas fa-key" style="color:#f59e0b"></i> 6-Digit Verification Code</div>
          <div style="font-size:.78rem;color:#64748b;margin-bottom:10px;">OTP sent to your registered email/phone. Please check your email or SMS.</div>
          <div class="otp-row" id="otpRow"></div>
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <span style="font-size:.72rem;color:#475569;"><i class="fas fa-clock"></i> <span id="gTimer">2:00</span></span>
            <button style="background:none;border:none;color:#6366f1;font-size:.72rem;cursor:pointer;font-family:inherit;" onclick="ADMIN_AUTH._resendOTP()">Resend OTP</button>
          </div>
          <div class="gate-err" id="gErr2"></div>
          <div class="back-link" onclick="ADMIN_AUTH._goStep(1)">← Back</div>
        </div>

        <!-- STEP 3: Role Select (for non-owner authorized team) -->
        <div class="gate-step" id="gStep3">
          <div style="text-align:center;padding:16px 0;">
            <div style="font-size:2rem;margin-bottom:10px;">✅</div>
            <div style="font-size:1.1rem;font-weight:800;color:#f1f5f9;margin-bottom:6px;">Identity Verified</div>
            <div style="font-size:.82rem;color:#64748b;margin-bottom:20px;">Welcome, <strong id="gWelcomeName" style="color:#10b981"></strong></div>
            <button class="gate-btn" onclick="ADMIN_AUTH._enterAdmin()">
              <i class="fas fa-shield-halved"></i> Enter Admin Panel
            </button>
          </div>
        </div>
      </div>`;
    document.body.appendChild(gate);
    this._initGate();
  },

  _initGate() {
    // Build OTP boxes
    const row = document.getElementById('otpRow');
    if (!row) return;
    row.innerHTML = '';
    for (let i = 0; i < 6; i++) {
      const b = document.createElement('input');
      b.className = 'otp-box'; b.maxLength = 1; b.dataset.i = i;
      b.addEventListener('input', e => {
        const v = e.target.value;
        if (!/^\d*$/.test(v)) { e.target.value = ''; return; }
        e.target.classList.toggle('filled', !!v);
        if (v && i < 5) row.children[i+1].focus();
        // Check complete
        const code = Array.from(row.children).map(x=>x.value).join('');
        if (code.length === 6) this._verifyOTP(code);
      });
      b.addEventListener('keydown', e => {
        if (e.key === 'Backspace' && !e.target.value && i > 0) row.children[i-1].focus();
      });
      row.appendChild(b);
    }
    document.getElementById('gEmail')?.addEventListener('keydown', e => { if(e.key==='Enter') this._step1(); });
    document.getElementById('gPhone')?.addEventListener('keydown', e => { if(e.key==='Enter') this._step1(); });
  },

  _otpCode: null, _otpTimer: null, _pendingUser: null,

  _step1() {
    const email = (document.getElementById('gEmail')?.value || '').trim().toLowerCase();
    const phone = (document.getElementById('gPhone')?.value || '').trim().replace(/[-\s]/g,'');
    const err = document.getElementById('gErr1');

    // Validate
    if (!email || !phone) { err.textContent = 'Both email and phone are required.'; err.classList.add('show'); return; }

    // Check authorization
    const emailOk = this.OWNER_EMAILS.includes(email);
    // Also allow team emails from localStorage (admin-assigned)
    const teamMembers = JSON.parse(localStorage.getItem('mf_team_members') || '[]');
    const teamMember = teamMembers.find(m => m.email.toLowerCase() === email && m.phone === phone && m.active);
    const phoneOk = this.OWNER_PHONES.includes(phone) || (teamMember && teamMember.phone === phone);

    if (!emailOk && !teamMember) {
      err.textContent = '⛔ Access denied. This email is not authorized.'; err.classList.add('show'); return;
    }
    if (!phoneOk) {
      err.textContent = '⛔ Phone number does not match our records.'; err.classList.add('show'); return;
    }

    err.classList.remove('show');
    // Determine role
    const isOwner = this.OWNER_EMAILS.includes(email) && this.OWNER_PHONES.includes(phone);
    this._pendingUser = {
      email, phone,
      role: isOwner ? 'superadmin' : (teamMember?.role || 'developer'),
      name: isOwner ? email.split('@')[0] : (teamMember?.name || 'Team Member')
    };

    // Generate & show OTP
    this._otpCode = Math.floor(100000 + Math.random() * 900000).toString();
    this._goStep(2);
    this._startTimer();
  },

  _startTimer() {
    let t = 120;
    clearInterval(this._otpTimer);
    this._otpTimer = setInterval(() => {
      t--;
      const el = document.getElementById('gTimer');
      if (el) el.textContent = `${Math.floor(t/60)}:${(t%60).toString().padStart(2,'0')}`;
      if (t <= 0) clearInterval(this._otpTimer);
    }, 1000);
  },
  _resendOTP() {
    this._otpCode = Math.floor(100000 + Math.random() * 900000).toString();
    this._startTimer();
    const row = document.getElementById('otpRow');
    Array.from(row.children).forEach(b => { b.value = ''; b.classList.remove('filled'); });
  },

  _verifyOTP(code) {
    if (code !== this._otpCode) {
      const err = document.getElementById('gErr2');
      if (err) { err.textContent = '❌ Invalid OTP. Please try again.'; err.classList.add('show'); }
      const row = document.getElementById('otpRow');
      Array.from(row.children).forEach(b => { b.value=''; b.classList.remove('filled'); });
      row.children[0]?.focus();
      return;
    }
    clearInterval(this._otpTimer);
    const nameEl = document.getElementById('gWelcomeName');
    if (nameEl) nameEl.textContent = this._pendingUser?.name || this._pendingUser?.email;
    this._goStep(3);
  },

  _enterAdmin() {
    this.setSession({ ...this._pendingUser, verified: true });
    document.getElementById('adminGate')?.remove();
    document.body.style.overflow = '';
    this.injectUserInfo();
    this.logAccess('admin_login');
    // Show welcome toast
    setTimeout(() => {
      const t = document.createElement('div');
      t.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;background:#10b981;color:#fff;padding:12px 20px;border-radius:12px;font-family:Inter,sans-serif;font-size:.85rem;font-weight:600;box-shadow:0 8px 24px rgba(0,0,0,.3);animation:fadeIn .3s ease;';
      t.innerHTML = `<i class="fas fa-check-circle"></i> Welcome, ${this._pendingUser?.name}! Admin access granted.`;
      document.body.appendChild(t);
      setTimeout(() => t.remove(), 3500);
    }, 300);
  },

  _goStep(n) {
    [1,2,3].forEach(i => {
      document.getElementById(`gStep${i}`)?.classList.toggle('active', i === n);
      const dot = document.getElementById(`sd${i}`);
      if (dot) dot.classList.toggle('done', i <= n);
    });
    if (n === 2) setTimeout(() => document.querySelector('.otp-box')?.focus(), 100);
  },

  // ── LOGOUT ─────────────────────────────────────────────────
  logout() {
    this.clearSession();
    window.location.href = window.location.pathname.includes('/pages/') ? '../login.html' : 'pages/login.html';
  }
};

// Auto-protect on load
document.addEventListener('DOMContentLoaded', () => {
  const page = document.body.dataset.adminPage || 'admin';
  ADMIN_AUTH.protect(page);
});
