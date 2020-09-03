from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from rest_framework import generics
from .serializers import QuestionSerializer
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView


def get_index_queryset():
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class IndexViewDRF(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'polls/index.html'

    def get(self, request):
        queryset = get_index_queryset()
        return Response({'latest_question_list': queryset})


# class IndexView(generic.ListView):
#     template_name = 'polls/index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


def get_detail_queryset():
    return Question.objects.filter(pub_date__lte=timezone.now())


@method_decorator(never_cache, name='get')
class DetailViewDRF(APIView):
    authentication_classes = []
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'polls/detail.html'

    # @csrf_exempt
    def get(self, request, pk):
        queryset = get_object_or_404(Question, pk=pk)
        return Response({'question': queryset})


# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
#
#     def get_queryset(self):
#         return Question.objects.filter(pub_date__lte=timezone.now())


# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/result.html'


class ResultsViewDRF(APIView):
    template_name = 'polls/result.html'
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        queryset = self.get_queryset()
        return Response({'question': queryset})

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))
# #   return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     # question = get_object_or_404(Question, pk = question_id)
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExists:
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})
#     # return HttpResponse("You're looking at question %s." % question_id)
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/result.html', {'question': question})
