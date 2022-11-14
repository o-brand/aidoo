import git
import subprocess
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        subprocess.check_call("cd  /home/teamgolf/golf; git fetch --all; git reset --hard origin/main; ", shell=True)
        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")
