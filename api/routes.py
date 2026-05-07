from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from graph.graph_builder import app

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

#Streaming Function
def generate_stream(query: str):
    for step in app.stream({"query": query}):

        for node, output in step.items():

            yield f"\n🔹 Agent: {node}\n"

            for key, value in output.items():
                yield f"{key}:\n{value}\n"


@router.post("/research/stream")
def stream_research(request: QueryRequest):

    return StreamingResponse(
        generate_stream(request.query),
        media_type="text/plain"
    )














# from fastapi import APIRouter
# from pydantic import BaseModel
#
# from graph.graph_builder import app
#
# router = APIRouter()
#
# #Pydantic Validation
# class QueryRequest(BaseModel):
#     query: str
#
# @router.post('/research')
# def run_research(request: QueryRequest):
#     result = app.invoke({"query": request.query})
#
#     return {
#         "query": request.query,
#         "result": result["final"]
#     }

