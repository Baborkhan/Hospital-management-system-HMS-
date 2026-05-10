<<<<<<< HEAD
# medfind/ai/views.py — Multi-provider AI proxy
import uuid, json, logging
=======
# medfind/ai/views.py — google-genai (new SDK) version
import uuid, json, logging
from google import genai
from google.genai import types
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import ChatSession, ChatMessage, HealthRecord
<<<<<<< HEAD
from .utils import (
    proxy_ai_call, call_gemini,
    extract_metadata, detect_emergency, SYSTEM_PROMPT,
    get_gemini_client, _call_gemini_rest
)

logger = logging.getLogger(__name__)

RENDER_URL = 'https://medfind-bangladesh-ai-healthcare-platform.onrender.com'


def _cors(response):
    response['Access-Control-Allow-Origin']  = '*'
    response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


# ── Proxy Chat View (used by medfind-ai.html frontend) ────────────────────
@method_decorator(csrf_exempt, name='dispatch')
class ProxyAIChatView(View):
    """
    POST /api/v1/ai/chat/
    Accepts Anthropic-format {messages:[{role,content}]}
    Returns Anthropic-format {content:[{type,text}]}
    Uses Gemini or Claude depending on available keys.
    """
=======
from .utils import call_gemini, extract_metadata, detect_emergency, SYSTEM_PROMPT, get_gemini_client

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class ProxyAIChatView(View):
    """Gemini proxy — frontend sends messages, backend adds API key."""
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072

    def post(self, request):
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
<<<<<<< HEAD
            return _cors(JsonResponse({'error': 'Invalid JSON'}, status=400))

        messages = body.get('messages', [])
        if not messages:
            return _cors(JsonResponse({'error': 'messages required'}, status=400))

        gemini_key    = getattr(settings, 'GEMINI_API_KEY', '')
        anthropic_key = getattr(settings, 'ANTHROPIC_API_KEY', '')

        if not gemini_key and not anthropic_key:
            logger.error('AI not configured! Set GEMINI_API_KEY in Render Dashboard → Environment')
            return _cors(JsonResponse(
                {'error': 'AI not configured. Set GEMINI_API_KEY=AIzaSyAJGKkaMB4ixVPmd5r-cRR1e5ea4AxKmwQ in Render Dashboard → Environment Variables.'},
                status=503
            ))

        try:
            reply_text = proxy_ai_call(messages)
            model_used = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash-lite')
            return _cors(JsonResponse({
                'content': [{'type': 'text', 'text': reply_text}],
                'model':   model_used,
                'role':    'assistant',
            }))
        except Exception as e:
            logger.error('ProxyAIChatView error: %s', e)
            return _cors(JsonResponse(
                {'error': 'AI service temporarily unavailable. Please try again in a moment.'},
                status=503
            ))

    def options(self, request, *args, **kwargs):
        return _cors(JsonResponse({}))


# ── Session Chat View (full history, DB-backed) ────────────────────────────
=======
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not getattr(settings, 'GEMINI_API_KEY', ''):
            return JsonResponse({'error': 'AI service not configured. Set GEMINI_API_KEY in .env'}, status=503)

        messages = body.get('messages', [])
        if not messages:
            return JsonResponse({'error': 'messages required'}, status=400)

        try:
            client     = get_gemini_client()
            model_name = getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash')

            contents = []
            for msg in messages:
                role = 'user' if msg['role'] == 'user' else 'model'
                content = msg.get('content', '')
                if isinstance(content, list):
                    content = ' '.join(c.get('text', '') for c in content if isinstance(c, dict))
                contents.append(types.Content(role=role, parts=[types.Part(text=content)]))

            config = types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=1500,
            )

            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            reply_text = response.text.strip()

            # Anthropic-compatible response so frontend works without changes
            return JsonResponse({
                'content': [{'type': 'text', 'text': reply_text}],
                'model': model_name,
                'role': 'assistant',
            })

        except Exception as e:
            logger.error(f'ProxyAIChatView Gemini error: {e}', exc_info=True)
            return JsonResponse({'error': f'AI error: {str(e)}'}, status=500)

    def options(self, request, *args, **kwargs):
        response = JsonResponse({})
        response['Access-Control-Allow-Origin']  = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response


>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
@method_decorator(csrf_exempt, name='dispatch')
class AIChatView(View):
    def post(self, request):
        try:
            body    = json.loads(request.body)
            message = body.get('message', '').strip()
            if not message:
                return JsonResponse({'error': 'Message required'}, status=400)

            sid = body.get('session_id') or request.session.get('ai_sid')
            if not sid:
                sid = str(uuid.uuid4())

            session, _ = ChatSession.objects.get_or_create(
                session_id=sid,
                defaults={
                    'user_ip': self._ip(request),
                    'user_id': str(request.user.id) if request.user.is_authenticated else None,
                }
            )
            request.session['ai_sid'] = sid

            recent  = list(ChatMessage.objects.filter(session=session).order_by('-created_at')[:20])
            history = [{'role': m.role, 'content': m.content} for m in reversed(recent)]
            history.append({'role': 'user', 'content': message})

<<<<<<< HEAD
            ChatMessage.objects.create(
                session=session, role='user', content=message,
                is_emergency=detect_emergency(message)
            )
            reply = call_gemini(history)
            meta  = extract_metadata(reply)

            ChatMessage.objects.create(
                session=session, role='assistant', content=reply,
                urgency=meta['urgency'], specialist=meta['specialist'],
                is_emergency=meta['is_emergency']
            )
=======
            ChatMessage.objects.create(session=session, role='user', content=message,
                                       is_emergency=detect_emergency(message))
            reply = call_gemini(history)
            meta  = extract_metadata(reply)

            ChatMessage.objects.create(session=session, role='assistant', content=reply,
                                       urgency=meta['urgency'], specialist=meta['specialist'],
                                       is_emergency=meta['is_emergency'])
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
            session.turn_count += 1
            session.save()

            return JsonResponse({
                'response':     reply,
                'session_id':   sid,
                'is_emergency': meta['is_emergency'],
                'urgency':      meta['urgency'],
                'specialist':   meta['specialist'],
                'disclaimer':   '⚠️ AI suggestions are supportive only. Always consult a qualified doctor.',
            })
        except Exception as e:
<<<<<<< HEAD
            logger.error('AIChatView error: %s', e, exc_info=True)
=======
            logger.error(f'AIChatView error: {e}', exc_info=True)
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
            return JsonResponse({'error': 'AI service error'}, status=500)

    def _ip(self, r):
        x = r.META.get('HTTP_X_FORWARDED_FOR')
        return x.split(',')[0].strip() if x else r.META.get('REMOTE_ADDR')


<<<<<<< HEAD
# ── Symptom Analyze View ───────────────────────────────────────────────────
=======
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
@method_decorator(csrf_exempt, name='dispatch')
class SymptomAnalyzeView(View):
    def post(self, request):
        try:
            body     = json.loads(request.body)
            symptoms = body.get('symptoms', [])
            if not symptoms:
                return JsonResponse({'error': 'Symptoms required'}, status=400)

            prompt = (
                f"Patient symptoms: {', '.join(symptoms)}\n"
                "Respond ONLY with valid JSON (no markdown):\n"
                '{"conditions":[{"name":"...","prob":75,"color":"#22d3ee"}],'
                '"urgency":"Mild","urgencyClass":"s","specialist":"...","action":"..."}'
            )
<<<<<<< HEAD
            result_text = call_gemini([{'role': 'user', 'content': prompt}])
            raw    = result_text.replace('```json', '').replace('```', '').strip()
            try:
                result = json.loads(raw)
                return _cors(JsonResponse(result))
            except (json.JSONDecodeError, KeyError):
                # AI offline — return safe fallback
                return _cors(JsonResponse({
                    'conditions': [{'name': 'Consultation Required', 'prob': 100, 'color': '#6b7280'}],
                    'urgency': 'Moderate', 'urgencyClass': 'y',
                    'specialist': 'General Physician',
                    'action': 'AI analysis temporarily unavailable. Please consult a doctor directly.',
                    'offline': True
                }))
        except Exception as e:
            return _cors(JsonResponse({'error': str(e)}, status=500))

    def options(self, request, *args, **kwargs):
        return _cors(JsonResponse({}))


# ── Chat History View ──────────────────────────────────────────────────────
=======

            client = get_gemini_client()
            config = types.GenerateContentConfig(
                system_instruction='Medical AI. Respond ONLY with valid JSON. No markdown.',
                max_output_tokens=600,
            )
            response = client.models.generate_content(
                model=getattr(settings, 'GEMINI_MODEL', 'gemini-2.0-flash'),
                contents=prompt,
                config=config,
            )
            raw    = response.text.replace('```json', '').replace('```', '').strip()
            result = json.loads(raw)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
class ChatHistoryView(View):
    def get(self, request):
        sid = request.GET.get('session_id')
        if not sid:
            return JsonResponse({'error': 'session_id required'}, status=400)
        try:
            session = ChatSession.objects.get(session_id=sid)
            msgs    = ChatMessage.objects.filter(session=session).order_by('created_at')
            return JsonResponse({
                'session_id': sid,
                'turn_count': session.turn_count,
                'messages': [{
                    'role': m.role, 'content': m.content,
                    'created_at': m.created_at.isoformat(),
                    'urgency': m.urgency, 'specialist': m.specialist,
                    'is_emergency': m.is_emergency,
                } for m in msgs]
            })
        except ChatSession.DoesNotExist:
            return JsonResponse({'error': 'Session not found'}, status=404)


<<<<<<< HEAD
# ── Health Record View ────────────────────────────────────────────────────
=======
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
@method_decorator(csrf_exempt, name='dispatch')
class HealthRecordView(View):
    def post(self, request):
        try:
            body = json.loads(request.body)
            HealthRecord.objects.create(
                user_id=body.get('user_id', 'anonymous'),
                bmi=body.get('bmi'), systolic=body.get('systolic'),
                diastolic=body.get('diastolic'), sugar=body.get('sugar'),
                weight=body.get('weight'), notes=body.get('notes', ''),
            )
<<<<<<< HEAD
            return _cors(JsonResponse({'status': 'saved'}))
        except Exception as e:
            return _cors(JsonResponse({'error': str(e)}, status=500))
=======
            return JsonResponse({'status': 'saved'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072

    def get(self, request):
        uid  = request.GET.get('user_id', 'anonymous')
        recs = HealthRecord.objects.filter(user_id=uid).order_by('-created_at')[:30]
<<<<<<< HEAD
        return _cors(JsonResponse({'records': [{
            'bmi': r.bmi, 'systolic': r.systolic, 'diastolic': r.diastolic,
            'sugar': r.sugar, 'weight': r.weight, 'notes': r.notes,
            'created_at': r.created_at.isoformat()
        } for r in recs]}))
=======
        return JsonResponse({'records': [{
            'bmi': r.bmi, 'systolic': r.systolic, 'diastolic': r.diastolic,
            'sugar': r.sugar, 'weight': r.weight, 'notes': r.notes,
            'created_at': r.created_at.isoformat()
        } for r in recs]})
>>>>>>> 58c405af0447997e6cf8a412fa3573bac7007072
