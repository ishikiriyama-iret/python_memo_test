import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def show_text():
    """ボタンクリックされたら表示"""

    input_text = entry.get()
    if input_text.strip():
        result_label.config(text=f"入力されたテキスト: {input_text}")
    else:
        messagebox.showwarning("警告", "テキストを入力してください")
        entry.focus()


# メインウィンドウ
root = tk.Tk()
root.title("Tkinterサンプルアプリ")

root.geometry("400x200")


root.resizable(True, True)

# メインフレーム
main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# ウィンドウ調整　レスポンシブみたいになる
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(0, weight=1)

# タイトルラベル
title_label = ttk.Label(
    main_frame, text="Tkinterサンプルアプリ", font=("Helvetica", 16)
)
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))


# ラベル文字を短くする
input_label = ttk.Label(main_frame, text="入力:", font=("Arial", 12))  # 短縮
input_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 15), pady=(0, 20))  # padx追加

# 解決方法3: stickyとpadxで適切に配置
entry = ttk.Entry(main_frame, font=("Arial", 12))
entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 20))
entry.focus()

# ボタン
show_button = ttk.Button(main_frame, text="表示", command=show_text)
show_button.grid(row=2, column=0, columnspan=2, pady=(0, 20))

# 結果ラベル
result_label = ttk.Label(main_frame, text="ここに結果が表示される", font=("Arial", 12))
result_label.grid(row=3, column=0, columnspan=2, pady=(0, 20))

# アプリケーション開始
root.mainloop()
