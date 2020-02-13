import json

import template as template
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

from orderapp.forms import OrderDetailsForm
from orderapp.models import OrderDetails

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

RESPONSE_DICT = {
        "type": "",
        "choice": "",
        "size": "",
        "customize": [],
        "quantity": "",
    }



def add_details_form(request):

    name = request.POST["name"]
    mobilenumber = request.POST["mobilenumber"]
    address = request.POST["address"]

    order_details = OrderDetails(
        name=name,
        mobile_no=mobilenumber,
        address=address,
        choice=RESPONSE_DICT['choice'],
        type=RESPONSE_DICT['size'],
        customize=RESPONSE_DICT['customize'],
        quantity=RESPONSE_DICT['quantity']
    )

    order_details.save()
    return render(request, "app.html")


def response_form(request):
    return render(request, "login_page.html")


class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


#class ChatterBotAppView1(TemplateView):
    #template_name = 'login_page.html'
 #   template_name = 'login_page.html'

# def ChatterBotAppView1(request):
#     order_form = OrderDetailsForm()
#     if request.method = "POST":
#         order_data= OrderDetailsForm(request.POST)
#     if order_data.is_valid():
#         order_data.save(commit=True)
# return  render(request=request)


#class FormNew(TemplateView):
  # template_name = 'login_page.html'

# def response_form(self, request):
#     template_name = 'login_page.html'
#     form = OrderDetailsForm()
#     if request.method == 'POST':
#         orderDetailsForm =OrderDetailsForm(request.POST)
#         if orderDetailsForm.is_valid():
#             orderDetailsForm.save(commit=True)
#             my_dict ={'order_form' : form}
#             template = loader.get_template('login_page.html')
#             return HttpResponse(template.render(my_dict, request))
#
#     return render(request=request, template_name='login_page.html')






# def response_form(self, request):
#     template_name = 'login_page.html'
#     form = OrderDetailsForm()
#         if request.method == 'POST':
#            if request.method == 'POST':
#
#             if orderDetailsForm.is_valid():
#                 Name=orderDetailsForm.cleaned_data['name']
#                 Mobile_no=orderDetailsForm.cleaned_data['Mobile_no']
#                 Address = orderDetailsForm.cleaned_data['Address']
#                 orderDetailsForm.save(commit=True)
#
#                 my_context = {'order_form': form}
#
#                 template = loader.get_template('login_page.html')
#
#                 return HttpResponse(template.render(my_context, request))
#
#
#
#         return render(request,template_name = 'login_page.html')
class ResponseObject():
    previous_question = ""


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT, read_only=True)
    trainer = ChatterBotCorpusTrainer(chatterbot)
    trainer.train(DATA_DIR + '/test_data.json')
    trainer.export_for_training('./test_data.json')
    respose_object = ResponseObject()

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

        previous_question = self.respose_object.previous_question

        current_question = response_data['text']
        answer = response_data['in_response_to']
        if current_question == 'I am sorry, but I do not understand.':
            current_question = previous_question
        if previous_question == 'veg or non veg?':
            RESPONSE_DICT['type'] = answer
        elif previous_question == 'Which one You Pick?: Margherita / Farm House / Peppy Paneer / Double Cheese ' \
                                       'Margherita' or previous_question == 'Which one You Pick? : Chicken ' \
                                                                                 'Sausage/ Chicken Delight':
            RESPONSE_DICT['choice'] = answer
        elif previous_question == 'Pick a Size? Regular / Medium / Large':
            RESPONSE_DICT['size'] = answer
        elif previous_question == 'Select topping: Extra Cheese / Paneer / Crispy Capsicum / Onion':
            RESPONSE_DICT['customize'].append(answer)
        elif previous_question == 'Select Crust type: Wheat Crust/ Fresh Pan Crust / Thick Crust':
            RESPONSE_DICT['customize'].append(answer)
        elif previous_question == 'How Many Pizzas? 1 / 2 / 3':
            RESPONSE_DICT['quantity'] = answer
        self.respose_object.previous_question = current_question

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })
