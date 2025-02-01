from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr
from pdf_parser import extract_text_from_pdf
from session_manager import simplify_report, handle_user_question, end_session
import logging
from typing import Optional

# Initialize API Router
app = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request body
class ChatRequest(BaseModel):
    session_id: constr(min_length=36, max_length=36)  # UUID validation
    question: constr(min_length=1)  # Ensure question is not empty


class EndSessionRequest(BaseModel):
    session_id: constr(min_length=36, max_length=36)  # UUID validation


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a PDF file, extract text, and generate a simplified report.

    Args:
        file (UploadFile): The PDF file uploaded by the user.

    Returns:
        JSONResponse: A response containing the session ID and simplified report.
    """
    if not file.filename.endswith('.pdf'):
        logger.error("File upload failed: Unsupported file type.")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        # Extract text from the uploaded PDF
        extracted_text = extract_text_from_pdf(file.file)
        if not extracted_text:
            logger.error("No text extracted from the PDF file.")
            raise HTTPException(status_code=400, detail="The PDF file is empty or could not be processed.")

        # Simplify the extracted text
        simplified_report = simplify_report(extracted_text)
        if not simplified_report:
            logger.error("Failed to simplify the report.")
            raise HTTPException(status_code=500, detail="Failed to simplify the report.")

        return JSONResponse(content=simplified_report, status_code=200)
    except HTTPException as http_exc:
        logger.error(f"HTTP exception during file upload: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error during file upload: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing the PDF file. Please try again."
        )


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Endpoint to handle user questions about the uploaded report.

    Args:
        request (ChatRequest): The request containing the session ID and user question.

    Returns:
        JSONResponse: A response containing the answer to the user's question.
    """
    try:
        # Handle the user's question
        answer = handle_user_question(request.session_id, request.question)
        if not answer:
            logger.error("No answer generated for the user's question.")
            raise HTTPException(status_code=500, detail="Failed to generate an answer.")

        return JSONResponse(content={"answer": answer}, status_code=200)
    except HTTPException as http_exc:
        logger.error(f"HTTP exception during chat: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error during chat: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while handling your request. Please try again."
        )


@app.post("/clear")
async def end_chat(request: EndSessionRequest):
    """
    Endpoint to clear a session and delete associated data.

    Args:
        request (EndSessionRequest): The request containing the session ID to clear.

    Returns:
        JSONResponse: A response confirming the session has been cleared.
    """
    try:
        # End the session
        response = end_session(request.session_id)
        if not response:
            logger.error("Failed to clear the session.")
            raise HTTPException(status_code=500, detail="Failed to clear the session.")

        return JSONResponse(content=response, status_code=200)
    except HTTPException as http_exc:
        logger.error(f"HTTP exception while ending session: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error while ending session: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while ending the session. Please try again."
        )