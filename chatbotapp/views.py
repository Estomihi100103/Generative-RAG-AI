from django.shortcuts import redirect, render
from chatbot.settings import GENERATIVE_AI_KEY
from chatbotapp.models import ChatMessage
import google.generativeai as genai
from django.http import JsonResponse
from rag_app.views import search_similar_chunks

def send_message(request):
    if request.method == 'POST':
        try:
            genai.configure(api_key=GENERATIVE_AI_KEY)
            model = genai.GenerativeModel("gemini-1.5-pro")

            user_message = request.POST.get('user_message')
            if not user_message:
                return JsonResponse({'status': 'error', 'message': 'No message provided'}, status=400)
            
            # Take the relevant context of the RAG results
            rag_response = search_similar_chunks(user_message)
            if rag_response['status'] == 'error':
                return JsonResponse(rag_response, status=500)
            
            # Arrange the context of the RAG results
            context_texts = []
            for result in rag_response['results']:
                context_texts.append(result['content'])
            context = "\n".join(context_texts)
            
            # Prompt template
            prompt_template = """
            Konteks Relevan:
            {context}

            Instruksi: Gunakan konteks di atas sebagai referensi tambahan untuk menjawab pertanyaan berikut.
            
            Pertanyaan: {question}
            """
            
            formatted_prompt = prompt_template.format(
                context=context,
                question=user_message
            )
                        
            bot_response = model.generate_content(formatted_prompt)
            
            # Save the original message (without context) to the database
            chat_message = ChatMessage.objects.create(
                user_message=user_message,  
                bot_response=bot_response.text
            )
            
            return JsonResponse({
                'status': 'success',
                'user_message': chat_message.user_message,
                'bot_response': chat_message.bot_response,
                'timestamp': chat_message.created_at.strftime("%I:%M %p")
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

def list_messages(request):
    messages = ChatMessage.objects.all().order_by('created_at')
    return render(request, 'chatbot/list_messages.html', {'messages': messages})