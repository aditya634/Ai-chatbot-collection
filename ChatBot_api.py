import google.generativeai as genai

def get_response(user_input):
    genai.configure(api_key="AIzaSyBNXw-2ZJU9ESHeBmT4R3rPc8beTug2xLA")
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(user_input)
    return response.text.strip()

def main():
    print("Welcome to the Gemini Terminal Chatbot! (type 'bye' to exit)")
    while True:
        user_input = input("You: ")
        if "bye" in user_input.lower():
            print("Bot: Goodbye! Have a nice day.")
            break
        response = get_response(user_input)
        print("Bot:", response)

if __name__ == "__main__":
    main()