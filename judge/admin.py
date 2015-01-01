from django.contrib import admin

from .models import Question, Code


class QuestionAdmin(admin.ModelAdmin):
    pass


class CodeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Question, QuestionAdmin)
admin.site.register(Code, CodeAdmin)
