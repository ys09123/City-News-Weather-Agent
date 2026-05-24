import streamlit as st
from dotenv import load_dotenv
import os, requests, json

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(page_title="City Agent", page_icon="🏙️", layout="centered")

# ── CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
  font-family: 'Outfit', sans-serif;
  background: #07080a;
  color: #e2e8f0;
}
.stApp { background: #07080a; }

/* ── Header ── */
.agent-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 2rem 0 1.2rem;
  border-bottom: 1px solid #1e2533;
  margin-bottom: 1.5rem;
}
.agent-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
  background: #22d3a5;
  box-shadow: 0 0 8px #22d3a5;
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
.agent-title {
  font-family: 'Space Mono', monospace;
  font-size: 1.1rem;
  font-weight: 700;
  color: #e2e8f0;
  letter-spacing: 0.05em;
}
.agent-sub {
  font-size: 0.72rem;
  color: #4a5568;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-top: 2px;
}

/* ── Chat messages ── */
.msg-row {
  display: flex;
  gap: 12px;
  margin-bottom: 1.2rem;
  align-items: flex-start;
}
.msg-row.user { flex-direction: row-reverse; }

.avatar {
  width: 34px; height: 34px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.9rem;
  flex-shrink: 0;
}
.avatar.bot { background: #0f2027; border: 1px solid #22d3a5; color: #22d3a5; }
.avatar.user { background: #1a1f2e; border: 1px solid #3b82f6; color: #93c5fd; }

.bubble {
  max-width: 78%;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  font-size: 0.92rem;
  line-height: 1.6;
}
.bubble.bot {
  background: #0d1117;
  border: 1px solid #1e2533;
  border-top-left-radius: 2px;
  color: #cbd5e1;
}
.bubble.user {
  background: #1e3a5f;
  border: 1px solid #2563eb44;
  border-top-right-radius: 2px;
  color: #e2e8f0;
  text-align: right;
}

/* ── Tool call approval card ── */
.approval-card {
  background: #0d1117;
  border: 1px solid #f59e0b44;
  border-left: 3px solid #f59e0b;
  border-radius: 10px;
  padding: 1.1rem 1.3rem;
  margin: 1rem 0;
}
.approval-tag {
  font-family: 'Space Mono', monospace;
  font-size: 0.7rem;
  color: #f59e0b;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}
.approval-tool {
  font-family: 'Space Mono', monospace;
  font-size: 1rem;
  font-weight: 700;
  color: #fcd34d;
  margin-bottom: 0.3rem;
}
.approval-args {
  font-family: 'Space Mono', monospace;
  font-size: 0.8rem;
  color: #94a3b8;
  background: #060810;
  border-radius: 6px;
  padding: 0.5rem 0.75rem;
  margin-top: 0.5rem;
}

/* ── Tool result badge ── */
.tool-result {
  background: #060d12;
  border: 1px solid #22d3a522;
  border-left: 3px solid #22d3a5;
  border-radius: 8px;
  padding: 0.7rem 1rem;
  margin: 0.6rem 0;
  font-family: 'Space Mono', monospace;
  font-size: 0.78rem;
  color: #64748b;
}
.tool-result-label {
  color: #22d3a5;
  font-size: 0.68rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  margin-bottom: 0.3rem;
}

/* ── Denied badge ── */
.denied-badge {
  display: inline-block;
  background: #1f0a0a;
  border: 1px solid #ef444433;
  color: #f87171;
  font-family: 'Space Mono', monospace;
  font-size: 0.72rem;
  padding: 0.25rem 0.7rem;
  border-radius: 4px;
  margin: 0.4rem 0;
}

/* ── Input ── */
.stChatInput > div {
  background: #0d1117 !important;
  border: 1px solid #1e2533 !important;
  border-radius: 10px !important;
}
.stChatInput textarea {
  background: transparent !important;
  color: #e2e8f0 !important;
  font-family: 'Outfit', sans-serif !important;
}
.stChatInput button {
  background: #22d3a5 !important;
  border-radius: 7px !important;
}

/* ── Approve/Deny buttons ── */
div[data-testid="column"]:nth-child(1) .stButton > button {
  background: #064e3b !important;
  color: #34d399 !important;
  border: 1px solid #059669 !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.08em !important;
  border-radius: 6px !important;
  width: 100% !important;
}
div[data-testid="column"]:nth-child(2) .stButton > button {
  background: #450a0a !important;
  color: #f87171 !important;
  border: 1px solid #dc2626 !important;
  font-family: 'Space Mono', monospace !important;
  font-size: 0.78rem !important;
  letter-spacing: 0.08em !important;
  border-radius: 6px !important;
  width: 100% !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #22d3a5 !important; }

/* ── Scrollable chat ── */
.chat-area { max-height: 62vh; overflow-y: auto; padding-right: 4px; }

/* Hide branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="agent-header">
  <div class="agent-dot"></div>
  <div>
    <div class="agent-title">CITY AGENT</div>
    <div class="agent-sub">Weather · News</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []          # chat history for display
if "lc_messages" not in st.session_state:
    st.session_state.lc_messages = []       # langchain message objects
if "pending_tool_call" not in st.session_state:
    st.session_state.pending_tool_call = None   # waiting for approval
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
        url = r.get("url", "")
        snippet = r.get("content", "")[:120]
        news_list.append(f"• {title}\n  {url}\n  {snippet}...")
    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)

tools = [get_weather, get_news]
tools_by_name = {t.name: t for t in tools}

llm = ChatMistralAI(model="mistral-small-2506")
llm_with_tools = llm.bind_tools(tools)

# ── Helper: run one LLM step ──────────────────────────────────────────────
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

# ── Render chat history ────────────────────────────────────────────────────
def render_history():
    for item in st.session_state.messages:
        kind = item["kind"]

        if kind == "user":
            st.markdown(f"""
<div class="msg-row user">
  <div class="avatar user">You</div>
  <div class="bubble user">{item['text']}</div>
</div>""", unsafe_allow_html=True)

        elif kind == "bot":
            st.markdown(f"""
<div class="msg-row">
  <div class="avatar bot">🤖</div>
  <div class="bubble bot">{item['text']}</div>
</div>""", unsafe_allow_html=True)

        elif kind == "tool_result":
            icon = "🌤️" if item["tool"] == "get_weather" else "📰"
            st.markdown(f"""
<div class="tool-result">
  <div class="tool-result-label">{icon} {item['tool']} result</div>
  {item['text']}
</div>""", unsafe_allow_html=True)

        elif kind == "denied":
            st.markdown(f'<div class="denied-badge">⛔ {item["tool"]} — denied by user</div>',
                        unsafe_allow_html=True)

render_history()

# ── Pending tool-call approval UI ─────────────────────────────────────────
if st.session_state.pending_tool_call:
    tc = st.session_state.pending_tool_call
    tool_name = tc["name"]
    tool_args = tc["args"]
    icon = "🌤️" if tool_name == "get_weather" else "📰"

    st.markdown(f"""
<div class="approval-card">
  <div class="approval-tag">⚠ Tool Call — Awaiting Approval</div>
  <div class="approval-tool">{icon} {tool_name}</div>
  <div class="approval-args">{json.dumps(tool_args, indent=2)}</div>
</div>""", unsafe_allow_html=True)

    col_a, col_d = st.columns(2)
    with col_a:
        if st.button("✓ Approve", key="approve_btn"):
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

# ── Continue agent after approval/denial ──────────────────────────────────
if st.session_state.processing and not st.session_state.pending_tool_call:
    with st.spinner("Thinking…"):
        response = call_llm()

    if response.tool_calls:
        # More tools to approve
        st.session_state.pending_tool_call = response.tool_calls[0]
        st.session_state.processing = False
    else:
        # Final answer
        answer = response.content
        st.session_state.messages.append({"kind": "bot", "text": answer})
        st.session_state.processing = False
    st.rerun()

# ── Chat input ────────────────────────────────────────────────────────────
if not st.session_state.pending_tool_call and not st.session_state.processing:
    user_input = st.chat_input("Ask about weather or news in any city…")
    if user_input:
        # Add user message
        st.session_state.messages.append({"kind": "user", "text": user_input})
        st.session_state.lc_messages.append(HumanMessage(content=user_input))

        with st.spinner("Thinking…"):
            response = call_llm()

        if response.tool_calls:
            st.session_state.pending_tool_call = response.tool_calls[0]
        else:
            st.session_state.messages.append({"kind": "bot", "text": response.content})

        st.rerun()