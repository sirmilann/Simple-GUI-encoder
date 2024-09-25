import tkinter as tk
from tkinter import filedialog, scrolledtext, StringVar
from tkinterdnd2 import DND_FILES, TkinterDnD
import base64
import marshal
import zlib

def drop(event):
    process_file(event.data)

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        process_file(file_path)

def process_file(file_path):
    with open(file_path, "rb") as file:
        file_content = file.read()
        
    encoding_method = encoding_var.get()

    if encoding_method == "Base64":
        encoded_content = base64.b64encode(file_content).decode('utf-8')
        exec_command = f'import base64; exec(base64.b64decode(\'{encoded_content}\'))'
        
    elif encoding_method == "marshal":
        encoded_content = base64.b64encode(marshal.dumps(file_content)).decode('utf-8')
        exec_command = f'import base64, marshal; exec(marshal.loads(base64.b64decode(\'{encoded_content}\')))'

    elif encoding_method == "zlib":
        encoded_content = base64.b64encode(zlib.compress(file_content)).decode('utf-8')
        exec_command = f'import base64, zlib; exec(zlib.decompress(base64.b64decode(\'{encoded_content}\')).decode())'

    elif encoding_method == "ALL":
        all_encoded = base64.b64encode(zlib.compress(marshal.dumps(file_content))).decode('utf-8')
        exec_command = f'import base64, zlib, marshal; exec(marshal.loads(zlib.decompress(base64.b64decode(\'{all_encoded}\'))))'

    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, exec_command)

def copy_code():
    root.clipboard_clear()  # Clear the clipboard
    root.clipboard_append(text_area.get(1.0, tk.END).strip())  # Append the text area content to the clipboard
    root.update()  # Keeps the clipboard updated

def save_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_area.get(1.0, tk.END))

def clear_text():
    text_area.delete(1.0, tk.END)

root = TkinterDnD.Tk()
root.title("Code Encoder")
root.geometry("500x400")

# Label for the program
label = tk.Label(root, text="SIMPLE CODE ENCODER - SR", padx=10, pady=10)
label.pack(fill=tk.BOTH)

# Dropdown for selecting encoding method
encoding_var = StringVar(value="Base64")
encoding_options = ["Base64", "marshal", "zlib", "ALL"]
encoding_menu = tk.OptionMenu(root, encoding_var, *encoding_options)
encoding_menu.pack(pady=5)

# Button Frame for horizontal layout
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

button = tk.Button(button_frame, text="Select File", command=select_file, width=15)
button.grid(row=0, column=0, padx=5)

copy_button = tk.Button(button_frame, text="Copy Code", command=copy_code, width=15)
copy_button.grid(row=0, column=1, padx=5)

save_button = tk.Button(button_frame, text="Save to File", command=save_to_file, width=15)
save_button.grid(row=0, column=2, padx=5)

clear_button = tk.Button(button_frame, text="Clear Text", command=clear_text, width=15)
clear_button.grid(row=0, column=3, padx=5)

# Text area for displaying the encoded content
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=10)
text_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

root.mainloop()
