import os
import requests

chat_history = []
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY_V10")


#Đọc và nạp biến {name} trong injection prompt
def load_prompt(file_path, user_name):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            template = f.read()
        # Thay thế placeholder {name} bằng tên người dùng nhập vào
        return template.replace("{name}", user_name)
    except FileNotFoundError:
        return f"You are LiemAI chatting with {user_name}."
#############################################################


def AI_response(question):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    chat_history.append({"role": "user", "content": question})

    data = {
        "model": "openai/gpt-oss-safeguard-20b",
        "messages": chat_history,
        "temperature": 0.7
    }

    print("Responding...")

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            ans = response.json()
            Answer = ans['choices'][0]['message']['content']

            chat_history.append({"role": "assistant", "content": Answer})

            print("-"*40)
            print(Answer)
            print("="*40)
        else:
            print("Limits reach!")
            if  input("Wanna see Error code ? [y/n] ").lower() == 'y':
                print(f"Error: {response.status_code}: {response.text}")
            chat_history.pop()
    except Exception as e:
        print(f"Network Error, please try again!")
        chat_history.pop()


if __name__ == "__main__":
    name = input("Your name: ")
    
    AI_response(load_prompt("prompt_v10.txt", name))
    
    NumOfQuestions = 0  
    QuestionLimit = 10      
    check = 0

    while True:

        if NumOfQuestions >= QuestionLimit:
            print("\n" + "💰"*15)
            print("Đoạn chat của bạn đã đến giới hạn...")
            print(f"Bản dùng thử chỉ cho phép hỏi {QuestionLimit} câu.")
            print("Vui lòng đăng kí để nâng cấp LiemAI Premium nhé !")
            print("💰"*15 + "\n")
            if input("Nhập key: ") == "key":
                print("Welcome to LiemAI PREMIUM")
                check = 1
                while True:
                    user_question = input(f"\n{name}: ")
        
                    if user_question.lower() == 'thoat':
                        print("Tạm biệt!")
                        break
            
                    AI_response(user_question)
            if check == 1:
                break
            print("Key không đúng!")
            input("Bấm Enter để thoát chương trình...")
            break
            
        user_question = input(f"\n{name}: ")
        
        if user_question.lower() == 'thoat':
            print("Tạm biệt!")
            break
            
        AI_response(user_question)
        
        NumOfQuestions += 1
