from django.http import HttpResponseRedirect

def login_authenticate_middleware(get_response):
    def middleware(request):
        print(request.user)
        response = get_response(request)        
        if response.status_code == 401:
            print(response.status_code)
        return response
    return middleware
        