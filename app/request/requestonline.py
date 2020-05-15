import requests
import json

#two model versions available v1 and v2
url = 'https://aonu-car-price.herokuapp.com/v1/predict_api' # or url = 'https://aonu-car-price.herokuapp.com/v0/predict'


# sample data
data = {'id':'NG-01',                  #unique car id, (must be string)
       'manufacturer':'Toyota',        # e.g toyota, honda, nissan, etc.. (must be string)
       'mileage':120,                  #mileage in Km (must be number; integer or float)
       'year': 2000,                   #year of make  (must be greater than 1980 and less than or equal to the current year (i.e. 2020 as at present))
       'sec_status': 'nigerian used'}  #must either be one of the following: Nigerian Used, New, Foreign Used (not case sensitive) 

data = json.dumps(data)

results = requests.post(url, data)

print(results.json())


#to run app, use command line and enter the below command in requestonline.py file directory

# python -m requestonline

