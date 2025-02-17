from .cli_chat import CLIChat
from .tinker_app import GUIChat

class ChatFactory:
    @staticmethod
    def get_chat_mode(mode, query_rag):
        if mode == "cli":
            return CLIChat(query_rag)
        elif mode == "gui":
            return GUIChat(query_rag)
        else:
            raise ValueError(f"Unsupported mode: {mode}")
