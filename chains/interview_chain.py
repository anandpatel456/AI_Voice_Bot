from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    temperature=0.7,
    model_name="llama-3.3-70b-versatile",  
)

memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

def run_interview(resume_text, chat_history, category="general"):
    formatted_history = "\n".join([
        f"Interviewer: {turn['question']}\nCandidate: {turn['answer']}"
        for turn in chat_history
    ])

    instructions = {
        "general": "Ask a behavioral or personality-based question.",
        "technical": "Ask a question about technical skills or tools from the resume.",
        "projects": "Ask about a project or hands-on experience from the resume."
    }

    prompt = f"""
You are a friendly and professional HR interviewer conducting a real interview.
Ask short questions not to long 

Resume:
\"\"\"{resume_text}\"\"\"

Past Conversation:
{formatted_history}

Now ask a single, concise question from this category: {category}.
{instructions[category]}
Make it sound human and engaging.
""".strip()

    return conversation.predict(input=prompt).strip()

def generate_feedback(chat_history):
    history = "\n".join([
        f"Interviewer: {turn['question']}\nCandidate: {turn['answer']}"
        for turn in chat_history
    ])

    prompt = f"""
You're an HR expert giving friendly feedback after a mock interview.
give short feedback.

Transcript:
{history}

Give:
- Strengths
- Areas to improve
- Comments on clarity and confidence

Speak like a human, not a bot.
""".strip()

    return conversation.predict(input=prompt).strip()
