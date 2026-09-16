import os
from groq import Groq

def check_groq_models():
    # 1. Khởi tạo Groq client
    # Script sẽ tự động lấy API key từ biến môi trường GROQ_API_KEY
    # Hoặc bạn có thể thay thế bằng: client = Groq(api_key="gsk_...")
    try:
        client = Groq()
    except Exception as e:
        print(f"Lỗi khởi tạo client (Hãy kiểm tra biến môi trường GROQ_API_KEY): {e}")
        return

    print("Đang kết nối tới Groq API để lấy danh sách model...\n")
    
    try:
        # 2. Gọi API lấy danh sách models
        models_response = client.models.list()
        
        # 3. Hiển thị kết quả
        print(f"{'STT':<5} | {'Tên Model (ID)':<35} | {'Được sở hữu bởi':<15}")
        print("-" * 65)
        
        for idx, model in enumerate(models_response.data, 1):
            model_id = model.id
            owned_by = getattr(model, 'owned_by', 'N/A')
            print(f"{idx:<5} | {model_id:<35} | {owned_by:<15}")
            
        print(f"\nTổng số model đang khả dụng: {len(models_response.data)}")

    except Exception as e:
        print(f"Đã xảy ra lỗi khi gọi API Groq: {e}")

if __name__ == "__main__":
    # (Tùy chọn) Bạn có thể gán trực tiếp API key ở đây nếu không muốn dùng biến môi trường
    os.environ["GROQ_API_KEY"] = "gsk_myapi"
    
    check_groq_models()