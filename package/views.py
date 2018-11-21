from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib import messages
from . import models

# Create your views here.

def home(request):
    return render(request, 'package/home.html')

def team(request):
	return render(request, 'package/team.html')

def project(request):
    return render(request, 'package/project.html')

def signup(request):
    if (request.method == 'POST'):
        name = request.POST.get("name")
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        password = request.POST.get('password')
        dbc = models.dbconnection()
        dbc.connect()
        if (dbc.reguser(phone, name, address, city, state, password)==1):
            messages.success(request, "Thank You For Joining!")
            request.session['user_id'] = phone
            dbc.con.commit()
            dbc.close()
            return render(request, 'package/ship.html')
        elif (dbc.reguser(phone, name, address, city, state, password)==0):
            messages.error(request, "Phone Number Already Exists!")
            request.session['user_id'] = "null"
            dbc.con.rollback()
            dbc.close()
            return render(request, 'package/home.html')
        else:
            messages.error(request, "Sign Up Failed, Please Try Again!")
            request.session['user_id'] = "null"
            dbc.con.rollback()
            dbc.close()
            return render(request, 'package/home.html')
        

def track(request):
    return render(request, 'package/track.html')



def ship(request):
    return render(request, 'package/ship.html')


def login(request):
    return render(request, 'package/login.html')
    
def loginauth(request):
    if (request.method == 'POST'):
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        dbc = models.dbconnection()
        dbc.connect()
        if(dbc.auth(phone, password)==0):
            request.session['user_id'] = phone
            messages.success(request, "Login Successful!")
            dbc.close()
            return redirect('/ship')
        elif(dbc.auth(phone, password)==1):
            messages.error(request, "Login Failed, Please Try Again!")
            dbc.close()
            return redirect('/login')
        else:
            messages.error(request, "Account Doesn't Exist, Please Try Again!")
            dbc.close()
            return redirect('/login')

        

def acc(request):
    uid = request.session.get('user_id', 'null')
    print(uid)
    if(uid=='null'):
        return redirect('/login')
    table = {}
    dbc = models.dbconnection()
    dbc.connect()
    res = dbc.table(uid)
    table = {'data': res}
    print(table)
    return render(request, 'package/acc.html', table)

def orders(request):
    uid = request.session.get('user_id', 'null')
    print(uid)
    if(uid=='null'):
        return redirect('/login')
    table = {}
    dbc = models.dbconnection()
    dbc.connect()
    res = dbc.orderstable(uid)
    table = {'data': res}
    print(res)
    print(table)
    return render(request, 'package/orders.html', table)

def logout(request):
    uid = request.session.get('user_id', 'null')
    print(uid)
    if(uid=='null'):
        return redirect('/login')
    del request.session['user_id']
    return redirect('/')
    
def updateaddress(request):
    uid = request.session.get('user_id', 'null')
    print(uid)
    if(uid=='null'):
        return redirect('/login')
    return render(request, 'package/updateaddress.html')

def doupdateaddress(request):
    uid = request.session.get('user_id', 'null')
    print(uid)
    if(uid=='null'):
        return redirect('/login')
    if (request.method == 'POST'):
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        dbc = models.dbconnection()
        dbc.connect()
        if(dbc.updateaddress(address, city, state, uid)==1):
            messages.success(request, "Update Successful!")
            dbc.con.commit()
            dbc.close()
            return redirect('/acc')
        else:
            messages.error(request, "Update Unsuccessful, Please Try Again!")
            dbc.con.rollback()
            dbc.close()
            return redirect('/updateaddress')

        

def addship(request):
    uid = request.session.get('user_id', 'null')
    print(uid)
    if(uid=='null'):
        return redirect('/login')
    if (request.method == 'POST'):
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        city = request.POST.get('city')
        state = request.POST.get('state')
        contents = request.POST.get('contents')
        weight = request.POST.get('weight')
        volume = request.POST.get('volume')
        dbc = models.dbconnection()
        dbc.connect()
        getid = dbc.addship(uid, name, phone, address, city, state, contents, weight, volume)
        if(getid != 1 or getid != 2):
            dbc.con.commit()
            messages.success(request, "Order Successful!")
            getprice = dbc.getprice(getid)
            dbc.close()
            print(getprice)
            id = {}
            id = {'data': getid, 'price': getprice}
            print(id)
            return render(request, 'package/trackerid.html', id)
        else:
            print(getid)
            dbc.con.rollback()
            dbc.close()
            messages.error(request, "Order Failed, Please Try Again!")
            return redirect('/ship')


        

def updatepass(request):
    uid = request.session.get('user_id', 'null')
    print(uid)
    if(uid=='null'):
        return redirect('/login')
    return render(request, 'package/updatepass.html')

def doupdatepass(request):
    uid = request.session.get('user_id', 'null')
    print(uid)
    if(uid=='null'):
        return redirect('/login')
    if (request.method == 'POST'):
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')
        dbc = models.dbconnection()
        dbc.connect()
        if(dbc.auth(uid, oldpass)):
            if(dbc.updatepass(uid, newpass)==1):
                messages.success(request, "Update Successful!")
                dbc.con.commit()
                dbc.close()
                return redirect('/acc')
            elif(dbc.updatepass(uid, newpass)==0):
                messages.error(request, "Account Doesn't Exist, Please Login And Try Again!")
                dbc.con.rollback()
                dbc.close()
                return redirect('/login')
            else:
                messages.error(request, "Update Failed, Please Try Again")
                dbc.con.rollback()
                dbc.close()
                return redirect('/login')
        else:
            messages.error(request, "Wrong Password")
            dbc.close()
            return redirect('/login')

def showtrack(request):
    if(request.method == "POST"):
        trackid = request.POST.get('trackid')
        table = {}
        dbc = models.dbconnection()
        dbc.connect()
        res = dbc.tracktable(trackid)
        info = dbc.recepient_info(trackid)
        table = {'data': res, 'r': info}
        print(res)
        print(info)
        print(table)
        return render(request, 'package/trackid.html', table)

def god(request):
    uid = request.session.get('user_id', 'null')
    if(uid!='null'):
        del request.session['user_id']
    return render(request, 'package/god.html')

def delacc(request):
    uid = request.session.get('user_id', 'null')
    print(uid)
    if(uid=='null'):
        return redirect('/login')
    del request.session['user_id']
    dbc = models.dbconnection()
    dbc.connect()
    if(dbc.delacc(uid)==1):
        messages.success(request, "Account Deletion Successful!")
        dbc.con.commit()
        dbc.close()
        return redirect('/')

    else:
        messages.error(request, "Account Deletion Failed, Please Try Again!")
        dbc.con.rollback()
        dbc.close()
        return redirect('/login')

def vieworders(request):
    table = {}
    dbc = models.dbconnection()
    dbc.connect()
    res = dbc.vieworders()
    table = {'data': res}
    print(res)
    print(table)
    return render(request, 'package/godviewsorders.html', table)

def viewusers(request):
    table = {}
    dbc = models.dbconnection()
    dbc.connect()
    res = dbc.viewusers()
    table = {'data': res}
    print(res)
    print(table)
    return render(request, 'package/godviewspunypeople.html', table)

def delusers(request):
    return render(request, 'package/getdel.html')

def delete(request):
    if(request.method == "POST"):
        phone = request.POST.get('phone')
        print(phone)
        dbc = models.dbconnection()
        dbc.connect()
        if(dbc.delacc(phone)==1):
            messages.success(request, "Account Deletion Successful!")
            dbc.con.commit()
            dbc.close()
            return redirect('/god')

        else:
            messages.error(request, "Account Deletion Failed, Please Try Again!")
            dbc.con.rollback()
            dbc.close()
            return redirect('/yourdead')

def updatestatus(request):
    return render(request, 'package/updatestatus.html')

def doupdatestatus(request):
    if (request.method == 'POST'):
        trackid = request.POST.get('trackid')
        status = request.POST.get('status')
        dbc = models.dbconnection()
        dbc.connect()
        if(dbc.updatestatus(trackid, status)==1):
            messages.success(request, "Update Successful!")
            dbc.con.commit()
            dbc.close()
            return redirect('/god')
        else:
            messages.error(request, "Update Unsuccessful, Please Try Again!")
            dbc.con.rollback()
            dbc.close()
            return redirect('/updatestatus')

    







    
    

