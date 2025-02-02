from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from typing import Literal

def classify(user_text : str) -> str :

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0, max_tokens =1)


    system_message = """

    You are an intent classifier. Given a user's response in an interview you should classify it into one
    of the following.

    -answer : The user attempting to give answer to the question
    -skip:the user wants to skip the question
    -repeat : the user wants the interviewer to repeat the question
    -exit : the user wishes to quirt the question.

    Output format instructions : You should reply only "answer" or "skip" or "exit" or "repeat" and nothing else

    """

    human_message = """

    The is the user input you need to classify : {user_input}

    """

    prompt_tuple = [
            ("system", system_message),
            ("human", human_message)
        ]
    
    prompt_value_dict = {
            "user_input": user_text
        }
    
    prompt = ChatPromptTemplate.from_messages(prompt_tuple)

    chain = prompt | llm

    response = chain.invoke(prompt_value_dict)

    return response.content

    

