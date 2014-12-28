from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import CodeUploadForm
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
        'code_form': CodeUploadForm,
        })

@login_required
@csrf_exempt
def upload(request, qid):
    user = request.user
    content = request.FILES['file'].read()
    code = Code.objects.create(user_id=user.id, question_id=qid, lang_type='cpp',
        content=content)
    print code.content
    return JsonResponse({'status': 'ok'})
