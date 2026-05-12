"""
Antigravity - Addict Aware
NLP Module: Sentiment Analysis using OpenAI API

Uses OpenAI's GPT model to analyze emotional feedback from users.
Provides sentiment classification, compound scoring, and emotion detection.
Falls back to a basic keyword-based analysis if the API is unavailable.
"""
import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY', ''))

SENTIMENT_PROMPT = """You are a digital wellness expert analyzing a user's emotional feedback about their screen time and phone usage habits.

Analyze the following text and return a JSON object with exactly these fields:
- "sentiment": one of "Positive", "Negative", or "Neutral"
- "compound_score": a float from -1.0 (most negative) to 1.0 (most positive)
- "scores": {{"positive": float 0-1, "negative": float 0-1, "neutral": float 0-1}} (must sum to ~1.0)
- "emotion": one of "😊 Very Positive", "🙂 Slightly Positive", "😐 Neutral", "😐 Slightly Negative", "😟 Very Negative"
- "brief_explanation": A 1-2 sentence explanation of the sentiment analysis in the context of digital wellness. Explain what the user's emotional state reveals about their relationship with technology and digital habits. Be empathetic and constructive.

Context: This is from a digital addiction awareness platform. The user is reflecting on how they feel about their phone/screen usage.

Respond with ONLY the JSON object, no markdown formatting or extra text.

Text: "{text}"
"""


def analyze_sentiment(text):
    """
    Analyze sentiment of user's emotional feedback text using OpenAI API.

    Args:
        text: User-provided emotional feedback string

    Returns:
        dict with sentiment label, compound score, detailed scores, and emotion
    """
    if not text or not text.strip():
        return {
            'sentiment': 'Neutral',
            'compound_score': 0.0,
            'scores': {'positive': 0, 'negative': 0, 'neutral': 1.0},
            'emotion': '😐 Neutral',
            'brief_explanation': 'No emotional feedback was provided for analysis.'
        }

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a sentiment analysis expert specializing in digital wellness and screen time behavior. Always respond with valid JSON only."
                },
                {
                    "role": "user",
                    "content": SENTIMENT_PROMPT.format(text=text.replace('"', '\\"'))
                }
            ],
            temperature=0.1,
            max_tokens=300
        )

        raw_content = response.choices[0].message.content.strip()

        # Extract JSON from response (handles markdown code blocks)
        import re
        json_match = re.search(r'\{[\s\S]*\}', raw_content)
        if not json_match:
            raise ValueError(f"No JSON found in response: {raw_content[:100]}")

        result = json.loads(json_match.group())

        # Validate and normalize the response
        sentiment = result.get('sentiment', 'Neutral')
        if sentiment not in ('Positive', 'Negative', 'Neutral'):
            sentiment = 'Neutral'

        compound = float(result.get('compound_score', 0.0))
        compound = max(-1.0, min(1.0, compound))

        scores = result.get('scores', {})
        emotion = result.get('emotion', '😐 Neutral')
        explanation = result.get('brief_explanation', 'Sentiment analysis completed.')

        # Safely convert score values to float (handles strings or nested types)
        def safe_float(val, default=0.0):
            try:
                return float(val)
            except (ValueError, TypeError):
                return default

        return {
            'sentiment': sentiment,
            'compound_score': round(compound, 4),
            'scores': {
                'positive': round(safe_float(scores.get('positive', 0)), 4),
                'negative': round(safe_float(scores.get('negative', 0)), 4),
                'neutral': round(safe_float(scores.get('neutral', 0)), 4)
            },
            'emotion': emotion,
            'brief_explanation': explanation
        }

    except Exception as e:
        print(f"[!] OpenAI API error: {e}. Using fallback analysis.")
        return _fallback_analyze(text)


def _fallback_analyze(text):
    """
    Basic keyword-based fallback sentiment analysis when OpenAI API is unavailable.
    """
    text_lower = text.lower()

    positive_words = ['happy', 'great', 'good', 'amazing', 'proud', 'better', 'improved',
                      'productive', 'wonderful', 'love', 'enjoy', 'excited', 'motivated',
                      'reduce', 'less', 'control', 'balance', 'success', 'progress']
    negative_words = ['sad', 'bad', 'terrible', 'anxious', 'stressed', 'addicted', 'hopeless',
                      'tired', 'exhausted', 'can\'t stop', 'ruining', 'wasting', 'worried',
                      'depressed', 'lonely', 'guilty', 'overwhelmed', 'struggling', 'worse']

    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    total = pos_count + neg_count

    if total == 0:
        compound = 0.0
    else:
        compound = round((pos_count - neg_count) / total, 4)

    if compound > 0.05:
        sentiment = 'Positive'
        emotion = '😊 Very Positive' if compound >= 0.5 else '🙂 Slightly Positive'
    elif compound < -0.05:
        sentiment = 'Negative'
        emotion = '😟 Very Negative' if compound <= -0.5 else '😐 Slightly Negative'
    else:
        sentiment = 'Neutral'
        emotion = '😐 Neutral'

    pos_score = pos_count / max(total, 1)
    neg_score = neg_count / max(total, 1)
    neu_score = 1.0 - pos_score - neg_score if total > 0 else 1.0
    # Generate contextual explanation
    if sentiment == 'Positive':
        explanation = 'Your feedback suggests a healthy awareness and positive outlook toward managing your digital habits. Keep up the great work!'
    elif sentiment == 'Negative':
        explanation = 'Your feedback indicates some emotional distress related to your digital usage patterns. Consider exploring our tips for healthier screen time habits.'
    else:
        explanation = 'Your feedback appears neutral regarding your digital habits. Regular self-reflection can help you stay mindful of your screen time.'

    return {
        'sentiment': sentiment,
        'compound_score': compound,
        'scores': {
            'positive': round(pos_score, 4),
            'negative': round(neg_score, 4),
            'neutral': round(max(0, neu_score), 4)
        },
        'emotion': emotion,
        'brief_explanation': explanation
    }


def batch_analyze(texts):
    """
    Analyze sentiment for multiple texts.

    Args:
        texts: List of text strings

    Returns:
        List of sentiment analysis results
    """
    return [analyze_sentiment(text) for text in texts]


def get_sentiment_summary(results):
    """
    Get summary statistics from multiple sentiment analyses.

    Args:
        results: List of sentiment result dicts

    Returns:
        Summary statistics dict
    """
    if not results:
        return {'total': 0, 'positive': 0, 'negative': 0, 'neutral': 0, 'avg_score': 0}

    sentiments = [r['sentiment'] for r in results]
    scores = [r['compound_score'] for r in results]

    return {
        'total': len(results),
        'positive': sentiments.count('Positive'),
        'negative': sentiments.count('Negative'),
        'neutral': sentiments.count('Neutral'),
        'avg_score': round(sum(scores) / len(scores), 4),
        'positive_pct': round(sentiments.count('Positive') / len(sentiments) * 100, 1),
        'negative_pct': round(sentiments.count('Negative') / len(sentiments) * 100, 1),
        'neutral_pct': round(sentiments.count('Neutral') / len(sentiments) * 100, 1)
    }


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    test_texts = [
        "I feel great and productive today!",
        "I'm so tired of being on my phone all the time. I feel hopeless.",
        "Just a normal day, nothing special happened.",
        "I managed to reduce my screen time and I'm really proud of myself!",
        "I can't stop scrolling and it's ruining my sleep."
    ]

    print("--- OpenAI Sentiment Analysis Tests ---\n")
    for text in test_texts:
        result = analyze_sentiment(text)
        print(f"Text: {text}")
        print(f"  → {result['emotion']} (score: {result['compound_score']})")
        print()
