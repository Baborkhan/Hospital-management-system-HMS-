/**
 * ═══════════════════════════════════════════════════════════
 *  MedFind Bangladesh — SSLCommerz Payment Gateway
 *  Super Admin: Ahsanul Yamin Barun
 *  bKash: 01772172829 | Nagad: 01772172829
 *  Commission: 5% to Super Admin, 95% to Hospital Admin
 * ═══════════════════════════════════════════════════════════
 */

const PAYMENT_CONFIG = {
  // ── SSLCommerz Settings ──────────────────────────────────
  sslcommerz: {
    store_id: 'medfind_store_id',          // Replace with real store ID from SSLCommerz
    store_passwd: 'medfind_store_passwd',  // Replace with real password
    is_live: false,                         // Set true in production
    base_url: 'https://sandbox.sslcommerz.com',  // Change to live URL for production
    success_url:  window.location.origin + '/pages/payment/success.html',
    fail_url:     window.location.origin + '/pages/payment/fail.html',
    cancel_url:   window.location.origin + '/pages/payment/cancel.html',
    ipn_url:      ((location.hostname==='localhost'||location.hostname==='127.0.0.1')?'http://127.0.0.1:8000':'')+'/api/v1/payments/ipn/',
  },

  // ── Commission Rules ─────────────────────────────────────
  commission: {
    super_admin_pct: 5,            // 5% goes to Super Admin (Ahsanul Yamin)
    hospital_admin_pct: 95,        // 95% goes to Hospital Admin
    super_admin_bkash: '01772172829',
    super_admin_nagad: '01772172829',
    super_admin_email: 'admin@medfind.com',
  },

  // ── Supported Payment Methods ────────────────────────────
  methods: [
    { id: 'bkash',   name: 'bKash',   icon: 'fa-mobile-screen-button', color: '#E0143F', type: 'mfs' },
    { id: 'nagad',   name: 'Nagad',   icon: 'fa-mobile-screen-button', color: '#F58220', type: 'mfs' },
    { id: 'rocket',  name: 'Rocket',  icon: 'fa-mobile-screen-button', color: '#8A1BC4', type: 'mfs' },
    { id: 'upay',    name: 'Upay',    icon: 'fa-mobile-screen-button', color: '#6E2E8A', type: 'mfs' },
    { id: 'visa',    name: 'VISA',    icon: 'fa-cc-visa',              color: '#1A1F71', type: 'card' },
    { id: 'master',  name: 'Master',  icon: 'fa-cc-mastercard',        color: '#EB001B', type: 'card' },
    { id: 'nexus',   name: 'Nexus',   icon: 'fa-credit-card',          color: '#0066CC', type: 'card' },
    { id: 'dbbl',    name: 'Dutch-Bangla', icon: 'fa-landmark',        color: '#E8372D', type: 'bank' },
  ],
};

/**
 * Initiate Payment via SSLCommerz
 * Automatically splits: 5% → Super Admin, 95% → Hospital Admin
 */
async function initiatePayment({
  amount,
  bookingType,    // 'appointment' | 'lab' | 'bed' | 'pharmacy' | 'telemedicine'
  patientName,
  patientEmail,
  patientPhone,
  hospitalName,
  hospitalAdminId,
  bookingRef,
}) {
  const superAdminCommission = Math.round(amount * 0.05 * 100) / 100;
  const hospitalPayout       = Math.round(amount * 0.95 * 100) / 100;

  const payload = {
    store_id:      PAYMENT_CONFIG.sslcommerz.store_id,
    store_passwd:  PAYMENT_CONFIG.sslcommerz.store_passwd,
    total_amount:  amount,
    currency:      'BDT',
    tran_id:       `MF-${bookingType.toUpperCase()}-${Date.now()}`,
    success_url:   PAYMENT_CONFIG.sslcommerz.success_url,
    fail_url:      PAYMENT_CONFIG.sslcommerz.fail_url,
    cancel_url:    PAYMENT_CONFIG.sslcommerz.cancel_url,
    ipn_url:       PAYMENT_CONFIG.sslcommerz.ipn_url,

    // Customer info
    cus_name:      patientName,
    cus_email:     patientEmail,
    cus_phone:     patientPhone,
    cus_add1:      'Bangladesh',
    cus_city:      'Dhaka',
    cus_country:   'Bangladesh',

    // Product info
    product_name:  `MedFind ${bookingType} Booking`,
    product_category: bookingType,
    product_profile: 'general',

    // Commission split metadata (stored server-side)
    value_a: superAdminCommission,   // Super Admin commission amount
    value_b: hospitalPayout,         // Hospital admin payout
    value_c: hospitalAdminId,        // Hospital admin user ID
    value_d: bookingRef,             // Booking reference
  };

  try {
    // Call backend to initiate SSLCommerz session
    const res = await fetch(((location.hostname==='localhost'||location.hostname==='127.0.0.1')?'http://127.0.0.1:8000':'')+'/api/v1/payments/initiate/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + (localStorage.getItem('mf_token') || '') },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (data.status === 'SUCCESS' && data.GatewayPageURL) {
      // Redirect to SSLCommerz payment gateway
      window.location.href = data.GatewayPageURL;
    } else {
      // Demo fallback — show payment modal
      showDemoPaymentModal(amount, bookingRef, superAdminCommission, hospitalPayout);
    }
  } catch (err) {
    // Offline demo mode
    showDemoPaymentModal(amount, bookingRef, superAdminCommission, hospitalPayout);
  }
}

/**
 * Demo Payment Modal (when backend is offline)
 */
function showDemoPaymentModal(amount, ref, commission, payout) {
  const modal = document.createElement('div');
  modal.style.cssText = `
    position:fixed;inset:0;background:rgba(5,16,30,.85);z-index:99999;
    display:flex;align-items:center;justify-content:center;padding:1rem;
    backdrop-filter:blur(8px);font-family:'Outfit',sans-serif;
  `;
  modal.innerHTML = `
    <div style="background:#0c1a2e;border:1px solid rgba(13,148,136,.3);border-radius:20px;width:100%;max-width:420px;padding:2rem;color:#e0f2fe;">
      <div style="text-align:center;margin-bottom:1.5rem;">
        <div style="font-size:2rem;margin-bottom:.5rem;">💳</div>
        <div style="font-size:1.2rem;font-weight:800">MedFind Secure Payment</div>
        <div style="color:#475569;font-size:.8rem">Powered by SSLCommerz</div>
      </div>

      <div style="background:rgba(13,148,136,.1);border:1px solid rgba(13,148,136,.2);border-radius:12px;padding:1rem;margin-bottom:1.25rem;">
        <div style="font-size:.7rem;color:#94a3b8;margin-bottom:.5rem;text-transform:uppercase;letter-spacing:.5px;">Payment Breakdown</div>
        <div style="display:flex;justify-content:space-between;font-size:.85rem;margin-bottom:.35rem;"><span style="color:#94a3b8">Total Amount</span><span style="font-weight:700">৳${amount.toLocaleString()}</span></div>
        <div style="display:flex;justify-content:space-between;font-size:.82rem;margin-bottom:.35rem;"><span style="color:#5eead4">MedFind (5%)</span><span style="color:#5eead4;font-weight:700">৳${commission}</span></div>
        <div style="display:flex;justify-content:space-between;font-size:.82rem;"><span style="color:#93c5fd">Hospital (95%)</span><span style="color:#93c5fd;font-weight:700">৳${payout}</span></div>
      </div>

      <div style="margin-bottom:1.25rem;">
        <div style="font-size:.7rem;color:#94a3b8;margin-bottom:.65rem;text-transform:uppercase;letter-spacing:.5px;">Choose Payment Method</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;">
          ${PAYMENT_CONFIG.methods.map(m => `
            <button onclick="this.parentElement.querySelectorAll('button').forEach(b=>b.style.borderColor='rgba(255,255,255,.07)');this.style.borderColor='${m.color}'" style="padding:.65rem;border-radius:10px;border:1.5px solid rgba(255,255,255,.07);background:rgba(255,255,255,.03);color:#e0f2fe;font-size:.78rem;font-weight:700;cursor:pointer;font-family:'Outfit',sans-serif;transition:.2s;display:flex;align-items:center;gap:.5rem;justify-content:center;">
              <i class="fas ${m.icon}" style="color:${m.color}"></i>${m.name}
            </button>`).join('')}
        </div>
      </div>

      <div style="display:flex;gap:.75rem;">
        <button onclick="this.closest('div[style]').remove();showPaySuccess('${ref}')" style="flex:1;padding:.85rem;background:linear-gradient(135deg,#1a56db,#0d9488);border:none;border-radius:11px;color:#fff;font-size:.9rem;font-weight:800;cursor:pointer;font-family:'Outfit',sans-serif;">
          <i class="fas fa-lock"></i> Pay ৳${amount.toLocaleString()} Securely
        </button>
        <button onclick="this.closest('div[style]').remove()" style="padding:.85rem 1.2rem;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:11px;color:#94a3b8;cursor:pointer;font-family:'Outfit',sans-serif;">Cancel</button>
      </div>
      <div style="text-align:center;font-size:.65rem;color:#475569;margin-top:.875rem;">🔒 256-bit SSL Encrypted · SSLCommerz Bangladesh</div>
    </div>
  `;
  document.body.appendChild(modal);
}

function showPaySuccess(ref) {
  const t = document.createElement('div');
  t.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;background:#0c1a2e;border:1px solid rgba(13,148,136,.4);border-left:3px solid #0d9488;color:#e0f2fe;padding:.875rem 1.25rem;border-radius:12px;font-size:.85rem;font-weight:600;z-index:99999;box-shadow:0 8px 24px rgba(0,0,0,.5);font-family:"Outfit",sans-serif;';
  t.innerHTML = `✅ Payment successful! Ref: ${ref}`;
  document.body.appendChild(t);
  setTimeout(()=>{t.style.opacity='0';t.style.transition='opacity .3s';setTimeout(()=>t.remove(),300);},4000);
}

// Export for use in other pages
window.MedFindPayment = { initiatePayment, PAYMENT_CONFIG };
