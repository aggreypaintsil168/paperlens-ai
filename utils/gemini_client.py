import google.generativeai as genai

# PUT YOUR GEMINI API KEY HERE
API_KEY = "AIzaSyAhUtDhlM_9gZ9kTxmnCA6_TEBCUTuBd1Y"

genai.configure(api_key=API_KEY)


def get_gemini_models():
    chat_model = genai.GenerativeModel("gemini-2.0-flash")
    return chat_model
