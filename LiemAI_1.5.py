import os
import requests

# Module nhập liệu đa dòng
from input_handler import get_multiline_input
from dotenv import load_dotenv

chat_history = []

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY_V15")
SYS_PROMPT = ""  # Khai báo biến toàn cục chứa luật AI


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
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {"Content-Type": "application/json"}

    chat_history.append({
        "role": "user",
        "parts": [{"text": question}]
    })

    # Đính kèm systemInstruction ở TẤT CẢ các lượt gọi để AI luôn nhớ vai
    data = {
        "contents": chat_history,
        "systemInstruction": {
            "parts": [{"text": SYS_PROMPT}]
        },
        "generationConfig": {"temperature": 0.7}
    }

    print("Responding...")

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            ans = response.json()
            Answer = ans['candidates'][0]['content']['parts'][0]['text']

            chat_history.append({
                "role": "model",
                "parts": [{"text": Answer}]
            })

            print("-" * 40)
            print(Answer)
            print("=" * 40)
        else:
            print("Limits reach!")
            if  input("Wanna see Error code ? [y/n] ").lower() == 'y':
                print(f"Error: {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Lỗi mạng: {e}")
        chat_history.pop()

if __name__ == "__main__":
    name = input("Your name: ").strip()

    # Tạo prompt định hình vai trò
    SYS_PROMPT = load_prompt("prompt_v15.txt", name)

    # Lượt chào khởi tạo đầu tiên
    first_greeting = f'Please acknowledge my presence by responding EXACTLY with: "Hello {name}, how can I help you ?" and nothing else.'
    AI_response(first_greeting)
    
    NumOfQuestions = 0  
    QuestionLimit = 6
    check = 0
    
    while True:
        # Kiểm tra nếu vượt quá số câu hỏi ở bản Free
        if NumOfQuestions >= QuestionLimit:
            print("\n" + "*" * 15)
            print("Cuộc trò chuyện đã đạt giới hạn...")
            print(f"Bản dùng thử chỉ cho phép hỏi {QuestionLimit} câu.")
            print("Vui lòng liên hệ Lương Minh Quân để nâng cấp LiemAI Premium nhé !")
            print("#" * 15 + "\n")
            
            if input("Nhập key: ").strip() == "MINHQUANLUONG2137v2":
                print("Welcome to LiemAI PREMIUM\n")
                check = 1
                while True:
                    # 2. Dùng get_multiline_input ở cả chế độ Premium
                    user_question = get_multiline_input(f"{name}: ")
        
                    if user_question.lower() == 'thoat':
                        print("Tạm biệt!")
                        break
                    if user_question:
                        AI_response(user_question)
            
            if check == 1:
                break
            
            print("Key không đúng!")
            input("Bấm Enter để thoát chương trình...")
            break
            
        # Chế độ dùng thử
        user_question = get_multiline_input(f"{name}: ")
        
        if user_question.lower() == 'thoat':
            print("Tạm biệt!")
            break
            
        if user_question:  # Bỏ qua nếu tin nhắn rỗng
            AI_response(user_question)
            NumOfQuestions += 1