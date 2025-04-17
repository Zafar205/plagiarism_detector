import ctypes
from tkinter import *

# g++ -shared -o bloom.dll bloom.cpp -static-libgcc -static-libstdc++ "-Wl,--subsystem,windows"

# Load the DLL
bloom = ctypes.CDLL(r"./bloom.dll")
bloom.check_bloom.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
bloom.check_bloom.restype = ctypes.c_int





import tkinter as tk

from tkinter import filedialog, messagebox, scrolledtext

def get_text_content(text_widget):
    """Retrieve and clean the content of a given text widget."""
    return text_widget.get("1.0", tk.END).strip()


def calculate_word_count(text):
    """Calculate word count from text."""
    words = text.split()
    return len(words)



def calculate_char_count(text):
    """Calculate character count (excluding whitespace)."""
    return len(text.replace(" ", "").replace("\n", ""))



def update_stats():

    """Update stats for both text boxes using widget-aware line count."""

    text1 = get_text_content(text_box1)
    text2 = get_text_content(text_box2)

    word1 = calculate_word_count(text1)
    word2 = calculate_word_count(text2)

    char1 = calculate_char_count(text1)
    char2 = calculate_char_count(text2)
    


    stats_label1.config(text=f"Words: {word1}  | Chars: {char1}")
    stats_label2.config(text=f"Words: {word2}  | Chars: {char2}")


def check_plagiarism():
    """Check the similarity between two texts."""
    text1 = get_text_content(text_box1)
    text2 = get_text_content(text_box2)


    if not text1 or not text2:
        messagebox.showwarning("Input Required", "Please provide text in both boxes.")
        return
    
    t1 = text1.encode('utf-8')
    t2 = text2.encode('utf-8')
    
    result = bloom.check_bloom(t1, t2)

    

        # Save texts to files
    try:
        with open("file1.txt", "w", encoding='utf-8') as f1:
            f1.write(text1)
        
        with open("file2.txt", "w", encoding='utf-8') as f2:
            f2.write(text2)
    except Exception as e:
        messagebox.showerror("File Error", f"Error saving to files: {e}")
        return


    words1 = set(text1.split())
    words2 = set(text2.split())

    similarity = result
    result_label.config(text=f"Plagiarism Score: {similarity:.2f}%")
    
    update_stats()


def upload_file(box_number):

    """Load content from a file into the corresponding text box."""
    
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )


    if file_path:
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                content = file.read()
                if box_number == 1:
                    text_box1.delete("1.0", tk.END)
                    text_box1.insert(tk.END, content)
                else:
                    text_box2.delete("1.0", tk.END)
                    text_box2.insert(tk.END, content)
            update_stats()
        except :
            messagebox.showerror("File Error", f"An error occurred:\n")


def on_key_release(event):
    """Trigger stat update on every key press."""
    update_stats()



# GUI Initialization
root = tk.Tk()
root.title("Plagiarism Detection App")
root.geometry("950x750")
root.configure(bg="#f0f0f0")



# Title Label
title_label = tk.Label(root, text="Plagiarism Detection Tool", font=("Arial", 20, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)



# Main Frame
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)



# ===================== Box 1 =====================
box1_frame = tk.Frame(frame, bg="#f0f0f0")
box1_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)



label1 = tk.Label(box1_frame, text="Text 1", font=("Arial", 12), bg="#f0f0f0")
label1.pack()



text_box1 = scrolledtext.ScrolledText(box1_frame, wrap=tk.WORD, width=50, height=20)
text_box1.pack(fill=tk.BOTH, expand=True)


text_box1.bind("<KeyRelease>", on_key_release)


upload_btn1 = tk.Button(box1_frame, text="Upload File", command=lambda: upload_file(1))
upload_btn1.pack(pady=5)



stats_label1 = tk.Label(box1_frame, text="Words: 0  | Chars: 0", font=("Arial", 10), bg="#f0f0f0")
stats_label1.pack()


# ===================== Box 2 =====================
box2_frame = tk.Frame(frame, bg="#f0f0f0")
box2_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

label2 = tk.Label(box2_frame, text="Text 2", font=("Arial", 12), bg="#f0f0f0")
label2.pack()


text_box2 = scrolledtext.ScrolledText(box2_frame, wrap=tk.WORD, width=50, height=20)
text_box2.pack(fill=tk.BOTH, expand=True)


text_box2.bind("<KeyRelease>", on_key_release)


upload_btn2 = tk.Button(box2_frame, text="Upload File", command=lambda: upload_file(2))
upload_btn2.pack(pady=5)


stats_label2 = tk.Label(box2_frame, text="Words: 0 | Chars: 0", font=("Arial", 10), bg="#f0f0f0")
stats_label2.pack()


# ===================== Bottom =====================
check_btn = tk.Button(root, text="Check Plagiarism", command=check_plagiarism, font=("Arial", 14), bg="#4caf50", fg="white")
check_btn.pack(pady=10)


result_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0", fg="blue")
result_label.pack()


# Start GUI loop
root.mainloop()

