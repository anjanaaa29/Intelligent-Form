import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))


def generate_summary(text, max_words=150):
    """Generate a concise summary for a single document."""
    if not text or text.strip() == "":
        return "No content."
    try:
        prompt = (
            f"Summarize the following document in under {max_words} words. "
            f"Focus on key details, roles, dates, and entities:\n\n{text}"
        )
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an intelligent summarization assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=400,
        )
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        return f"[Error generating summary: {e}]"


def generate_holistic_summary(form_texts: dict, max_words=200):
    """
    Generate a combined summary across multiple forms.
    form_texts: dict -> {'file_path1': 'text1', 'file_path2': 'text2', ...}
    """
    if not form_texts or all(not t.strip() for t in form_texts.values()):
        return "No content to summarize."
    
    combined_text = "\n\n".join(form_texts.values())

    try:
        prompt = (
            f"Create a holistic summary across multiple documents (under {max_words} words). "
            f"Identify shared patterns, common entities, or relationships.\n\n{combined_text}"
        )
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an intelligent summarization assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )
        summary = response.choices[0].message.content.strip()
        return summary

    except Exception as e:
        return f"[Error generating holistic summary: {e}]"


# if __name__ == "__main__":
#     # Example single summary
#     sample_text = """
#     Candidate Name: John Doe
#     Education: B.Tech in Computer Science, 2020
#     Experience: 3 years at Infosys as a Data Analyst
#     Skills: Python, SQL, Tableau, Power BI
#     """
#     print("Generated Summary:\n", generate_summary(sample_text))

#     # Example holistic summary
#     forms = {
#         "form1.pdf": "John Doe, Data Analyst, 3 years experience.",
#         "form2.pdf": "Jane Smith, Data Engineer, 5 years experience.",
#     }
#     print("\nHolistic Summary:\n", generate_holistic_summary(forms))
