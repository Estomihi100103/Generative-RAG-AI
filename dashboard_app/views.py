import os
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from .models import Document, DocumentChunk
from django.views.decorators.csrf import csrf_exempt
import PyPDF2
import docx
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag_app.views import process_embeddings


def handle_uploaded_file(file):
    content = ""
    file_extension = Path(file.name).suffix.lower()

    if file_extension == ".pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            content += page.extract_text()

    elif file_extension in [".doc", ".docx"]:
        doc = docx.Document(file)
        for para in doc.paragraphs:
            content += para.text + "\n"

    elif file_extension == ".txt":
        content = file.read().decode("utf-8")

    return content


@csrf_exempt
def upload_document(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        # Validate file type
        allowed_extensions = [".pdf", ".doc", ".docx", ".txt"]
        file_extension = Path(file.name).suffix.lower()

        if file_extension not in allowed_extensions:
            return JsonResponse(
                {
                    "status": "failed",
                    "message": "Invalid file type. Only PDF, DOC, DOCX, and TXT files are allowed.",
                }
            )

        # Save file
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_url = fs.url(filename)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        # Extract content
        content = handle_uploaded_file(file)

        # Create document
        document = Document.objects.create(
            title=file.name,
            content=content,
            file_type=file.content_type,
            file_path=file_path,
        )

        # Create chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )
        chunks = splitter.split_text(content)

        # Save chunks
        for idx, chunk_text in enumerate(chunks):
            DocumentChunk.objects.create(
                document=document, chunk_index=idx, content=chunk_text
            )

        chunk_ids = [
            chunk.id for chunk in DocumentChunk.objects.filter(document=document)
        ]
        
        # Process embeddings
        embedding_result = process_embeddings(chunk_ids)

        if embedding_result['status'] == 'success':
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Document uploaded and chunked successfully.",
                }
            )
        else:
            return JsonResponse(
                {
                    "status": "failed",
                    "message": f"Document uploaded and chunked successfully, but embeddings failed to process. Error: {embedding_result['message']}",
                }
            )

    return JsonResponse({"status": "failed", "message": "No file uploaded."})


# Create your views here.
def dashboard_view(request):
    return render(request, "dashboard_app/dashboard.html")
