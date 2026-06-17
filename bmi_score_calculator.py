import tkinter as tk
from tkinter import messagebox
import ctypes
import os
import sys

# ================= 運算防呆處理 =================
def parse_float(val_str):
    cleaned_val = val_str.replace('．', '.').replace('。', '.').replace(' ', '')
    return float(cleaned_val)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "體重過輕"
    elif 18.5 <= bmi < 24:
        return "健康體位"
    elif 24 <= bmi < 27:
        return "體重過重"
    elif 27 <= bmi < 30:
        return "輕度肥胖"
    elif 30 <= bmi < 35:
        return "中度肥胖"
    else:
        return "重度肥胖"

def get_body_fat_category(gender, age, fat):
    if gender == "男":
        if age < 30:
            if fat < 14: return "偏低"
            elif 14 <= fat <= 20: return "標準"
            elif 20 < fat < 25: return "偏高"
            else: return "肥胖"
        else:
            if fat < 17: return "偏低"
            elif 17 <= fat <= 23: return "標準"
            elif 23 < fat < 25: return "偏高"
            else: return "肥胖"
    elif gender == "女":
        if age < 30:
            if fat < 17: return "偏低"
            elif 17 <= fat <= 24: return "標準"
            elif 24 < fat < 30: return "偏高"
            else: return "肥胖"
        else:
            if fat < 20: return "偏低"
            elif 20 <= fat <= 27: return "標準"
            elif 27 < fat < 30: return "偏高"
            else: return "肥胖"
    else:
        raise ValueError("請選擇性別")

# ================= 自動計算 BMI 與 體脂判定 =================
def update_stats(*args):
    # 前測 BMI
    try:
        h = parse_float(var_h.get()) / 100.0
        w0 = parse_float(var_w0.get())
        if h > 0:
            bmi0 = w0 / (h * h)
            cat0 = get_bmi_category(bmi0)
            lbl_bmi0.config(text=f"BMI: {bmi0:.1f} ({cat0})")
        else:
            lbl_bmi0.config(text="BMI: --")
    except:
        lbl_bmi0.config(text="BMI: --")

    # 目標/目前 BMI
    try:
        h = parse_float(var_h.get()) / 100.0
        w1 = parse_float(var_w1.get())
        if h > 0:
            bmi1 = w1 / (h * h)
            cat1 = get_bmi_category(bmi1)
            lbl_bmi1.config(text=f"BMI: {bmi1:.1f} ({cat1})")
        else:
            lbl_bmi1.config(text="BMI: --")
    except:
        lbl_bmi1.config(text="BMI: --")

    # 前測體脂判定
    try:
        age = parse_float(var_age.get())
        gender = var_gender.get()
        f0 = parse_float(var_f0.get())
        cat_f0 = get_body_fat_category(gender, age, f0)
        lbl_fat0.config(text=f"判定: {cat_f0}")
    except:
        lbl_fat0.config(text="判定: --")

    # 目標/目前體脂判定
    try:
        age = parse_float(var_age.get())
        gender = var_gender.get()
        f1 = parse_float(var_f1.get())
        cat_f1 = get_body_fat_category(gender, age, f1)
        lbl_fat1.config(text=f"判定: {cat_f1}")
    except:
        lbl_fat1.config(text="判定: --")

# ================= 運算邏輯區 =================
def calculate_forward():
    try:
        w0 = parse_float(var_w0.get())
        f0 = parse_float(var_f0.get())
        w1 = parse_float(var_w1.get())
        f1 = parse_float(var_f1.get())
        
        score_w = ((w0 - w1) / w0) * 0.4
        score_f = ((f0 - f1) / f0) * 0.6
        total_score = (score_w + score_f) * 100
        
        res_text = (
            f"【詳細計算過程】\n"
            f"1. 體重貢獻：(({w0} - {w1}) / {w0}) × 40% = {score_w*100:.2f}%\n"
            f"2. 體脂貢獻：(({f0} - {f1}) / {f0}) × 60% = {score_f*100:.2f}%\n"
            f"--------------------------------------\n"
            f"🎯 最終計算積分：{total_score:.2f} %"
        )
        lbl_fwd_result.config(text=res_text, fg="#0056b3")
    except ValueError:
        messagebox.showerror("輸入錯誤", "請檢查『基準數值』與『目前/目標數值』是否皆已填入有效數字。")

def calculate_reverse():
    try:
        w0 = parse_float(var_w0.get())
        f0 = parse_float(var_f0.get())
        target_score = parse_float(var_target_score.get()) / 100.0
        
        w1_input = var_target_w_opt.get().strip()
        
        if w1_input:
            w1 = parse_float(w1_input)
            score_w = ((w0 - w1) / w0) * 0.4
            score_f = target_score - score_w
            
            if score_f < 0:
                messagebox.showwarning("提示", "您設定的目標體重降幅已經超過總分數目標，不需要再降體脂了！")
                return
                
            f1 = f0 - (f0 * (score_f / 0.6))
            
            res_text = (
                f"【客製化推算結果】\n"
                f"要達成總積分 {target_score*100:.2f}%\n"
                f"在目標體重為 {w1} kg 的情況下：\n"
                f"👉 你的目標體脂必須降至： {f1:.2f} %"
            )
        else:
            w1_balanced = w0 * (1 - target_score)
            f1_balanced = f0 * (1 - target_score)
            
            res_text = (
                f"【均衡降幅推算結果】 (未指定體重時的建議)\n"
                f"要達成總積分 {target_score*100:.2f}%\n"
                f"建議體重與體脂以相同比例下降：\n"
                f"👉 目標體重建議： {w1_balanced:.2f} kg\n"
                f"👉 目標體脂建議： {f1_balanced:.2f} %"
            )
            
        lbl_rev_result.config(text=res_text, fg="#d9534f")
    except ValueError:
        messagebox.showerror("輸入錯誤", "請檢查『逆向推算區』欄位，請輸入包含小數點的有效數字。")

# ================= UI 介面設計區 =================
prev_decimal_state = 0
def check_numpad_decimal():
    global prev_decimal_state
    # 0x6E is VK_DECIMAL (Numpad .)
    state = ctypes.windll.user32.GetAsyncKeyState(0x6E) & 0x8000
    if state and not prev_decimal_state:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        pid = ctypes.c_ulong()
        ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if pid.value == os.getpid():
            widget = root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.insert(tk.INSERT, ".")
    prev_decimal_state = state
    root.after(20, check_numpad_decimal)

def disable_tk_decimal(event):
    return "break"

root = tk.Tk()
root.bind_all("<KP_Decimal>", disable_tk_decimal)
root.after(20, check_numpad_decimal)
root.title("2026佰瘦之王挑戰賽計分")
root.geometry("550x800")
root.configure(padx=20, pady=15)

try:
    icon_path = None
    if os.path.exists("app_icon.ico"):
        icon_path = "app_icon.ico"
    elif hasattr(sys, '_MEIPASS'):
        p = os.path.join(sys._MEIPASS, "app_icon.ico")
        if os.path.exists(p):
            icon_path = p
    else:
        p = os.path.join(os.path.dirname(sys.argv[0]), "app_icon.ico")
        if os.path.exists(p):
            icon_path = p
    if icon_path:
        root.iconbitmap(icon_path)
except Exception:
    pass

var_gender = tk.StringVar(value="None")
var_age = tk.StringVar()
var_h = tk.StringVar()
var_w0 = tk.StringVar()
var_f0 = tk.StringVar()
var_w1 = tk.StringVar()
var_f1 = tk.StringVar()
var_target_score = tk.StringVar()
var_target_w_opt = tk.StringVar()

var_h.trace_add("write", update_stats)
var_age.trace_add("write", update_stats)
var_gender.trace_add("write", update_stats)
var_w0.trace_add("write", update_stats)
var_w1.trace_add("write", update_stats)
var_f0.trace_add("write", update_stats)
var_f1.trace_add("write", update_stats)

# --- 基本資料設定 ---
tk.Label(root, text="Step 0: 請輸入基本資料", font=("Arial", 12, "bold"), fg="#333", bg="#e2e3e5", anchor="w").pack(fill="x", anchor="w", pady=(0,5))
frame_info = tk.Frame(root)
frame_info.pack(fill="x")

tk.Label(frame_info, text="生理性別:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
tk.Radiobutton(frame_info, text="男", variable=var_gender, value="男", font=("Arial", 10)).grid(row=0, column=1, sticky="w")
tk.Radiobutton(frame_info, text="女", variable=var_gender, value="女", font=("Arial", 10)).grid(row=0, column=2, sticky="w")

tk.Label(frame_info, text="年齡 (歲):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame_info, textvariable=var_age, width=15).grid(row=1, column=1, columnspan=2, padx=10, sticky="w")

tk.Label(frame_info, text="身高 (cm):", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
tk.Entry(frame_info, textvariable=var_h, width=15).grid(row=2, column=1, columnspan=2, padx=10, sticky="w")

tk.Label(root, text="="*65, fg="#ccc").pack(pady=5)

# --- 共用基準值設定 ---
tk.Label(root, text="Step 1: 確認前測基準數值", font=("Arial", 12, "bold"), fg="#333", bg="#e2e3e5", anchor="w").pack(fill="x", anchor="w", pady=(0,5))

frame_base = tk.Frame(root)
frame_base.pack(fill="x")
tk.Label(frame_base, text="前測體重 (kg):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
tk.Entry(frame_base, textvariable=var_w0, width=15).grid(row=0, column=1, padx=10)
lbl_bmi0 = tk.Label(frame_base, text="BMI: --", font=("Arial", 9, "bold"), fg="#0056b3")
lbl_bmi0.grid(row=0, column=2, padx=5, sticky="w")

tk.Label(frame_base, text="前測體脂 (%):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame_base, textvariable=var_f0, width=15).grid(row=1, column=1, padx=10)
lbl_fat0 = tk.Label(frame_base, text="判定: --", font=("Arial", 9, "bold"), fg="#0056b3")
lbl_fat0.grid(row=1, column=2, padx=5, sticky="w")

tk.Label(root, text="="*65, fg="#ccc").pack(pady=5)

# --- 區塊 1: 正向計算 (算分數) ---
tk.Label(root, text="Step 2: 正向計算 (輸入測量值算分數)", font=("Arial", 12, "bold"), fg="#333", bg="#cce5ff", anchor="w").pack(fill="x", anchor="w", pady=5)

frame_fwd = tk.Frame(root)
frame_fwd.pack(fill="x")
tk.Label(frame_fwd, text="目標/目前體重 (kg):", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
tk.Entry(frame_fwd, textvariable=var_w1, width=15).grid(row=0, column=1, padx=10)
lbl_bmi1 = tk.Label(frame_fwd, text="BMI: --", font=("Arial", 9, "bold"), fg="#0056b3")
lbl_bmi1.grid(row=0, column=2, padx=5, sticky="w")

tk.Label(frame_fwd, text="目標/目前體脂 (%):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame_fwd, textvariable=var_f1, width=15).grid(row=1, column=1, padx=10)
lbl_fat1 = tk.Label(frame_fwd, text="判定: --", font=("Arial", 9, "bold"), fg="#0056b3")
lbl_fat1.grid(row=1, column=2, padx=5, sticky="w")

btn_fwd = tk.Button(frame_fwd, text="計算總分數", command=calculate_forward, bg="#007bff", fg="white", font=("Arial", 10, "bold"))
btn_fwd.grid(row=0, column=3, rowspan=2, padx=10, ipadx=5, ipady=5)

lbl_fwd_result = tk.Label(root, text="等待計算...", font=("Arial", 10), justify="left")
lbl_fwd_result.pack(pady=10, anchor="w")

tk.Label(root, text="="*65, fg="#ccc").pack(pady=5)

# --- 區塊 2: 逆向推算 (算目標) ---
tk.Label(root, text="Step 3: 逆向推算 (輸入預期分數算目標)", font=("Arial", 12, "bold"), fg="#333", bg="#f8d7da", anchor="w").pack(fill="x", anchor="w", pady=5)

frame_rev = tk.Frame(root)
frame_rev.pack(fill="x")
tk.Label(frame_rev, text="預期目標總分數 (%):", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
tk.Entry(frame_rev, textvariable=var_target_score, width=15).grid(row=0, column=1, padx=10)

tk.Label(frame_rev, text="預設目標體重 (可留空):", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame_rev, textvariable=var_target_w_opt, width=15).grid(row=1, column=1, padx=10)

btn_rev = tk.Button(frame_rev, text="推算目標數值", command=calculate_reverse, bg="#dc3545", fg="white", font=("Arial", 10, "bold"))
btn_rev.grid(row=0, column=2, rowspan=2, padx=10, ipadx=5, ipady=5)

lbl_rev_result = tk.Label(root, text="等待推算...\n(若體重留空，將給出均衡比例建議)", font=("Arial", 10), justify="left")
lbl_rev_result.pack(pady=10, anchor="w")

root.mainloop()
