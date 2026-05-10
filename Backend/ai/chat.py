import anthropic

client = anthropic.Anthropic(api_key="your-key")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    system=SYSTEM_PROMPT,
    messages=conversation_history
)
reply = response.content[0].text