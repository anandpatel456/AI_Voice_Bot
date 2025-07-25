from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os 
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the API key from .env
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    temperature=0.7,
    model_name="llama-3.3-70b-versatile",  
    )

# Use memory to store conversation context
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory, verbose=False)

# Interviewer function
def run_interview(resume_text, chat_history, category="general"):
    formatted_history = ""
    for turn in chat_history:
        formatted_history += f"Interviewer: {turn['question']}\nCandidate: {turn['answer']}\n"

    instructions = {
        "general": (
            "Ask a behavioral or personality-based interview question to understand the candidate's goals, "
            "values, or motivations. Vary question phrasing, be warm and engaging, and avoid repetition."
        ),
        "technical": (
            "Ask a technical question based on the candidate's resume. Focus on their skills, tools, or technologies, "
            "and avoid repeating already-asked topics. Make it sound natural and thoughtful."
        ),
        "projects": (
            "Ask about a project or hands-on experience from the resume. Pick a unique project or perspective, "
            "and ask in a human, curious tone as if you’re genuinely interested in their contribution."
        ),
    }

    # Fallback if invalid category
    if category not in instructions:
        category = "general"

    prompt = f"""
You are a senior HR interviewer conducting a live job interview with a candidate.
Speak naturally, like a friendly professional. Show curiosity and empathy.
Your questions should sound like real human HR professionals—not robotic or repetitive.

Resume:
\"\"\"{resume_text}\"\"\"

Previous conversation:
{formatted_history}

Task:
{instructions[category]}

Ask exactly one clear, short, conversational question—no explanations. Avoid repeating past questions.
""".strip()

    return conversation.predict(input=prompt).strip()


# Feedback generation function
def generate_feedback(chat_history):
    history = "\n".join(
        [f"Interviewer: {x['question']}\nCandidate: {x['answer']}" for x in chat_history]
    )

    prompt = f"""
You are a professional HR expert giving feedback after a mock interview.

Transcript:
{history}

Please provide:
- What the candidate did well (Strengths)
- What could be improved (Areas for growth)
- How clear, confident, and natural their communication was

Keep your feedback concise, spoken naturally like in a real conversation (1-2 minutes).
Avoid sounding like a computer or giving numbered bullet points.
""".strip()

    return conversation.predict(input=prompt).strip()