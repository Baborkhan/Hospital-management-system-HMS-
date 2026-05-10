/**
 * MedFind Shared Components v2.0
 * Auto-detects depth, injects navbar/footer/toast on all pages
 */
const MedFindComponents = {
  API_BASE: (location.hostname==='localhost'||location.hostname==='127.0.0.1')?'http://127.0.0.1:8000/api/v1':'/api/v1',

  init() {
    this.injectNavbar();
    this.injectFooter();
    this.injectToastContainer();
    this.setupAuth();
  },

  getBasePath() {
    const p = location.pathname.replace(/\\/g, '/');
    if (!p.includes('/pages/')) return './';
    const after = p.split('/pages/')[1] || '';
    return after.split('/').length >= 2 ? '../../' : '../';
  },

  // ── NAVBAR ──────────────────────────────────────────────
  injectNavbar() {
    if (document.getElementById('mfNavbar')) return;
    const base = this.getBasePath();
    const user = this.getCurrentUser();

    const nav = document.createElement('nav');
    nav.className = 'mf-navbar';
    nav.id = 'mfNavbar';
    nav.innerHTML = `
      <div class="mf-nav-inner">
        <a href="${base}index.html" class="mf-logo">
          <img src="${base}assets/medfind-logo.png" alt="MedFind" style="height:44px;width:auto;object-fit:contain;" onerror="this.style.display='none'">
          <div class="mf-logo-icon" style="display:none"><i class="fas fa-heartbeat"></i></div>
          <span>Med<strong>Find</strong></span>
        </a>
        <ul class="mf-nav-links" id="mfNavLinks">
          <li><a href="${base}index.html" class="mf-nav-link">Home</a></li>
          <li class="mf-dropdown">
            <a class="mf-nav-link mf-drop-trigger">Find <i class="fas fa-chevron-down fa-xs"></i></a>
            <div class="mf-drop-menu">
              <a href="${base}pages/doctors/search.html"><i class="fas fa-user-md"></i> Doctors</a>
              <a href="${base}pages/hospital/list.html"><i class="fas fa-hospital-alt"></i> Hospitals</a>
              <a href="${base}pages/lab/tests.html"><i class="fas fa-flask"></i> Lab Tests</a>
              <a href="${base}pages/billing/pharmacy.html"><i class="fas fa-pills"></i> Pharmacy</a>
            </div>
          </li>
          <li class="mf-dropdown">
            <a class="mf-nav-link mf-drop-trigger" style="color:#1a56db;font-weight:600">Medical Info <i class="fas fa-chevron-down fa-xs"></i></a>
            <div class="mf-drop-menu">
              <a href="${base}pages/symptoms/index.html"><i class="fas fa-stethoscope" style="color:#1a56db"></i> Symptom Checker</a>
              <a href="${base}pages/treatments/index.html"><i class="fas fa-notes-medical" style="color:#0d9488"></i> Treatment Guide</a>
              <a href="${base}pages/drugs/index.html"><i class="fas fa-pills" style="color:#d97706"></i> Drug Directory</a>
              <a href="${base}pages/medfind-ai.html" style="color:#00d4aa !important"><i class="fas fa-robot" style="color:#00d4aa"></i> MedFind AI ✨</a>
            </div>
          </li>
          <li><a href="${base}pages/patients/appointments.html" class="mf-nav-link">Appointments</a></li>
          <li><a href="${base}pages/health-articles.html" class="mf-nav-link">Health Tips</a></li>
          <li class="mf-dropdown">
            <a class="mf-nav-link mf-drop-trigger">Services <i class="fas fa-chevron-down fa-xs"></i></a>
            <div class="mf-drop-menu">
              <a href="${base}pages/patients/opd.html"><i class="fas fa-file-invoice-dollar"></i> OPD Billing</a>
              <a href="${base}pages/admin/dashboard.html"><i class="fas fa-tachometer-alt"></i> Admin Panel</a>
              <a href="${base}pages/admin/analytics.html"><i class="fas fa-chart-bar"></i> Analytics</a>
              <a href="${base}pages/hospital/admin.html"><i class="fas fa-hospital"></i> Hospital Admin</a>
              <a href="${base}pages/patients/viewmaps.html"><i class="fas fa-map-marked-alt"></i> Hospital Map</a>
            </div>
          </li>
        </ul>
        <div class="mf-nav-auth" id="mfNavAuth">
          ${user
            ? `<div class="mf-dropdown mf-user-dd">
                <div class="mf-drop-trigger mf-user-btn">
                  <div class="mf-avatar">${(user.name||'U')[0].toUpperCase()}</div>
                  <span>${(user.name||'').split(' ')[0]}</span>
                  <i class="fas fa-chevron-down fa-xs"></i>
                </div>
                <div class="mf-drop-menu mf-drop-right">
                  <a href="${base}pages/patients/dashboard.html"><i class="fas fa-th-large"></i> Dashboard</a>
                  <a href="${base}pages/patients/profile.html"><i class="fas fa-user-circle"></i> My Profile</a>
                  <a href="${base}pages/patients/medical-history.html"><i class="fas fa-file-medical"></i> Medical History</a>
                  <a href="${base}pages/patients/appointments.html"><i class="fas fa-calendar-check"></i> Appointments</a>
                  <a href="${base}pages/patients/settings.html" title="Settings"><i class="fas fa-gear"></i> Settings</a>
                  <div style="height:1px;background:var(--g200,#e2e8f0);margin:4px 0;"></div>
                  <a href="#" id="mfLogoutBtn"><i class="fas fa-sign-out-alt"></i> Logout</a>
                </div>
              </div>`
            : `<a href="${base}pages/patients/settings.html" class="mf-nav-gear-btn" title="Settings" style="width:36px;height:36px;border-radius:50%;background:rgba(37,99,235,.08);border:1px solid rgba(37,99,235,.18);display:flex;align-items:center;justify-content:center;color:#2563eb;font-size:.9rem;text-decoration:none;transition:.2s;" onmouseover="this.style.background='rgba(37,99,235,.18)'" onmouseout="this.style.background='rgba(37,99,235,.08)'"><i class="fas fa-gear"></i></a>
               <a href="${base}pages/login.html" class="mf-btn-outline">Login</a>
               <a href="${base}pages/register.html" class="mf-btn-primary">Sign Up Free</a>`
          }
        </div>
        <button class="mf-hamburger" id="mfHamburger" aria-label="Toggle menu">
          <span></span><span></span><span></span>
        </button>
      </div>`;

    // CSS
    if (!document.getElementById('mf-nav-css')) {
      const s = document.createElement('style');
      s.id = 'mf-nav-css';
      s.textContent = `
        .mf-navbar{position:sticky;top:0;z-index:900;background:rgba(255,255,255,.97);backdrop-filter:blur(12px);border-bottom:1px solid rgba(37,99,235,.08);box-shadow:0 1px 10px rgba(0,0,0,.05);font-family:'Inter',sans-serif;}
        .mf-nav-inner{max-width:1280px;margin:0 auto;padding:0 1.5rem;height:68px;display:flex;align-items:center;gap:1.5rem;}
        .mf-logo{display:flex;align-items:center;gap:10px;color:#2563eb;font-size:1.3rem;font-weight:700;flex-shrink:0;text-decoration:none;}
        .mf-logo strong{font-weight:900;}
        .mf-logo-icon{width:38px;height:38px;background:linear-gradient(135deg,#2563eb,#7c3aed);border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:1rem;}
        .mf-nav-links{list-style:none;display:flex;align-items:center;gap:2px;flex:1;padding:0;margin:0;}
        .mf-nav-link{display:flex;align-items:center;gap:5px;padding:8px 13px;border-radius:9px;color:#334155;font-weight:500;font-size:.88rem;cursor:pointer;transition:all .2s;white-space:nowrap;text-decoration:none;}
        .mf-nav-link:hover,.mf-nav-link.active{background:#eff6ff;color:#2563eb;}
        .mf-nav-link i{font-size:.65rem;}
        .mf-dropdown{position:relative;}
        .mf-drop-menu{position:absolute;top:calc(100% + 8px);left:0;background:#fff;border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,.12);border:1px solid #e2e8f0;min-width:215px;padding:6px 0;opacity:0;visibility:hidden;transform:translateY(-6px);transition:all .2s;z-index:200;}
        .mf-drop-right{left:auto;right:0;}
        .mf-dropdown:hover .mf-drop-menu,.mf-dropdown.open .mf-drop-menu{opacity:1;visibility:visible;transform:none;}
        .mf-drop-menu a{display:flex;align-items:center;gap:10px;padding:9px 14px;color:#374151;font-size:.85rem;transition:all .15s;text-decoration:none;}
        .mf-drop-menu a:hover{background:#f0f9ff;color:#2563eb;padding-left:18px;}
        .mf-drop-menu a i{width:15px;color:#2563eb;font-size:.85rem;}
        .mf-nav-auth{display:flex;align-items:center;gap:10px;flex-shrink:0;}
        .mf-btn-outline{padding:8px 18px;border-radius:9px;border:1.5px solid #d1d5db;color:#374151;text-decoration:none;font-weight:500;font-size:.88rem;transition:all .2s;}
        .mf-btn-outline:hover{border-color:#2563eb;color:#2563eb;background:#eff6ff;}
        .mf-btn-primary{padding:8px 18px;border-radius:9px;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;text-decoration:none;font-weight:600;font-size:.88rem;box-shadow:0 4px 12px rgba(37,99,235,.25);transition:all .2s;}
        .mf-btn-primary:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(37,99,235,.35);}
        .mf-user-btn{display:flex;align-items:center;gap:8px;padding:5px 12px 5px 5px;border-radius:10px;cursor:pointer;font-size:.87rem;color:#334155;transition:all .2s;}
        .mf-user-btn:hover{background:#f3f4f6;}
        .mf-avatar{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;font-weight:700;font-size:.85rem;display:flex;align-items:center;justify-content:center;}
        .mf-hamburger{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:6px;margin-left:auto;}
        .mf-hamburger span{width:22px;height:2px;background:#334155;border-radius:2px;transition:all .3s;display:block;}
        .mf-hamburger.open span:nth-child(1){transform:rotate(45deg) translate(5px,5px);}
        .mf-hamburger.open span:nth-child(2){opacity:0;}
        .mf-hamburger.open span:nth-child(3){transform:rotate(-45deg) translate(5px,-5px);}
        @media(max-width:960px){
          .mf-hamburger{display:flex;}
          .mf-nav-links,.mf-nav-auth{display:none;position:fixed;top:68px;left:0;right:0;background:#fff;flex-direction:column;padding:12px 1rem;box-shadow:0 8px 24px rgba(0,0,0,.1);z-index:899;gap:4px;}
          .mf-nav-links.show,.mf-nav-auth.show{display:flex;}
          .mf-drop-menu{position:static;opacity:1;visibility:visible;transform:none;box-shadow:none;border:none;background:#f8fafc;border-radius:10px;margin:4px 0;}
        }`;
      document.head.appendChild(s);
    }

    document.body.insertBefore(nav, document.body.firstChild);
    this._setupNavEvents();
  },

  _setupNavEvents() {
    const ham = document.getElementById('mfHamburger');
    const links = document.getElementById('mfNavLinks');
    const auth = document.getElementById('mfNavAuth');

    ham?.addEventListener('click', () => {
      ham.classList.toggle('open');
      links?.classList.toggle('show');
      auth?.classList.toggle('show');
    });
    document.querySelectorAll('.mf-drop-trigger').forEach(t => {
      t.addEventListener('click', e => {
        const dd = t.closest('.mf-dropdown');
        document.querySelectorAll('.mf-dropdown.open').forEach(d => { if (d !== dd) d.classList.remove('open'); });
        dd?.classList.toggle('open');
        e.stopPropagation();
      });
    });
    document.addEventListener('click', () => document.querySelectorAll('.mf-dropdown.open').forEach(d => d.classList.remove('open')));

    document.getElementById('mfLogoutBtn')?.addEventListener('click', e => {
      e.preventDefault();
      this.logout();
    });

    // Mark active
    const cur = location.pathname.split('/').pop() || '';
    document.querySelectorAll('.mf-nav-link').forEach(a => {
      if (cur && (a.getAttribute('href')||'').includes(cur)) a.classList.add('active');
    });
  },

  // ── FOOTER ─────────────────────────────────────────────
  injectFooter() {
    if (document.getElementById('mfFooter')) return;
    const base = this.getBasePath();
    const f = document.createElement('footer');
    f.id = 'mfFooter';

    const linkStyle = `color:#94a3b8;font-size:.84rem;text-decoration:none;transition:color .2s;`;
    const hoverIn  = `this.style.color='#fff'`;
    const hoverOut = `this.style.color='#94a3b8'`;
    const colHead  = `color:#f8fafc;font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.07em;margin-bottom:.85rem;border-bottom:1px solid rgba(255,255,255,.07);padding-bottom:.5rem;`;

    const platform = [
      ['Symptom Checker','pages/symptoms/index.html'],
      ['Drug Directory','pages/drugs/index.html'],
      ['Treatment Guide','pages/treatments/index.html'],
      ['Blood Donors','pages/blood-donor/search.html'],
      ['Donate Life (Organ)','pages/donate/index.html'],
      ['Find Doctors','pages/doctors/search.html'],
      ['Find Hospitals','pages/hospital/list.html'],
      ['Book Appointment','pages/patients/appointments.html'],
    ];
    const legal = [
      ['Privacy Policy','pages/privacy.html'],
      ['Terms of Service','pages/terms.html'],
      ['Medical Disclaimer','pages/medical-disclaimer.html'],
      ['Consent Forms','pages/consent-forms.html'],
      ['Data & Security','pages/data-backup-policy.html'],
      ['Cookie Policy','pages/cookies.html'],
    ];
    const admin = [
      ['Admin Dashboard','pages/admin/dashboard.html'],
      ['Analytics','pages/admin/analytics.html'],
      ['Bed Management','pages/hospital/bed-management.html'],
      ['Hospital Admin','pages/hospital/admin.html'],
      ['OPD Billing','pages/patients/opd.html'],
      ['Lab Tests','pages/lab/tests.html'],
      ['Pharmacy','pages/billing/pharmacy.html'],
      ['Health Articles','pages/health-articles.html'],
    ];
    const team = [
      {name:'Ahsanul Yamin Babor',  role:'Lead Full Stack Dev', init:'AY', color:'#2563eb'},
      {name:'Md Monowarul Aziz',    role:'Backend Developer',   init:'MA', color:'#7c3aed'},
      {name:'Tandra Pramanik',      role:'Frontend Developer',  init:'TP', color:'#0891b2'},
      {name:'A H M Al Toufiq Noor',role:'UI/UX Designer',      init:'TN', color:'#059669'},
    ];

    f.innerHTML = `
      <div class="mf-ft-inner">
        <!-- Top grid: Brand | Platform | Legal | Admin | Contact -->
        <div class="mf-ft-grid">

          <!-- Brand -->
          <div class="mf-ft-brand">
            <a href="${base}index.html" style="display:inline-flex;align-items:center;gap:8px;margin-bottom:1rem;text-decoration:none;">
              <img src="${base}assets/medfind-logo.png" alt="MedFind" style="height:42px;width:auto;object-fit:contain;filter:brightness(1.15);">
              <span style="font-size:1.25rem;font-weight:700;color:#60a5fa;">Med<strong style="color:#a78bfa;">Find</strong></span>
            </a>
            <p style="font-size:.83rem;color:#94a3b8;line-height:1.7;max-width:270px;margin-bottom:1.2rem;">
              Bangladesh's trusted digital healthcare platform — connecting patients with verified doctors and hospitals nationwide.
            </p>
            <div style="display:flex;gap:8px;margin-bottom:1.4rem;">
              ${['fab fa-facebook-f','fab fa-twitter','fab fa-linkedin-in','fab fa-instagram'].map(ic=>
                `<a href="#" style="width:33px;height:33px;border-radius:50%;background:rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;color:#fff;transition:all .2s;" onmouseover="this.style.background='#2563eb'" onmouseout="this.style.background='rgba(255,255,255,.08)'"><i class="${ic}"></i></a>`
              ).join('')}
            </div>
            <!-- Emergency box -->
            <div style="background:rgba(220,38,38,.1);border:1px solid rgba(220,38,38,.25);border-radius:12px;padding:12px 14px;">
              <div style="font-size:.72rem;font-weight:700;color:#fca5a5;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px;">🚨 Emergency</div>
              <a href="tel:999" style="display:block;color:#fca5a5;font-size:.84rem;font-weight:700;text-decoration:none;margin-bottom:4px;">999 — National Emergency</a>
              <a href="tel:+8801772172829" style="display:block;color:#fca5a5;font-size:.82rem;text-decoration:none;margin-bottom:4px;">📞 MedFind: 01772-172829</a>
              <a href="tel:029667722" style="display:block;color:#94a3b8;font-size:.81rem;text-decoration:none;margin-bottom:4px;">🏥 Dhaka Medical: 02-9667722</a>
              <a href="mailto:medfindbd2026@gmail.com" style="display:block;color:#94a3b8;font-size:.81rem;text-decoration:none;">✉️ medfindbd2026@gmail.com</a>
            </div>
          </div>

          <!-- Platform -->
          <div>
            <div style="${colHead}">Platform</div>
            <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:.5rem;">
              ${platform.map(([n,h])=>`<li><a href="${base}${h}" style="${linkStyle}" onmouseover="${hoverIn}" onmouseout="${hoverOut}">${n}</a></li>`).join('')}
            </ul>
          </div>

          <!-- Legal -->
          <div>
            <div style="${colHead}">Legal</div>
            <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:.5rem;">
              ${legal.map(([n,h])=>`<li><a href="${base}${h}" style="${linkStyle}" onmouseover="${hoverIn}" onmouseout="${hoverOut}">${n}</a></li>`).join('')}
            </ul>
          </div>

          <!-- Admin / Quick Links -->
          <div>
            <div style="${colHead}">Admin & Tools</div>
            <ul style="list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:.5rem;">
              ${admin.map(([n,h])=>`<li><a href="${base}${h}" style="${linkStyle}" onmouseover="${hoverIn}" onmouseout="${hoverOut}">${n}</a></li>`).join('')}
            </ul>
          </div>

          <!-- Contact + Dev Team -->
          <div>
            <div style="${colHead}">Contact</div>
            <div style="display:flex;flex-direction:column;gap:9px;font-size:.83rem;color:#94a3b8;margin-bottom:1.2rem;">
              <div style="display:flex;gap:8px;align-items:center;"><i class="fas fa-phone" style="color:#2563eb;width:14px;"></i> 01772-172829</div>
              <div style="display:flex;gap:8px;align-items:center;"><i class="fas fa-phone" style="color:#2563eb;width:14px;"></i> 01820-832814</div>
              <div style="display:flex;gap:8px;align-items:center;"><i class="fas fa-envelope" style="color:#2563eb;width:14px;"></i> medfindbd2026@gmail.com</div>
              <div style="display:flex;gap:8px;align-items:center;"><i class="fas fa-map-marker-alt" style="color:#2563eb;width:14px;"></i> Dhaka, Bangladesh</div>
              <div style="display:flex;gap:8px;align-items:center;"><i class="fas fa-clock" style="color:#2563eb;width:14px;"></i> 24/7 Support</div>
            </div>
            <!-- Dev Team card -->
            <div style="padding:14px;background:linear-gradient(135deg,rgba(37,99,235,.13),rgba(99,102,241,.10));border-radius:14px;border:1px solid rgba(99,130,235,.18);">
              <div style="display:flex;align-items:center;gap:6px;margin-bottom:10px;">
                <div style="width:22px;height:22px;border-radius:6px;background:linear-gradient(135deg,#2563eb,#6366f1);display:flex;align-items:center;justify-content:center;font-size:.6rem;color:#fff;"><i class="fas fa-code"></i></div>
                <span style="color:#93c5fd;font-size:.72rem;font-weight:700;letter-spacing:.05em;text-transform:uppercase;">Dev Team</span>
              </div>
              <div style="display:flex;flex-direction:column;gap:8px;">
                ${team.map(m=>`
                  <div style="display:flex;align-items:center;gap:8px;">
                    <div style="width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,${m.color},${m.color}99);display:flex;align-items:center;justify-content:center;font-size:.6rem;font-weight:700;color:#fff;flex-shrink:0;box-shadow:0 2px 6px ${m.color}55;">${m.init}</div>
                    <div>
                      <div style="font-size:.73rem;color:#cbd5e1;font-weight:600;line-height:1.2;">${m.name}</div>
                      <div style="font-size:.63rem;color:#64748b;line-height:1.2;">${m.role}</div>
                    </div>
                  </div>`).join('')}
              </div>
            </div>
          </div>

        </div>

        <!-- Bottom bar -->
        <div style="border-top:1px solid rgba(255,255,255,.07);padding:1.1rem 0;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.8rem;font-size:.78rem;color:#64748b;">
          <p>© 2026 MedFind Bangladesh. All rights reserved. Not a substitute for professional medical advice. Made with <i class="fas fa-heart" style="color:#ef4444;"></i> in Bangladesh | DGHS Compliant</p>
          <nav style="display:flex;gap:1.2rem;">
            <a href="${base}pages/privacy.html" style="color:#64748b;text-decoration:none;" onmouseover="this.style.color='#93c5fd'" onmouseout="this.style.color='#64748b'">Privacy</a>
            <a href="${base}pages/terms.html" style="color:#64748b;text-decoration:none;" onmouseover="this.style.color='#93c5fd'" onmouseout="this.style.color='#64748b'">Terms</a>
            <a href="${base}pages/cookies.html" style="color:#64748b;text-decoration:none;" onmouseover="this.style.color='#93c5fd'" onmouseout="this.style.color='#64748b'">Cookies</a>
          </nav>
        </div>
      </div>`;

    if (!document.getElementById('mf-ft-css')) {
      const s = document.createElement('style');
      s.id = 'mf-ft-css';
      s.textContent = `
        #mfFooter{background:linear-gradient(135deg,#0f172a,#1e293b);padding:3.5rem 0 0;font-family:'Inter',sans-serif;}
        .mf-ft-inner{max-width:1280px;margin:0 auto;padding:0 1.5rem;}
        .mf-ft-grid{display:grid;grid-template-columns:1.6fr 1fr 1fr 1fr 1.35fr;gap:2rem;padding-bottom:2.5rem;}
        @media(max-width:1100px){.mf-ft-grid{grid-template-columns:1fr 1fr 1fr;}}
        @media(max-width:700px){.mf-ft-grid{grid-template-columns:1fr 1fr;}}
        @media(max-width:480px){.mf-ft-grid{grid-template-columns:1fr;}}
        .mf-ft-brand{grid-column:1;}
      `;
      document.head.appendChild(s);
    }
    document.body.appendChild(f);
    // ── AI FLOATING BUTTON ──
    if (!document.getElementById('mfAiBtn')) {
      const aiBtn = document.createElement('a');
      aiBtn.id = 'mfAiBtn';
      aiBtn.href = base + 'pages/medfind-ai.html';
      aiBtn.title = 'MedFind AI Health Assistant';
      aiBtn.innerHTML = '⚕️';
      aiBtn.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:800;width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,#0891b2,#00d4aa);display:flex;align-items:center;justify-content:center;font-size:1.4rem;box-shadow:0 4px 20px rgba(0,212,170,.4);text-decoration:none;transition:all .2s;animation:aiPulse 2.5s ease-in-out infinite;';
      const s = document.createElement('style');
      s.textContent = '@keyframes aiPulse{0%,100%{box-shadow:0 4px 20px rgba(0,212,170,.4)}50%{box-shadow:0 4px 32px rgba(0,212,170,.7),0 0 0 8px rgba(0,212,170,.1)}}';
      document.head.appendChild(s);
      aiBtn.onmouseover = () => { aiBtn.style.transform = 'scale(1.12)'; };
      aiBtn.onmouseout  = () => { aiBtn.style.transform = 'scale(1)'; };
      document.body.appendChild(aiBtn);
    }
  },

  // ── TOAST ───────────────────────────────────────────────
  injectToastContainer() {
    if (document.getElementById('mfToasts')) return;
    const c = document.createElement('div');
    c.id = 'mfToasts';
    c.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;display:flex;flex-direction:column;gap:10px;max-width:380px;pointer-events:none;';
    document.body.appendChild(c);
    const s = document.createElement('style');
    s.textContent = `.mf-toast{background:#fff;border-radius:14px;padding:13px 16px;box-shadow:0 8px 32px rgba(0,0,0,.14);display:flex;align-items:flex-start;gap:11px;pointer-events:all;animation:mfTSlide .3s ease;border-left:4px solid #2563eb;}.mf-toast.success{border-left-color:#10b981;}.mf-toast.error{border-left-color:#ef4444;}.mf-toast.warning{border-left-color:#f59e0b;}.mf-toast i{font-size:1rem;margin-top:2px;flex-shrink:0;}.mf-toast.success i{color:#10b981;}.mf-toast.error i{color:#ef4444;}.mf-toast.warning i{color:#f59e0b;}.mf-toast.info i{color:#2563eb;}.mf-toast-body{flex:1;}.mf-toast-title{font-size:.84rem;font-weight:700;color:#0f172a;margin-bottom:2px;}.mf-toast-msg{font-size:.8rem;color:#475569;line-height:1.45;}.mf-toast-close{background:none;border:none;color:#94a3b8;cursor:pointer;font-size:1rem;padding:0 3px;flex-shrink:0;}@keyframes mfTSlide{from{opacity:0;transform:translateX(18px);}to{opacity:1;transform:none;}}`;
    document.head.appendChild(s);
  },

  toast(msg, type='info', title='', ms=4500) {
    const c = document.getElementById('mfToasts');
    if (!c) return;
    const icons = {success:'fa-check-circle',error:'fa-exclamation-circle',warning:'fa-exclamation-triangle',info:'fa-info-circle'};
    const el = document.createElement('div');
    el.className = `mf-toast ${type}`;
    el.innerHTML = `<i class="fas ${icons[type]||icons.info}"></i><div class="mf-toast-body">${title?`<div class="mf-toast-title">${title}</div>`:''}<div class="mf-toast-msg">${msg}</div></div><button class="mf-toast-close" onclick="this.parentElement.remove()">&times;</button>`;
    c.appendChild(el);
    setTimeout(() => el.remove(), ms);
  },

  // ── AUTH ────────────────────────────────────────────────
  getCurrentUser() { try { return JSON.parse(localStorage.getItem('mf_user')||'null'); } catch { return null; } },
  getToken()       { return localStorage.getItem('mf_token'); },
  isLoggedIn()     { return !!(this.getCurrentUser() && this.getToken()); },
  saveUser(u,t)    { localStorage.setItem('mf_user',JSON.stringify(u)); localStorage.setItem('mf_token',t); },
  logout() {
    localStorage.removeItem('mf_user');
    localStorage.removeItem('mf_token');
    this.toast('Logged out successfully','info');
    setTimeout(() => location.href = this.getBasePath()+'pages/login.html', 800);
  },

  setupAuth() {
    const guarded = ['patients/dashboard','patients/appointments','patients/medical','admin/dashboard','hospital/admin'];
    const p = location.pathname;
    if (guarded.some(g => p.includes(g)) && !this.isLoggedIn()) {
      location.href = this.getBasePath() + 'pages/login.html?redirect=' + encodeURIComponent(location.href);
    }
  },

  // ── API ─────────────────────────────────────────────────
  async apiCall(endpoint, opts={}) {
    const tok = this.getToken();
    const res = await fetch(this.API_BASE + endpoint, {
      headers: { 'Content-Type':'application/json', ...(tok?{Authorization:'Bearer '+tok}:{}), ...(opts.headers||{}) },
      ...opts
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.message||data.detail||'Server error');
    return data;
  }
};

document.addEventListener('DOMContentLoaded', () => MedFindComponents.init());
window.MFC = MedFindComponents;

/* ── PAGE PROGRESS LOADER ── */
(function() {
  const bar = document.createElement('div');
  bar.id = 'mf-progress';
  Object.assign(bar.style, {
    position: 'fixed', top: '0', left: '0', height: '3px', width: '0',
    background: 'linear-gradient(90deg, #2563eb, #7c3aed)',
    zIndex: '99999', transition: 'width 0.3s ease', pointerEvents: 'none',
    boxShadow: '0 0 8px rgba(37,99,235,0.6)'
  });
  document.addEventListener('DOMContentLoaded', () => {
    document.body.prepend(bar);
    bar.style.width = '30%';
    setTimeout(() => bar.style.width = '70%', 200);
    window.addEventListener('load', () => {
      bar.style.width = '100%';
      setTimeout(() => { bar.style.opacity = '0'; setTimeout(() => bar.remove(), 400); }, 300);
    });
  });
})();

/* ── GLOBAL EMERGENCY SHORTCUT ── */
document.addEventListener('DOMContentLoaded', function() {
  // Add emergency floating button
  const isMap = location.pathname.includes('viewmaps');
  if (!isMap) {
    const emBtn = document.createElement('a');
    emBtn.href = (MedFindComponents?.getBasePath?.() || '../') + 'pages/patients/viewmaps.html?emergency=true';
    emBtn.innerHTML = '<i class="fas fa-ambulance"></i>';
    emBtn.title = 'Emergency — Find Nearest Hospital';
    Object.assign(emBtn.style, {
      position: 'fixed', bottom: '24px', right: '24px', zIndex: '8000',
      width: '54px', height: '54px', background: 'linear-gradient(135deg, #dc2626, #ef4444)',
      color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center',
      justifyContent: 'center', fontSize: '1.3rem', textDecoration: 'none',
      boxShadow: '0 4px 20px rgba(220,38,38,0.5)',
      animation: 'emBtnPulse 3s ease-in-out infinite',
    });
    const style = document.createElement('style');
    style.textContent = '@keyframes emBtnPulse { 0%,100% { box-shadow: 0 4px 20px rgba(220,38,38,.5); } 50% { box-shadow: 0 4px 30px rgba(220,38,38,.8), 0 0 0 12px rgba(220,38,38,.1); } }';
    document.head.appendChild(style);
    document.body.appendChild(emBtn);
  }
});


/* ════════════════════════════════════════════════════════════
   ██████╗  █████╗ ██████╗  ██████╗ ██████╗ ██╗  ██╗ █████╗ ███╗
   ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝██╔══██╗████╗
   ██████╔╝███████║██████╔╝██║   ██║██████╔╝█████╔╝ ███████║██╔██╗
   ██╔══██╗██╔══██║██╔══██╗██║   ██║██╔══██╗██╔═██╗ ██╔══██║██║╚██╗
   ██████╔╝██║  ██║██████╔╝╚██████╔╝██║  ██║██║  ██╗██║  ██║██║ ╚█║
   ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚╝
   ─────────────────────────────────────────────────────────────────
   DEVELOPER : Ahsanul Yamin Babor
   ROLE      : Lead Full Stack Developer
   EMAIL     : ahsanulyaminbabor@gmail.com
   GITHUB    : https://github.com/Baborkhan
   PROJECT   : MedFind Healthcare Platform — Bangladesh
   BUILT WITH: Django + DRF + PostgreSQL + Redis + Pandas + NumPy
   ─────────────────────────────────────────────────────────────────
   ⚠️  ATTRIBUTION NOTICE: Removing or altering this developer
       credit violates the attribution agreement embedded in
       this codebase. The MutationObserver guard will re-inject
       this signature if removed from the DOM.
════════════════════════════════════════════════════════════ */
(function MedFindDevSignature() {
  "use strict";

  const DEV = {
    name:   "Ahsanul Yamin Babor",
    role:   "Lead Full Stack Developer",
    email:  "ahsanulyaminbabor@gmail.com",
    github: "https://github.com/Baborkhan",
    initials: "AYB",
    project: "MedFind Healthcare Platform",
    year:   2026,
  };

  function injectCSS() {
    if (document.getElementById("mf-dev-css")) return;
    const s = document.createElement("style");
    s.id = "mf-dev-css";
    s.textContent = `
      #mf-dev-bar {
        font-family: 'Inter', sans-serif;
        background: #060b18;
        border-top: 1px solid rgba(255,255,255,.06);
        position: relative;
        overflow: hidden;
        z-index: 9999;
      }
      #mf-dev-bar::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #0d9488, #f59e0b, #ef4444, #4f46e5);
        background-size: 300% 100%;
        animation: mf-rainbow 5s linear infinite;
      }
      @keyframes mf-rainbow { 0%{background-position:0% 0%} 100%{background-position:300% 0%} }
      #mf-dev-bar .mf-inner {
        max-width: 1400px; margin: 0 auto;
        padding: 12px 24px;
        display: flex; align-items: center;
        justify-content: space-between; flex-wrap: wrap; gap: 12px;
      }
      #mf-dev-bar .mf-left { display: flex; align-items: center; gap: 12px; }
      #mf-dev-bar .mf-ava {
        width: 44px; height: 44px; border-radius: 50%;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        display: flex; align-items: center; justify-content: center;
        font-weight: 900; font-size: .95rem; color: #fff;
        box-shadow: 0 0 0 2px rgba(79,70,229,.4), 0 0 0 4px rgba(79,70,229,.12);
        flex-shrink: 0; letter-spacing: -.5px;
        animation: mf-pulse-ava 3s ease-in-out infinite;
      }
      @keyframes mf-pulse-ava {
        0%,100%{box-shadow:0 0 0 2px rgba(79,70,229,.4),0 0 0 4px rgba(79,70,229,.12)}
        50%{box-shadow:0 0 0 3px rgba(79,70,229,.6),0 0 0 8px rgba(79,70,229,.05)}
      }
      #mf-dev-bar .mf-badge {
        font-size: .63rem; font-weight: 700; letter-spacing: .6px;
        text-transform: uppercase; color: #818cf8; margin-bottom: 2px;
        display: flex; align-items: center; gap: 4px;
      }
      #mf-dev-bar .mf-name {
        font-size: .92rem; font-weight: 800; color: #e2e8f0; letter-spacing: -.2px;
      }
      #mf-dev-bar .mf-links { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
      #mf-dev-bar .mf-link {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 6px 14px; border-radius: 100px; font-size: .73rem;
        font-weight: 700; text-decoration: none; transition: all .2s; white-space: nowrap;
      }
      #mf-dev-bar .mf-link.email {
        background: rgba(79,70,229,.14); color: #818cf8;
        border: 1px solid rgba(79,70,229,.28);
      }
      #mf-dev-bar .mf-link.email:hover {
        background: rgba(79,70,229,.28); color: #fff;
        box-shadow: 0 0 14px rgba(79,70,229,.3);
        transform: translateY(-1px);
      }
      #mf-dev-bar .mf-link.github {
        background: rgba(255,255,255,.06); color: #94a3b8;
        border: 1px solid rgba(255,255,255,.1);
      }
      #mf-dev-bar .mf-link.github:hover {
        background: rgba(255,255,255,.12); color: #fff;
        border-color: rgba(255,255,255,.2);
        transform: translateY(-1px);
      }
      #mf-dev-bar .mf-shield {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 5px 10px; background: rgba(16,185,129,.1);
        border: 1px solid rgba(16,185,129,.2); border-radius: 100px;
        font-size: .67rem; font-weight: 800; color: #10b981; letter-spacing: .3px;
      }
      #mf-dev-bar .mf-copy {
        font-size: .69rem; color: #334155;
        display: flex; align-items: center; gap: 6px; flex-wrap: wrap;
      }
      #mf-dev-bar .mf-copy strong { color: #475569; font-weight: 700; }
      #mf-dev-bar .mf-dot {
        width: 3px; height: 3px; border-radius: 50%; background: #334155; display: inline-block;
      }
      @media(max-width:640px) {
        #mf-dev-bar .mf-inner { justify-content: center; text-align: center; }
        #mf-dev-bar .mf-left { flex-direction: column; align-items: center; }
        #mf-dev-bar .mf-links { justify-content: center; }
        #mf-dev-bar .mf-copy { justify-content: center; }
      }
    `;
    document.head.appendChild(s);
  }

  function injectBar() {
    if (document.getElementById("mf-dev-bar")) return;
    injectCSS();
    const bar = document.createElement("div");
    bar.id = "mf-dev-bar";
    bar.setAttribute("data-dev", "ahsanulyaminbabor");
    bar.setAttribute("data-github", "Baborkhan");
    bar.setAttribute("data-protected", "true");
    bar.innerHTML = `
      <div class="mf-inner">
        <div class="mf-left">
          <div class="mf-ava" title="${DEV.name}">${DEV.initials}</div>
          <div>
            <div class="mf-badge">
              <svg width="10" height="10" viewBox="0 0 10 10" fill="#818cf8"><path d="M5 0L6.12 3.38H9.51L6.82 5.49L7.94 8.87L5 6.76L2.06 8.87L3.18 5.49L0.49 3.38H3.88L5 0Z"/></svg>
              Full Stack Developer
            </div>
            <div class="mf-name">${DEV.name}</div>
          </div>
        </div>

        <div class="mf-links">
          <a href="mailto:${DEV.email}" class="mf-link email">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
            ${DEV.email}
          </a>
          <a href="${DEV.github}" target="_blank" rel="noopener" class="mf-link github">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
            github.com/Baborkhan
          </a>
          <span class="mf-shield">
            <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            Protected Credit
          </span>
        </div>

        <div class="mf-copy">
          <span>© ${DEV.year} ${DEV.project}</span>
          <span class="mf-dot"></span>
          <strong>Developed by ${DEV.name}</strong>
          <span class="mf-dot"></span>
          <span>All rights reserved</span>
        </div>
      </div>
    `;
    document.body.appendChild(bar);

    // Console watermark
color:#fff;font-size:13px;font-weight:800;padding:6px 16px;border-radius:6px;letter-spacing:-.2px"
    );
  }

  // ── MutationObserver guard — re-injects if removed ──────────
  function startGuard() {
    const obs = new MutationObserver((mutations) => {
      for (const m of mutations) {
        for (const node of m.removedNodes) {
          if (node.id === "mf-dev-bar" || node.id === "mf-dev-css") {
            setTimeout(injectBar, 80);
            return;
          }
        }
      }
    });
    obs.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => { injectBar(); startGuard(); });
  } else {
    injectBar(); startGuard();
  }
})();
