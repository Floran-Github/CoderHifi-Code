from django.shortcuts import render

# Create your views here.
def mainpage(request):
    return render(request,'index.html')

def devpage(request):
    return render(request,'devlogin.html')

def recpage(request):
    return render(request,'recuiter.html')

