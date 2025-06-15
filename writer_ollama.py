from ollama import Client

client = Client()

def ai_writer(text, model="llama3"):
    prompt = f"""
Rewrite the following chapter in a vivid, modern, and engaging way while keeping the original meaning intact.

{text}
    """
    try:
        response = client.chat(model=model, messages=[
            {"role": "user", "content": prompt}
        ])
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"[ERROR] Writer failed: {e}")
        return ""
