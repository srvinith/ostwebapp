from django.shortcuts import render,redirect
import pyrebase
import datetime
import pytz
# Create your views here.
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
            uid = user["localId"]  # to get the uid of the authentication
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
    t1 =  asiaTime.strftime("%I:%M:%S %p")
    t2 = asiaTime.strftime("%H:%M:%S")
    hour=int(t2[0:2])
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
    name="NULL"
    profile="NULL"
    try:
        if homedata[uid]:
            for homeid in homedata[uid]:
                for roomid in homedata[uid][homeid]["rooms"]:
                    for productid in homedata[uid][homeid]["rooms"][roomid]["products"]:
                        for deviceid in homedata[uid][homeid]["rooms"][roomid]["products"][productid]["device"]:
                            did=homedata[uid][homeid]["rooms"][roomid]["products"][productid]["device"][deviceid]["id"]
                            did=productid+"_"+deviceid
                            idlist.append(did)
                            namelist.append(homedata[uid][homeid]["rooms"][roomid]["products"][productid]["device"][deviceid]["name"])
                            typelist.append(homedata[uid][homeid]["rooms"][roomid]["products"][productid]["device"][deviceid]["type"])
                # name=homedata[uid][homeid]["name"]                
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
                                    namelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                                    typelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
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
                                    namelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["type"])
                                    typelist.append(homedata[ownerid][homeid]["rooms"][roomid]["products"][productid]["devices"][deviceid]["name"])
                                except:
                                    pass
            name= userdata[uid]["name"]
            try:
                profile= userdata[uid]["photoUrl"]
            except:
                pass                      
    if request.method=="POST":
        pass
    print(name,wish,profile)
    alldevice=zip(idlist,namelist,typelist)
    context={
        "name":name,
        "wish":wish,
        "profile":profile,
        "alldevice":alldevice
    }            
    return render(request,'home.html',context)

def logout(request):
    response = redirect("login")
    response.delete_cookie("uid")
    response.delete_cookie("loginState")
    return response
