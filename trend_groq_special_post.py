import tweepy
import requests
import random
import os

API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET = os.environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Initialize the Twitter API v2 client
client = tweepy.Client(
    consumer_key=API_KEY, 
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN, 
    access_token_secret=ACCESS_TOKEN_SECRET
)

TREND_TOPICS = [
    "web3 development", "AI in coding", "blockchain security", "smart contracts",
    "machine learning", "open source tools", "devops best practices", "prompt engineering",
    "cloud functions", "zero-knowledge proofs", "ReactJS trends", "TypeScript tips",
    "Python automation", "Llama 3 models", "coding productivity hacks", "frontend frameworks",
    "backend scaling", "cybersecurity basics", "mobile app debugging"
]

def get_trend():
    return random.choice(TREND_TOPICS)

def generate_post(trend):
    tech_keywords = {
        "web3": ["web3", "decentralized", "crypto", "ethereum", "solidity", "dapp", "blockchain", "nft", "dao", "defi"],
        "ai": ["ai", "artificial intelligence", "machine learning", "ml", "deep learning", "llm", "neural network", "chatgpt", "openai", "stable diffusion", "midjourney"],
        "blockchain": ["blockchain", "bitcoin", "ethereum", "crypto", "smart contract", "defi", "web3", "nft", "token", "mining"],
        "frontend": ["react", "vue", "angular", "javascript", "typescript", "css", "html", "nextjs", "frontend", "ui", "ux"],
        "backend": ["nodejs", "python", "java", "golang", "api", "rest", "graphql", "microservices", "database", "sql"],
        "devops": ["docker", "kubernetes", "aws", "azure", "devops", "ci/cd", "cloud", "deployment", "scaling", "monitoring"],
        "cybersecurity": ["security", "hack", "vulnerability", "encryption", "cyber", "privacy", "authentication", "breach"],
        "mobile": ["android", "ios", "flutter", "react native", "swift", "kotlin", "mobile app", "pwa"]
    }
    lower_trend = trend.lower()
    topic = None
    for key, keywords in tech_keywords.items():
        if any(word in lower_trend for word in keywords):
            topic = key
            break

    if topic == "web3":
        extra = ("Drop a super practical Web3 hack you discovered recently - could be a gas optimization trick, "
                 "a smart contract security tip, or your fav dev tool. What's your current Web3 stack? 🛠️")
    elif topic == "ai":
        extra = ("Share your hands-on experience with AI tools - performance tips, model tweaking secrets, "
                 "or that one weird trick that saved you hours. What surprised you most about working with AI? 🤔")
    elif topic == "frontend":
        extra = ("Drop that frontend trick that made you go 'why didn't I know this before?!' "
                 "Performance hacks, CSS magic, or React patterns - what's your secret sauce? 💅")
    elif topic == "backend":
        extra = ("Backend wizards, share that database query optimization trick, API design pattern, "
                 "or scaling hack that saved your day. What's your current backend stack? 🚀")
    elif topic == "devops":
        extra = ("DevOps ninjas, what's that deployment script or monitoring setup that's been a game-changer? "
                 "Share your container optimization tricks or CI/CD time-savers! 🔧")
    elif topic == "cybersecurity":
        extra = ("Security folks, drop that essential protection tip or detection technique "
                 "you wish every dev knew about. What's your go-to security testing approach? 🔒")
    elif topic == "mobile":
        extra = ("Mobile devs, share your app performance secrets, state management tricks, "
                 "or cross-platform hacks. What's your favorite debugging technique? 📱")
    elif topic == "blockchain":
        extra = ("Blockchain devs, what's your favorite smart contract pattern or gas optimization trick? "
                 "Share your testing approach or deployment checklist! ⛓️")
    else:
        extra = ("Share that game-changing dev tip you learned recently - could be about testing, "
                 "coding patterns, or tools. What made you level up as a developer? 🎯")

    other_trends = random.sample([t for t in TREND_TOPICS if t != trend], 2)

    prompt = (
        f"You're a developer who loves sharing practical tips. The trending topic is '{trend}' "
        f"and some other hot topics are {', '.join(other_trends)}. {extra} "
        f"Write a tweet that's specific, useful, and conversation-starting. Include relevant emojis, "
        f"but use them naturally. Keep it under 260 chars. Make it sound like a real dev sharing their experience."
    )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You're an experienced developer who loves sharing specific, practical tips. "
                                          "You write in a natural, conversational style with personality. "
                                          "You avoid generic advice and corporate speak."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.85,
        "top_p": 0.95,
        "presence_penalty": 0.3,
        "frequency_penalty": 0.5
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    tweet = resp.json()["choices"][0]["message"]["content"].strip()
    tweet = tweet.replace('"', '')

    if tweet.lower().startswith(("hey", "quick tip", "pro tip")):
        tweet = tweet.split(' ', 1)[1]

    return tweet

def post_tweet(text):
    try:
        response = client.create_tweet(text=text)
        print("✅ Tweet posted successfully!")
        return response
    except tweepy.errors.TweepyException as e:
        print("❌ Tweet failed:", str(e))
        return None

if __name__ == "__main__":
    trend = get_trend()
    print(f"🔥 Today's trend: {trend}")
    tweet = generate_post(trend)
    print(f"📝 Generated tweet: {tweet}\n")
    post_tweet(tweet)