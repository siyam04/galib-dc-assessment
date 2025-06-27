import os, requests, json, re
from rest_framework import serializers
from content.models import Category, Content
from content.serializers.category_serializers import CategorySerializer


class ContentSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False
    )

    class Meta:
        model = Content
        fields = [
            'id', 'title', 'body', 'category', 'category_id', 'metadata',
            'owner', 'is_public', 'created_at', 'updated_at',
            'summary', 'sentiment', 'topics', 'recommendations',
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at', 'summary', 'sentiment', 'topics', 'recommendations']

    def analyze_with_groq(self, text):
        """
        Calls the GROQ API to analyze the given text and return a dict with
        summary, sentiment, topics, and recommendations. Handles extracting
        the JSON object from the AI's response, even if wrapped in markdown.
        """
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key or not text:
            return {}
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are an AI assistant that summarizes, analyzes sentiment, extracts topics, and recommends related content. Return a JSON object with keys: summary, sentiment, topics, recommendations."},
                {"role": "user", "content": f"Summarize, analyze sentiment, extract topics, and recommend related content for: {text}"}
            ],
            "max_tokens": 256,
        }
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30,
            )
            if response.status_code != 200:
                return {}
            result = response.json()
            ai_content = result['choices'][0]['message']['content']
            match = re.search(r'```\n({[\s\S]+?})\n```', ai_content)
            if match:
                return json.loads(match.group(1))
            match = re.search(r'({[\s\S]+?})', ai_content)
            if match:
                return json.loads(match.group(1))
            return {}
        except Exception:
            return {}

    def create(self, validated_data):
        """
        On content creation, automatically analyze the body text using GROQ
        and populate summary, sentiment, topics, and recommendations fields.
        """
        ai_result = self.analyze_with_groq(validated_data.get('body', ''))
        validated_data['summary'] = ai_result.get('summary') or ''
        validated_data['sentiment'] = ai_result.get('sentiment') or ''
        validated_data['topics'] = ai_result.get('topics')
        validated_data['recommendations'] = ai_result.get('recommendations') or ''
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        On content update, re-analyze the (possibly updated) body text using GROQ
        and update the AI-generated fields accordingly.
        """
        ai_result = self.analyze_with_groq(validated_data.get('body', instance.body))
        validated_data['summary'] = ai_result.get('summary') or ''
        validated_data['sentiment'] = ai_result.get('sentiment') or ''
        validated_data['topics'] = ai_result.get('topics')
        validated_data['recommendations'] = ai_result.get('recommendations') or ''
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        """
        When serializing (GET), if any AI field is missing, analyze the content
        on-the-fly and save the results. Ensures all AI fields are always present
        in API responses, even for legacy or incomplete data.
        """
        if not instance.summary or not instance.sentiment or not instance.topics or not instance.recommendations:
            ai_result = self.analyze_with_groq(instance.body)
            instance.summary = ai_result.get('summary') or ''
            instance.sentiment = ai_result.get('sentiment') or ''
            instance.topics = ai_result.get('topics')
            instance.recommendations = ai_result.get('recommendations') or ''
            instance.save(update_fields=['summary', 'sentiment', 'topics', 'recommendations'])
        return super().to_representation(instance)
