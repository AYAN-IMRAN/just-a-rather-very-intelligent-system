import google.generativeai as genai

# Function to process commands using Gemini API
def aiProcess(command):
    # Configure Gemini with your API key
    genai.configure(api_key="<Your Gemini Api Key Here>")

    # Instructions for Jarvis' persona
    instructions = """
    You are Jarvis, a highly intelligent virtual assistant skilled in general tasks like Alexa and Google Assistant.and make sure respond in short.You help users with a variety of tasks such as searching the web, playing music, providing news updates, and answering questions.You are polite, efficient, and always strive to provide accurate and helpful information.Please respond in a friendly and professional tone, providing clear answers to the user's queries..
    """

    # Combine instructions with user command
    prompt = instructions + "\n\nUser: " + command + "\nJarvis:"

    # Generate response from Gemini
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Return the response
    return response.text
