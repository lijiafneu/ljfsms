from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q


from common.models import Customer

import traceback

def listcustomers(request):

    try:
        # return a QuerySet Object, which contains all information
        qs = Customer.objects.values().order_by('-id')

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


def addcustomer(request):

    info    = request.params['data']

    # Get the information of the customer to be added from the request message
    # insert into database
    # return id
    record = Customer.objects.create(name=info['name'] ,
                            phonenumber=info['phonenumber'] ,
                            address=info['address'])


    return JsonResponse({'ret': 0, 'id':record.id})


def modifycustomer(request):
    # Obtain the information to modify the customer from the request message
    # Find the customer and modify it

    customerid = request.params['id']
    newdata = request.params['newdata']

    try:
        # Find the corresponding customer record from the database based on id
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return {
            'ret': 1,
            'msg': f'id `{customerid}` does not exist'
        }

    if 'name' in newdata:
        customer.name = newdata['name']
    if 'phonenumber' in newdata:
        customer.phonenumber = newdata['phonenumber']
    if 'address' in newdata:
        customer.address = newdata['address']

    customer.save()

    return JsonResponse({'ret': 0})


def deletecustomer(request):

    customerid = request.params['id']

    try:
        # find by id
        customer = Customer.objects.get(id=customerid)
    except Customer.DoesNotExist:
        return  {
                'ret': 1,
                'msg': f'id 为`{customerid}`的客户不存在'
        }

    # delete
    customer.delete()

    return JsonResponse({'ret': 0})


from lib.handler import dispatcherBase

Action2Handler = {
    'list_customer': listcustomers,
    'add_customer': addcustomer,
    'modify_customer': modifycustomer,
    'del_customer': deletecustomer,
}

def dispatcher(request):
    return dispatcherBase(request, Action2Handler)