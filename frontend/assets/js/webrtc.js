/**
 * MedFind — WebRTC Video Call Engine
 * Handles: WebSocket signaling, peer connection, media, UI state
 *
 * Usage (Patient side):
 *   const call = new MedFindCall({ role: 'patient', sessionId, token, apiBase });
 *   call.joinWaitingRoom();
 *
 * Usage (Doctor side):
 *   const call = new MedFindCall({ role: 'doctor', sessionId, token, apiBase });
 *   call.startSession();
 */

const API_BASE = window.API_BASE || 'http://127.0.0.1:8000/api/v1';
const WS_BASE  = window.WS_BASE  || 'ws://127.0.0.1:8001';

class MedFindCall {
  /**
   * @param {Object} opts
   * @param {'patient'|'doctor'} opts.role
   * @param {string} opts.sessionId  — room_id from backend
   * @param {string} opts.token      — JWT access token
   * @param {string} [opts.apiBase]  — override API base URL
   * @param {string} [opts.wsBase]   — override WebSocket base URL
   * @param {Object} [opts.callbacks]
   *   onWaiting, onDoctorJoined, onPatientWaiting, onCallStarted,
   *   onCallEnded, onError, onIceConnected
   */
  constructor(opts = {}) {
    this.role       = opts.role;           // 'patient' | 'doctor'
    this.sessionId  = opts.sessionId;
    this.token      = opts.token;
    this.apiBase    = opts.apiBase || API_BASE;
    this.wsBase     = opts.wsBase  || WS_BASE;
    this.callbacks  = opts.callbacks || {};

    this.pc         = null;   // RTCPeerConnection
    this.ws         = null;   // WebSocket (signaling)
    this.localStream  = null;
    this.remoteStream = null;
    this.iceServers   = [
      { urls: 'stun:stun.l.google.com:19302' },
      { urls: 'stun:stun1.l.google.com:19302' },
    ];

    this._log('MedFindCall initialized', { role: this.role, sessionId: this.sessionId });
  }

  // ── PUBLIC API ─────────────────────────────────────────────────────────────

  /** Patient: enters waiting room, notifies doctor */
  async joinWaitingRoom() {
    this._log('Patient joining waiting room…');
    try {
      const res = await this._api(
        `telemedicine/sessions/${this.sessionId}/patient-join/`, 'POST'
      );
      if (res.data?.ice_servers) this.iceServers = res.data.ice_servers;
      await this._getMedia();
      this._connectSignaling();   // Listen for doctor_joined event
      this._emit('onWaiting', res.data);
    } catch (e) {
      this._handleError('joinWaitingRoom', e);
    }
  }

  /** Doctor: clicks JOIN SESSION */
  async startSession() {
    this._log('Doctor starting session…');
    try {
      const res = await this._api(
        `telemedicine/sessions/${this.sessionId}/doctor-join/`, 'POST'
      );
      if (res.data?.ice_servers) this.iceServers = res.data.ice_servers;
      await this._getMedia();
      this._connectSignaling(true);  // true = initiator (sends offer)
    } catch (e) {
      this._handleError('startSession', e);
    }
  }

  /** End call — both sides */
  async endCall(prescriptionData = {}) {
    this._log('Ending call…');
    this._closeConnections();
    try {
      await this._api(`telemedicine/sessions/${this.sessionId}/end/`, 'POST', {
        duration_seconds:  this._callSeconds(),
        prescription_text: prescriptionData.text    || '',
        follow_up_notes:   prescriptionData.followUp || '',
        recommended_tests: prescriptionData.tests    || '',
      });
    } catch (e) {
      this._log('End call API error (non-fatal):', e);
    }
    this._emit('onCallEnded', { duration: this._callSeconds() });
  }

  /** Toggle local audio */
  toggleAudio() {
    if (!this.localStream) return false;
    const track = this.localStream.getAudioTracks()[0];
    if (track) track.enabled = !track.enabled;
    return track?.enabled ?? false;
  }

  /** Toggle local video */
  toggleVideo() {
    if (!this.localStream) return false;
    const track = this.localStream.getVideoTracks()[0];
    if (track) track.enabled = !track.enabled;
    return track?.enabled ?? false;
  }

  /** Attach local video to an <video> element */
  attachLocalVideo(videoEl) {
    if (this.localStream && videoEl) {
      videoEl.srcObject = this.localStream;
      videoEl.muted = true;
      videoEl.play().catch(() => {});
    }
  }

  /** Attach remote video to a <video> element */
  attachRemoteVideo(videoEl) {
    if (this.remoteStream && videoEl) {
      videoEl.srcObject = this.remoteStream;
      videoEl.play().catch(() => {});
    }
    this._remoteVideoEl = videoEl;  // Save for when stream arrives later
  }

  // ── PRIVATE — Media ────────────────────────────────────────────────────────

  async _getMedia() {
    try {
      this.localStream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: 'user' },
        audio: { echoCancellation: true, noiseSuppression: true, sampleRate: 44100 },
      });
      this._log('Media acquired');
    } catch (e) {
      // Fallback: audio only if no camera
      this._log('Camera failed, trying audio only:', e.message);
      try {
        this.localStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (e2) {
        throw new Error('Cannot access microphone. Please allow permissions.');
      }
    }
  }

  // ── PRIVATE — WebSocket signaling ──────────────────────────────────────────

  _connectSignaling(isInitiator = false) {
    const wsUrl = `${this.wsBase}/ws/session/${this.sessionId}/`;
    this._log('Connecting WebSocket:', wsUrl);

    this.ws = new WebSocket(wsUrl);
    this._callStartTime = null;
    this._isInitiator   = isInitiator;

    this.ws.onopen = () => {
      this._log('WS connected');
      this.ws.send(JSON.stringify({ type: 'join', role: this.role }));
      if (isInitiator) {
        // Doctor side: create peer connection and send offer immediately
        this._createPeerConnection();
        this._sendOffer();
      }
    };

    this.ws.onmessage = (evt) => {
      let msg;
      try { msg = JSON.parse(evt.data); } catch { return; }
      this._handleSignal(msg);
    };

    this.ws.onerror = (e) => {
      this._log('WS error', e);
      this._emit('onError', { code: 'WS_ERROR', message: 'Signaling connection failed' });
    };

    this.ws.onclose = () => {
      this._log('WS closed');
    };
  }

  _handleSignal(msg) {
    this._log('Signal received:', msg.type);

    switch (msg.type) {
      case 'patient_waiting':
        // Doctor's browser: patient is in waiting room
        this._emit('onPatientWaiting', msg);
        break;

      case 'doctor_joined':
        // Patient's browser: doctor joined → create PC, wait for offer
        this._emit('onDoctorJoined', msg);
        this._createPeerConnection();
        break;

      case 'offer':
        this._handleOffer(msg.sdp);
        break;

      case 'answer':
        if (this.pc) {
          this.pc.setRemoteDescription(new RTCSessionDescription({ type: 'answer', sdp: msg.sdp }))
            .then(() => this._log('Remote answer set'))
            .catch(e => this._log('setRemoteDescription error:', e));
        }
        break;

      case 'ice-candidate':
        if (this.pc && msg.candidate) {
          this.pc.addIceCandidate(new RTCIceCandidate(msg.candidate))
            .catch(e => this._log('addIceCandidate error:', e));
        }
        break;

      case 'peer_left':
        this._log('Other peer left');
        this._emit('onCallEnded', { reason: 'peer_left' });
        break;

      case 'pong':
        break;
    }
  }

  // ── PRIVATE — RTCPeerConnection ────────────────────────────────────────────

  _createPeerConnection() {
    this._log('Creating RTCPeerConnection');
    this.pc = new RTCPeerConnection({ iceServers: this.iceServers });
    this.remoteStream = new MediaStream();

    // Add local tracks to connection
    if (this.localStream) {
      this.localStream.getTracks().forEach(track => {
        this.pc.addTrack(track, this.localStream);
      });
    }

    // Receive remote tracks
    this.pc.ontrack = (evt) => {
      evt.streams[0]?.getTracks().forEach(track => {
        this.remoteStream.addTrack(track);
      });
      if (this._remoteVideoEl) {
        this._remoteVideoEl.srcObject = this.remoteStream;
        this._remoteVideoEl.play().catch(() => {});
      }
      this._emit('onCallStarted', { remoteStream: this.remoteStream });
      if (!this._callStartTime) this._callStartTime = Date.now();
    };

    // Send ICE candidates to peer via WebSocket
    this.pc.onicecandidate = (evt) => {
      if (evt.candidate) {
        this._send({ type: 'ice-candidate', candidate: evt.candidate.toJSON() });
      }
    };

    this.pc.oniceconnectionstatechange = () => {
      this._log('ICE state:', this.pc.iceConnectionState);
      if (this.pc.iceConnectionState === 'connected') {
        this._emit('onIceConnected');
      }
      if (['failed', 'disconnected', 'closed'].includes(this.pc.iceConnectionState)) {
        this._emit('onCallEnded', { reason: this.pc.iceConnectionState });
      }
    };
  }

  async _sendOffer() {
    if (!this.pc) return;
    try {
      const offer = await this.pc.createOffer({
        offerToReceiveVideo: true,
        offerToReceiveAudio: true,
      });
      await this.pc.setLocalDescription(offer);
      this._send({ type: 'offer', sdp: offer.sdp });
      this._log('Offer sent');
    } catch (e) {
      this._handleError('_sendOffer', e);
    }
  }

  async _handleOffer(sdp) {
    if (!this.pc) this._createPeerConnection();
    try {
      await this.pc.setRemoteDescription(new RTCSessionDescription({ type: 'offer', sdp }));
      const answer = await this.pc.createAnswer();
      await this.pc.setLocalDescription(answer);
      this._send({ type: 'answer', sdp: answer.sdp });
      this._log('Answer sent');
    } catch (e) {
      this._handleError('_handleOffer', e);
    }
  }

  // ── PRIVATE — Helpers ──────────────────────────────────────────────────────

  _send(data) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  async _api(path, method = 'GET', body = null) {
    const res = await fetch(`${this.apiBase}/${path}`, {
      method,
      headers: {
        'Content-Type':  'application/json',
        'Authorization': `Bearer ${this.token}`,
      },
      body: body ? JSON.stringify(body) : undefined,
    });
    const json = await res.json();
    if (!json.success && res.status >= 400) throw new Error(json.message || 'API error');
    return json;
  }

  _closeConnections() {
    this.localStream?.getTracks().forEach(t => t.stop());
    this.pc?.close();
    this.ws?.close();
    this.pc = null;
    this.ws = null;
  }

  _callSeconds() {
    if (!this._callStartTime) return 0;
    return Math.round((Date.now() - this._callStartTime) / 1000);
  }

  _emit(event, data = {}) {
    if (typeof this.callbacks[event] === 'function') {
      this.callbacks[event](data);
    }
  }

  _handleError(context, err) {
    this._log(`Error in ${context}:`, err);
    this._emit('onError', { code: context, message: err.message });
  }

  _log(...args) {
  }
}

// Make globally available
window.MedFindCall = MedFindCall;
