import tkinter as tk
from tkinter import ttk
from .base_class import ChatInterface

class GUIChat(ChatInterface):
    def __init__(self, query_rag):
        self.query_rag = query_rag
        self.history = ""
        self.root = tk.Tk()
        self.root.title("Chat GUI")
        self.root.configure(bg="#FFFFFF")  # Set background color

        # Set window size
        self.root.geometry("600x700")

        # Create styles
        self.style = ttk.Style()
        self.style.configure('Message.TLabel', foreground='#000000', font=('Helvetica', 12), background='#FFFFFF', wraplength=500)
        self.style.configure('UserLabel.TLabel', foreground='#1E90FF', font=('Helvetica', 10, 'bold'), background='#FFFFFF')
        self.style.configure('AgentLabel.TLabel', foreground='#32CD32', font=('Helvetica', 10, 'bold'), background='#FFFFFF')
        self.style.configure('System.TLabel', foreground='#FF4500', font=('Helvetica', 10, 'italic'), background='#FFFFFF', wraplength=500)

    def start_chat(self):
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for scrollbar
        self.canvas = tk.Canvas(self.main_frame, bg="#FFFFFF", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Frame inside the canvas
        self.chat_frame = tk.Frame(self.canvas, bg="#FFFFFF")
        self.canvas.create_window((0, 0), window=self.chat_frame, anchor='nw')

        # User input field frame
        self.input_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.input_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # User input field
        self.user_input = tk.Entry(self.input_frame, font=("Helvetica", 14))
        self.user_input.pack(fill=tk.X, padx=(10, 5), pady=5, side=tk.LEFT, expand=True)
        self.user_input.bind("<Return>", self.handle_user_input)

        # Send button
        self.send_button = tk.Button(self.input_frame, text="Send", command=self.handle_user_input, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
        self.send_button.pack(padx=(5, 10), pady=5, side=tk.RIGHT)

    def handle_user_input(self, event=None):
        user_text = self.user_input.get().strip()
        if not user_text:
            return

        if user_text.lower() in ["exit", "quit"]:
            self.display_message("System", "Exiting the chat. Goodbye!")
            self.root.after(1000, self.root.quit)
        else:
            # Display user's message
            self.display_message("You", user_text)

            # Clear input field after sending message
            self.user_input.delete(0, tk.END)

            # Display loading message
            self.display_message("System", "Agent is typing...")

            # Get the response asynchronously
            self.root.after(100, self.query_and_display_response, user_text)

    def query_and_display_response(self, user_text):
        response, sources = self.query_rag(user_text, self.history)
        formatted_sources = set()
        for source in sources:
            doc_name = source.split("\\")[1].split(":")[0]
            formatted_sources.add(doc_name)

        # Update history
        self.history += f"You: {user_text}\nAgent: {response}\n"

        # Remove the "Agent is typing..." message
        self.chat_frame.winfo_children()[-1].destroy()

        # Display agent's response
        self.display_message("Agent", response)

        if sources:
            sources_text = f"Sources: {', '.join(formatted_sources)}"
            self.display_message("System", sources_text)

        # Scroll to the bottom
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)

    def display_message(self, sender, message):
        """
        Display a message in the chat window with styles.
        """
        msg_frame = tk.Frame(self.chat_frame, bg="#FFFFFF")

        # Sender label and message content
        if sender == "You":
            sender_label = ttk.Label(msg_frame, text=f"{sender}:", style='UserLabel.TLabel', anchor='w')
            sender_label.pack(anchor='w', padx=10, pady=(2, 0))
            message_label = ttk.Label(msg_frame, text=message, style='Message.TLabel', justify='left')
            message_label.pack(anchor='w', padx=20, pady=(0, 2))
        elif sender == "Agent":
            sender_label = ttk.Label(msg_frame, text=f"{sender}:", style='AgentLabel.TLabel', anchor='w')
            sender_label.pack(anchor='w', padx=10, pady=(8, 0))  # Added extra space before agent's response
            message_label = ttk.Label(msg_frame, text=message, style='Message.TLabel', justify='left')
            message_label.pack(anchor='w', padx=20, pady=(0, 2))
        else:  # System messages (e.g., sources)
            # No sender label for system messages to reduce whitespace
            message_label = ttk.Label(msg_frame, text=message, style='System.TLabel', justify='left')
            message_label.pack(anchor='w', padx=10, pady=(1, 2))

        msg_frame.pack(fill=tk.X, anchor='w', pady=(0, 0))

        # Update the scroll region
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)
