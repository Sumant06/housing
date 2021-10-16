from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

import pandas as pd
from sklearn.model_selection import train_test_split
from .models import HousingData
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder


# Create your views here.
def Home(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        # v = DoctorReg.objects.all()
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return render(request, 'data.html')
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already exist')
                return render(request,'register.html')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already exist')
                return render(request,'register.html')
            else:

                #save data in db
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save();
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'register.html')
        return redirect('/')
    else:
        return render(request, 'register.html')

def predict(request):
    if (request.method == 'POST'):
        area = request.POST['area']
        bhk = request.POST['bhk']
        parking = request.POST['parking']
        furnishing = request.POST['furnishing']
        transaction = request.POST['transaction']


        df = pd.read_csv(r"static/dataset/Housing.csv")
        df.dropna(inplace=True)
        df.isnull().sum()
        #Area,BHK,Parking,Furnish,
        #Area,BHK,Bathroom,Furnishing,Locality,Parking,Price,Status,Transaction,Type,Per_Sqft
        z=df.drop(["Furnishing","Locality","Transaction","Type","Per_Sqft"],axis=1)
        l=LabelEncoder()
        f=l.fit_transform(df["Furnishing"])
        t=l.fit_transform(df["Transaction"])
        z["Furnish"]=f
        z["Transaction"]=t
        X_train=z[['Area', 'BHK', 'Parking', 'Furnish', 'Transaction']]
        y_train=z[["Price"]]

        ran = LinearRegression()
        ran.fit(X_train, y_train)
        prediction = ran.predict([[area,bhk,parking,furnishing,transaction]])
        #housing=HousingData.objects.create(area=area,bhk=bhk,parking=parking,furnishing=furnishing,transaction=transaction)
        #housing.save()
        print("Predicted Value of House Prediction: ",prediction)

        return render(request, 'predict.html',
                      {"data": prediction, 'Area': area,  'BHK': bhk,
                       'Parking': parking, 'Furnishing': furnishing,"Transaction":transaction
                       })


    else:
        return render(request, 'predict.html')




