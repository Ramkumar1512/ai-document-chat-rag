import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings

from .rag_pipeline import create_vector_db, ask_question


@api_view(['POST'])
def upload_pdf(request):

    file = request.FILES['file']

    save_path = os.path.join(settings.BASE_DIR, "documents", file.name)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    create_vector_db(save_path)

    return Response({
        "message": "PDF uploaded and indexed successfully"
    })


@api_view(['POST'])
def ask(request):

    question = request.data.get("question")

    answer = ask_question(question)

    return Response({
        "answer": answer
    })