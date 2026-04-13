from django.shortcuts import render

def index(request):
    return render(request, "core/home_index.html")
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     template = loader.get_template("polls/index.html")
#     context = {"latest_question_list": latest_question_list}
#     #return HttpResponse(template.render(context, request))
#     return render(request, "polls/index.html", context)