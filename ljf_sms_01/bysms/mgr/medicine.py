from django.http import JsonResponse

import traceback


from  common.models import  Medicine

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q


def listmedicine(request):
    try:

         # return a QuerySet Object, which contains all information
        qs = Medicine.objects.values().order_by('-id')

        # check if there is any keyword for seraching 
        keywords = request.params.get('keywords',None)
        if keywords:
            conditions = [Q(name__contains=one) for one in keywords.split(' ') if one]
            query = Q()
            for condition in conditions:
                query &= condition
            qs = qs.filter(query)

        # pages needed
        pagenum = request.params['pagenum']

        # number of record per page
        pagesize = request.params['pagesize']

        # Use paging objects to set how many records per page
        pgnt = Paginator(qs, pagesize)

        # Read data from the database, specify which page to read
        page = pgnt.page(pagenum)

        # Convert QuerySet object to list type
        retlist = list(page)

        # total, specifies how much data there is
        return JsonResponse({'ret': 0, 'retlist': retlist,'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2,  'msg': f'未知错误\n{traceback.format_exc()}'})


def addmedicine(request):

    info    = request.params['data']

    # Get the information of the medicine to be added from the request message
    # insert into database
    # return id
    medicine = Medicine.objects.create(name=info['name'] ,
                            sn=info['sn'] ,
                            desc=info['desc'])


    return JsonResponse({'ret': 0, 'id':medicine.id})


def modifymedicine(request):

    # Obtain the information to modify the medicine from the request message
    # Find the medicine and modify it

    medicineid = request.params['id']
    newdata    = request.params['newdata']

    try:
        # Find the corresponding record from the database based on id
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{medicineid}`的药品不存在'
        }


    if 'name' in  newdata:
        medicine.name = newdata['name']
    if 'sn' in  newdata:
        medicine.sn = newdata['sn']
    if 'desc' in  newdata:
        medicine.desc = newdata['desc']


    medicine.save()

    return JsonResponse({'ret': 0})


def deletemedicine(request):

    medicineid = request.params['id']

    try:
        # find by id
        medicine = Medicine.objects.get(id=medicineid)
    except Medicine.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{medicineid}`的客户不存在'
        }

    # delete
    medicine.delete()

    return JsonResponse({'ret': 0})



from lib.handler import dispatcherBase

Action2Handler = {
    'list_medicine': listmedicine,
    'add_medicine': addmedicine,
    'modify_medicine': modifymedicine,
    'del_medicine': deletemedicine,
}

def dispatcher(request):
    return dispatcherBase(request, Action2Handler)