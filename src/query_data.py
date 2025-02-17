import argparse
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from .get_embedding_function import get_embedding_function
from .model import model_instance
from .utils import PROMPT_TEMPLATE, CHROMA_PATH


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str, history: str, score_threshold: float = 0.75):
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    results = db.similarity_search_with_score(query_text, k=5)
    filtered_results = [(doc, score) for doc, score in results if score <= score_threshold]

    if not filtered_results:
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context="",history=history, question=query_text)
        response_text = model_instance.invoke(prompt)
        return response_text, [] 

    else:
        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in filtered_results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, history=history, question=query_text)
        response_text = model_instance.invoke(prompt)
        sources = [doc.metadata.get("id", None) for doc, _score in filtered_results]
        return response_text, sources
    
if __name__ == "__main__":
    main()
