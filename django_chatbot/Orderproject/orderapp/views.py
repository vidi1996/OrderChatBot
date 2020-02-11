import json

from django.shortcuts import render
from django.template import loader
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

from chatterbot.ext.django_chatterbot import settings
from .forms import OrderDetailsForm

#from orderapp.forms import OrderDetailsForm
#from  orderapp.models import OrderDetails

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')


class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotAppView1(TemplateView):
    template_name = 'login_page.html'

# def ChatterBotAppView1(request):
#     order_form = OrderDetailsForm()
#     if request.method = "POST":
#         order_data= OrderDetailsForm(request.POST)
#     if order_data.is_valid():
#         order_data.save(commit=True)
# return  render(request=request)


class FormNew(View):

    def response_form(self, request):
        if request.method == 'POST':
            orderDetailsForm = OrderDetailsForm(request.POST)

            if orderDetailsForm.is_valid():
                name = orderDetailsForm.cleaned_data['name']
                Mobile_no = orderDetailsForm.cleaned_data['Mobile_no']
                Address = orderDetailsForm.cleaned_data['Address']

                context = {
                    'name': name,
                    'Mobile_no': Mobile_no,
                    'Address': Address
                }

                template = loader.get_template('login_page.html')

                return HttpResponse(template.render(context, request))

        form = OrderDetailsForm()

        return render(request, 'login_page.html');


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT, read_only=True)
    trainer = ChatterBotCorpusTrainer(chatterbot)
    trainer.train(DATA_DIR + '/test_data.json')
    trainer.export_for_training('./test_data.json')

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(input_data)

        response_data = response.serialize()

        print(response_data)


        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })
