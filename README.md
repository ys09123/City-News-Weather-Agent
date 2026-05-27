# 🏙️ City Agent

A conversational AI agent that fetches **real-time weather** and **latest news** for any city, with a **human-in-the-loop approval system** before every tool call. Built with Streamlit, LangChain, Mistral AI, Tavily, and OpenWeatherMap.

---

## ✨ Features

- 💬 **Chat Interface** — Natural language conversation powered by Mistral AI
- 🌤️ **Weather Tool** — Live weather data via OpenWeatherMap API
- 📰 **News Tool** — Latest city news via Tavily Search
- 🔐 **Human-in-the-Loop** — Approve or deny every tool call before it executes
- 🎨 **Dark Terminal UI** — Sleek Space Mono + Outfit typography, teal/amber accents

---

## 🖥️ Demo

```
You:  What's the weather like in Mumbai?

⚠ Tool Call — Awaiting Approval
  get_weather  →  { "city": "Mumbai" }

  [ ✓ Approve ]  [ ✕ Deny ]

🤖  Weather in Mumbai: haze, 34°C (feels like 39°C), humidity 72%
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Mistral AI (`mistral-small-2506`) |
| Agent Framework | LangChain Core |
| News Search | Tavily |
| Weather Data | OpenWeatherMap |
| Env Management | python-dotenv |

---

## 📁 Project Structure

```
city-agent/
├── city_agent.py       # Main Streamlit app
├── .env                # API keys (never commit this)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/city-agent.git
cd city-agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

> **Where to get API keys:**
> - Mistral AI → [console.mistral.ai](https://console.mistral.ai)
> - Tavily → [app.tavily.com](https://app.tavily.com)
> - OpenWeatherMap → [openweathermap.org/api](https://openweathermap.org/api)

### 4. Run the app

```bash
streamlit run city_agent.py
```

The app will open at `http://localhost:8501`.

---

## 📦 Requirements

```txt
streamlit
langchain-mistralai
langchain-core
tavily-python
requests
python-dotenv
```

Or install all at once:

```bash
pip install streamlit langchain-mistralai langchain-core tavily-python requests python-dotenv
```

---

## 🔄 How It Works

```
User Input
    │
    ▼
Mistral LLM  ──── decides tool needed ────▶  Approval Card (Approve / Deny)
    │                                               │
    │◀────────── tool result ────────────── Execute Tool
    │
    ▼
Final Answer → Chat Bubble
```

1. User sends a message
2. The LLM decides if a tool (`get_weather` or `get_news`) is needed
3. An approval card appears showing the tool name and arguments
4. User clicks **Approve** → tool runs, result shown inline
5. User clicks **Deny** → LLM is informed and responds without the tool
6. LLM generates a final natural language answer

---

## 🚀 Deployment

### Streamlit Community Cloud (Recommended)

1. Push the project to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Under **Advanced Settings → Secrets**, add your API keys:

```toml
MISTRAL_API_KEY = "your_key"
TAVILY_API_KEY = "your_key"
OPENWEATHER_API_KEY = "your_key"
```

4. Click **Deploy** — live in under 2 minutes

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "city_agent.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t city-agent .
docker run -p 8501:8501 --env-file .env city-agent
```

---

## ⚠️ Important Notes

- The weather API uses `IN` (India) as the default country code. Change `q={city},IN` in `get_weather` to target other countries.
- Never commit your `.env` file. Add it to `.gitignore`:

```bash
echo ".env" >> .gitignore
```

---

## 📄 License

MIT License — free to use, modify, and distribute.
