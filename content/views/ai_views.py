import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status


class AIAnalysisView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can use AI features (DRF built-in).

    def post(self, request):
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Text is required.'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return Response({'error': 'GROQ API key not set.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are an AI assistant that summarizes, analyzes sentiment, extracts topics, and recommends related content."},
                {"role": "user", "content": f"Summarize, analyze sentiment, extract topics, and recommend related content for: {text}"}
            ],
            "max_tokens": 256,
        }
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            ai_content = response.json()['choices'][0]['message']['content']
            return Response({'ai_result': ai_content})
        except requests.RequestException as e:
            return Response({'error': 'GROQ API error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
