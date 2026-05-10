/**
 * MedFind API Service
 * Connects frontend to Django REST backend at http://localhost:8000/api/v1
 */

const API_BASE = (function() {
  if (window.MEDFIND_CONFIG && window.MEDFIND_CONFIG.API_BASE) return window.MEDFIND_CONFIG.API_BASE;
  const isLocal = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
  return isLocal ? 'http://127.0.0.1:8000/api/v1' : '/api/v1';
})();

const MedFindAPI = {

  _token: localStorage.getItem("mf_token"),

  _headers(extra = {}) {
    const h = { "Content-Type": "application/json", ...extra };
    if (this._token) h["Authorization"] = `Bearer ${this._token}`;
    return h;
  },

  async _req(path, options = {}) {
    try {
      const res = await fetch(API_BASE + path, {
        headers: this._headers(options.headers || {}),
        ...options,
        body: options.body ? JSON.stringify(options.body) : undefined,
      });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.message || data.detail || "Request failed");
      return data;
    } catch (err) {
      console.error("[MedFindAPI]", path, err.message);
      throw err;
    }
  },

  // ── AUTH ──
  async register(payload) { return this._req("/accounts/register/", { method: "POST", body: payload }); },
  async login(email, password) {
    const res = await this._req("/accounts/login/", { method: "POST", body: { email, password } });
    if (res.token) { this._token = res.token; localStorage.setItem("mf_token", res.token); }
    if (res.user) localStorage.setItem("mf_user", JSON.stringify(res.user));
    return res;
  },
  logout() { this._token = null; localStorage.removeItem("mf_token"); localStorage.removeItem("mf_user"); },
  getUser() { try { return JSON.parse(localStorage.getItem("mf_user")); } catch { return null; } },

  // ── HOSPITALS ──
  async getHospitals(params = {}) { return this._req("/hospitals/?" + new URLSearchParams(params)); },
  async getHospital(id) { return this._req(`/hospitals/${id}/`); },
  async getNearby(lat, lng, radius = 20) { return this._req(`/hospitals/nearby/?lat=${lat}&lng=${lng}&radius=${radius}`); },
  async updateAvailability(id, data) { return this._req(`/hospitals/${id}/availability/`, { method: "PUT", body: data }); },

  // ── DOCTORS ──
  async getDoctors(params = {}) { return this._req("/doctors/?" + new URLSearchParams(params)); },
  async getDoctor(id) { return this._req(`/doctors/${id}/`); },

  // ── APPOINTMENTS ──
  async getAppointments(params = {}) { return this._req("/appointments/?" + new URLSearchParams(params)); },
  async createAppointment(data) { return this._req("/appointments/", { method: "POST", body: data }); },
  async updateAppointment(id, data) { return this._req(`/appointments/${id}/`, { method: "PATCH", body: data }); },
  async getAppointmentStats() { return this._req("/appointments/stats/"); },

  // ── PHARMACY ──
  async getMedicines(params = {}) { return this._req("/pharmacy/medicines/?" + new URLSearchParams(params)); },
  async createOrder(data) { return this._req("/pharmacy/orders/", { method: "POST", body: data }); },
  async getOrders(params = {}) { return this._req("/pharmacy/orders/?" + new URLSearchParams(params)); },
  async updateOrderStatus(id, status) { return this._req(`/pharmacy/orders/${id}/`, { method: "PATCH", body: { status } }); },

  // ── LAB TESTS ──
  async getLabTests(params = {}) { return this._req("/labs/tests/?" + new URLSearchParams(params)); },
  async bookLabTest(data) { return this._req("/labs/bookings/", { method: "POST", body: data }); },

  // ── BILLING ──
  async createInvoice(data) { return this._req("/billing/invoices/", { method: "POST", body: data }); },
  async getInvoices(params = {}) { return this._req("/billing/invoices/?" + new URLSearchParams(params)); },
  async updateInvoice(id, data) { return this._req(`/billing/invoices/${id}/`, { method: "PATCH", body: data }); },

  // ── ANALYTICS ──
  async getDashboardSummary() { return this._req("/analytics/dashboard/"); },
  async getPlatformAnalytics() { return this._req("/analytics/platform/"); },
  async getHospitalAnalytics(hospital_id) { return this._req(`/analytics/hospitals/${hospital_id ? "?hospital_id=" + hospital_id : ""}`); },

  // ── REVIEWS ──
  async getReviews(params = {}) { return this._req("/reviews/?" + new URLSearchParams(params)); },
  async createReview(data) { return this._req("/reviews/", { method: "POST", body: data }); },

  // ── RECORDS ──
  async getRecords(patient_id) { return this._req(`/records/?patient=${patient_id}`); },
  async createRecord(data) { return this._req("/records/", { method: "POST", body: data }); },

  // ── LOCATIONS ──
  async getDivisions() { return this._req("/locations/divisions/"); },

  // ── NOTIFICATIONS ──
  async getNotifications(user_id) { return this._req(`/notifications/?user_id=${user_id}`); },
  async markRead(ids) { return this._req("/notifications/", { method: "POST", body: { ids } }); },

  // ── TELEMEDICINE ──
  async createVideoSession(appointment_id) { return this._req("/telemedicine/sessions/", { method: "POST", body: { appointment_id } }); },
};

// Make globally available
window.MedFindAPI = MedFindAPI;
window.API_BASE_URL = API_BASE; // legacy compat
