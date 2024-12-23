from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pdf_extractor import extract_text_from_pdf
from huggingface_client import send_to_huggingface_api_with_client

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, change as needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Store extracted text globally for chatting
extracted_text_context = ""

@app.get("/")
async def root():
    """Root endpoint to display a welcome message."""
    return {"message": "Hello! The API is running. Use the /upload endpoint to upload a PDF file and /chat to chat with the bot."}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Endpoint to handle PDF file upload, text extraction, and summary generation."""
    global extracted_text_context

    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        # Extract text from the uploaded PDF
        pdf_file = file.file
        extracted_text_context = extract_text_from_pdf(pdf_file)

        # Generate a short summary using Hugging Face API
        summary_messages = [
            {"role": "system", "content": "Summarize the following text in a concise manner."},
            {"role": "user", "content": extracted_text_context}
        ]
        summary = send_to_huggingface_api_with_client(summary_messages)

        # Generate sample questions based on the PDF content
        questions_messages = [
            {"role": "system", "content": "Based on the following text, provide 3 sample questions someone might ask."},
            {"role": "user", "content": extracted_text_context}
        ]
        sample_questions = send_to_huggingface_api_with_client(questions_messages)

        return JSONResponse(content={
            "message": "PDF uploaded and processed successfully.",
            "summary": summary,
            "sample_questions": sample_questions,
            "extracted_text": extracted_text_context
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_bot(question: str):
    """Endpoint to chat with the bot based on the uploaded PDF content."""
    global extracted_text_context

    if not extracted_text_context:
        raise HTTPException(status_code=400, detail="No PDF content available. Please upload a PDF first using the /upload endpoint.")

    try:
        # Construct messages for the chat
        messages = [
            {"role": "system", "content": "You are an AI assistant acting as an experienced medical doctor with 20 years of practice in diagnosing and explaining medical conditions. You specialize in translating complex medical terms and reports into simple, easy-to-understand language for patients. Your role is to: \n- Carefully read the provided clinical report or text. \n- Accurately interpret the content, ensuring you maintain medical correctness. \n- Answer any questions posed by the user in a way that a non-medical professional can easily understand, using analogies and examples where appropriate. \n- Always communicate with empathy and reassurance, ensuring that your explanations are clear and concise. \n- Provide explanations as though you are speaking directly to a patient or their family, avoiding unnecessary jargon, and focusing on what the patient needs to know and understand."},
            {"role": "user", "content": question}
        ]

        # Send the question and context to Hugging Face API
        api_response = send_to_huggingface_api_with_client(messages)

        return JSONResponse(content={"question": question, "answer": api_response}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
