# importing render and redirect
from django.shortcuts import render, redirect
# importing the openai API
import openai
# import the generated API key from the secret_key file
from .secret_key import API_KEY
# loading the API key from the secret_key file
openai.api_key = API_KEY
from test1.models import *

def calcular_valor_total_deudas(request):
    usuario = request.user

    deudas = Deudas.objects.filter(fk_user=usuario)
    total_deudas = sum(deuda.valor_total_deuda for deuda in deudas)

    total_ingresos = Transacciones.objects.filter(
        fk_cuenta__fk_user=usuario,
        es_ingreso=True
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    total_gastos = Transacciones.objects.filter(
        fk_cuenta__fk_user=usuario,
        es_ingreso=False
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    context = {
        'total_deudas': total_deudas,
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos
    }
    return render(request, 'assistant/home.html', context)

# this is the home view for handling home page logic
def home(request):
    usuario = request.user
    deudas = Deudas.objects.filter(fk_user=usuario)
    total_deudas = sum(deuda.valor_total_deuda for deuda in deudas)

    total_ingresos = Transacciones.objects.filter(
        fk_cuenta__fk_user=usuario,
        es_ingreso=True
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    total_gastos = Transacciones.objects.filter(
        fk_cuenta__fk_user=usuario,
        es_ingreso=False
    ).aggregate(Sum('monto'))['monto__sum'] or 0

    try:
        # if the session does not have a messages key, create one
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "You are now chatting with a financial analyst. Please provide information about your income, expenses, and debts for analysis."},
            ]
        if request.method == 'POST':
            # get the prompt from the form
            prompt = request.POST.get('prompt')
            # get the temperature from the form
            temperature = float(request.POST.get('temperature', 0.2))
            # append the prompt to the messages list
            request.session['messages'].append({"role": "user", "content": prompt})
            # set the session as modified
            request.session.modified = True
            
            deudas = Deudas.objects.all()

            # call the openai API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000,
            )
            # format the response
            formatted_response = response['choices'][0]['message']['content']
            # append the response to the messages list
            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True
            # redirect to the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': temperature,
                'deudas': deudas,
            }
            return render(request, 'assistant/home.html', context)
        else:
            # if the request is not a POST request, render the home page
            context = {
                'messages': request.session['messages'],
                'prompt': '',
                'temperature': 0.1,
                'total_deudas': total_deudas,
                'total_ingresos': total_ingresos,
                'total_gastos': total_gastos
            }
            return render(request, 'assistant/home.html', context)
        
    except Exception as e:
        print(e)
        # if there is an error, redirect to the error handler
        return redirect('error_handler')

def new_chat(request):
    # clear the messages list
    request.session.pop('messages', None)
    return redirect('home')

# this is the view for handling errors
def error_handler(request):
    return render(request, 'assistant/404.html')
