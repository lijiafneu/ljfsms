from django.db import models
import datetime

class Customer(models.Model):
    # Customer name
    name = models.CharField(max_length=200)

    # phone
    phonenumber = models.CharField(max_length=200)

    # address
    address = models.CharField(max_length=200)



class Medicine(models.Model):
    # med name
    name = models.CharField(max_length=200)
    # med number
    sn = models.CharField(max_length=200)
    # discription
    desc = models.CharField(max_length=200)




class Order(models.Model):
    # order name
    name = models.CharField(max_length=200,null=True,blank=True)

    # create date
    create_date = models.DateTimeField(default=datetime.datetime.now)

    # customer 
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)


    # many-to-many relationship with medicines of order
    medicines = models.ManyToManyField(Medicine, through='OrderMedicine')

    # to enhance efficiency, store Redundant data here
    medicinelist =  models.CharField(max_length=2000,null=True,blank=True)


class OrderMedicine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    medicine = models.ForeignKey(Medicine, on_delete=models.PROTECT)

    # amount in order
    amount = models.PositiveIntegerField()



from django.contrib import admin
admin.site.register(Customer)
