from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException

def generate_questions(cv, jd, sample_questions) -> str :

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0)

    class questions(BaseModel):
        question : list[str] = Field(description = "List of interview questions")


    system_message = """

    You are a highly experienced Recruitment Specialist and Interview Strategist with expertise in 
    creating tailored interview questions for a wide range of roles and industries. Your task is to 
    generate a list of **10 customized interview questions** for a specific job candidate based on 
    the provided **Job Description**, their **CV**, and a set of **Sample Questions** for reference.

    Key areas to focus on:

    1. **Relevance to Job Description**: The questions should target the essential skills, 
    responsibilities, and expectations outlined in the job description.

    2. **Candidate-Specific Tailoring**: The questions must delve deeper into the candidate's 
    professional experience, achievements, skills, and qualifications mentioned in their CV.

    3. **Inspiration from Sample Questions**: Use the provided sample questions as a baseline to 
    craft high-quality, insightful queries.

    4. **Competency Assessment**: Include questions that evaluate the candidate's:

    - Technical expertise and problem-solving abilities.
    - Soft skills and behavioral traits (e.g., teamwork, leadership, adaptability).
    - Alignment with the job’s responsibilities and organizational values.

    Output format: {format_instructions}

    """

    human_message = """

    Here are the input details :

    Job Description: {jd_text}
    Candidate CV: {cv_content}
    Sample Questions: {sample_questions}

    """

    prompt_tuple = [
            ("system", system_message),
            ("human", human_message)
        ]
    
    prompt_value_dict = {
            "jd_text": jd,
            "cv_content": cv,
            "sample_questions": sample_questions
        }
    
    prompt = ChatPromptTemplate.from_messages(prompt_tuple)
    parser = PydanticOutputParser(pydantic_object=questions)
    format_instructions =  parser.get_format_instructions() # parsing format instructions
    prompt_value_dict["format_instructions"] = str(format_instructions)


    chain = prompt | llm

    response = chain.invoke(prompt_value_dict)
    result = parser.parse(response.content)    

    return result.question


    

