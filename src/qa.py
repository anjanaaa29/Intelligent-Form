import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client=Groq(api_key=os.getenv("GROQ_API_KEY"))

def answer_question(form_text,qst):
    prompt=f"""You are an intelligent document assistant.
    Your task is to answer questions using the given form content accurately.
    Do not make up information — only use what is found in the form.
    {form_text} 
    Question: {qst}
    Answer clearly and concisely:
    """
    try:
        response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"Error occurred: {e}"
    

