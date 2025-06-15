from ollama import Client

client = Client()

def ai_reviewer(text, model="llama3"):
    prompt = f"""
Act as an editor. Improve the grammar, flow, and style of the following chapter without changing its meaning.

{text}
    """
    try:
        response = client.chat(model=model, messages=[
            {"role": "user", "content": prompt}
        ])
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"[ERROR] Reviewer failed: {e}")
        return ""
