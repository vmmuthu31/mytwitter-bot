# My Twitter Bot 🚀

An AI-powered Twitter bot that shares authentic, technical developer experiences and tips across Web3, Full Stack, DevOps, and emerging technologies. Built with Python, Tweepy, and Groq LLM.

## Features ✨

- Shares daily tech insights across multiple domains:
  - Web3 & Blockchain Development
  - Full Stack Development
  - DevOps & Cloud
  - Emerging Technologies
  - Open Source & Career
- Generates human-like tweets based on real development experiences
- Uses Groq's LLM for natural language generation
- Runs automatically via GitHub Actions

## Tech Stack 🛠️

- Python 3.11+
- Tweepy (Twitter API v2)
- Groq API (LLama 3 70B model)
- GitHub Actions for automation

## Setup 🔧

1. Clone the repository:

```bash
git clone https://github.com/vmmuthu31/mytwitter-bot
cd mytwitter-bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
GROQ_API_KEY=your_groq_api_key
```

4. Run the bot:

```bash
python trend_groq_special_post.py
```

## GitHub Actions Automation ⚡

The bot is configured to run daily at 8:10 AM UTC using GitHub Actions. You can also trigger it manually through the Actions tab.

## Configuration 🔨

- Modify `TREND_TOPICS` in the script to customize topics
- Adjust `PERSONAL_EXPERIENCES` to add your own experiences
- Fine-tune the Groq LLM parameters in `generate_post()`

## Contributing 🤝

Contributions are welcome! Feel free to:

- Add new tech topics
- Improve tweet generation
- Enhance code quality
- Fix bugs

## License 📝

MIT License - See [LICENSE](LICENSE) for details.

## Author 👨‍💻

Vairamuthu M

- GitHub: [@vmmuthu31](https://github.com/vmmuthu31)
- LinkedIn: [vmmuthu31](https://linkedin.com/in/vmmuthu31)
- Portfolio: [vm-portfolio3.netlify.app](https://vm-portfolio3.netlify.app)

## Acknowledgments 🙏

- Built during various hackathon experiences
- Inspired by real developer conversations and experiences
- Uses technology stack from production experience at Polkassembly.io
