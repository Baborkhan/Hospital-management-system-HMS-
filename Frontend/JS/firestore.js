/**
 * MedFind — Firestore Database Service
 * Project: medfind-bangladesh
 * Database: (default) — Firestore
 *
 * Collections Structure:
 * ├── users/{uid}              → all user profiles (patients, doctors, admins)
 * ├── appointments/{id}        → appointments
 * ├── doctors/{uid}            → doctor profiles & schedules
 * ├── hospitals/{id}           → hospital data
 * ├── organ_donors/{id}        → voluntary organ donor registrations
 * ├── blood_requests/{id}      → blood donation requests
 * ├── lab_tests/{id}           → lab test bookings
 * └── notifications/{uid}/{id} → per-user notifications
 */

'use strict';

/* ══════════════════════════════════════════════════════════════
   INIT — Wait for Firebase Auth + Firestore both ready
══════════════════════════════════════════════════════════════ */
let _db = null;
let _auth = null;
let _dbReady = false;

window.MedFirestore = (function () {

  function init() {
    if (_dbReady) return;
    try {
      if (!firebase.apps.length) {
        firebase.initializeApp(window.MEDFIND_FIREBASE);
      }
      _db   = firebase.firestore();
      _auth = firebase.auth();
      _dbReady = true;

      // Enable offline persistence (works even without internet)
      _db.enablePersistence({ synchronizeTabs: true })
        .then(() => _log('✅ Firestore offline persistence enabled'))
        .catch(err => {
          if (err.code === 'failed-precondition') {
            _log('⚠️ Multiple tabs open — persistence disabled for this tab');
          } else if (err.code === 'unimplemented') {
            _log('⚠️ Browser does not support offline persistence');
          }
        });

      _log('🔥 Firestore ready — project: medfind-bangladesh');
    } catch (e) {
      console.error('Firestore init error:', e);
    }
  }

  function _log(msg) {
    if (location.hostname === 'localhost' || location.hostname === '127.0.0.1') {
      console.log('%c[MedFirestore]%c ' + msg, 'color:#f59e0b;font-weight:bold', 'color:#e2e8f0');
    }
  }

  function _err(fn, e) {
    console.error('[MedFirestore] ' + fn + ':', e);
    return null;
  }

  function _ready() {
    if (!_dbReady) init();
    return _dbReady && _db;
  }

  // ── SERVER TIMESTAMP ──────────────────────────────────────
  function ts() {
    return firebase.firestore.FieldValue.serverTimestamp();
  }

  /* ══════════════════════════════════════════════════════════
     USERS — Save / Get / Update
  ══════════════════════════════════════════════════════════ */
  async function saveUser(uid, userData) {
    if (!_ready()) return null;
    try {
      const ref = _db.collection('users').doc(uid);
      const doc = await ref.get();
      const payload = {
        ...userData,
        uid,
        updatedAt: ts(),
        // Never overwrite createdAt if user already exists
        ...(doc.exists ? {} : { createdAt: ts() })
      };
      // Remove undefined fields
      Object.keys(payload).forEach(k => payload[k] === undefined && delete payload[k]);
      await ref.set(payload, { merge: true });
      _log('User saved: ' + uid);
      return true;
    } catch (e) { return _err('saveUser', e); }
  }

  async function getUser(uid) {
    if (!_ready()) return null;
    try {
      const doc = await _db.collection('users').doc(uid).get();
      return doc.exists ? { id: doc.id, ...doc.data() } : null;
    } catch (e) { return _err('getUser', e); }
  }

  async function updateUser(uid, fields) {
    if (!_ready()) return null;
    try {
      await _db.collection('users').doc(uid).update({ ...fields, updatedAt: ts() });
      _log('User updated: ' + uid);
      return true;
    } catch (e) { return _err('updateUser', e); }
  }

  async function getUsersByRole(role, limitN = 50) {
    if (!_ready()) return [];
    try {
      const snap = await _db.collection('users')
        .where('role', '==', role)
        .where('isActive', '==', true)
        .limit(limitN).get();
      return snap.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (e) { _err('getUsersByRole', e); return []; }
  }

  /* ══════════════════════════════════════════════════════════
     APPOINTMENTS
  ══════════════════════════════════════════════════════════ */
  async function createAppointment(data) {
    if (!_ready()) return null;
    try {
      const ref = await _db.collection('appointments').add({
        ...data,
        status: 'pending',
        createdAt: ts(),
        updatedAt: ts()
      });
      _log('Appointment created: ' + ref.id);
      return ref.id;
    } catch (e) { return _err('createAppointment', e); }
  }

  async function getAppointments(uid, role = 'patient') {
    if (!_ready()) return [];
    try {
      const field = role === 'doctor' ? 'doctorId' : 'patientId';
      const snap = await _db.collection('appointments')
        .where(field, '==', uid)
        .orderBy('createdAt', 'desc')
        .limit(30).get();
      return snap.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (e) { _err('getAppointments', e); return []; }
  }

  async function updateAppointmentStatus(appointmentId, status, note = '') {
    if (!_ready()) return null;
    try {
      await _db.collection('appointments').doc(appointmentId).update({
        status, note, updatedAt: ts()
      });
      return true;
    } catch (e) { return _err('updateAppointmentStatus', e); }
  }

  /* ══════════════════════════════════════════════════════════
     DOCTORS
  ══════════════════════════════════════════════════════════ */
  async function saveDoctorProfile(uid, profileData) {
    if (!_ready()) return null;
    try {
      await _db.collection('doctors').doc(uid).set({
        ...profileData,
        uid,
        isVerified: false,
        isActive: true,
        updatedAt: ts()
      }, { merge: true });
      _log('Doctor profile saved: ' + uid);
      return true;
    } catch (e) { return _err('saveDoctorProfile', e); }
  }

  async function getDoctors(filters = {}) {
    if (!_ready()) return [];
    try {
      let q = _db.collection('doctors').where('isActive', '==', true);
      if (filters.specialty)  q = q.where('specialty', '==', filters.specialty);
      if (filters.district)   q = q.where('district', '==', filters.district);
      if (filters.isVerified) q = q.where('isVerified', '==', true);
      const snap = await q.limit(filters.limit || 20).get();
      return snap.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (e) { _err('getDoctors', e); return []; }
  }

  /* ══════════════════════════════════════════════════════════
     ORGAN DONORS
  ══════════════════════════════════════════════════════════ */
  async function saveOrganDonor(data) {
    if (!_ready()) return null;
    try {
      const donorId = 'MF-' + new Date().getFullYear() + '-' +
        Math.random().toString(36).substr(2, 6).toUpperCase();
      await _db.collection('organ_donors').doc(donorId).set({
        ...data,
        donorId,
        status: 'registered',
        createdAt: ts(),
        updatedAt: ts()
      });
      _log('Organ donor saved: ' + donorId);
      return donorId;
    } catch (e) { return _err('saveOrganDonor', e); }
  }

  /* ══════════════════════════════════════════════════════════
     BLOOD REQUESTS
  ══════════════════════════════════════════════════════════ */
  async function createBloodRequest(data) {
    if (!_ready()) return null;
    try {
      const ref = await _db.collection('blood_requests').add({
        ...data,
        status: 'open',
        createdAt: ts(),
        updatedAt: ts()
      });
      return ref.id;
    } catch (e) { return _err('createBloodRequest', e); }
  }

  async function getBloodRequests(bloodGroup = null, district = null) {
    if (!_ready()) return [];
    try {
      let q = _db.collection('blood_requests').where('status', '==', 'open');
      if (bloodGroup) q = q.where('bloodGroup', '==', bloodGroup);
      if (district)   q = q.where('district', '==', district);
      const snap = await q.orderBy('createdAt', 'desc').limit(20).get();
      return snap.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (e) { _err('getBloodRequests', e); return []; }
  }

  /* ══════════════════════════════════════════════════════════
     LAB TESTS
  ══════════════════════════════════════════════════════════ */
  async function bookLabTest(data) {
    if (!_ready()) return null;
    try {
      const ref = await _db.collection('lab_tests').add({
        ...data,
        status: 'booked',
        createdAt: ts(),
        updatedAt: ts()
      });
      return ref.id;
    } catch (e) { return _err('bookLabTest', e); }
  }

  /* ══════════════════════════════════════════════════════════
     NOTIFICATIONS
  ══════════════════════════════════════════════════════════ */
  async function addNotification(uid, message, type = 'info', link = '') {
    if (!_ready()) return null;
    try {
      await _db.collection('notifications').doc(uid)
        .collection('items').add({
          message, type, link,
          read: false,
          createdAt: ts()
        });
      return true;
    } catch (e) { return _err('addNotification', e); }
  }

  async function getNotifications(uid) {
    if (!_ready()) return [];
    try {
      const snap = await _db.collection('notifications').doc(uid)
        .collection('items')
        .orderBy('createdAt', 'desc').limit(20).get();
      return snap.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (e) { _err('getNotifications', e); return []; }
  }

  async function markNotificationRead(uid, notifId) {
    if (!_ready()) return null;
    try {
      await _db.collection('notifications').doc(uid)
        .collection('items').doc(notifId).update({ read: true });
      return true;
    } catch (e) { return null; }
  }

  /* ══════════════════════════════════════════════════════════
     REAL-TIME LISTENER — for live dashboard updates
  ══════════════════════════════════════════════════════════ */
  function listenToAppointments(uid, role, callback) {
    if (!_ready()) return () => {};
    const field = role === 'doctor' ? 'doctorId' : 'patientId';
    return _db.collection('appointments')
      .where(field, '==', uid)
      .orderBy('createdAt', 'desc')
      .limit(10)
      .onSnapshot(snap => {
        const items = snap.docs.map(d => ({ id: d.id, ...d.data() }));
        callback(items);
      }, e => _err('listenToAppointments', e));
  }

  function listenToNotifications(uid, callback) {
    if (!_ready()) return () => {};
    return _db.collection('notifications').doc(uid)
      .collection('items')
      .where('read', '==', false)
      .orderBy('createdAt', 'desc')
      .onSnapshot(snap => {
        callback(snap.docs.map(d => ({ id: d.id, ...d.data() })));
      }, e => _err('listenToNotifications', e));
  }

  /* ══════════════════════════════════════════════════════════
     AUTH INTEGRATION — Auto-save user on login/register
  ══════════════════════════════════════════════════════════ */
  function attachAuthListener() {
    if (!_ready()) return;
    _auth.onAuthStateChanged(async (firebaseUser) => {
      if (!firebaseUser) return;

      // Check if user doc already exists
      const existing = await getUser(firebaseUser.uid);
      const localUser = (() => {
        try { return JSON.parse(localStorage.getItem('mf_user') || 'null'); } catch { return null; }
      })();

      if (!existing) {
        // New user — save to Firestore
        await saveUser(firebaseUser.uid, {
          email:       firebaseUser.email,
          full_name:   firebaseUser.displayName || (localUser && localUser.full_name) || firebaseUser.email.split('@')[0],
          phone:       (localUser && localUser.phone) || '',
          role:        (localUser && localUser.role) || 'patient',
          picture:     firebaseUser.photoURL || '',
          auth_provider: firebaseUser.providerData[0]?.providerId || 'email',
          isActive:    true,
          isVerified:  firebaseUser.emailVerified || false,
          emailVerified: firebaseUser.emailVerified || false,
        });
        _log('New user saved to Firestore: ' + firebaseUser.email);
      } else {
        // Existing user — update last login
        await updateUser(firebaseUser.uid, {
          lastLogin:    ts(),
          emailVerified: firebaseUser.emailVerified,
          // Sync any profile picture changes from Google
          ...(firebaseUser.photoURL ? { picture: firebaseUser.photoURL } : {})
        });
        _log('Existing user login recorded: ' + firebaseUser.email);
      }

      // Merge Firestore data into localStorage for offline use
      const fsUser = await getUser(firebaseUser.uid);
      if (fsUser && localUser) {
        localStorage.setItem('mf_user', JSON.stringify({
          ...localUser,
          ...fsUser,
          uid: firebaseUser.uid
        }));
      }
    });
  }

  /* ══════════════════════════════════════════════════════════
     SEARCH — Full-text-like search (Firestore prefix search)
  ══════════════════════════════════════════════════════════ */
  async function searchDoctors(query, limit = 10) {
    if (!_ready() || !query) return [];
    try {
      const q = query.toLowerCase();
      // Firestore doesn't do full-text search natively
      // Use name prefix search with range query
      const snap = await _db.collection('doctors')
        .where('nameSearch', '>=', q)
        .where('nameSearch', '<=', q + '\uf8ff')
        .where('isActive', '==', true)
        .limit(limit).get();
      return snap.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (e) { _err('searchDoctors', e); return []; }
  }

  /* ══════════════════════════════════════════════════════════
     STATS — For admin dashboard
  ══════════════════════════════════════════════════════════ */
  async function getStats() {
    if (!_ready()) return {};
    try {
      const [usersSnap, apptSnap, donorSnap, bloodSnap] = await Promise.all([
        _db.collection('users').get(),
        _db.collection('appointments').where('status', '==', 'pending').get(),
        _db.collection('organ_donors').get(),
        _db.collection('blood_requests').where('status', '==', 'open').get(),
      ]);
      return {
        totalUsers:        usersSnap.size,
        pendingAppts:      apptSnap.size,
        organDonors:       donorSnap.size,
        openBloodRequests: bloodSnap.size,
      };
    } catch (e) { _err('getStats', e); return {}; }
  }

  /* ══════════════════════════════════════════════════════════
     HOSPITALS
  ══════════════════════════════════════════════════════════ */
  async function getHospitals(district = null, limit = 20) {
    if (!_ready()) return [];
    try {
      let q = _db.collection('hospitals').where('isActive', '==', true);
      if (district) q = q.where('district', '==', district);
      const snap = await q.limit(limit).get();
      return snap.docs.map(d => ({ id: d.id, ...d.data() }));
    } catch (e) { _err('getHospitals', e); return []; }
  }

  // ── Public API ─────────────────────────────────────────────
  return {
    init,
    // Users
    saveUser, getUser, updateUser, getUsersByRole,
    // Appointments
    createAppointment, getAppointments, updateAppointmentStatus,
    // Doctors
    saveDoctorProfile, getDoctors, searchDoctors,
    // Hospitals
    getHospitals,
    // Organ Donation
    saveOrganDonor,
    // Blood
    createBloodRequest, getBloodRequests,
    // Lab
    bookLabTest,
    // Notifications
    addNotification, getNotifications, markNotificationRead,
    // Real-time
    listenToAppointments, listenToNotifications,
    // Auth integration
    attachAuthListener,
    // Stats
    getStats,
    // Utils
    ts,
    get db() { return _db; },
    get ready() { return _dbReady; }
  };

})();

// Auto-init when script loads
window.MedFirestore.init();

// Auto-attach auth listener (saves every login to Firestore)
document.addEventListener('DOMContentLoaded', function () {
  if (window.firebase && window.firebase.auth) {
    window.MedFirestore.attachAuthListener();
  }
});
