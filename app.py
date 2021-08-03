from flask import Flask, render_template,request
from scape import *
from data import *
app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/dashboard',methods=["GET","POST"])
def dashboard():
  title = request.form.get('title')
  location = request.form.get('location')
  df = main(title,location)
  data  = final_df(df)
  print(data)
  final  = get_data(data)
  
  return render_template('dashboard.html',title=title,location=location,skills = final[1],data = data,exp=final[-1],pieData=final[0],openings = len(data["Company"]), positions = len(set(data["Title"])))

if __name__ == "__main__":
  app.run(debug=True)
