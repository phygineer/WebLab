from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from langchain_community.llms import Ollama 

router = APIRouter(
    prefix="/ollama",
    tags=["ollama"],
    responses={404: {"description": "Not found"}}
)

class Payload(BaseModel):
    host:str="http://localhost:11434"
    model:str="llama3.2:latest"

class ChatPayload(BaseModel):
    host:str="http://localhost:11434"
    context:str = ""
    text: str
    model:str="llama3.2:latest"

@router.post("/pull")
def pull_model(payload: Payload):
    url=f"{payload.host}/api/pull"
    data = {
        "name": payload.model
    }
    response=requests.post(url, json=data)
    if response.status_code == 200:
        response = response.json()
        return {response}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.content)
    
@router.delete("/remove")
def delete_model(payload: Payload):
    url=f"{payload.host}/api/delete"
    data = {
        "name": payload.model
    }
    response=requests.delete(url, json=data)
    if response.status_code == 200:
        response = response.json()
        return {response}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.content)
    

@router.get("/list")
def list_models(host:str="http://localhost:11434"):
    url=f"{host}/api/tags"
    response=requests.get(url)
    if response.status_code == 200:
        response = response.json()
        return response
    else:
        raise HTTPException(status_code=response.status_code, detail=response.content)

@router.get("/running")
def list_running_models(host:str="http://localhost:11434"):
    url=f"{host}/api/ps"
    response=requests.get(url)
    if response.status_code == 200:
        response = response.json()
        return response
    else:
        raise HTTPException(status_code=response.status_code, detail=response.content)
    

@router.post("/chat")
def chat(msg: ChatPayload):
    model = Ollama(model=msg.model,base_url=msg.host,keep_alive="-1m")
    response=model.invoke(msg.text)
    return {"query":msg.text, "response":response}