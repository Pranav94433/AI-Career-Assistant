import streamlit as st
try:
    import ollama
except ImportError:
    ollama = None
import io
import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --ink: #f5f5f5;
    --muted: #b5b5b5;
    --mint: #263c37;
    --teal: #167d72;
    --coral: #f47b61;
    --paper: #050505;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}

[data-testid="stAppViewContainer"] {
    background: var(--paper);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stAppViewContainer"] * {
    color: var(--ink);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #151515 0%, #0b0b0b 100%);
    border-right: 1px solid #2d2d2d;
    min-width: 17rem;
    max-width: 17rem;
}

[data-testid="stSidebar"] * {
    color: var(--ink);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #8de0c2 !important;
}

[data-testid="stFileUploader"] {
    background: #1b1b1b;
    border: 2px solid #3f9f7f;
    border-radius: 8px;
    box-shadow: 0 5px 16px rgba(22, 125, 114, 0.16);
    padding: 0.8rem;
}

[data-testid="stMainBlockContainer"] {
    width: min(100%, 52rem);
    max-width: 52rem;
    padding-top: 2rem;
    padding-bottom: 8rem;
}

[data-testid="stHorizontalBlock"] {
    width: 100%;
}

[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
    background: #111111;
    border: 2px dashed #5eb997;
    border-radius: 6px;
    min-height: 6rem;
}

[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] button {
    color: #f5f5f5 !important;
}

[data-testid="stFileUploader"] button {
    background: var(--teal) !important;
    border: 0 !important;
    border-radius: 6px !important;
    color: #ffffff !important;
    font-weight: 700;
}

[data-testid="stChatMessage"] {
    background: transparent;
    border: 0;
    color: var(--ink) !important;
}

[data-testid="stChatMessage"][aria-label="assistant message"] {
    background: #171717;
    border: 1px solid #292929;
    border-radius: 8px;
    padding: 0.75rem 1rem;
}

[data-testid="stChatMessage"][aria-label="assistant message"] * {
    color: #ffffff !important;
    font-size: 0.94rem;
    line-height: 1.45;
}

[data-testid="stChatMessage"][aria-label="assistant message"] code {
    background: #292929;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] strong,
[data-testid="stChatMessage"] code {
    color: var(--ink) !important;
}

[data-testid="stChatInput"] {
    background: #161616;
    border: 1px solid #424242;
    border-radius: 18px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    padding: 0.35rem 0.55rem;
}

[data-testid="stChatInput"] textarea {
    background: #161616 !important;
    border: 0 !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    caret-color: var(--teal);
    min-height: 4.5rem !important;
    padding: 0.8rem 0.85rem !important;
    box-shadow: none;
    transition: background 160ms ease, border-color 160ms ease, box-shadow 160ms ease;
}

[data-testid="stChatInput"] textarea:focus {
    background: #1d1d1d !important;
    border-color: transparent !important;
    box-shadow: none;
}

[data-testid="stChatInputSubmitButton"] button {
    background: #3f9f7f !important;
    border-radius: 50% !important;
    color: #ffffff !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: var(--muted) !important;
    opacity: 1;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 0;
}

.welcome {
    padding: 1.5rem 0 0.7rem;
    text-align: center;
}

.welcome-kicker {
    color: var(--teal);
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

.welcome h2 {
    color: var(--ink);
    font-size: clamp(1.8rem, 4vw, 3.1rem);
    line-height: 1.05;
    margin: 0.35rem 0 0.65rem;
}

.welcome p {
    color: var(--muted);
    font-size: 1.05rem;
    max-width: 42rem;
    margin: 0 auto;
}

div.stButton > button {
    border: 1px solid #3b514a;
    border-radius: 8px;
    color: #f5f5f5;
    background: #1b2b27;
    min-height: 3.2rem;
    text-align: left;
    transition: border-color 160ms ease, transform 160ms ease, background 160ms ease;
}

@media (max-width: 900px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1.25rem 1rem 7rem;
    }

    .welcome h2 {
        font-size: 2.2rem;
    }
}

@media (max-width: 600px) {
    [data-testid="stMainBlockContainer"] {
        padding: 0.75rem 0.7rem 6rem;
    }

    h1 {
        font-size: 1.65rem !important;
    }

    .welcome {
        padding-top: 0.75rem;
    }

    .welcome h2 {
        font-size: 1.8rem;
    }

    .welcome p {
        font-size: 0.95rem;
    }

    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap;
        gap: 0.5rem;
    }

    [data-testid="stHorizontalBlock"] > [data-testid="column"] {
        flex: 1 1 100% !important;
        min-width: 100% !important;
    }

    [data-testid="stChatMessage"] {
        padding-left: 0.45rem;
        padding-right: 0.45rem;
    }

    [data-testid="stChatInput"] textarea {
        min-height: 3.8rem !important;
        padding: 0.7rem !important;
    }

    [data-testid="stFileUploader"] {
        padding: 0.55rem;
    }
}

div.stButton > button:hover {
    border-color: var(--teal);
    background: var(--mint);
    transform: translateY(-2px);
}

[data-testid="stChatMessage"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

MODEL_NAME = "llama3.2:1b"

KNOWLEDGE_FILE = "universal_ai_career_assistant_knowledge_base.txt"
FEEDBACK_RECIPIENT = "pranavkumar86530@gmail.com"


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

@st.cache_resource
def load_knowledge_base():

    file_path = Path(KNOWLEDGE_FILE)

    if not file_path.exists():
        return [], None, None

    text = file_path.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    chunks = []

    chunk_size = 1000
    overlap = 200

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        chunks.append(chunk)

        start += chunk_size - overlap

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(chunks)

    return chunks, vectorizer, vectors


# ============================================================
# SEARCH RELEVANT KNOWLEDGE
# ============================================================

def search_knowledge(question, chunks, vectorizer, vectors):

    if not chunks:
        return ""

    question_vector = vectorizer.transform(
        [question]
    )

    similarities = cosine_similarity(
        question_vector,
        vectors
    ).flatten()

    top_results = similarities.argsort()[-2:][::-1]

    relevant_chunks = []

    for index in top_results:

        if similarities[index] > 0:

            relevant_chunks.append(
                chunks[index]
            )

    return "\n\n".join(relevant_chunks)


# ============================================================
# AI RESPONSE
# ============================================================

def get_ai_response(question, knowledge_context, conversation_history):

    memory_context = "\n".join(
        f"{message['role'].title()}: {message['content']}"
        for message in conversation_history[-8:]
    )

    system_prompt = f"""
You are a warm, practical AI career coach. Make the conversation feel personal,
useful, and encouraging without being vague or overconfident. Answer the exact
question first, then give clear next steps. When an uploaded resume is present,
refer to its actual details and clearly say when information is missing. Do not
guarantee jobs or salaries and do not invent qualifications.

Context:

{knowledge_context}

Recent conversation memory:
{memory_context or "No previous conversation yet."}

Answer in a friendly structure with a short direct answer, 3-6 useful bullets,
and one thoughtful follow-up question when it would help the user continue.
"""

    ollama_client = get_ollama_client()

    return ollama_client.chat(

        model=MODEL_NAME,

        stream=True,

        keep_alive="10m",

        options={
            "temperature": 0.2,
            "num_predict": 300
        },

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ]

    )


def extract_resume_text(uploaded_file):

    file_type = Path(uploaded_file.name).suffix.lower()
    file_bytes = uploaded_file.getvalue()

    if file_type == ".pdf":
        reader = PdfReader(io.BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()

    if file_type == ".docx":
        document = Document(io.BytesIO(file_bytes))
        return "\n".join(paragraph.text for paragraph in document.paragraphs).strip()

    if file_type == ".txt":
        return file_bytes.decode("utf-8", errors="ignore").strip()

    raise ValueError("Unsupported file type")


def get_response_text(response_chunk):

    if isinstance(response_chunk, dict):
        return response_chunk.get("message", {}).get("content", "")

    message = getattr(response_chunk, "message", None)

    return getattr(message, "content", "")


def get_setting(name, default=""):

    if name in os.environ:
        return os.environ[name]

    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


@st.cache_resource
def get_ollama_client():

    ollama_host = get_setting("OLLAMA_HOST", "http://localhost:11434")
    return ollama.Client(host=ollama_host)


def send_feedback_email(rating, feedback):

    smtp_user = get_setting("SMTP_USER")
    smtp_password = get_setting("SMTP_PASSWORD")
    smtp_host = get_setting("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(get_setting("SMTP_PORT", "465"))

    if not smtp_user or not smtp_password:
        return False, "Email is not configured yet. Add SMTP_USER and SMTP_PASSWORD to send notifications."

    message = EmailMessage()
    message["Subject"] = f"AI Career Assistant feedback: {rating}/5"
    message["From"] = smtp_user
    message["To"] = FEEDBACK_RECIPIENT
    message.set_content(
        f"New chatbot feedback received.\n\n"
        f"Rating: {rating}/5\n"
        f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"Feedback:\n{feedback or '(No written feedback provided)'}\n"
    )

    try:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15) as smtp:
            smtp.login(smtp_user, smtp_password)
            smtp.send_message(message)
    except Exception as error:
        return False, f"Email could not be sent: {error}"

    return True, "Feedback sent successfully. Thank you!"

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 AI Career Assistant")

    st.write(
        "Your personal AI assistant for career guidance."
    )

    st.divider()

    st.subheader("Upload your resume")

    uploaded_resume = st.file_uploader(
        "Choose a resume file",
        type=["pdf", "docx", "txt"],
        help="Upload a text-based PDF, DOCX, or TXT resume to ask questions about it."
    )

    if uploaded_resume is not None:
        resume_id = f"{uploaded_resume.name}:{uploaded_resume.size}"

        if st.session_state.get("resume_id") != resume_id:
            try:
                st.session_state.resume_text = extract_resume_text(uploaded_resume)
                st.session_state.resume_id = resume_id
            except Exception as error:
                st.session_state.resume_text = ""
                st.session_state.resume_id = resume_id
                st.error(f"Could not read the resume: {error}")

        if st.session_state.get("resume_text"):
            st.success(f"Resume loaded: {uploaded_resume.name}")
        elif not st.session_state.get("resume_error"):
            st.warning("No readable text was found in that file.")

    if st.session_state.get("resume_text"):
        st.caption("You can now ask questions about your resume in the chat below.")

    st.divider()

    st.subheader("What can I help with?")

    topic_questions = {
        "Career guidance": "What career direction would fit my interests and current skills?",
        "Resume improvement": "How can I improve my resume to get more interviews?",
        "Interview preparation": "Help me prepare for an upcoming job interview.",
        "Career roadmaps": "Create a practical career roadmap for me.",
        "Skill recommendations": "Which skills should I learn next for my target career?",
        "Job search guidance": "What is the best strategy for finding a suitable job?",
        "LinkedIn advice": "How can I improve my LinkedIn profile and presence?",
        "Career changes": "How can I plan a successful career change?",
    }

    for topic, topic_question in topic_questions.items():
        if st.button(topic, key=f"topic_{topic}", use_container_width=True):
            st.session_state.pending_question = topic_question
            st.rerun()

    st.divider()

    with st.expander("Rate this chatbot"):
        st.caption("Your feedback helps improve the career assistant.")

        with st.form("feedback_form", clear_on_submit=True):
            feedback_rating = st.radio(
                "How helpful was this chatbot?",
                options=[1, 2, 3, 4, 5],
                format_func=lambda value: "★" * value + "☆" * (5 - value),
                horizontal=True,
            )
            feedback_text = st.text_area(
                "Share your feedback (optional)",
                placeholder="What worked well, or what should be better?",
                max_chars=1000,
            )
            feedback_submitted = st.form_submit_button(
                "Send feedback",
                use_container_width=True,
            )

        if feedback_submitted:
            feedback_sent, feedback_message = send_feedback_email(
                feedback_rating,
                feedback_text.strip(),
            )
            if feedback_sent:
                st.success(feedback_message)
            else:
                st.warning(feedback_message)

    if st.session_state.get("messages"):
        st.caption(f"🧠 Memory active: {len(st.session_state.messages)} messages")

        if st.button("Clear memory", key="clear_memory", use_container_width=True):
            st.session_state.messages = []
            st.session_state.pop("pending_question", None)
            st.rerun()

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# MAIN PAGE
# ============================================================

st.title("🤖 AI Career Assistant Chatbot")

st.write(
    "Ask me about careers, skills, resumes, "
    "interviews, jobs, and professional development."
)


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

chunks, vectorizer, vectors = load_knowledge_base()


if not chunks:

    st.error(
        f"Knowledge base file not found: {KNOWLEDGE_FILE}"
    )

    st.stop()


# ============================================================
# CHECK OLLAMA
# ============================================================

try:

    get_ollama_client().list()

except Exception:

    st.error(
        "Ollama is not running. "
        "Please install and start Ollama."
    )

    st.stop()


# ============================================================
# CHAT HISTORY
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome">
        <div class="welcome-kicker">Your next move starts here</div>
        <h2>Turn career uncertainty<br>into a clear plan.</h2>
        <p>Ask a question, upload your resume, or pick a starting point. I will help you think it through step by step.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Start with a question")
    starter_questions = [
        "What career path fits my current skills?",
        "How can I improve my resume?",
        "Build me a 30-day learning roadmap",
        "Give me 5 interview questions to practice",
    ]
    prompt_columns = st.columns(2)
    for index, starter_question in enumerate(starter_questions):
        with prompt_columns[index % 2]:
            if st.button(starter_question, key=f"starter_{index}", use_container_width=True):
                st.session_state.pending_question = starter_question
                st.rerun()

    if st.session_state.get("resume_text"):
        st.caption("Resume loaded. Try asking: “What are the strongest parts of my resume?”")


for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ============================================================
# USER INPUT
# ============================================================

pending_question = st.session_state.pop("pending_question", None)
typed_question = st.chat_input("Ask about your career or resume...")
user_question = typed_question or pending_question


if user_question:

    # Display user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):

        st.markdown(user_question)


    # Generate AI response

    with st.chat_message("assistant"):

        with st.spinner(
            "AI Career Assistant is thinking..."
        ):

            try:

                knowledge_context = search_knowledge(

                    user_question,

                    chunks,

                    vectorizer,

                    vectors

                )

                resume_context = st.session_state.get("resume_text", "")
                if resume_context:
                    knowledge_context = (
                        f"General career guidance:\n{knowledge_context}\n\n"
                        "Uploaded resume:\n"
                        f"{resume_context[:12000]}"
                    )


                response = get_ai_response(

                    user_question,

                    knowledge_context,

                    st.session_state.messages[:-1]

                )

                answer = st.write_stream(
                    get_response_text(chunk)
                    for chunk in response
                )


                st.session_state.messages.append(

                    {
                        "role": "assistant",
                        "content": answer
                    }

                )


            except Exception as error:

                error_message = f"""
Error while generating the response:

{error}

Please make sure Ollama is running and the model
'{MODEL_NAME}' has been downloaded.
"""

                st.error(error_message)