from django.shortcuts import render,redirect
import pyrebase
import datetime
import pytz,requests
from django.http import JsonResponse
import json


config = {
  "apiKey": "AIzaSyC2psok5Y20qJvtXjiPZEDQYbGkitdwk0M",
  "authDomain": "smart-things-ab7d2.firebaseapp.com",
  "databaseURL": "https://smart-things-ab7d2-default-rtdb.firebaseio.com",
  "projectId": "smart-things-ab7d2",
  "storageBucket": "smart-things-ab7d2.appspot.com",
  "messagingSenderId": "928008787147",
  "appId": "1:928008787147:web:a4e37aca5a8a4fb186b74e",
  "measurementId": "G-9XGW5SE323"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

def login(request):
    try:
        uid = request.COOKIES["uid"]
        loginState = request.COOKIES["loginState"]
        if bool(loginState) == True:
                response = redirect("home")
                return response
    except:
        pass
    if request.method == "POST":
        try:
            email = request.POST["email"]
            password = request.POST["password"]
            user = auth.sign_in_with_email_and_password(email, password)
            uid = user["localId"]
            exp = 100 * 365 * 24 * 60 * 60
            response = redirect("home")
            response.set_cookie("uid", uid, expires=exp)
            response.set_cookie("loginState", "loggedIn", expires=exp)
            return response
        except:
            context = {"error": "* The name or password you entered is incorrect."}
            return render(request, "login.html", context)
    return render(request, "login.html")


def home(request):
    uid = request.COOKIES["uid"]
    asiaTime = pytz.timezone("Asia/Kolkata")
    asiaTime = datetime.datetime.now(asiaTime)
    t1 = asiaTime.strftime("%H:%M:%S")
    hour=int(t1[0:2])
    wish="Hi"
    if hour >= 1 and hour <= 12:
        wish="Good Morning !"
    elif hour >=12 and  hour <= 15:
        wish="Good Afternoon !"
    elif hour >=15 and hour <= 20:
        wish ="Good Evening !"     
    homedata=db.child("Homes").get().val()
    userdata=db.child("Users").get().val()
    homeidlist=[]
    homenamelist=[]
    name="NULL"
    profile="NULL"

    try:
        
        if homedata[uid]:
            for homeid in homedata[uid]:
                homeidlist.append(homeid)
                homenamelist.append(homedata[uid][homeid]["name"])
        if userdata[uid]:
            for ownerid in userdata[uid]["Access"]:
                for homeid in userdata[uid]["Access"][ownerid]:
                    # for roomid in userdata[uid]["Access"][ownerid][homeid]["rooms"]:
                    #     for productid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"]:
                    #         for deviceid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"][productid]:
                                try:
                                    homename=homedata[ownerid][homeid]["name"]
                                    homeidlist.append(homeid)
                                    homenamelist.append(homename)
                                except:
                                    pass
            name= userdata[uid]["name"]
            try:
                profile= userdata[uid]["photoUrl"]
            except:
                pass    

    except:
        try:
            if userdata[uid]:
                for ownerid in userdata[uid]["Access"]:
                    for homeid in userdata[uid]["Access"][ownerid]:
                        # for roomid in userdata[uid]["Access"][ownerid][homeid]["rooms"]:
                        #     for productid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"]:
                        #         for deviceid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"][productid]:
                                    try:
                                        homename=homedata[ownerid][homeid]["name"]
                                        homeidlist.append(homeid)
                                        homenamelist.append(homename)
                                    except:
                                        pass
                name= userdata[uid]["name"]
                try:
                    profile= userdata[uid]["photoUrl"]
                except:
                    pass
        except:
            pass        

    if request.method=="POST":
        if "devicechange" in request.POST:
            deviceid = request.POST["devicechange"]
            state = request.POST["state"]
    print(homeidlist,homenamelist)
    alldevice=zip(homeidlist,homenamelist)
    context={
        "name":name,
        "wish":wish,
        "profile":profile,
        "alldevice":alldevice,
    }
    return render(request,'home.html',context)

def lightpage(request):
    uid = request.COOKIES["uid"]
    asiaTime = pytz.timezone("Asia/Kolkata")
    asiaTime = datetime.datetime.now(asiaTime)
    t1 = asiaTime.strftime("%H:%M:%S")
    hour=int(t1[0:2])
    wish="Hi"
    if hour >= 1 and hour <= 12:
        wish="Good Morning !"
    elif hour >=12 and  hour <= 15:
        wish="Good Afternoon !"
    elif hour >=15 and hour <= 20:
        wish ="Good Evening !"     
    homedata=db.child("Homes").get().val()
    userdata=db.child("Users").get().val()
    idlist=[]
    namelist=[]
    typelist=[]
    roomwallpaper=[]
    name="NULL"
    profile="NULL"
    if request.method=="POST":
        if 'homeidlight' in request.POST:
            homeidget=request.POST["homeidlight"]
            try:
                if homedata[uid]:
                    for roomid in  homedata[uid][homeidget]["rooms"]:
                        for productid in homedata[uid][homeidget]["rooms"][roomid]["products"]:
                                for deviceid in homedata[uid][homeidget]["rooms"][roomid]["products"][productid]["devices"]:
                                    did=homedata[uid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                                    did=productid+"_"+deviceid
                                    idlist.append(did)
                                    namelist.append(homedata[uid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
                                    typelist.append(homedata[uid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                                    try:
                                        roomwallpaper.append(homedata[uid][homeidget]["rooms"][roomid]['wallpaper'])
                                    except:
                                        roomwallpaper.append("NULL")   

                if userdata[uid]:
                    for ownerid in userdata[uid]["Access"]:
                            for roomid in userdata[uid]["Access"][ownerid][homeidget]["rooms"]:
                                for productid in userdata[uid]["Access"][ownerid][homeidget]["rooms"][roomid]["products"]:
                                    for deviceid in userdata[uid]["Access"][ownerid][homeidget]["rooms"][roomid]["products"][productid]:
                                        try:
                                            id=homedata[ownerid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                                            did=productid+"_"+id
                                            idlist.append(did)
                                            namelist.append(homedata[ownerid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
                                            typelist.append(homedata[ownerid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                                            try:
                                                roomwallpaper.append(homedata[ownerid][homeidget]["rooms"][roomid]['wallpaper'])
                                            except:
                                                roomwallpaper.append("NULL")     
                                        except:
                                            pass
                    name= userdata[uid]["name"]
            except:
                if userdata[uid]:
                    try:
                        for ownerid in userdata[uid]["Access"]:
                                for roomid in userdata[uid]["Access"][ownerid][homeidget]["rooms"]:
                                    for productid in userdata[uid]["Access"][ownerid][homeidget]["rooms"][roomid]["products"]:
                                        for deviceid in userdata[uid]["Access"][ownerid][homeidget]["rooms"][roomid]["products"][productid]:
                                            try:
                                                id=homedata[ownerid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                                                did=productid+"_"+id
                                                idlist.append(did)
                                                namelist.append(homedata[ownerid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
                                                typelist.append(homedata[ownerid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                                                try:
                                                    roomwallpaper.append(homedata[ownerid][homeidget]["rooms"][roomid]['wallpaper'])
                                                except:
                                                    roomwallpaper.append("NULL")
                                            except:
                                                pass
                        name= userdata[uid]["name"]
                    except:
                        pass
            alldevice=zip(idlist,namelist,typelist)
            context={
                "name":name,
                "wish":wish,
                "profile":profile,
                "alldevice":alldevice,
            }
            return render(request,"device.html",context)
        
        if 'roomidlight' in request.POST:
            roomidlight=request.POST["roomidlight"]
            try:
                if homedata[uid]:
                    # for roomid in  homedata[uid][homeidget]["rooms"]:
                        for productid in homedata[uid][homeidget]["rooms"][roomidlight]["products"]:
                                for deviceid in homedata[uid][homeidget]["rooms"][roomidlight]["products"][productid]["devices"]:
                                    did=homedata[uid][homeidget]["rooms"][roomidlight]["products"][productid]["devices"][deviceid]["id"]
                                    did=productid+"_"+deviceid
                                    idlist.append(did)
                                    namelist.append(homedata[uid][homeidget]["rooms"][roomidlight]["products"][productid]["devices"][deviceid]["name"])
                                    typelist.append(homedata[uid][homeidget]["rooms"][roomidlight]["products"][productid]["devices"][deviceid]["type"])
                                    try:
                                        roomwallpaper.append(homedata[uid][homeidget]["rooms"][roomidlight]['wallpaper'])
                                    except:
                                        roomwallpaper.append("NULL")    

                if userdata[uid]:
                    for ownerid in userdata[uid]["Access"]:
                            # for roomid in userdata[uid]["Access"][ownerid][homeidget]["rooms"]:
                                for productid in userdata[uid]["Access"][ownerid][homeidget]["rooms"][roomidlight]["products"]:
                                    for deviceid in userdata[uid]["Access"][ownerid][homeidget]["rooms"][roomidlight]["products"][productid]:
                                        try:
                                            id=homedata[ownerid][homeidget]["rooms"][roomidlight]["products"][productid]["devices"][deviceid]["id"]
                                            did=productid+"_"+id
                                            idlist.append(did)
                                            namelist.append(homedata[ownerid][homeidget]["rooms"][roomidlight]["products"][productid]["devices"][deviceid]["name"])
                                            typelist.append(homedata[ownerid][homeidget]["rooms"][roomidlight]["products"][productid]["devices"][deviceid]["type"])
                                            try:
                                                roomwallpaper.append(homedata[ownerid][homeidget]["rooms"][roomidlight]['wallpaper'])
                                            except:
                                                roomwallpaper.append("NULL")     
                                        except:
                                            pass
                    name= userdata[uid]["name"]
            except:
                if userdata[uid]:
                    try:
                        for ownerid in userdata[uid]["Access"]:
                                # for roomid in userdata[uid]["Access"][ownerid][homeidget]["rooms"]:
                                    for productid in userdata[uid]["Access"][ownerid][homeidget]["rooms"][roomidlight]["products"]:
                                        for deviceid in userdata[uid]["Access"][ownerid][homeidget]["rooms"][roomidlight]["products"][productid]:
                                            try:
                                                id=homedata[ownerid][homeidget]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                                                did=productid+"_"+id
                                                idlist.append(did)
                                                namelist.append(homedata[ownerid][homeidget]["rooms"][roomidlight]["products"][productid]["devices"][deviceid]["name"])
                                                typelist.append(homedata[ownerid][homeidget]["rooms"][roomidlight]["products"][productid]["devices"][deviceid]["type"])
                                                try:
                                                    roomwallpaper.append(homedata[ownerid][homeidget]["rooms"][roomidlight]['wallpaper'])
                                                except:
                                                    roomwallpaper.append("NULL")  
                                            except:
                                                pass
                        name= userdata[uid]["name"]
                    except:
                        pass
            alldevice=zip(idlist,namelist,typelist)
            context={
                "name":name,
                "wish":wish,
                "profile":profile,
                "alldevice":alldevice,
            }
            return render(request,"device.html",context)
    try:
        if homedata[uid]:
            for homeid in homedata[uid]:
                for roomid in homedata[uid][homeid]["rooms"]:
                    for productid in homedata[uid][homeid]["rooms"][roomid]["products"]:
                        for deviceid in homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"]:
                            did=homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                            did=productid+"_"+deviceid
                            idlist.append(did)
                            namelist.append(homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
                            typelist.append(homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                            try:
                                roomwallpaper.append(homedata[uid][homeid]["rooms"][roomid]["wallpaper"])
                            except:
                                roomwallpaper.append("NULL")     
     
        if userdata[uid]:
            for ownerid in userdata[uid]["Access"]:
                for homeid in userdata[uid]["Access"][ownerid]:
                    for roomid in userdata[uid]["Access"][ownerid][homeid]["rooms"]:
                        for productid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"]:
                            for deviceid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"][productid]:
                                try:
                                    id=homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                                    did=productid+"_"+id
                                    idlist.append(did)
                                    namelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
                                    typelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                                    try:
                                        roomwallpaper.append(homedata[ownerid][homeid]["rooms"][roomid]["wallpaper"])
                                    except:
                                        roomwallpaper.append("NULL")
                                except:
                                    pass
            name= userdata[uid]["name"]
            try:
                profile= userdata[uid]["photoUrl"]
            except:
                pass    

    except:
        if userdata[uid]:
            for ownerid in userdata[uid]["Access"]:
                for homeid in userdata[uid]["Access"][ownerid]:
                    for roomid in userdata[uid]["Access"][ownerid][homeid]["rooms"]:
                        for productid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"]:
                            for deviceid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"][productid]:
                                try:
                                    id=homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                                    did=productid+"_"+id
                                    idlist.append(did)
                                    namelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
                                    typelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                                    try:
                                        roomwallpaper.append(homedata[ownerid][homeid]["rooms"][roomid]["wallpaper"])
                                    except:
                                        roomwallpaper.append("NULL")
                                except:
                                    pass
            name= userdata[uid]["name"]
            try:
                profile= userdata[uid]["photoUrl"]
            except:
                pass                      
    # light_id=["3chfb001","3chfb002","3chfb003"]
    # light_state=[1,0,1]    
    # alldevice=zip(light_id,light_state)
    alldevice=zip(idlist,namelist,typelist)
    context={
        "name":name,
        "wish":wish,
        "profile":profile,
        "alldevice":alldevice,
    }
    return render(request,"device.html",context)

def roompage(request):
    uid = request.COOKIES["uid"]
    asiaTime = pytz.timezone("Asia/Kolkata")
    asiaTime = datetime.datetime.now(asiaTime)
    t1 = asiaTime.strftime("%H:%M:%S")
    hour=int(t1[0:2])
    wish="Hi"
    if hour >= 1 and hour <= 12:
        wish="Good Morning !"
    elif hour >=12 and  hour <= 15:
        wish="Good Afternoon !"
    elif hour >=15 and hour <= 20:
        wish ="Good Evening !"     
    homedata=db.child("Homes").get().val()
    userdata=db.child("Users").get().val()
    roomlist=[]
    roomnamelist=[]
    name="NULL"
    profile="NULL"
    try:
        if homedata[uid]:
            for homeid in homedata[uid]:
                for roomid in homedata[uid][homeid]["rooms"]:
                    # for productid in homedata[uid][homeid]["rooms"][roomid]["products"]:
                    #     for deviceid in homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"]:
                    #         did=homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                    #         did=productid+"_"+deviceid
                            roomlist.append(roomid)
                            roomnamelist.append(homedata[uid][homeid]["rooms"][roomid]['name'])
     
        if userdata[uid]:
            for ownerid in userdata[uid]["Access"]:
                for homeid in userdata[uid]["Access"][ownerid]:
                    for roomid in userdata[uid]["Access"][ownerid][homeid]["rooms"]:
                        # for productid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"]:
                        #     for deviceid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"][productid]:
                                # try:
                        #             id=homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                        #             did=productid+"_"+id
                                    roomlist.append(roomid)
                                    roomnamelist.append(homedata[ownerid][homeid]["rooms"][roomid]['name'])
                                    # namelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
                                    # typelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                                # except:
                                #     pass
            name= userdata[uid]["name"]
            try:
                profile= userdata[uid]["photoUrl"]
            except:
                pass    

    except:
        if userdata[uid]:
            for ownerid in userdata[uid]["Access"]:
                for homeid in userdata[uid]["Access"][ownerid]:
                    for roomid in userdata[uid]["Access"][ownerid][homeid]["rooms"]:
                        # for productid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"]:
                        #     for deviceid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"][productid]:
                        #         try:
                                    # id=homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
                                    # did=productid+"_"+id
                                    roomlist.append(roomid)
                                    roomnamelist.append(homedata[ownerid][homeid]["rooms"][roomid]['name'])
                                #     namelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
                                #     typelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                                # except:
                                #     pass
            name= userdata[uid]["name"]
            try:
                profile= userdata[uid]["photoUrl"]
            except:
                pass
    allroomlist=zip(roomlist,roomnamelist)        
    context={
         "name":name,
         "wish":wish,
         "profile":profile,
         "allroomlist":allroomlist
    }
    return render(request,"home.html",context)
def get_state(request):
    if request.method == 'POST':
        homeid = request.POST.get('homeidlight')
        parts = homeid.split('_')
        if len(parts) == 2:
            product_id = parts[0]
            device_id = parts[1]
        else:
            product_id="NULL"
            device_id="NULL"   
        data = requests.get(url=f"http://192.168.1.13:8182/Get_Device_Status/{product_id}/{device_id}").json()
        try:
            data = json.loads(data[0])
            device_value = data.get(device_id)
            device_value = int(device_value)
            state = True if device_value == 1 or device_value is True else False
            data = {
                "light_id": homeid,
                "light_state": state
            }
        except Exception as e:
            data = {
                "light_id": "None",
                "light_state": "None"
            }

        return JsonResponse(data)
def change_state(request):
    print("==============================")
    if request.method == 'POST':
        homeid = request.POST.get('homeidlight')
        parts = homeid.split('_')
        if len(parts) == 2:
            product_id = parts[0]
            device_id = parts[1]
        else:
            product_id="NULL"
            device_id="NULL"  
        print(product_id,device_id)     
        data = requests.get(url=f"http://192.168.1.13:8182/Get_Device_Status/{product_id}/{device_id}").json()
        try:
            data = json.loads(data[0])
            device_value = data.get(device_id)
            device_value = int(device_value)
            state = 0 if device_value == 1 or device_value is True else 1
            print("current state",state)
            data = requests.post(url=f"http://192.168.1.13:8182/Change_device_status/{product_id}/{device_id}/{state}").json()
            state = True if device_value == 1 or device_value is True else False
            data = {
                "light_id": homeid,
                "light_state": state
            }
        except Exception as e:
            data = {
                "light_id": "None",
                "light_state": "None"
            }

        return JsonResponse(data)  
# def home(request):
    # uid = request.COOKIES["uid"]
    # print(uid)
    # asiaTime = pytz.timezone("Asia/Kolkata")
    # asiaTime = datetime.datetime.now(asiaTime)
    # t1 = asiaTime.strftime("%H:%M:%S")
    # hour=int(t1[0:2])
    # wish="Hi"
    # if hour >= 1 and hour <= 12:
    #     wish="Good Morning !"
    # elif hour >=12 and  hour <= 15:
    #     wish="Good Afternoon !"
    # elif hour >=15 and hour <= 20:
    #     wish ="Good Evening !"     
    # homedata=db.child("Homes").get().val()
    # userdata=db.child("Users").get().val()
    # idlist=[]
    # namelist=[]
    # typelist=[]
    # name="NULL"
    # profile="NULL"
    # try:
        
    #     if homedata[uid]:
    #         for homeid in homedata[uid]:
    #             for roomid in homedata[uid][homeid]["rooms"]:
    #                 for productid in homedata[uid][homeid]["rooms"][roomid]["products"]:
    #                     for deviceid in homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"]:
    #                         did=homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
    #                         did=productid+"_"+deviceid
    #                         idlist.append(did)
    #                         namelist.append(homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
    #                         typelist.append(homedata[uid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                     
    #     if userdata[uid]:
    #         for ownerid in userdata[uid]["Access"]:
    #             for homeid in userdata[uid]["Access"][ownerid]:
    #                 for roomid in userdata[uid]["Access"][ownerid][homeid]["rooms"]:
    #                     for productid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"]:
    #                         for deviceid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"][productid]:
    #                             try:
    #                                 id=homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
    #                                 did=productid+"_"+id
    #                                 idlist.append(did)
    #                                 namelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
    #                                 typelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
    #                             except:
    #                                 pass
    #         name= userdata[uid]["name"]
    #         try:
    #             profile= userdata[uid]["photoUrl"]
    #         except:
    #             pass    

    # except:
    #     if userdata[uid]:
    #         for ownerid in userdata[uid]["Access"]:
    #             for homeid in userdata[uid]["Access"][ownerid]:
    #                 for roomid in userdata[uid]["Access"][ownerid][homeid]["rooms"]:
    #                     for productid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"]:
    #                         for deviceid in userdata[uid]["Access"][ownerid][homeid]["rooms"][roomid]["products"][productid]:
    #                             try:
    #                                 id=homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["id"]
    #                                 did=productid+"_"+id
    #                                 idlist.append(did)
    #                                 namelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
    #                                 typelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
    #                             except:
    #                                 pass
    #         name= userdata[uid]["name"]
    #         try:
    #             profile= userdata[uid]["photoUrl"]
    #         except:
    #             pass                      
    # if request.method=="POST":
    #     if "devicechange" in request.POST:
    #         deviceid = request.POST["devicechange"]
    #         state = request.POST["state"]
    # alldevice=zip(idlist,namelist,typelist)
    # context={
    #     "name":name,
    #     "wish":wish,
    #     "profile":profile,
    #     "alldevice":alldevice,
    # }            
    # return render(request,'home.html',context)

# data = requests.get(url=f"http://13.126.197.225:8000/Get_Device_Status/{product_id}/{device_id}").json()
# data = json.loads(data[0])
# device_value = data.get(device_id)
# device_value = int(device_value)
# state = "ON" if device_value == 1 or device_value == "true" else "OFF"

# if device_id == "device4":
#     speed_value=data.get("speed")

#     device_state = {
#         'rangeValue':speed_value,
#         'powerState':state
#     }
# else:
#     device_state = {
#         'powerState': state,
#     }


def logout(request):
    response = redirect("login")
    response.delete_cookie("uid")
    response.delete_cookie("loginState")
    return response