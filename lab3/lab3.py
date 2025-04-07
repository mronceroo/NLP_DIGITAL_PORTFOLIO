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

        #Dificulty selector
        self.level_var = tk.StringVar(value="Beginner")
        levels = ["Beginner", "Intermediate", "Advanced"]
        ttk.Label(lang_frame, text="Explanation Level:").pack(side=tk.LEFT, padx=5)
        self.level_dropdown = ttk.Combobox(lang_frame, textvariable=self.level_var, values=levels, state="readonly", width=15)
        self.level_dropdown.pack(side=tk.LEFT, padx=5)

        #Search for common terms in Chess button
        terms_frame = ttk.LabelFrame(main_frame, text="Common Chess Terms")
        terms_frame.pack(fill=tk.X, pady=5)

        self.terms_buttons_frame = ttk.Frame(terms_frame)
        self.terms_buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        # Results area
        results_frame = ttk.LabelFrame(main_frame, text="Explanation")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.result_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def load_example_terms(self):
        # Common chess terms
        terms = [
            "Queen", "Rook", "Aperture", "Defense", 
            "Castling", "Discovered Check", "Gambit",
            "Zwischenzug", "Prophylaxis", "Tempo"
        ]
        
        # Create buttons dynamically
        for i, term in enumerate(terms):
            row, col = divmod(i, 4)
            btn = ttk.Button(
                self.terms_buttons_frame, 
                text=term, 
                command=lambda t=term: self.set_term(t),
                width=15
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky=tk.W)
    
    def set_term(self, term):
        #Set the selected term in the entry field and trigger search
        self.term_entry.delete(0, tk.END)
        self.term_entry.insert(0, term)
        self.explain_term()
        
    def explain_term(self):
        #Process the term and get explanation
        term = self.term_entry.get().strip()
        if not term:
            messagebox.showwarning("Empty Term", "Please enter a chess term or select one from the examples.")
            return
        
        # Get selected language and level
        language = self.language.get()
        level = self.level_var.get()
        
        # Disable UI elements during processing
        self.search_button.config(state=tk.DISABLED)
        self.term_entry.config(state=tk.DISABLED)
        self.lang_dropdown.config(state=tk.DISABLED)
        self.level_dropdown.config(state=tk.DISABLED)
        
        # Execute in second plane to not block the grafic interface
        threading.Thread(
            target=self._get_explanation,
            args=(term, language, level),
            daemon=True
        ).start()
        
    def _get_explanation(self, term, language, level):
        try:
            # Create system prompt for the LLM
            prompt = f"""
            Please explain the chess term or concept: "{term}"
            
            Provide the explanation in {language}.
            
            The explanation should be suitable for a {level.lower()} chess player.
            
            Include:
            1. A clear definition of the term
            2. When and how it's typically used in chess
            3. An example position or scenario (described in words)
            4. The term in its original language if applicable
            5. Related chess terms
            
            If this is not a recognized chess term, please explain that and suggest what the user might have meant.
            """
            
            # Call the local LLM through LM Studio
            response = self.model.respond(prompt)
            
            # Update UI in the main thread
            self.root.after(0, lambda: self._update_result(response))
            
        except Exception as e:
            self.root.after(0, lambda: self._handle_error(str(e)))



