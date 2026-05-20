import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class GeminiAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_name = "gemini-flash-latest"
        # self.model_name = "gemini-2.0-flash"
    def ask(self, system_instruction, user_input):
        try:
            # Combine the instruction and input
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{system_instruction}\n\nUser Question: {user_input}"
            )
            return response.text
        except Exception as e:
            print(f"Gemini SDK Error: {str(e)}")
            return f"Error: {str(e)}"