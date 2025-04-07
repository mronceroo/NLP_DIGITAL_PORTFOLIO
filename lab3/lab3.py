import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import lmstudio as lms

class ChessTermApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Terminology Helper")
        self.root.geometry("800x600")
        
        # Initialize model
        self.model = lms.llm("llama-3.2-1b-instruct")
        
        self.create_widgets()
        self.load_example_terms()
        
    def create_widgets(self):
    # Main frame
    main_frame = ttk.Frame(self.root, padding=10)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = ttk.Label(main_frame, text="Chess Terminology Helper", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)
    
    # Input area
    input_frame = ttk.LabelFrame(main_frame, text="Enter a chess term or concept")
    input_frame.pack(fill=tk.X, pady=5)
    
    self.term_entry = ttk.Entry(input_frame, width=50)
    self.term_entry.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.X, expand=True)
    self.term_entry.bind("<Return>", lambda e: self.explain_term())
    
    self.search_button = ttk.Button(input_frame, text="Explain", command=self.explain_term)
    self.search_button.pack(side=tk.LEFT, padx=5, pady=10)
    
    # Language selection
    lang_frame = ttk.Frame(main_frame)
    lang_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(lang_frame, text="Translate to:").pack(side=tk.LEFT, padx=5)
    
    self.language = tk.StringVar(value="English")
    languages = ["English", "Spanish", "French", "German", "Russian", "Italian"]
    self.lang_dropdown = ttk.Combobox(lang_frame, textvariable=self.language, values=languages, state="readonly", width=15)
    self.lang_dropdown.pack(side=tk.LEFT, padx=5)