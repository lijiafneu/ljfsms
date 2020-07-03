from django.http import JsonResponse
from django.db.models import F
from django.db import IntegrityError, transaction


from  common.models import  Order,OrderMedicine

import json,traceback

from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q


def listorder(request):

    try:


        qs = Order.objects \
            .annotate(
                    customer_name=F('customer__name')
            )\
            .values(
            'id', 'name', 'create_date',
            'customer_name',
            'medicinelist'
        ).order_by('-id')

 
        keywords = request.params.get('keywords',None)
        if keywords:
            conditions = [Q(name__contains=one) for one in keywords.split(' ') if one]
            query = Q()
            for condition in conditions:
                query &= condition
            qs = qs.filter(query)



        pagenum = request.params['pagenum']


        pagesize = request.params['pagesize']

  
        pgnt = Paginator(qs, pagesize)


        page = pgnt.page(pagenum)


        retlist = list(page)


        return JsonResponse({'ret': 0, 'retlist': retlist,'total': pgnt.count})

    except EmptyPage:
        return JsonResponse({'ret': 0, 'retlist': [], 'total': 0})

    except:
        return JsonResponse({'ret': 2,  'msg': f'未知错误\n{traceback.format_exc()}'})




def addorder(request):
    info = request.params['data']


    with transaction.atomic():
        medicinelist  = info['medicinelist']

        new_order = Order.objects.create(name=info['name'],
            customer_id=info['customerid'],
            # Write medicine data in json format to the medicinelist field
            medicinelist=json.dumps(medicinelist,ensure_ascii=False),)

        batch = [OrderMedicine(order_id=new_order.id,
                               medicine_id=medicine['id'],
                               amount=medicine['amount'])
                 for medicine in medicinelist]

        OrderMedicine.objects.bulk_create(batch)

    return JsonResponse({'ret': 0, 'id': new_order.id})


def deleteorder(request):

    oid = request.params['id']

    try:

        one = Order.objects.get(id=oid)
        with transaction.atomic():


            OrderMedicine.objects.filter(order_id=oid).delete()

            one.delete()

        return JsonResponse({'ret': 0, 'id': oid})

    except Order.DoesNotExist:
        return JsonResponse({
            'ret': 1,
            'msg': f'id 为`{oid}`的订单不存在'
        })

    except:
        err = traceback.format_exc()
        return JsonResponse({'ret': 1, 'msg': err})


from lib.handler import dispatcherBase

Action2Handler = {
    'list_order': listorder,
    'add_order': addorder,
    'delete_order': deleteorder,
}

def dispatcher(request):
    return  dispatcherBase(request, Action2Handler)