# input_handler.py
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

def get_multiline_input(prompt_text="User: ") -> str:
    """
    Hàm nhận input đa dòng từ Terminal:
    - Shift + Enter hoặc Alt + Enter: Xuống dòng
    - Enter: Gửi tin nhắn
    """
    bindings = KeyBindings()

    # Bắt sự kiện phím Enter thuần túy -> Gửi/Submit dữ liệu
    @bindings.add('enter')
    def _(event):
        event.current_buffer.validate_and_handle()

    # Bắt sự kiện Shift + Enter (hoặc Alt + Enter) -> Chèn dòng mới
    @bindings.add('c-j')      # Ctrl+J (Mã ANSI tiêu chuẩn cho Shift+Enter trên nhiều Terminal)
    @bindings.add('escape', 'enter') # Alt+Enter (Dự phòng cho Windows CMD/PowerShell)
    def _(event):
        event.current_buffer.insert_text('\n')

    try:
        text = prompt(
            prompt_text,
            key_bindings=bindings,
            multiline=True
        )
        return text.strip()
    except (KeyboardInterrupt, EOFError):
        return "thoat"