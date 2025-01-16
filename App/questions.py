from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=0)

JD = """
About the job
About us:



At Praktika.ai we are on a mission to deliver efficient and engaging learning experiences for billions of students worldwide by bridging the gap between learning apps and human tutors.

We have done this by creating a fully automated language tutorship experience powered by generative AI Avatars.



After raising $30 million in Series-A funding, we are growing and looking for a Senior AI/LLM Engineer to join us! We are a global small team of 35 innovators who are pushing the boundaries of what’s possible in language learning and tutoring.



In this fast-paced environment we like independent self-starters who can work well in a team as well as unassisted and who enjoy the working environment of an early-stage startup.



About the role:



We are seeking a highly skilled Senior AI/LLM Engineer to research and implement the latest advancements in Language Learning Models (LLMs) and AI technologies.



Your role will be pivotal in enhancing our AI language learning tutors to be effective, personal, and emotionally intuitive. You will be responsible for designing, testing, and deploying AI solutions that align with user learning goals and preferences.



What you'll do with us:



Research and integrate state-of-the-art LLM and AI technologies to improve avatar tutors' teaching effectiveness and personalization.
Design and implement metrics to evaluate the performance and efficiency of our avatar LLM engine.
Conduct experiments and A/B tests based on defined metrics to optimize the learning experience.
Stay updated with the latest advancements in LLM technologies and apply them to production environments, including third-party and open-source LLMs, Retrieval-Augmented Generation (RAG), model fine-tuning, structured output, and external connectors.
Collaborate with instructional designers to refine and optimize prompt engineering for enhanced learning outcomes.
Develop and maintain backend services, ensuring robust, well-architected, and well-tested production-grade code.
Foster a passion for language learning and continuously seek to expand technical knowledge in machine learning and AI.


What we are looking for from you:



Bachelor's or Master's degree in Computer Science, AI, or a related field, with a strong foundation in machine learning.
Deep expertise in AI and LLMs, with a solid understanding of LLM architecture and experience in implementing latest LLM techniques.
Proficient in Python, with a proven track record of writing and maintaining production-grade backend code.
Keen interest in language learning and a desire to explore and expand technical competencies.
Experience in MLOps and DevOps is a plus.


Why should you join Praktika:



Be part of the story of one of the fastest-growing early-stage consumer AI companies globally
Work with a highly ambitious team using the best technologies on the market
Drive innovation and make a significant impact in the AI and education sectors
Competitive salary
Flexibility to work remotely
Health and wellness benefits to support your overall well-being
Opportunity for rapid career growth and personal development
Access to an AI toolkit including ChatGPT, Copilot, and other productivity tools
Annual educational budget of up to $1,000


We are a remote and ever growing team, spanning Brazil, UK, Spain, Germany, Romania, UAE, Ukraine, Indonesia, Poland, Korea and more, bringing diversity of talent and backgrounds.
"""
CV = """
DIVYAPRAKASH RATHINASABAPATHY – AI/ML ENGINEER
    rdivyaprakash78@gmail.com|| +44 7818337189 ||https://www.linkedin.com/in/divyaprakash-rathinasabapathy-6340861a7/
London, UK.
A highly skilled Data Scientist and Machine Learning Engineer with experience in natural language processing (NLP), large language models (LLMs), and cloud-based AI systems. Proficient in fine-tuning and implementing LLMs for applications such as RAG-based chatbot frameworks, real-time transcription, and multilingual speech-to-text (STT) and text-to-speech (TTS) systems. Adept in web development, building scalable applications using frameworks like Flask and Langgraph, and architecting robust AI-driven solutions. Hands-on experience with cloud platforms, specifically Google Cloud, and a strong understanding of integrating LLM-based frameworks using TensorFlow and PyTorch. Passionate about leveraging cutting-edge AI techniques to optimize system performance, automate workflows, and improve product functionality. GitHub

EDUCATION	
Data Science, M.Sc., – Kingston University, U.K.			                                                                               Jan 2023 – Jan 2024
Electronics and Communication Engineering, B.Tech., – Amrita School of Engineering, India		                             Jul 2017 – May 2021

SKILLS AND EXPERTISE
	
	Natural Language Processing (NLP) & LLMs: Experienced in fine-tuning LLMs for RAG systems and conducting NLP evaluations, including semantic similarity and WEAT tests to improve model performance and fairness.
	Machine Learning Frameworks: Skilled in TensorFlow and PyTorch for developing LLMs and deep learning models focused on NLP tasks such as language understanding and generation.
	Cloud Computing & Services: Hands-on with GCP services (STT and TTS) and Dialogflow for building chatbots and integrating speech-based technologies into applications.
	Web Development: Experienced in Flask for web applications and audio-to-text streaming; familiar with FastAPI for building fast, scalable APIs.
	Version Control & Collaboration: Proficient in GitHub for version control and team collaboration, ensuring smooth development workflows.
	System Optimization & Workflow Automation: Focused on optimizing ML models and automating workflows for data labeling, model evaluation, and deployment.
	Testing & Evaluation: Skilled in implementing NLP-based testing mechanisms for evaluating LLM responses and ensuring model accuracy and fairness.
	Other Technologies & Tools: Proficient in Python and SQL, with introductory experience in Docker for deploying models and containerizing applications.

WORK EXPERIENCE	

AI Engineer Intern – Navi Promotions, Remote. 			                                                                                   Oct 2024 – Present
	Developed Retrieval-Augmented Generation (RAG) based prototypes for chatbots, tailored to client specifications, incorporating advanced NLP models to enhance user interactions and meet business objectives.
	Engineered multi-agent flow architectures using frameworks such as Autogen and LangGraph, enabling the creation of dynamic, scalable AI systems that can handle complex, multi-step user interactions.
	Worked with backend frameworks like Flask to design and implement server-side architectures for AI solutions, ensuring smooth integration with client systems and services.
	Built and optimized robust Generative AI systems, focusing on improving the reliability and responsiveness of large language model (LLM) outputs, ensuring accurate and contextually appropriate results.
	Implemented advanced parsing techniques using libraries like Pydantic and Instructor, improving the extraction and validation of structured data from natural language inputs, enhancing the chatbot's performance and reliability.
	Documented development processes, model specifications, and system architectures to ensure clarity and facilitate future enhancements and knowledge transfer.
	Worked independently on the entire project, organizing and managing all aspects of the workflow, from requirements gathering to model deployment. This autonomy enhanced my ability to prioritize tasks, meet deadlines, and deliver high-quality solutions with minimal supervision.


Junior Machine Learning Engineer Volunteer – Omdena, Remote. 			                                               Apr 2024 – Jun 2024
	Collaborated with senior data scientists and clients to identify and define project objectives, gathering requirements and collecting relevant data to effectively address specific business challenges.
	Conducted thorough data validation using standardized protocols to ensure accuracy and integrity, laying a solid foundation for subsequent analysis.
	Performed exploratory data analysis (EDA), including data cleaning, visualization, and documentation, to uncover insights and support informed decision-making.
	Actively participated in workshops and training sessions, providing guidance and support to colleagues who required assistance in unfamiliar tasks, fostering a collaborative and inclusive team environment.
	Developed comprehensive reports and visualizations to clearly communicate findings to stakeholders, facilitating a better understanding of data-driven insights.
	Engaged in continuous learning and skill development, staying updated with industry best practices to enhance analytical capabilities and contribute effectively to team projects.

Programmer Analyst trainee: Data Science – Cognizant Technology Solutions, India.			                             Aug 2021 – Nov 2022
	Developed and optimized NLP models for extracting actionable insights from large datasets, utilizing state-of-the-art text processing techniques and parameter-efficient fine-tuning methods such as LoRA, Prompt Tuning, and P-tuning to enhance business decision-making processes.
	Implemented Retrieval-Augmented Generation (RAG) systems, combining document retrieval and generative models to improve the accuracy and relevance of automated responses for customer-facing applications.
	Utilized advanced NLP frameworks, including Hugging Face (for model deployment and fine-tuning) and TensorFlow, to build, fine-tune, and deploy language models for tasks including text summarization, sentiment analysis, and question-answering.
	Designed and built data pipelines for the efficient processing and transformation of textual data, ensuring that NLP models received high-quality, clean data for optimal performance.
	Integrated NLP solutions with external systems using RESTful APIs, enabling seamless interaction between the AI models and enterprise platforms, thus enhancing user experience and operational efficiency.
	Collaborated with cross-functional teams to gather requirements, define business goals, and deliver NLP solutions aligned with customer needs and business objectives.

PROJECT EXPERIENCE	

AI powered CV optimization tool using Langgraph 								                          Link
	Built an AI-driven CV optimization tool using Python, LangChain, Cohere LLM API, and Streamlit to enhance CV relevance based on job descriptions. 
	Designed a StateGraph framework for iterative CV evaluation, scoring, and refinement, with automated suggestions and keyword alignment. 
	Developed a user-friendly interface enabling real-time CV updates, leveraging Regex for precise data extraction and actionable insights. 

Doctor’s appointment managing Chatbot										         Link 
	Designed and built an interactive chatbot system for managing doctor appointments, using Google’s Gemini Large Language Model for NLP tasks such as intent and entity recognition.
	Implemented MySQL for database management and used Streamlit for the front-end interface. The chatbot automated tasks like appointment booking, editing, and cancellations, improving operational efficiency and user experience. 

Ship Performance analysis: 											         Link
	Applied statistical techniques such as ANOVA and Tukey HSD to assess ship performance over time, identifying significant differences in performance metrics.
	Developed a dynamic Power BI dashboard to visualize time-series data, highlighting critical trends for strategic decision-making.
	Used ARIMAX forecasting to predict fuel consumption, achieving a Mean Absolute Percentage Error (MAPE) of 7.42%, providing reliable insights for optimizing fuel efficiency and reducing operational costs. 

"""

class Question(BaseModel):
    question : str = Field(description = "Question")

class responseModel(BaseModel):
    response : list[Question] = Field(description = "List of questions") 

system_message = """

You are an experienced recruiter. Given a job description you should find the key requirements for the role
and draft questions to ask to that candidate who is participating in the interview.

Furthermore, you will be provided with the candidate's CV, You should tailor the questions
based upon it.

Make sure that you choose the right candidate, That solely dependent on the questions you prepare.

Your response should just be the list of questions. 

*PREPARE ATLEAST 10 QUESTIONS*

Here's the format instructions  : {format_instructions}
"""
human_message = """
Job description : {JD}
CV : {CV}
"""

load_dotenv()

prompt_tuple = [
            ("system", system_message),
            ("human", human_message)
        ]
    
prompt_value_dict = {
            "JD" : JD,
            "CV" : CV
        }


prompt = ChatPromptTemplate.from_messages(prompt_tuple)

parser = PydanticOutputParser(pydantic_object=responseModel) # initialzing the parser
format_instructions =  parser.get_format_instructions() # parsing format instructions
prompt_value_dict["format_instructions"] = str(format_instructions)
chain = prompt | llm
response = chain.invoke(prompt_value_dict) 

result = parser.parse(response.content) 

array = []

for i in result.response:
    array.append(i.question)