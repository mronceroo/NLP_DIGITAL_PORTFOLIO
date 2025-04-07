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