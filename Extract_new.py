import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
# from PIL import Image, ImageTk

def browse_photo_path():
    path = filedialog.askdirectory(title="Select Photo Folder")
    if path:
        photo_path_var.set(path)


def browse_des_path():
    path = filedialog.askdirectory(title="Select Destination Folder")
    if path:
        des_path_var.set(path)


def browse_txt_path():
    path = filedialog.askopenfilename(
        title="Select Extract List File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if path:
        txt_path_var.set(path)


def run_move():
    photo_path = photo_path_var.get().strip()
    des_path = des_path_var.get().strip()
    txt_path = txt_path_var.get().strip()

    if not photo_path or not os.path.isdir(photo_path):
        messagebox.showerror("Error", "photo_path is invalid.")
        return

    if not des_path:
        messagebox.showerror("Error", "des_path is empty.")
        return

    if not txt_path or not os.path.isfile(txt_path):
        messagebox.showerror("Error", "txt_path is invalid.")
        return

    try:
        os.makedirs(des_path, exist_ok=True)

        # 1. 读取 txt，提取编号
        with open(txt_path, "r", encoding="utf-8") as f:
            extract_list = list(set(line.strip() for line in f if line.strip()))

        # 2. 读取所有图片名
        photo_list = os.listdir(photo_path)

        # 3. 根据编号筛选文件
        move_list = []
        for photo_name in photo_list:
            for num in extract_list:
                if num in photo_name:
                    move_list.append(photo_name)
                    break

        # 去重，防止重复加入
        move_list = list(dict.fromkeys(move_list))

        if not move_list:
            messagebox.showinfo("Result", "No matching files found.")
            return

        # 4. move 文件
        moved_count = 0
        skipped_files = []

        for name in move_list:
            src = os.path.join(photo_path, name)
            dst = os.path.join(des_path, name)

            if not os.path.isfile(src):
                skipped_files.append(name)
                continue

            # 如果目标已存在，可选择跳过
            if os.path.exists(dst):
                skipped_files.append(name)
                continue

            shutil.copy(src, dst)
            moved_count += 1

        msg = f"Moved {moved_count} files."

        if skipped_files:
            msg += f"\nSkipped {len(skipped_files)} files (already existed or invalid)."

        messagebox.showinfo("Done", msg)

    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

try:
    logo = tk.PhotoImage(file=resource_path("snorlax.png"))
    logo_label = tk.Label(root, image=logo)
    logo_label.image = logo
    logo_label.grid(row=3, column=0, rowspan=3, padx=10, pady=10)
except Exception as e:
    print("Logo load failed:", e)


# ===== UI =====
root = tk.Tk()
root.title("Photo Filter and Move Tool")
root.geometry("700x300")
root.resizable(False, False)

# # ===== 底部署名 =====
footer = tk.Label(root, text="By @GlennQAQ", font=("SimHei", 10, "bold"))
footer.grid(row=5, column=0, columnspan=3, pady=5)


# ===== Logo =====
try:
    logo = tk.PhotoImage(file=resource_path("snorlax1.png"))

    logo_label = tk.Label(root, image=logo)
    logo_label.image = logo  # 防止被回收
    logo_label.grid(row=3, column=0, rowspan=3, padx=10, pady=10)

except Exception as e:
    print("Logo load failed:", e)

photo_path_var = tk.StringVar()
des_path_var = tk.StringVar()
txt_path_var = tk.StringVar()

# Row 1: photo_path
tk.Label(root, text="Photo Folder:", width=15, anchor="e").grid(row=0, column=0, padx=10, pady=15)
tk.Entry(root, textvariable=photo_path_var, width=60).grid(row=0, column=1, padx=5)
tk.Button(root, text="Browse", command=browse_photo_path, width=10).grid(row=0, column=2, padx=10)

# Row 2: des_path
tk.Label(root, text="Destination Folder:", width=15, anchor="e").grid(row=1, column=0, padx=10, pady=15)
tk.Entry(root, textvariable=des_path_var, width=60).grid(row=1, column=1, padx=5)
tk.Button(root, text="Browse", command=browse_des_path, width=10).grid(row=1, column=2, padx=10)

# Row 3: txt_path
tk.Label(root, text="Extract List TXT:", width=15, anchor="e").grid(row=2, column=0, padx=10, pady=15)
tk.Entry(root, textvariable=txt_path_var, width=60).grid(row=2, column=1, padx=5)
tk.Button(root, text="Browse", command=browse_txt_path, width=10).grid(row=2, column=2, padx=10)

# Run button
tk.Button(root, text="Run Move", command=run_move, width=20, height=2).grid(row=3, column=1, pady=25)

root.mainloop()