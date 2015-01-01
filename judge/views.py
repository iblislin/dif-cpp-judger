from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags import humanize
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
    user = request.user
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
        'code': code.id,
    })

@login_required
def result(request, question_id, code_id=None):
    user = request.user
    payload = {'code': {}}
    fields = ('status', 'get_status', 'create_time', 'compile_msg', 'exec_msg')
    question = get_object_or_404(Question, id=question_id)

    if code_id:
        code = get_object_or_404(Code, id=code_id,
            user_id=user.id,
            question_id=question_id,
            )
    else:
        try:
            code = Code.objects.filter(user_id=user.id,
                question_id=question_id).latest('create_time')
        except Code.DoesNotExist:
            return JsonResponse(payload)

    for field in fields:
        if field == 'create_time':
            time = humanize.naturaltime(getattr(code, field))
            payload['code'][field] = time
            continue
        elif field == 'get_status':
            payload['code'][field] = code.get_status()
            continue
        payload['code'][field] = getattr(code, field)

    return JsonResponse(payload)

@login_required
def result_list(request):
    return render(request, 'judge/result_list.html', {
        'codes': Code.objects.filter(user_id=user.id).order_by('-id')[:5],
        })
