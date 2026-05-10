<<<<<<< HEAD
# medfind/ai/utils.py — Multi-provider AI (Gemini primary, Claude fallback)
import re
import logging
import os
import json
import urllib.request
import urllib.error
from django.conf import settings

logger = logging.getLogger(__name__)

=======
# medfind/ai/utils.py  — google-genai (new SDK) version
import re
from google import genai
from google.genai import types
from django.conf import settings

>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
SYSTEM_PROMPT = """You are MedFind AI — a highly accurate medical guidance assistant for Bangladesh.
Developer: Ahsanul Yamin Babor (medfindbd2026@gmail.com) | BAUET 2026

LANGUAGE: Detect user's language. Bengali → respond fully in Bengali. English → respond in English.

ACCURACY PROTOCOL (90%+ target):
1. Ask clarifying questions if symptoms are vague (age, duration, severity 1-10)
2. Differential diagnosis: top 3 with probability %
3. Red flag emergency screening always
4. WHO / DGHS Bangladesh / BIRDEM guidelines
5. Never fabricate — if uncertain, ask more

RESPONSE STRUCTURE:
🔍 Symptom Analysis
🎯 Possible Conditions (X% probability)
⚡ Urgency: EMERGENCY 🔴 / Urgent 🟠 / Moderate 🟡 / Mild 🟢
👨‍⚕️ Recommended Specialist + Bangladesh hospital
💡 Do This Now (numbered steps)
⚠️ Go to hospital if: [red flags]
---
*AI suggestion only — consult a qualified doctor*

EMERGENCY TRIGGERS: chest pain, unconscious, can't breathe, stroke, severe bleeding,
seizure, poisoning, dengue shock. BANGLADESH: 999 | 16167 (DGHS)

NEVER: prescribe controlled medicines, say definitely, ignore emergency symptoms."""

EMERGENCY_PATTERNS = [
    r'chest pain', r'heart attack', r'unconscious', r'হার্ট অ্যাটাক', r'অজ্ঞান',
    r'শ্বাস নিতে পারছি না', r'stroke', r'seizure', r'severe bleeding',
    r'choking', r'not breathing', r'dengue shock', r'poisoning', r'বিষ',
]

SPECIALIST_MAP = {
    'Cardiologist':       r'cardiolog|cardiac|heart|হার্ট',
    'Neurologist':        r'neurolog|stroke|epilep|migraine|মাথা ঘোরা',
    'Pediatrician':       r'pediatric|child|শিশু|বাচ্চা|baby',
    'Dermatologist':      r'dermatolog|skin|rash|চর্ম|ত্বক',
    'Gastroenterologist': r'gastro|liver|stomach|পেট|যকৃত',
    'Pulmonologist':      r'pulmo|respirat|lung|ফুসফুস|শ্বাসকষ্ট',
    'Gynecologist':       r'gynecolog|obstet|pregnancy|গর্ভ|মহিলা',
    'Orthopedist':        r'orthop|bone|joint|হাড়|জয়েন্ট',
    'Psychiatrist':       r'psychiatr|mental|depress|anxiety|মানসিক',
    'General Physician':  r'general|সাধারণ|fever|জ্বর',
}

URGENCY_MAP = {
    'EMERGENCY': r'EMERGENCY 🔴|🔴',
    'Urgent':    r'Urgent 🟠|🟠',
    'Moderate':  r'Moderate 🟡|🟡',
    'Mild':      r'Mild 🟢|🟢',
}


def detect_emergency(text: str) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in EMERGENCY_PATTERNS)


def extract_metadata(text: str) -> dict:
<<<<<<< HEAD
    is_emerg = detect_emergency(text)
    urgency = 'Moderate'
=======
    is_emerg   = detect_emergency(text)
    urgency    = 'EMERGENCY' if is_emerg else 'Mild'
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
    specialist = ''
    for u, pattern in URGENCY_MAP.items():
        if re.search(pattern, text):
            urgency = u
            break
    for name, pattern in SPECIALIST_MAP.items():
        if re.search(pattern, text, re.IGNORECASE):
            specialist = name
            break
    return {'urgency': urgency, 'specialist': specialist, 'is_emergency': is_emerg}


<<<<<<< HEAD
# ── Provider 1: Gemini (google-genai SDK) ──────────────────────────────────
def get_gemini_client():
    from google import genai
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _call_gemini_sdk(messages: list) -> str:
    """Call Gemini via official SDK. Raises on failure."""
    from google import genai
    from google.genai import types

    client = get_gemini_client()
    model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash-lite')

    contents = []
    for msg in messages:
        role = 'user' if msg['role'] == 'user' else 'model'
        content = msg.get('content', '')
        if isinstance(content, list):
            content = ' '.join(c.get('text', '') for c in content if isinstance(c, dict))
        contents.append(types.Content(role=role, parts=[types.Part(text=content)]))

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        max_output_tokens=getattr(settings, 'AI_MAX_TOKENS', 1500),
    )
    response = client.models.generate_content(
        model=model_name, contents=contents, config=config
    )
    return response.text.strip()


# ── Provider 2: Gemini REST API (no SDK, bypasses some restrictions) ──────
def _call_gemini_rest(messages: list) -> str:
    """Call Gemini via raw REST API. Raises on failure."""
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    model   = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash-lite')
    url     = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'

    contents = []
    for msg in messages:
        role = 'user' if msg['role'] == 'user' else 'model'
        content = msg.get('content', '')
        if isinstance(content, list):
            content = ' '.join(c.get('text', '') for c in content if isinstance(c, dict))
        contents.append({'role': role, 'parts': [{'text': content}]})

    payload = {
        'systemInstruction': {'parts': [{'text': SYSTEM_PROMPT}]},
        'contents': contents,
        'generationConfig': {
            'maxOutputTokens': getattr(settings, 'AI_MAX_TOKENS', 1500),
        }
    }

    data = json.dumps(payload).encode('utf-8')
    req  = urllib.request.Request(
        url, data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())

    return result['candidates'][0]['content']['parts'][0]['text'].strip()


# ── Provider 3: Anthropic Claude (fallback) ────────────────────────────────
def _call_anthropic(messages: list) -> str:
    """Call Anthropic Claude API. Raises on failure."""
    api_key = getattr(settings, 'ANTHROPIC_API_KEY', '')
    if not api_key:
        raise ValueError('ANTHROPIC_API_KEY not configured')

    model = getattr(settings, 'ANTHROPIC_MODEL', 'claude-haiku-4-5-20251001')
    url   = 'https://api.anthropic.com/v1/messages'

    # Convert messages - filter out non-user/assistant roles
    claude_msgs = []
    for msg in messages:
        role = msg.get('role', 'user')
        if role not in ('user', 'assistant'):
            role = 'user'
        content = msg.get('content', '')
        if isinstance(content, list):
            content = ' '.join(c.get('text', '') for c in content if isinstance(c, dict))
        if content.strip():
            claude_msgs.append({'role': role, 'content': content})

    if not claude_msgs:
        raise ValueError('No valid messages')

    payload = {
        'model':      model,
        'max_tokens': getattr(settings, 'AI_MAX_TOKENS', 1500),
        'system':     SYSTEM_PROMPT,
        'messages':   claude_msgs,
    }

    data = json.dumps(payload).encode('utf-8')
    req  = urllib.request.Request(
        url, data=data,
        headers={
            'Content-Type':      'application/json',
            'x-api-key':         api_key,
            'anthropic-version': '2023-06-01',
        },
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read())

    return result['content'][0]['text'].strip()


# ── Master call_gemini (used by AIChatView) ────────────────────────────────
def call_gemini(history: list) -> str:
    """Try Gemini SDK → Gemini REST → Anthropic. Return reply text."""
    gemini_key    = getattr(settings, 'GEMINI_API_KEY', '')
    anthropic_key = getattr(settings, 'ANTHROPIC_API_KEY', '')

    if gemini_key:
        # Try SDK first
        try:
            return _call_gemini_sdk(history)
        except Exception as e1:
            logger.warning('Gemini SDK failed: %s', e1)
            # Try REST
            try:
                return _call_gemini_rest(history)
            except Exception as e2:
                logger.warning('Gemini REST failed: %s', e2)

    if anthropic_key:
        try:
            return _call_anthropic(history)
        except Exception as e3:
            logger.warning('Anthropic failed: %s', e3)

    return 'দুঃখিত, AI সেবা সাময়িকভাবে অনুপলব্ধ। অনুগ্রহ করে আবার চেষ্টা করুন। | Sorry, AI service temporarily unavailable. Please try again.'


# ── Master proxy_call (used by ProxyAIChatView) ───────────────────────────
def proxy_ai_call(messages: list) -> str:
    """For the proxy endpoint — same fallback chain."""
    return call_gemini(messages)
=======
def get_gemini_client():
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def call_gemini(history: list) -> str:
    client = get_gemini_client()
    model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash')

    # Build contents list
    contents = []
    for msg in history:
        role = 'user' if msg['role'] == 'user' else 'model'
        contents.append(types.Content(
            role=role,
            parts=[types.Part(text=msg['content'])]
        ))

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        max_output_tokens=1500,
    )

    response = client.models.generate_content(
        model=model_name,
        contents=contents,
        config=config,
    )
    return response.text.strip() or 'দুঃখিত, একটি সমস্যা হয়েছে। আবার চেষ্টা করুন।'
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
