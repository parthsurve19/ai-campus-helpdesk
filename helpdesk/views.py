from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat
from .services import ask_campus_ai

@login_required
def campus_helpdesk(request):
    chats = Chat.objects.filter(user=request.user).order_by("-created_at")

    if request.method == "POST":
        question = request.POST.get("question")
        answer = ask_campus_ai(question)

        Chat.objects.create(
            user=request.user,
            question=question,
            answer=answer
        )

    return render(request, "helpdesk/chat.html", {"chats": chats})


# Create your views here.
