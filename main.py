from flask import Flask
from twilio.rest import Client
from flask import render_template
import requests
import requests_cache
from  flask import request
acct = "ACc257964cb776cb869ee749af9f8285ec"
token  = "3014cf062a1aae2a7536e2ea08a6675a"
client = Client(acct,token)

app = Flask(__name__, static_url_path='/static')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index',methods=['POST','GET'])
def reg():
    fname=request.form['FirstName']
    lname = request.form['LastName']
    mno=request.form['mobile']
    eid=request.form['Emailid']
    state=request.form['cstate']
    source=request.form['source']
    ds=request.form['destination state']
    d=request.form['destination']
    td=request.form['dt']
    rd=request.form['dr']
    fullname=fname+" "+lname
    covid_data=requests.get('https://api.covid19india.org/v4/data.json')
    js=covid_data.json()
    conformed=js[ds]['districts'][d]['total']['confirmed']
    total_pop=js[ds]['districts'][d]['meta']['population']
    epass=((conformed/total_pop)*100)
    if epass<40 and request.method=='POST':
        status='CONFIRMED'
        message = client.messages.create(
            to="+919133947076",
            from_="+14232056030",
            body='Dear'+" "+fullname+"your epass status for travelling to"+" "+ds+" "+d+" "+"is"+" "+status)
        return render_template('epass_status.html',f=fname,l=lname,phno=mno,mail=eid,cs=state,
                               place=source,des_s=ds,destination=d,md=td,cd=rd,es=status)
    else:
        status='REJECTED'
        message = client.messages.create(
            to="+919133947076",
            from_="+14232056030",
            body='Dear' + " " + fullname + "your epass status for travelling to" +" "+ ds + " " + d + "is" + status+
                 " "+"due to more covid cases in destination area")
        return render_template('epass_status.html', f=fname, l=lname, phno=mno, mail=eid, cs=state,
                               place=source, des_s=ds, destination=d, md=td, cd=rd,es=status)




if __name__=='__main__':
    app.run(debug=True)