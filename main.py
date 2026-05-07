
from fastapi import FastAPI
from api.routes import router

app = FastAPI()

app.include_router(router)


# from agents.researcher import researcher_agent
# from agents.summarizer import summarizer_agent
# from agents.fact_checker import fact_checker_agent
# from agents.writer import writer_agent
#
# query = "RAG vs Fine-tuning"
#
# research = researcher_agent(query)
# summary = summarizer_agent(research)
# checked = fact_checker_agent(summary)
# final = writer_agent(checked)
#
# print("FINAL OUTPUT: \n")
# print(final)
#
