from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite", google_api_key=os.getenv("GOOGLE_API_KEY")
)

parser = StrOutputParser()


class PromptType(Enum):
    ZERO_SHOT = "zero_shot"
    ONE_SHOT = "one_shot"
    FEW_SHOT = "few_shot"
    CHAIN_OF_THOUGHT = "chain_of_thought"
    SELF_CONSISTENCY = "self_consistency"


def zero_shot_prompt(sentence: str, target_language: str = "French"):
    prompt = PromptTemplate.from_template(
        f"Translate the following sentence to {target_language}:\n{{sentence}}"
    )
    chain = prompt | llm | parser
    return chain.invoke({"sentence": sentence})


def one_shot_prompt(review: str):
    prompt = PromptTemplate.from_template(
        """You are a sentiment classifier. 
    Example:
    Review: "I love this phone, it's fast and reliable."
    Sentiment: Positive

    Now classify the next review:
    Review: {review}
    Sentiment:"""
    )
    chain = prompt | llm | parser
    return chain.invoke({"review": review})


def few_shot_prompt(input_word: str):
    example_prompt = PromptTemplate(
        input_variables=["word", "antonym"], template="Word: {word}\nAntonym: {antonym}"
    )

    examples = [
        {"word": "big", "antonym": "small"},
        {"word": "happy", "antonym": "sad"},
        {"word": "light", "antonym": "dark"},
        {"word": "fast", "antonym": "slow"},
    ]

    few_shot_template = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        suffix="Word: {input}\nAntonym:",
        input_variables=["input"],
    )

    chain = few_shot_template | llm | parser
    return chain.invoke({"input": input_word})


def chain_of_thought_prompt(question: str):
    prompt = PromptTemplate.from_template(
        """Solve the problem step by step, then give the final answer.

    Question: {qs}

    Answer: Let's think step by step."""
    )
    chain = prompt | llm | parser
    return chain.invoke({"qs": question})


def self_consistency_prompt(question: str):
    prompt = PromptTemplate.from_template(
        """Solve the following problem in three *independent* ways, 
            each with reasoning and a final answer.

            Problem:
            {qs}

            Provide three calculations and explanations, then end with:
            Final Answer:"""
    )
    chain = prompt | llm | parser
    return chain.invoke({"qs": question})


def execute_prompt(prompt_type: PromptType, **kwargs):
    """Main dispatcher function that calls appropriate prompt function based on enum"""
    if prompt_type == PromptType.ZERO_SHOT:
        return zero_shot_prompt(
            kwargs.get("sentence", ""), kwargs.get("target_language", "French")
        )
    elif prompt_type == PromptType.ONE_SHOT:
        return one_shot_prompt(kwargs.get("review", ""))
    elif prompt_type == PromptType.FEW_SHOT:
        return few_shot_prompt(kwargs.get("input_word", ""))
    elif prompt_type == PromptType.CHAIN_OF_THOUGHT:
        return chain_of_thought_prompt(kwargs.get("question", ""))
    elif prompt_type == PromptType.SELF_CONSISTENCY:
        return self_consistency_prompt(kwargs.get("question", ""))
    else:
        raise ValueError(f"Unsupported prompt type: {prompt_type}")


if __name__ == "__main__":
    print("=== Zero-Shot Example ===")
    result = execute_prompt(PromptType.ZERO_SHOT, sentence="Hello, how are you?")
    print(result)

    print("\n=== One-Shot Example ===")
    result = execute_prompt(
        PromptType.ONE_SHOT, review="I hate this product! It's terrible."
    )
    print(result)

    print("\n=== Few-Shot Learning Example ===")
    result = execute_prompt(PromptType.FEW_SHOT, input_word="hot")
    print(result)

    print("\n=== Chain of Thought Example ===")
    result = execute_prompt(
        PromptType.CHAIN_OF_THOUGHT,
        question="A shopkeeper buys 12 pens at $1.50 each and sells them all for $24. What is his profit percentage?",
    )
    print(result)

    print("\n=== Self Consistency Example ===")
    result = execute_prompt(
        PromptType.SELF_CONSISTENCY,
        question="When I was 6, my sister was half my age. Now I am 70, what age is my sister?",
    )
    print(result)
