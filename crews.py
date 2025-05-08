import os
from crewai import Crew, Process
from gaeni_toolkit.agents import Agents, Validator
from gaeni_toolkit.tasks import Tasks, TaskValidator 
from static import Static
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
load_dotenv()

llmx = Static.load_api()

if llmx is None:
    raise ValueError("Failed to load API. Please check your API key and connection.")

search_tool = SerperDevTool(
    api_key=os.getenv("SERPER_API_KEY"),
    search_engine_type="google",
    max_results=2
)
class SetAgent:
    masterH = Agents(llm=llmx, tools=[search_tool]).master_historian_agent()
    questionV = Validator(llm=llmx, tools=[search_tool]).question_validator_agent()
    locationV = Validator(llm=llmx, tools=[search_tool]).location_validator_agent()
    languageV = Validator(llm=llmx, tools=[search_tool]).language_validator_agent()

class Crews:
    def __init__(self, question, location, language):
        self.iquestion = question
        self.ilocation = location
        self.ilanguage = language
        
    def main_crew(self):
        return Crew(
            agents=[
                SetAgent.masterH,
            ],
            tasks=[
                Tasks().historical_task(question=self.iquestion, location=self.ilocation, language=self.ilanguage, agent=SetAgent.masterH),
                Tasks().summarize(question=self.iquestion, location=self.ilocation, language=self.ilanguage, agent=SetAgent.masterH)
            ],
            process=Process.sequential,
            manager_llm=llmx
        )
        
    def validate_crew(self):
        return Crew(
            agents=[
                SetAgent.questionV, SetAgent.locationV, SetAgent.languageV    
            ],
            tasks=[
                TaskValidator().question_validate(self.iquestion, agent=SetAgent.questionV),
                TaskValidator().location_validate(self.ilocation, agent=SetAgent.locationV),
                TaskValidator().language_validate(self.ilanguage, agent=SetAgent.languageV)
            ],
            process=Process.sequential,
            manager_llm=llmx,
            verbose=True
        )