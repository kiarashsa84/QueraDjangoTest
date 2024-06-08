from .models import Employee, Product, Company, Order, Customer
from django.db.models import Avg
from django.db.models import Sum
from datetime import datetime

def young_employees(job_S: str):
    epm = Employee.objects.filter(job = job_S , age__lt = 30)
    return epm


def cheap_products():
    
    pr = Product.objects.all()

    avg = pr.aggregate(avg_price = Avg("price"))
    avg_= avg.get('avg_price')
    


    ltpr = Product.objects.filter(price__lt = avg_).order_by("price")
    listnames = []; 
    for i in ltpr : 
        listnames.append(i.name)

    return listnames 


def products_sold_by_companies():
    
    company = Company.objects.annotate(total_sold = Sum("product__sold"))
    company = company.values('name', 'total_sold')
    
    company_list = []
    for cmp in company: 
        company_list.append((cmp['name'], cmp['total_sold']))

    return company_list


def sum_of_income(start_date: str, end_date: str):

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    sumOfDaramad = Order.objects.filter(time__range =   [start_date, end_date]).aggregate(sumOfDaramad =  Sum("price"))
    # total_price = Order.objects.filter(time__range=[start_date, end_date]).aggregate(total_price=Sum('price'))
    # return total_price['total_price'] 

    return sumOfDaramad['sumOfDaramad']

    

    # if isinstance(start_date, str):
    #     start_date = datetime.strptime(start_date, '%Y-%m-%d')
    # if isinstance(end_date, str):
    #     end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # total_price = Order.objects.filter(time__range=[start_date, end_date]).aggregate(total_price=Sum('price'))

    # return total_price['total_price'] if total_price['total_price'] else 0

def good_customers():

    customers = Customer.objects.all()

    lis_cus = []; 

    for cus in customers: 
        if (cus.order_set.count() > 1 and cus.level == 'G'): 
            name = cus.name
            print("I'm here")
            print(name)
            phone = cus.phone
            print(phone)
            lis_cus.append((name, phone))

    
    return lis_cus
            


    
    


def nonprofitable_companies():
    company = Company.objects.all()
    lis_com = []

    for com in company: 
        cnt  = 0; 
        for cmp in com.product_set.all() : 
            if (cmp.sold < 100):                 
                cnt += 1

        if (cnt >= 4 ):
            lis_com.append(com.name)

    
    return lis_com