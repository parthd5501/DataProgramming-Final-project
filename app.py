from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import requests
import pandas as pd
import numpy as np
from datetime import date
from datetime import timedelta
import urllib.parse
import random 

app = Flask(__name__)



# MONGO DB Connection
password = "Parth@5501"
escaped_password = urllib.parse.quote_plus(password)
connection_string = f"mongodb+srv://parth5501:{escaped_password}@cluster0.maso3xe.mongodb.net/"
client = MongoClient(connection_string)
db = client['DataProgramming']
#client = MongoClient("mongodb+srv://parth5501:Parth@5501@cluster0.maso3xe.mongodb.net/",)                    
#db = client.get_database('DataProgramming')
records = db.Currency

# Dates for 2022 (Ref : https://www.w3resource.com/pandas/date_range.php)
y1 = '2022'
M1 = 12 # Month count
begin2022 = pd.date_range(y1, periods=M1, freq='MS').strftime("%Y-%m-%d")
end2022 = pd.date_range(y1, periods=M1, freq='M').strftime("%Y-%m-%d")
begin2022 = begin2022.tolist()
end2022 = end2022.tolist()

# Dates for 2022
y2 = '2023'
M2 = 3 # Month count
begin2023 = pd.date_range(y2, periods=4, freq='MS').strftime("%Y-%m-%d")
end2023 = pd.date_range(y2, periods=M2, freq='M').strftime("%Y-%m-%d")
begin2023 = begin2023.tolist()
end2023 = end2023.tolist()

today = date.today()
# Yesterday date
yesterday = today - timedelta(days = 1)
yes_str = yesterday.strftime("%Y-%m-%d")
yes_lst = list(yes_str.split(" "))

#Combining both lists
start_date = begin2022 + begin2023
end_date = end2022 + end2023 + yes_lst

lineChart_RUB = []
lineChart_USD = []
lineChart_CAD = []
lineChart_GBP = []
lineChart_INR = []
usd = []
rub = []
cad = []
inr = []
eur = []
gbp = []
aed = []
cny = []

symbols = 'USD,RUB,CAD,INR,EUR,GBP,AED,CNY'

res = {start_date[i]: end_date[i] for i in range(len(start_date))}  
#print(str(res))



for start, end in res.items():

    url = "https://api.exchangerate.host/fluctuation?start_date=2020-01-01&end_date=2020-01-04"
    #print(url)
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        #print(data)
        
        #time.sleep(5)
        records.insert_one(data) #inserting data into MongoDB

        #Line Charts
        lineChart_RUB.append(data["rates"]["RUB"]["change"])
        lineChart_USD.append(data["rates"]["USD"]["change"])
        lineChart_CAD.append(data["rates"]["CAD"]["change"])
        lineChart_GBP.append(data["rates"]["GBP"]["change"])
        lineChart_INR.append(data["rates"]["INR"]["change"])

        #Bar Charts
        usd.append(data["rates"]["USD"]["start_rate"])
        cad.append(data["rates"]["CAD"]["start_rate"])
        inr.append(data["rates"]["INR"]["start_rate"])
        rub.append(data["rates"]["RUB"]["start_rate"])
        gbp.append(data["rates"]["GBP"]["start_rate"])
        eur.append(data["rates"]["EUR"]["start_rate"])
        aed.append(data["rates"]["AED"]["start_rate"])
        cny.append(data["rates"]["CNY"]["start_rate"])
    else:
        exit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/lineChart1")
def lineChart1():
    months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22","Jan'22","Feb'22","Mar'22","Apr'22"]
    values = lineChart_RUB
    return render_template('lineChart1.html',labels = months, values = values)

@app.route("/lineChart2")
def lineChart2():
    months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22","Jan'22","Feb'22","Mar'22","Apr'22"]
    values = lineChart_CAD
    return render_template('lineChart2.html',labels = months, values = values)

@app.route("/lineChart3")
def lineChart3():
    months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22","Jan'22","Feb'22","Mar'22","Apr'22"]
    values = lineChart_INR
    return render_template('lineChart3.html',labels = months, values = values)


@app.route("/lineChart Multiple")
def lineChart_M():
    months = ["Jan'22", "Feb'22", "Mar'22", "Apr'22", "May'22", "Jun'22", "Jul'22", "Aug'22", "Sep'22", "Oct'22", "Nov'22", "Dec'22", "Jan'23", "Feb'23", "Mar'23", "Apr'23"]
    num_charts = 3
    chart_data = []

    for _ in range(num_charts):
        chart_values = [random.uniform(0.5, 2) for _ in months]
        chart_data.append(chart_values)

    return render_template('lineChartMultiple.html', labels=months, chart_data=chart_data)


#@app.route("/lineChart_Multiple")
#def lineChart_M():
 #   months = ["Jan'22", "Feb'22", "Mar'22", "Apr'22", "May'22", "Jun'22", "Jul'22", "Aug'22", "Sep'22", "Oct'22", "Nov'22", "Dec'22", "Jan'23", "Feb'23", "Mar'23", "Apr'23"]
  #  values1 = lineChart_RUB
   # values2 = lineChart_CAD
    #values3 = lineChart_INR

    #return render_template('lineChart Multiple.html', labels=months, values1=values1, values2=values2, values3=values3)


#@app.route("/lineChart Multiple")
#def lineChart_M():
    #months = ["Jan'22","Feb'22","Mar'22","Apr'22","May'22","Jun'22","Jul'22","Aug'22","Sep'22","Oct'22","Nov'22","Dec'22","Jan'22","Feb'22","Mar'22","Apr'22"]
    #values1 = lineChart_RUB
    #values2 = lineChart_CAD
    #values3 = lineChart_INR

    #return render_template('lineChart Multiple.html',labels = months, values1 = values1, values2 = values2, values3 = values3)

Bar_Values = [np.average(usd), np.average(cad), np.average(aed), np.average(gbp),np.average(cny),np.average(eur)]
@app.route("/BarChart")
def BarChart():
    labels = ["USD", "CAD", "AED", "GBP", "CNY", "EUR"]
    values = Bar_Values
    return render_template('BarChart.html', labels=labels, values=values)


if __name__ == "__main__":
    app.debug = False
    app.run()
