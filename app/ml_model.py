import os
# from google import genai
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GeminiAgent: # Keeping the class name so you don't have to change imports
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # Llama 3 70B is excellent for SQL tasks
        self.model_name = "llama-3.3-70b-versatile" 

    def ask(self, system_instruction, user_input):
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input},
                ],
                model=self.model_name,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Groq API Error: {str(e)}")
            return f"Error: {str(e)}"

# class GeminiAgent:
#     def __init__(self):
#         self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
#         # self.model_name = "gemini-2.0-flash"
#         # self.model_name = "gemini-flash-latest"
#         # self.model_name = "gemini-2.0-flash-lite"
    
#     def ask(self, system_instruction, user_input):
#         try:
#             # Combine the instruction and input
#             response = self.client.models.generate_content(
#                 model=self.model_name,
#                 contents=f"{system_instruction}\n\nUser Question: {user_input}"
#             )
#             return response.text
#         except Exception as e:
#             print(f"Gemini SDK Error: {str(e)}")
#             return f"Error: {str(e)}"