import os
from crewai import Crew, Process
from gaeni_toolkit.agents import Agents, Validator
from gaeni_toolkit.tools import Tools
from gaeni_toolkit.tasks import Tasks, TaskValidator 
from static import Static
from dotenv import load_dotenv
load_dotenv()

llmx = Static.load_api()
if llmx is None:
    raise ValueError("Failed to load API. Please check your API key and connection.")

class SetTool:
    @staticmethod
    def search_tool():
        return Tools().search_tool(serper_key=os.getenv("SERPER_API_KEY"))
    
    @staticmethod
    def news_finder_tool(question):
        return Tools().news_finder(news_key=os.getenv("NEWS_API_KEY"), query=question)


class SetAgent:
    masterH = Agents().master_historian_agent(llm=llmx, tools=[SetTool.search_tool()])
    
    @staticmethod
    def reporterH(question):
        return Agents().reporter_historian_agent(llm=llmx, tools=[SetTool.news_finder_tool(question)])
    
    questionV = Validator().question_validator_agent(llm=llmx, tools=[SetTool.search_tool()])
    locationV = Validator().location_validator_agent(llm=llmx, tools=[SetTool.search_tool()])
    languageV = Validator().language_validator_agent(llm=llmx, tools=[SetTool.search_tool()])

class Crews:
    def __init__(self, question, location, language):
        self.iquestion = question
        self.ilocation = location
        self.ilanguage = language
        
    def main_crew(self):
        if any(agent is None for agent in [SetAgent.masterH, SetAgent.reporterH(self.iquestion)]):
            raise ValueError("One or more required agents are not initialized.")
        
        reporter_agent = SetAgent.reporterH(self.iquestion)
        
        return Crew(
            agents=[
                SetAgent.masterH, reporter_agent
            ],
            tasks=[
                Tasks().historical_task(question=self.iquestion, location=self.ilocation, language=self.ilanguage, agent=SetAgent.masterH),
                Tasks().news_task(question=self.iquestion, location=self.ilocation, language=self.ilanguage, agent=reporter_agent),  # Perbaikan: gunakan reporter_agent
                Tasks().summarize(question=self.iquestion, location=self.ilocation, language=self.ilanguage, agent=SetAgent.masterH)
            ],
            process=Process.sequential,
            manager_llm=llmx
        )
        
    def validate_crew(self):
        if any(agent is None for agent in [SetAgent.questionV, SetAgent.locationV, SetAgent.languageV]):
            raise ValueError("One or more required agents are not initialized.")
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
            manager_llm=llmx
        )