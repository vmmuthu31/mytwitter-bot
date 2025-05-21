import tweepy
import requests
import random
import os

# Twitter API Credentials
API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET = os.environ["TWITTER_API_SECRET"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
BEARER_TOKEN = os.environ["TWITTER_BEARER_TOKEN"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]

try:
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,  
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True
    )
    
    me = client.get_me()
    print("✅ Twitter authentication successful!")
except tweepy.errors.TweepyException as e:
    print(f"❌ Twitter authentication failed: {str(e)}")
    raise

TREND_TOPICS = [
    # Web3 & Blockchain
    "web3 development", "blockchain security", "smart contracts", "NFT development",
    "decentralized apps", "zero-knowledge proofs", "DAO development", "DeFi tips",
    # Full Stack Development
    "NextJS tips", "React optimization", "NestJS backend", "PostgreSQL tips",
    "Mantine UI", "TailwindCSS tricks", "AWS deployment", "Kafka patterns",
    # Open Source & Career
    "open source contribution", "hackathon tips", "tech speaking", "mentorship",
    # DevOps & Cloud
    "AWS S3 tips", "AWS EC2 setup", "AWS SES integration", "cloud deployment",
    # Emerging Tech
    "lit-element", "web components", "storybook patterns", "drupal headless"
]

PERSONAL_EXPERIENCES = {
    "web3": [
        "Built GreenDAO for farmer supply chain management 🌾",
        "Developed Matic Naming Service for decentralized domains 🔍",
        "Created NFT Media - a Web3 social platform with NFT subscriptions 🎨",
        "Won multiple blockchain hackathons including Starknet & APTOS 🏆"
    ],
    "fullstack": [
        "Built scalable systems with NextJS, NestJS & PostgreSQL 🚀",
        "Integrated AWS services (S3, EC2, SES) in production apps ☁️",
        "Developed features for Polkassembly.io including Activity Feed 📱",
        "Created decoupled Drupal systems with web components 🔧"
    ],
    "opensource": [
        "1500+ GitHub contributions and growing 📈",
        "Google Summer of Code 2022 project completion ✨",
        "Mentored 500+ students in technical workshops 👨‍🏫",
        "Speaker at multiple tech conferences and hackathons 🎤"
    ]
}

def get_trend():
    return random.choice(TREND_TOPICS)

def generate_post(trend):
    tech_keywords = {
        "web3": ["web3", "decentralized", "crypto", "ethereum", "solidity", "dapp", "blockchain", "nft", "dao", "defi"],
        "ai": ["ai", "artificial intelligence", "machine learning", "ml", "deep learning", "llm", "neural network", "chatgpt", "openai"],
        "blockchain": ["blockchain", "bitcoin", "ethereum", "crypto", "smart contract", "defi", "web3", "nft", "token"],
        "frontend": ["react", "vue", "nextjs", "frontend", "ui", "tailwind", "mantine", "storybook", "web components"],
        "backend": ["nodejs", "nestjs", "postgresql", "kafka", "api", "graphql", "microservices", "database"],
        "devops": ["aws", "s3", "ec2", "ses", "cloud", "deployment", "scaling"],
        "opensource": ["gsoc", "drupal", "mentorship", "contribution", "community"]
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

    experience = None
    if topic == "web3" or topic == "blockchain":
        experience = random.choice(PERSONAL_EXPERIENCES["web3"])
    elif topic in ["frontend", "backend", "devops"]:
        experience = random.choice(PERSONAL_EXPERIENCES["fullstack"])
    elif topic == "opensource":
        experience = random.choice(PERSONAL_EXPERIENCES["opensource"])

    prompt = (
        f"You're a developer sharing real experience. The topic is '{trend}'.\n"
        + (f"Here's a relevant experience: {experience}.\n" if experience else "")
        + "Write a tweet that's specific, technical, and helpful. Include relevant emojis naturally.\n"
        + "Keep it under 260 chars. Make it sound like a real dev sharing their experience.\n"
        + "Format the tweet with appropriate line breaks for readability. Use 2-3 short paragraphs max.\n"
        + "Start with the main point, then add context or results in the next paragraph."
    )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You're an experienced developer who loves sharing specific, practical tips. "
                                          "You write in a natural, conversational style with personality. "
                                          "Focus on one concrete tip or discovery. No marketing speak."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.9,  
        "top_p": 0.9,
        "presence_penalty": 0.6,  
        "frequency_penalty": 0.7  
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    tweet = resp.json()["choices"][0]["message"]["content"].strip()
    tweet = tweet.replace('"', '')
    tweet = tweet.replace('I would recommend', 'I recommend')
    tweet = tweet.replace('I have found', 'I found')
    tweet = tweet.replace('I am', "I'm")
    tweet = tweet.replace('Just a tip:', '')
    
    # Remove common AI-style starters
    common_starts = ('hey', 'quick tip', 'pro tip', 'tip:', 'fun fact', 'reminder')
    if tweet.lower().startswith(common_starts):
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