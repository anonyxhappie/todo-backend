from django.http import HttpResponse

def home(request):
    return HttpResponse('API Working Successfully!')