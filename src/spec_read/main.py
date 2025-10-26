#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from spec_read.crew import SpecRead

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def chat_with_agent():
    print("🧠 Chat started. Type 'exit' to quit.\n")
    print("The Admin Agent will talk to the Researcher to answer your questions.\n")
    spec_dir = os.path.join(os.getcwd(), "spec")
    

    # Initialize conversation loop
    while True:
        
        user_question = input("You: ").strip()
        inputs={"query": user_question, "spec": spec_dir}
        if user_question.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        try:
            # Run the agent (or crew) with user input
            result = SpecRead().crew().kickoff(inputs=inputs)
            print(f"\nAgent: {result}\n")

        except Exception as e:
            print(f"⚠️ Error: {e}\n")

if __name__ == "__main__":
    chat_with_agent()

# def run():
#     """
#     Run the crew.
#     """
#     spec_dir = os.path.join(os.getcwd(), "spec")
#     print(spec_dir)

#     user_question = input("Ask a question about your documents: ")
#     inputs={"query": user_question, "spec": spec_dir}

#     try:
#         result = SpecRead().crew().kickoff(inputs=inputs)
#         print(result.raw)
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")

# if __name__ == "__main__":
#     run()