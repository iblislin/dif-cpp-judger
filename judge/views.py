from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

from .models import Code, Question


@login_required
def list(request, page):
    page = page if page else 0
    num = settings.JUDGE_ITEM_PER_LIST
    return render(request, 'judge/list.html', {
        'questions': Question.objects.all()[page*num:(page + 1)*num],
        })

@login_required
def detail(request, qid):
    ques = get_object_or_404(Question, id=qid)
    return render(request, 'judge/detail.html', {
        'question': ques,
        })
