from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Literal


def classify(transcript: str) -> str:
    class intent(BaseModel):
        intent: Literal["answer", "skip", "repeat", "exit"] = Field(description= "intent of the user")

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0, max_tokens=1)

    system_message = """
    
    You will classify a candidate's response from an interview transcript into one of the following categories:

    answer – The candidate is responding to a question.
    skip – The candidate wants to skip the question.("Can I skip this?", "I want to move to the next qyuestion")
    repeat – The candidate asks for the question to be repeated.("Can you come again", "Can you repeat it once again?")
    exit – The candidate wants to exit the interview. (eg: "Can I exit the interview?" , "Can i quit the interview?")

    Output Format:
    
    Respond with only one of the following labels: "answer", "skip", "repeat", or "exit". No additional text.

    """

    human_message = """Here's the transcript of candidate response : {transcript}"""

    prompt_tuple = [
            ("system", system_message),
            ("human", human_message)
        ]
    
    prompt_value_dict = {
            "transcript" : transcript
        }
    
    prompt = ChatPromptTemplate.from_messages(prompt_tuple)

    #parser = PydanticOutputParser(pydantic_object=intent)
    #format_instructions =  parser.get_format_instructions()
    #prompt_value_dict["format_instructions"] = str(format_instructions)

    chain = prompt | llm
    response = chain.invoke(prompt_value_dict)

    print("intent: " + response.content)

    return response.content



    


