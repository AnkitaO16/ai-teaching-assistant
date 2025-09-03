from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

resp = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[{"role": "user", "content": "Hello Groq, are you working?"}]
)

print(resp.choices[0].message.content)   # ✅ correct way
