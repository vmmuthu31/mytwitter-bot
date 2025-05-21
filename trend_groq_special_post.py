import tweepy
import requests
import random
import time
import os

API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET = os.environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

def get_trend():
    trends = api.get_place_trends(1)[0]["trends"]
    trending_topics = [t for t in trends if t["tweet_volume"] and not t["promoted_content"]]
    return random.choice(trending_topics)["name"] if trending_topics else "technology"

def generate_post(trend):
    tech_keywords = {
        "web3": ["web3", "decentralized", "crypto", "ethereum", "solidity", "dapp", "blockchain"],
        "ai": ["ai", "artificial intelligence", "machine learning", "ml", "deep learning", "llm", "neural network"],
        "blockchain": ["blockchain", "bitcoin", "ethereum", "crypto", "smart contract", "defi"],
    }
    lower_trend = trend.lower()
    topic = None
    for key, keywords in tech_keywords.items():
        if any(word in lower_trend for word in keywords):
            topic = key
            break
    if topic == "web3":
        extra = ("Share a practical web3 tip, tutorial, or resource for devs in a fun, human way. "
                 "Encourage followers to share their web3 learning journey or favorite tools.")
    elif topic == "ai":
        extra = ("Share a cool AI/ML tip, tutorial, or resource for developers. "
                 "Make it engaging, and ask followers for their go-to AI libraries or use-cases.")
    elif topic == "blockchain":
        extra = ("Share a helpful blockchain development tip, tutorial, or resource. "
                 "Ask followers about their favorite blockchain projects or what they find most challenging.")
    else:
        extra = ("Share a quick, actionable dev tip or resource related to the trend. "
                 "Encourage devs to discuss or ask questions about this topic.")
    prompt = (
        f"Write an irresistible, witty, and conversation-starting tweet for developers about the trending topic '{trend}'. "
        f"{extra} Make it sound like a real human, use a touch of humor, and keep it under 260 characters."
    )
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a fun, witty, and creative developer and social media expert."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 80,
        "temperature": 0.97
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()

def post_tweet(text):
    try:
        api.update_status(status=text)
        print("✅ Tweet posted successfully!")
    except tweepy.TweepError as e:
        print("❌ Tweet failed:", e)

if __name__ == "__main__":
    trend = get_trend()
    print(f"🔥 Today's trend: {trend}")
    tweet = generate_post(trend)
    print(f"📝 Generated tweet: {tweet}\n")
    post_tweet(tweet)