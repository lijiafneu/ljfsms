from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout


# Login processing
def signin(request):
    # Get username and password parameters from HTTP POST request
    userName = request.POST.get('username')
    passWord = request.POST.get('password')

    # Use the methods in the Django auth library to verify the username and password
    user = authenticate(username=userName, password=passWord)

    # If the user can be found and the password is correct
    if user is not None:
        if user.is_active:
            if user.is_superuser:
                login(request, user)
                # Store user type in session
                request.session['usertype'] = 'mgr'

                return JsonResponse({'ret': 0})
            else:
                return JsonResponse({'ret': 1, 'msg': '请使用管理员账户登录'})
        else:
            return JsonResponse({'ret': 0, 'msg': '用户已经被禁用'})

    # Otherwise, the user name and password are incorrect
    else:
        return JsonResponse({'ret': 1, 'msg': '用户名或者密码错误'})


# Logout processing
def signout(request):
    # Use logout method
    logout(request)
    return JsonResponse({'ret': 0})