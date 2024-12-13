from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")


openai_llm = ChatOpenAI(temperature=0.3, model="gpt-3.5-turbo")

my_prompt_template_pitch_insights = PromptTemplate(
    input_variables=["deck_content"],
    template=(
        "As a VC analyst provide concise answers based solely on the data presented. "
        "If information for a specific point is not explicitly provided or is unclear, "
        "mark it as \"NA\" (Not Available).\n\nSolution (Product/Service) :\n"
        "What do they sell? (Product or service, and how it's used)\n"
        "Clients:\n"
        "To whom do they sell?\n"
        "Who pays for the product/service?\n"
        "Who uses the product/service?\n"
        "Where are the clients located? In francophone Africa ??\n"
        "Business Model:\n"
        "How does the company generate revenue?\n"
        "Management / Team:\n"
        "What is the background of the entrepreneur(s)?\n"
        "Traction and Historical Financial Performance:\n"
        "(MRR (Monthly Recurring Revenue) or Yearly Revenue traction KPIs )\n"
        "Fundraising:\n"
        "How much capital is the startup seeking to raise?\n"
        "At what valuation are they proposing this fundraise?\n"
        "Remember to stick strictly to the information provided in the pitch deck. "
        "Do not make assumptions or invent data. If any information is missing or not "
        "clearly stated, mark it as \"NA\" for that specific point.\n---\n"
        "Content: {deck_content}.\n"
        "Important: make sure to present the information in a clear and concise manner."
    )
)
chain = my_prompt_template_pitch_insights | openai_llm

def get_pitch_insights(deck_content_txt):
    answer = chain.invoke(deck_content_txt)
    return answer.content
    
def deck_direct_chat(deck_content_txt, query):
    """
    Generate a response to a user query about the deck using direct context
    
    Args:
        deck_content_txt (str): Full text content of the deck
        query (str): User's question about the deck
    
    Returns:
        str: AI's response to the query
    """
    # Create a prompt that includes the deck content as context
    chat_prompt = PromptTemplate(
        input_variables=["deck_content", "query"],
        template=(
            "You are an AI assistant helping to analyze a startup pitch deck. "
            "Use ONLY the information provided in the deck content to answer the question. "
            "If the information is not available in the deck, clearly state that.\n\n"
            "Deck Content:\n{deck_content}\n\n"
            "Question: {query}\n\n"
            "Answer:"
        )
    )
    
    # Create a chain with the prompt and LLM
    chat_chain = chat_prompt | openai_llm
    
    try:
        # Invoke the chain with deck content and query
        response = chat_chain.invoke({
            "deck_content": deck_content_txt, 
            "query": query
        })
        return response.content
    except Exception as e:
        return f"An error occurred: {str(e)}"


