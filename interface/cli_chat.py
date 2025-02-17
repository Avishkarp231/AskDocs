from .base_class import ChatInterface
class CLIChat(ChatInterface):
    def __init__(self, query_rag):
        self.query_rag = query_rag
    
    def start_chat(self):
        print("="*50)
        print("Welcome to the interactive LLM chat!")
        print("Type your questions below.")
        print("Type 'exit' or 'quit' to end the conversation.")
        print("="*50)

        history = ""
        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ["exit", "quit"]:
                    print("\nExiting the chat. Goodbye!")
                    break
                response, sources = self.handle_user_input(user_input, history)
                formatted_sources = set()
                for source in sources:
                    doc_name = source.split("\\")[1].split(":")[0]
                    formatted_sources.add(doc_name)

                print("="*50)
                print(f"RAG Agent: {response}")
                if formatted_sources:
                    print(f"Sources: {', '.join(formatted_sources)}")
                print("="*50)
                history += f"User: {user_input}\nAssistant: {response}\n"

            except KeyboardInterrupt:
                print("\nExiting the chat. Goodbye!")
                break
            except Exception as e:
                print("\nAn error occurred. Please try again.")
                print(f"Error: {e}")

    def handle_user_input(self, user_input: str, history: str):
        # Here we can call query_rag (or any other function that processes user input)
        response, sources = self.query_rag(user_input, history)
        return response, sources

    def query_rag(self, query_text: str, history: str):
        return self.query_rag(query_text, history)