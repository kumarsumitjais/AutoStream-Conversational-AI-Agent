import re
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings


# ----------------------------
# Embedding model (loaded once)
# ----------------------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


INTENT_EXAMPLES = {
    "greeting": [
        "hi",
        "hello",
        "hey there",
        "how are you",
        "anyone there",
        "good morning",
        "good evening"
    ],
    "inquiry": [
        "tell me about your plans",
        "what pricing do you have",
        "explain the pro plan",
        "compare basic and pro",
        "what features are included",
        "refund policy details",
        "customer support information"
    ],
    "high_intent": [
        "i want to buy the pro plan",
        "i want to subscribe",
        "ready to get started",
        "interested in premium plan",
        "how do i sign up",
        "i want to purchase this plan"
    ]
}


# Precompute embeddings for intent examples
INTENT_VECTORS = {
    intent: embedding_model.embed_documents(examples)
    for intent, examples in INTENT_EXAMPLES.items()
}


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def semantic_intent_match(message: str, threshold: float = 0.55):
    query_vec = embedding_model.embed_query(message)

    best_intent = None
    best_score = 0.0

    for intent, vectors in INTENT_VECTORS.items():
        for vec in vectors:
            score = cosine_similarity(query_vec, vec)
            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score >= threshold:
        return best_intent, float(best_score)

    return None, 0.0


PLAN_KEYWORDS = [
    "basic plan", "basic",
    "pro plan", "pro",
    "premium plan", "premium"
]



greeting_phrases = [
    "hi", "hii", "hello", "hey", "hey there",
    "yo", "whats up", "how are you",
    "good morning", "good evening"
]

high_intent_phrases = [
    "want to buy", "purchase", "subscribe",
    "sign up", "signup", "get started",
    "interested in", "ready to buy",
    "buy pro", "purchase pro",
    "want the pro plan", "want pro plan",
    "upgrade to pro", "go pro","want to have the pro plan",
    
]

inquiry_phrases = [
    "plan", "plans", "pricing", "price",
    "features", "details", "compare",
    "refund", "support", "information",
    "tell me about"
]
def classify_intent(user_message: str):
    message = normalize(user_message)

    # -------- HIGH INTENT (TOP PRIORITY) --------
    buy_words = [
        "want", "buy", "purchase", "subscribe",
        "sign up", "signup", "register",
        "upgrade", "go for", "choose", "take"
    ]

    plan_keywords = [
        "basic", "basic plan",
        "pro", "pro plan",
        "premium", "premium plan"
    ]

    if any(buy in message for buy in buy_words) and any(plan in message for plan in plan_keywords):
        return "high_intent", 0.93

    # -------- INQUIRY (SECOND PRIORITY) --------
    if any(phrase in message for phrase in inquiry_phrases):
        return "inquiry", 0.85

    # -------- GREETING (ONLY IF PURE GREETING) --------
    if any(phrase in message for phrase in greeting_phrases):
        return "greeting", 0.90

    # -------- SEMANTIC FALLBACK --------
    semantic_intent, score = semantic_intent_match(message)
    if semantic_intent:
        return semantic_intent, score

    # -------- SAFE FALLBACK --------
    return "inquiry", 0.40



