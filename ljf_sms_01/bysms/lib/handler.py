from django.http import JsonResponse
import json


def dispatcherBase(request,action2HandlerTable):
    # jundge authentication by session
    if 'usertype' not in request.session:
        return JsonResponse({
            'ret': 302,
            'msg': '未登录',
            'redirect': '/mgr/sign.html'},
            status=302)

    if request.session['usertype'] != 'mgr':
        return JsonResponse({
            'ret': 302,
            'msg': '用户非mgr类型',
            'redirect': '/mgr/sign.html'},
            status=302)


    # Put the request parameters into the params attribute of the request, to facilitate subsequent processing

    
    if request.method == 'GET':
        request.params = request.GET

    # POST/PUT/DELETE request parameters are obtained from the body property of the request object
    elif request.method in ['POST','PUT','DELETE']:
        # According to the interface, the message body of POST/PUT/DELETE request is in json format
        request.params = json.loads(request.body)


    # Distribute to different functions for processing according to different actions
    action = request.params['action']
    if action in action2HandlerTable:
        handlerFunc = action2HandlerTable[action]
        return handlerFunc(request)

    else:
        return JsonResponse({'ret': 1, 'msg': 'action参数错误'})