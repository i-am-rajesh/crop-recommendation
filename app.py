from flask import Flask, render_template, redirect, jsonify, request, url_for
import pickle
import sklearn
import datetime as dt
date_details = dt.datetime.now()
day = date_details.weekday()
import smtplib

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

# labels
crop_list=["APPLE","BANANA","BLACK GRAM","CHICK PEA","COCONUT","COFFEE",
           "COTTON","GRAPES","JUTE","KIDNEY BEAN","MANGO","MOTHBEAN","MUNGBEAN",
           "MUSKMELON","ORANGE","PAPAYA","PIGEON PEA","PROMOGRANATE","RICE",
           "WATERMELON"]
days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY",
        "FRIDAY", "SATURDAY", "SUNDAY"]


@app.route("/")
def home():
    global day, days
    return render_template("index.html",time=days[day])


@app.route("/Recommand_crop.html",methods=['POST','GET'])
def Recommand_crop():
    global model,crop_list
    b=1
    crop=""
    nitrogen=""
    phosphorus=""
    potassium=""
    temperature=""
    humidity=""
    ph=""
    rainfall=""
    predict=[]
    import numpy as np
    if request.method=='POST':
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        predict = model.predict((np.array([[nitrogen,phosphorus,potassium,temperature,humidity,ph,rainfall]])))
        a=str(predict)
        l=len(a)
        print(a)
        return render_template("Recommand_crop.html",nitrovalue=a[2:l-2],nitrogen=nitrogen,
                           phosphorus=phosphorus,potassium=potassium,temperature=temperature,humidity=humidity,
                           ph=ph,rainfall=rainfall)
        # for _ in a:
        #     if _ == "1":
        #         crop=crop_list[b-9]
        #     else:
        #         b+=1
    else:
        pass
    # for _ in predict:
    return render_template("Recommand_crop.html",nitrogen=nitrogen,
                           phosphorus=phosphorus,potassium=potassium,temperature=temperature,humidity=humidity,
                           ph=ph,rainfall=rainfall)


# @app.route("/contact_us.html",methods=['POST','GET'])
# def contact_us():
# #     my_email = "type your own mail id"
# #     password = "get your own app password"
#     recipient= [""]
#     if request.method=="POST":
#         name = request.form['name']
#         recipient2 = (request.form['email']).lower()
#         message1 = request.form['message']
#         recipient.append(recipient2)
#         for mail in recipient:
#             with smtplib.SMTP("smtp.gmail.com", 587) as connection:
#                 connection.starttls()
#                 connection.login(user=my_email, password=password)
#                 # message to be sent
#                 SUBJECT = f"Thanks for your feedback {name}"
#                 TEXT = message1
#                 message = 'subject: {}\n\n{}'.format(SUBJECT, TEXT)
#                 connection.sendmail(
#                         from_addr=my_email,
#                         to_addrs=mail,
#                         msg=message)
#     else:
#         pass
#     return render_template("contact_us.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)
