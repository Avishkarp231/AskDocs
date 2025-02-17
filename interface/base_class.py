from abc import ABC, abstractmethod

class ChatInterface(ABC):
    @abstractmethod
    def start_chat(self):
        pass

    @abstractmethod
    def handle_user_input(self, user_input):
        pass
