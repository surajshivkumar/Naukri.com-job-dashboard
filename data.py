from scape import *
import numpy as np
import json
import pandas as pd
from collections import Counter

def get_salaries(salaries):
  sals = salaries.ravel().tolist()
  sals = [float(i) for i in sals]
  # salaries ={"Salaries":sals}
  # salaries = [salaries]
  df = pd.DataFrame({"Salary":sals})
  df.to_csv('./static/salary.csv',index=False) 
  # out_file = open("salary.json", "w") 
  # json.dump(salaries, out_file, indent = 6) 
  #return salaries.ravel().tolist()

def get_exp(exp):
  experience =  exp.ravel().tolist()
  experience = [float(i) for i in experience]
  return experience

def date(day):
  latest ={"Latest":0,"This_week":0,"Older_than_a_week":0}
  for i in day:
    if i<=2:
        latest["Latest"]+=1
    elif i<=8 and i>2:
        latest["This_week"]+=1
    else:
        latest["Older_than_a_week"]+=1
  latest = {"labels":list(latest.keys()),"values":list(latest.values())}
  return latest

def get_skills(data):
  data = dict(Counter(data))
  g = []
  for i in data.items():
    g.append({'name':i[0],'value':i[1]})
  return g

def get_data(data):
  salaries = get_salaries(data["Salary"])
  date_posted = date(data["Date"])
  skills = get_skills(data["Requirements"])
  exp = get_exp(data["Experience"])

  return [date_posted,skills,exp]
