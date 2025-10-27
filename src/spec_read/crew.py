from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.pdf_reader import PDFReaderTool
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
import os

# Initialize the tool
# pdf_reader_tool = PDFReaderTool()



@CrewBase
class SpecRead():
    """SpecRead crew"""

    agents_config= 'config/agents.yaml'
    tasks_config= 'config/tasks.yaml'

    @agent
    def admin(self) -> Agent:
        return Agent(
            config=self.agents_config['admin'], # type: ignore[index]
            verbose=True
        )

    @agent
    def spec_researcher(self) -> Agent:
        """Researcher agent — reads and extracts information from all PDFs in knowledge folder."""
        # Resolve absolute path to the project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        knowledge_dir = os.path.join(project_root, "knowledge")
        print(knowledge_dir)

        # Ensure knowledge directory exists
        if not os.path.exists(knowledge_dir):
            raise FileNotFoundError(f"Knowledge folder not found: {knowledge_dir}")

        # Load all PDF files from the knowledge folder
        pdf_sources = []
        for filename in os.listdir(knowledge_dir):
            if filename.lower().endswith(".pdf"):
                print("file name:")
                print(filename)
                print(os.path.join("knowledge", filename))
                pdf_sources.append(
                    PDFKnowledgeSource(
                        file_paths=filename,  # relative to project root
                        chunk_size=800,
                        chunk_overlap=100
                    )
                )

        if not pdf_sources:
            raise FileNotFoundError(f"No PDF files found in {knowledge_dir}")
        print(pdf_sources)

        return Agent(
            config=self.agents_config['spec_researcher'],  # type: ignore[index]
            knowledge_sources=pdf_sources,
            verbose=True
        )


    @agent
    def spec_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['spec_analyst'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def admin_task(self) -> Task:
        return Task(
            config=self.tasks_config['admin_task'], # type: ignore[index]
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='output/report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SpecRead crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
