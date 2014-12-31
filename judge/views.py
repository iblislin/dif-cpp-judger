from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Code, Question
from .judgers import CppJudgerTask

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

@login_required
@require_http_methods(['POST'])
def upload(request, qid):
    if not qid:
        raise Http404
    user = request.user
    content = request.FILES['file'].read()
    code = Code.objects.create(user_id=user.id, question_id=qid, lang_type='cpp',
        content=content)
    task = CppJudgerTask()
    task.delay(code)
    return JsonResponse({
        'status': code.get_status(),
        'code': code.id,
        'result_url': reverse('judge:result', args=[code.id]),
    })

@login_required
def result(request, code_id=None):
    user = request.user

    if code_id:
        code = get_object_or_404(Code, id=code_id, user_id=user.id)
    else:
        code = Code.objects.last()
        if not code:
            raise Http404
    return render(request, 'judge/result.html', {
        'code': code,
    })

@login_required
def result_list(request):
    return render(request, 'judge/result_list.html', {
        'codes': Code.objects.filter(user_id=user.id).order_by('-id')[:5],
        })
