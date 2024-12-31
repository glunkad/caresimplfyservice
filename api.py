from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from pdf_parser import extract_text_from_pdf
from session_manager import simplify_report, handle_user_question, end_session

app = APIRouter()

# Pydantic models for the request body
class ChatRequest(BaseModel):
    session_id: str
    question: str

class EndSessionRequest(BaseModel):
    session_id: str

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    try:
        extracted_text = extract_text_from_pdf(file.file)
        simplified_report = simplify_report(extracted_text)
        return JSONResponse(content=simplified_report, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        answer = handle_user_question(request.session_id, request.question)
        return JSONResponse(content={"answer": answer}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during chat: {str(e)}")

@app.post("/clear")
async def end_chat(request: EndSessionRequest):
    try:
        response = end_session(request.session_id)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ending session: {str(e)}")
