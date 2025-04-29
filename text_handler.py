import tkinter as tk
import re
import requests
import pyperclip

# API 키를 전역 변수로 선언 (초기에 비워둠)
api_key = ""

# DeepL API를 사용한 번역 함수
def translate_text(text, source_lang="EN", target_lang="KO"):
    """DeepL API를 사용하여 텍스트 번역"""
    global api_key
    url = "https://api-free.deepl.com/v2/translate"
    
    data = {
        "auth_key": api_key,
        "text": text,
        "source_lang": source_lang,  # 원본 언어
        "target_lang": target_lang   # 목표 언어
    }
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        result = response.json()
        return result["translations"][0]["text"]
    else:
        print("번역 실패:", response.status_code, response.text)
        return "번역 실패"

def process_text():
    """입력 텍스트 처리 및 번역"""
    text = input_text.get("1.0", tk.END).strip()  # 입력창에서 텍스트 가져오기
    if not text:
        success_label.config(text="입력된 텍스트가 없습니다.", fg="red")
        return

    text_without_linebreaks = re.sub(r'\n', ' ', text) # 기존 줄바꿈 제거

    # 약어 및 특수 케이스 처리
    special_cases = ["i.e.,", "e.g.,", "Fig.", "Dr."]
    for case in special_cases:
        text_without_linebreaks = text_without_linebreaks.replace(case, case.replace(".", "[DOT]"))

    # 문장 끝 구분
    formatted_text = re.sub(r'(?<=[.!?])\s+', r'\n', text_without_linebreaks)

    # 특수 케이스 복원
    formatted_text = formatted_text.replace("[DOT]", ".")

    # 번역 실행
    translated_text = translate_text(formatted_text)

    # 원문 출력
    original_text_display.delete("1.0", tk.END)
    original_text_display.insert(tk.END, formatted_text)

    # 번역 출력
    translated_text_display.delete("1.0", tk.END)
    translated_text_display.insert(tk.END, translated_text)

    # 클립보드에 원문 복사
    try:
        pyperclip.copy(formatted_text) # pyperclip으로 텍스트 복사
        success_label.config(text="결과가 클립보드에 복사되었습니다.", fg="green")
    except Exception as e:
        success_label.config(text=f"클립보드 복사 중 오류 발생: {e}", fg="red")

def toggle_pin():
    """고정 기능 토글"""
    global is_pinned
    is_pinned = not is_pinned
    root.wm_attributes("-topmost", is_pinned)
    pin_button.config(text="고정 해제" if is_pinned else "고정")

def ask_api_key():
    """API 키를 GUI로 입력받는 함수"""
    def submit_key():
        global api_key
        api_key = api_entry.get().strip()
        if api_key:
            key_window.destroy()
        else:
            error_label.config(text="API 키를 입력하세요.", fg="red")

    key_window = tk.Toplevel()
    key_window.title("API 키 입력")
    key_window.geometry("300x150")
    key_window.attributes('-topmost', True)

    tk.Label(key_window, text="DeepL API 키를 입력하세요:").pack(pady=10)
    api_entry = tk.Entry(key_window, show="*")
    api_entry.pack(pady=5)

    submit_button = tk.Button(key_window, text="확인", command=submit_key)
    submit_button.pack(pady=10)

    error_label = tk.Label(key_window, text="", fg="red")
    error_label.pack()

    # 메인 창이 대기하도록 (blocking)
    key_window.grab_set()
    root.wait_window(key_window)

# GUI 생성
root = tk.Tk()
root.title("텍스트 처리기")

# API 키 입력창 먼저 띄우기
ask_api_key()

# 초기 고정 상태
is_pinned = True
root.wm_attributes("-topmost", is_pinned)

# 입력 텍스트 라벨과 텍스트박스
tk.Label(root, text="입력 텍스트:").pack(pady=5)
input_text = tk.Text(root, height=10, width=50)
input_text.pack(pady=5)

# 확인 버튼과 성공 메시지 라벨
process_button = tk.Button(root, text="확인", command=process_text)
process_button.pack(pady=10)
success_label = tk.Label(root, text="", fg="green")
success_label.pack()

# 고정 토글 버튼
pin_button = tk.Button(root, text="고정 해제" if is_pinned else "고정", command=toggle_pin)
pin_button.pack(pady=5)

# 원문 출력 텍스트 라벨과 텍스트박스
tk.Label(root, text="원문 출력:").pack(pady=5)
original_text_display = tk.Text(root, height=10, width=50, bg="#f0f0f0")
original_text_display.pack(pady=5)

# 번역 출력 텍스트 라벨과 텍스트박스
tk.Label(root, text="번역 출력:").pack(pady=5)
translated_text_display = tk.Text(root, height=10, width=50, bg="#f0f0f0")
translated_text_display.pack(pady=5)

# GUI 실행
root.mainloop()
