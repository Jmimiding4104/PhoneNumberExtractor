import pandas as pd
import re
import tkinter as tk
import pyperclip
import os
import sys

from tkinter import filedialog, messagebox

def resource_path(relative_path):
    """獲取資源的絕對路徑"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 手機號碼正則表達式
phone_pattern = r'09\d{8}'

def extract_phone_numbers(cell):
    """從一個儲存格中提取手機號碼，並確保號碼以 09 開頭"""
    if isinstance(cell, str):  # 確保是字串
        # 如果號碼沒有以 09 開頭，手動加上
        if not cell.startswith('09'):
            cell = '0' + cell  # 為缺少 09 的號碼加上 09
        
        matches = re.findall(phone_pattern, cell)
        if matches:
            return matches[0]  # 只取第一個
    return None

def open_file():
  """選擇並打開檔案"""
  file_path = filedialog.askopenfilename(title="選擇 Excel 檔案", filetypes=[("Excel Files", "*.xlsx;*.xls;*.csv")])
  if file_path:
    try:
      if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
      else:
        df = pd.read_excel(file_path)
      
      df['電話'] = df['電話'].astype(str)
      df['提取的手機'] = df['電話'].apply(extract_phone_numbers)
      extracted_phones = df['提取的手機'].dropna()
      phone_numbers = ",".join(extracted_phones)

      # 顯示提取的手機號碼
      text_box.delete(1.0, tk.END)  # 清空之前的內容
      text_box.insert(tk.END, phone_numbers)  # 插入新內容
    except Exception as e:
      messagebox.showerror("錯誤", f"無法讀取檔案: {e}")

def save_file():
    """保存提取的手機號碼到檔案"""
    phone_numbers = text_box.get(1.0, tk.END).strip()
    if phone_numbers:
        pyperclip.copy(phone_numbers)
        messagebox.showinfo("成功", "複製成功")
    else:
        messagebox.showerror("失敗", "沒有內容可複製")

# GUI 設定
root = tk.Tk()
root.title("佩佩專用診篩工具")

# 設定應用程式圖示
icon_path = resource_path('phonenumberextractor\icon\icon-1.ico')
root.iconbitmap(icon_path)

# 設定 UI 元素
open_button = tk.Button(root, text="選擇 Excel 檔案", command=open_file)
open_button.pack(pady=10)

save_button = tk.Button(root, text="保存提取的手機號碼", command=save_file)
save_button.pack(pady=10)

text_box = tk.Text(root, height=10, width=50)
text_box.pack(pady=10)

# 啟動 GUI 主循環
root.mainloop()