from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite", google_api_key=os.getenv("GOOGLE_API_KEY")
)

sentiment_prompt = ChatPromptTemplate.from_template(
    'Classify sentiment (positive, negative, or neutral):\n"{review}"'
)
features_prompt = ChatPromptTemplate.from_template(
    'Extract product features mentioned:\n"{review}"'
)
summary_prompt = ChatPromptTemplate.from_template(
    'Summarize in one sentence:\n"{review}"'
)

sentiment_chain = sentiment_prompt | llm
features_chain = features_prompt | llm
summary_chain = summary_prompt | llm


parallel_chain = RunnableParallel(
    sentiment=sentiment_chain,
    features=features_chain,
    summary=summary_chain,
)
