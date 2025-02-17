from langchain_ollama import OllamaLLM

class Model:
    def __init__(self, model_name="mistral"):
        if not hasattr(self, 'instance'):
            print(f"Initializing model: {model_name}")
            self.instance = OllamaLLM(model=model_name)
    
    def get_model(self):
        return self.instance

# Initialize the model instance globally
model_instance = Model().get_model()
