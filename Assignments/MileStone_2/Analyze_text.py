from transformers import pipeline
import time

sentiment_analyzer = pipeline("sentiment-analysis", model = "distilbert/distilbert-base-uncased-finetuned-sst-2-english")
tone_analyzer = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
intent_analyzer = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def summarize_results(sentiment, tone, intent):
    sentiment_label = sentiment[0]['label']
    tone_label = tone[0]['label']
    intent_label = intent['labels'][0] 
    intent_score = intent['scores'][0]

    if sentiment_label == "NEGATIVE" and tone_label == "joy":
        tone_interpretation = "Polite Concern"
    elif sentiment_label == "POSITIVE" and tone_label == "joy":
        tone_interpretation = "Positive Joy"
    elif sentiment_label == "NEGATIVE" and tone_label != "joy":
        tone_interpretation = f"Negative {tone_label.capitalize()}"
    else:
        tone_interpretation = tone_label.capitalize()

    summary = {
        "Sentiment": sentiment_label.capitalize(),
        "Tone": tone_interpretation,
        "Intent": f"{intent_label.capitalize()} ({intent_score * 100:.2f}% confidence)"
    }
    return summary

def analyze_audio(transcription):
    start = time.time()
    sentiment = sentiment_analyzer(transcription)
    tone = tone_analyzer(transcription)
    # intent = intent_analyzer(transcription, candidate_labels=["question", "command", "statement"])
    intent = intent_analyzer(
        transcription, 
        candidate_labels=[
            "product inquiry",
            "pricing inquiry",
            "comparison inquiry",
            "usage inquiry",
            "availability inquiry",
            "ready to purchase",
            "seeking discounts",
            "bulk purchase inquiry",
            "payment terms negotiation",
            "trust evaluation",
            "long-term partnership",
            "feedback sharing",
            "issue resolution",
            "service guarantee",
            "requesting customization",
            "clarification",
            "deadline push",
            "alternative offers",
            "approval seeking",
            "exit intention",
            "expressing frustration",
            "seeking reassurance",
            "hesitation/uncertainty",
            "positive feedback",
            "referrals",
            "competitive pricing inquiry",
            "market exploration",
            "service complaint",
            "refund request",
            "escalation request",
            "order confirmation",
            "follow-up inquiry",
            "re-engagement",
            "seeking recommendations",
            "learning more"
        ]
    )

    end = time.time()
    print(f"Time taken for analysis: {end - start:.2f}s")

    summary = summarize_results(sentiment, tone, intent)
    print("Summary:")
    print(summary)

if __name__ == "__main__":
    analyze_audio("could you tell me more about your product offerings?")
