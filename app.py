import argparse
from interface.Interface_Factory import ChatFactory
from src.query_data import query_rag

def main():
    parser = argparse.ArgumentParser(description="Start the LLM chat application.")
    parser.add_argument('--mode', type=str, choices=['cli', 'gui', 'web'], default='cli',
                        help="Choose the mode to run the app. Options: 'cli', 'gui', 'web'. Default is 'cli'.")
    args = parser.parse_args()
    chat_instance = ChatFactory.get_chat_mode(args.mode, query_rag)
    chat_instance.start_chat()

if __name__ == "__main__":
    main()
