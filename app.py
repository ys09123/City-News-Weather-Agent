import streamlit as st
from dotenv import load_dotenv
import os, requests, json

load_dotenv()

st.set_page_config(page_title="City Agent", page_icon="🏙️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
  background: #17212b;
  color: #e8e8e8;
}
.stApp { background: #17212b; }
#MainMenu, footer, header { visibility: hidden; }

.block-container {
  max-width: 680px !important;
  padding: 0 !important;
  margin: 0 auto !important;
}

/* ── Top bar ── */
.topbar {
  position: sticky;
  top: 0;
  z-index: 200;
  background: #212d3b;
  border-bottom: 1px solid #1a2535;
  padding: 0.7rem 1.2rem;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: 0 1px 8px rgba(0,0,0,0.3);
}
.tb-avatar {
  width: 40px; height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2b5278, #3a7bd5);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.1rem;
  flex-shrink: 0;
}
.tb-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: #e8e8e8;
  line-height: 1.2;
}
.tb-status {
  font-size: 0.72rem;
  color: #5bbf82;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 1px;
}
.tb-dot { width: 6px; height: 6px; border-radius: 50%; background: #5bbf82; display:inline-block; }
.tb-pills { margin-left: auto; display: flex; gap: 6px; }
.tb-pill {
  font-size: 0.66rem;
  font-weight: 500;
  color: #7ab3d4;
  background: rgba(58,123,213,0.12);
  border: 1px solid rgba(58,123,213,0.25);
  border-radius: 99px;
  padding: 0.18rem 0.6rem;
  letter-spacing: 0.02em;
}

/* ── Chat area ── */
.chat-area {
  padding: 1rem 1rem 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

/* ── Date stamp ── */
.datesep {
  text-align: center;
  margin: 0.8rem 0;
}
.datesep span {
  font-size: 0.68rem;
  color: #8a9ab0;
  background: #1e2d3d;
  border-radius: 8px;
  padding: 0.22rem 0.75rem;
}

/* ── Message rows ── */
.row-out {
  display: flex;
  justify-content: flex-end;
  margin: 1px 0;
}
.row-in {
  display: flex;
  justify-content: flex-start;
  align-items: flex-end;
  gap: 8px;
  margin: 1px 0;
}
.in-avatar {
  width: 28px; height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2b5278, #3a7bd5);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.78rem;
  flex-shrink: 0;
  margin-bottom: 2px;
}
.in-avatar.ghost { background: transparent; }

/* ── Bubbles ── */
.bbl {
  max-width: 72%;
  padding: 0.52rem 0.85rem 0.45rem;
  font-size: 0.9rem;
  line-height: 1.55;
  word-break: break-word;
  position: relative;
}
.bbl-in {
  background: #182533;
  color: #e8e8e8;
  border-radius: 0 10px 10px 10px;
}
.bbl-out {
  background: #2b5278;
  color: #e8e8e8;
  border-radius: 10px 10px 0 10px;
}
.bbl-time {
  font-size: 0.6rem;
  color: rgba(255,255,255,0.35);
  float: right;
  margin-left: 10px;
  margin-top: 3px;
}
.bbl-out .bbl-time { color: rgba(255,255,255,0.45); }

/* ── Tool result card ── */
.tool-row {
  display: flex;
  justify-content: flex-start;
  align-items: flex-end;
  gap: 8px;
  margin: 3px 0;
}
.tool-card {
  max-width: 72%;
  background: #1e2d3d;
  border: 1px solid #2a3f57;
  border-left: 3px solid;
  border-radius: 0 10px 10px 10px;
  padding: 0.6rem 0.85rem;
  font-size: 0.82rem;
  color: #b0c4d8;
  line-height: 1.55;
}
.tool-card.weather { border-left-color: #f59e0b; }
.tool-card.news    { border-left-color: #3a7bd5; }
.tool-label {
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 0.3rem;
}
.tool-label.weather { color: #f59e0b; }
.tool-label.news    { color: #3a7bd5; }

/* ── Denied ── */
.denied-row {
  display: flex;
  justify-content: center;
  margin: 0.5rem 0;
}
.denied-pill {
  font-size: 0.7rem;
  color: #8a9ab0;
  background: #1e2d3d;
  border-radius: 8px;
  padding: 0.22rem 0.85rem;
}

/* ── Approval card ── */
.appr-row {
  display: flex;
  justify-content: flex-start;
  align-items: flex-end;
  gap: 8px;
  margin: 6px 0 4px;
}
.appr-card {
  max-width: 72%;
  background: #1e2d3d;
  border: 1px solid #2a3f57;
  border-left: 3px solid #f59e0b;
  border-radius: 0 10px 10px 10px;
  padding: 0.75rem 0.9rem;
}
.appr-tag {
  font-size: 0.62rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #f59e0b;
  margin-bottom: 0.5rem;
}
.appr-fn {
  font-family: 'Courier New', monospace;
  font-size: 0.88rem;
  font-weight: 600;
  color: #e8e8e8;
  margin-bottom: 0.4rem;
}
.appr-args {
  font-family: 'Courier New', monospace;
  font-size: 0.76rem;
  color: #7a9ab8;
  background: #141e28;
  border-radius: 6px;
  padding: 0.4rem 0.6rem;
  white-space: pre;
}

/* ── Approve/Deny buttons ── */
div[data-testid="column"]:nth-child(2) .stButton > button {
  background: #1a4a2e !important;
  color: #5bbf82 !important;
  border: 1px solid #2d6b45 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 500 !important;
  border-radius: 8px !important;
  padding: 0.4rem 1rem !important;
  width: 100% !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button:hover {
  background: #1f5c38 !important;
}
div[data-testid="column"]:nth-child(3) .stButton > button {
  background: #3a1a1a !important;
  color: #e05a5a !important;
  border: 1px solid #6b2d2d !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.78rem !important;
  font-weight: 500 !important;
  border-radius: 8px !important;
  padding: 0.4rem 1rem !important;
  width: 100% !important;
}
div[data-testid="column"]:nth-child(3) .stButton > button:hover {
  background: #4a2020 !important;
}

/* ── Chat input ── */
.stChatInput > div {
  background: #212d3b !important;
  border: 1px solid #2a3f57 !important;
  border-radius: 12px !important;
  box-shadow: none !important;
  margin: 0.5rem 1rem 1rem !important;
}
.stChatInput > div:focus-within {
  border-color: #3a7bd5 !important;
}
.stChatInput textarea {
  background: transparent !important;
  color: #e8e8e8 !important;
  font-family: 'Inter', sans-serif !important;
  font-size: 0.9rem !important;
}
.stChatInput textarea::placeholder { color: #4a5e72 !important; }
.stChatInput button {
  background: #2b5278 !important;
  border-radius: 8px !important;
}
.stChatInput button:hover { background: #3a6898 !important; }

/* ── Empty state ── */
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 4rem 1rem 2rem;
  text-align: center;
  color: #8a9ab0;
}
.empty-icon { font-size: 2.8rem; margin-bottom: 0.8rem; opacity: 0.7; }
.empty-title { font-size: 1rem; font-weight: 600; color: #c5d5e5; margin-bottom: 0.4rem; }
.empty-sub { font-size: 0.82rem; line-height: 1.6; max-width: 260px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 1.2rem; }
.chip {
  font-size: 0.78rem;
  color: #7ab3d4;
  background: rgba(58,123,213,0.1);
  border: 1px solid rgba(58,123,213,0.22);
  border-radius: 8px;
  padding: 0.3rem 0.75rem;
}

.stSpinner > div { border-top-color: #3a7bd5 !important; }
</style>
""", unsafe_allow_html=True)

# ── Topbar ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="tb-avatar">🏙️</div>
  <div>
    <div class="tb-name">City Agent</div>
    <div class="tb-status"><span class="tb-dot"></span> online</div>
  </div>
  <div class="tb-pills">
    <span class="tb-pill">☁ Weather</span>
    <span class="tb-pill">📰 News</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "lc_messages" not in st.session_state:
    st.session_state.lc_messages = []
if "pending_tool_call" not in st.session_state:
    st.session_state.pending_tool_call = None
if "processing" not in st.session_state:
    st.session_state.processing = False

# ── Tools ─────────────────────────────────────────────────────────────────
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from tavily import TavilyClient

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Could not fetch weather')}"
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    humidity = data["main"]["humidity"]
    feels = data["main"]["feels_like"]
    return f"Weather in {city}: {desc}, {temp}°C (feels like {feels}°C), humidity {humidity}%"

@tool
def get_news(city: str) -> str:
    """Get latest news about a city"""
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily.search(query=f"latest news in {city}", search_depth="basic", max_results=3)
    results = response.get("results", [])
    if not results:
        return f"No news found for {city}"
    news_list = []
    for r in results:
        title = r.get("title", "No title")
        url   = r.get("url", "")
        snippet = r.get("content", "")[:120]
        news_list.append(f"• {title}\n  {url}\n  {snippet}...")
    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)

tools = [get_weather, get_news]
tools_by_name = {t.name: t for t in tools}

llm = ChatMistralAI(model="mistral-small-2506")
llm_with_tools = llm.bind_tools(tools)

def call_llm():
    response = llm_with_tools.invoke(st.session_state.lc_messages)
    st.session_state.lc_messages.append(response)
    return response

def execute_tool(tool_call):
    tool_fn = tools_by_name[tool_call["name"]]
    result = tool_fn.invoke(tool_call["args"])
    tm = ToolMessage(content=result, tool_call_id=tool_call["id"])
    st.session_state.lc_messages.append(tm)
    return result

# ── Chat area ─────────────────────────────────────────────────────────────
st.markdown('<div class="chat-area">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
<div class="empty">
  <div class="empty-icon">🏙️</div>
  <div class="empty-title">City Agent</div>
  <div class="empty-sub">Ask me about the weather or latest news in any Indian city.</div>
  <div class="chips">
    <span class="chip">☁ Weather in Mumbai</span>
    <span class="chip">📰 News in Delhi</span>
    <span class="chip">🌡 How's Bangalore?</span>
  </div>
</div>
""", unsafe_allow_html=True)

prev_kind = None
for item in st.session_state.messages:
    kind = item["kind"]

    if kind == "user":
        st.markdown(f"""
<div class="row-out">
  <div class="bbl bbl-out">
    {item['text']}
  </div>
</div>
""", unsafe_allow_html=True)

    elif kind == "bot":
        show_av = prev_kind not in ("bot", "tool_result")
        av = '<div class="in-avatar">🏙</div>' if show_av else '<div class="in-avatar ghost"></div>'
        st.markdown(f"""
<div class="row-in">
  {av}
  <div class="bbl bbl-in">{item['text']}</div>
</div>
""", unsafe_allow_html=True)

    elif kind == "tool_result":
        is_w = item["tool"] == "get_weather"
        cls   = "weather" if is_w else "news"
        icon  = "☁ Weather" if is_w else "📰 News"
        show_av = prev_kind not in ("bot", "tool_result")
        av = '<div class="in-avatar">🏙</div>' if show_av else '<div class="in-avatar ghost"></div>'
        st.markdown(f"""
<div class="tool-row">
  {av}
  <div class="tool-card {cls}">
    <div class="tool-label {cls}">{icon} result</div>
    {item['text']}
  </div>
</div>
""", unsafe_allow_html=True)

    elif kind == "denied":
        st.markdown(f"""
<div class="denied-row">
  <span class="denied-pill">🚫 {item['tool']} denied</span>
</div>
""", unsafe_allow_html=True)

    prev_kind = kind

st.markdown('</div>', unsafe_allow_html=True)

# ── Approval card ─────────────────────────────────────────────────────────
if st.session_state.pending_tool_call:
    tc = st.session_state.pending_tool_call
    tool_name = tc["name"]
    tool_args = tc["args"]
    icon = "☁" if tool_name == "get_weather" else "📰"

    st.markdown(f"""
<div class="appr-row">
  <div class="in-avatar">🏙</div>
  <div class="appr-card">
    <div class="appr-tag">⚡ Tool request</div>
    <div class="appr-fn">{icon} {tool_name}()</div>
    <div class="appr-args">{json.dumps(tool_args, indent=2)}</div>
  </div>
</div>
""", unsafe_allow_html=True)

    _, col_a, col_d, _ = st.columns([0.28, 1, 1, 1.8])
    with col_a:
        if st.button("✓ Allow", key="approve_btn"):
            with st.spinner(f"Running {tool_name}…"):
                result = execute_tool(tc)
            st.session_state.messages.append({"kind": "tool_result", "tool": tool_name, "text": result})
            st.session_state.pending_tool_call = None
            st.session_state.processing = True
            st.rerun()
    with col_d:
        if st.button("✕ Deny", key="deny_btn"):
            deny_msg = ToolMessage(content="Tool call denied by user.", tool_call_id=tc["id"])
            st.session_state.lc_messages.append(deny_msg)
            st.session_state.messages.append({"kind": "denied", "tool": tool_name})
            st.session_state.pending_tool_call = None
            st.session_state.processing = True
            st.rerun()

# ── Continue processing ───────────────────────────────────────────────────
if st.session_state.processing and not st.session_state.pending_tool_call:
    with st.spinner("typing…"):
        response = call_llm()
    if response.tool_calls:
        st.session_state.pending_tool_call = response.tool_calls[0]
        st.session_state.processing = False
    else:
        st.session_state.messages.append({"kind": "bot", "text": response.content})
        st.session_state.processing = False
    st.rerun()

# ── Input ─────────────────────────────────────────────────────────────────
if not st.session_state.pending_tool_call and not st.session_state.processing:
    user_input = st.chat_input("Message City Agent…")
    if user_input:
        st.session_state.messages.append({"kind": "user", "text": user_input})
        st.session_state.lc_messages.append(HumanMessage(content=user_input))
        with st.spinner("typing…"):
            response = call_llm()
        if response.tool_calls:
            st.session_state.pending_tool_call = response.tool_calls[0]
        else:
            st.session_state.messages.append({"kind": "bot", "text": response.content})
        st.rerun()