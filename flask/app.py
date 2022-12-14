from flask import Flask, render_template, request
import mysql.connector, datetime


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')




@app.route("/result", methods=["POST"])
def result():
    webhook_url = request.form["webhook_url"]
    Cname = request.form["Cname"]
    Cid = request.form["Cid"]
    token = request.form["token"]
    user = request.form["user"]
    sub_date = str(datetime.datetime.today())

    db=mysql.connector.connect(host="mysql", user="root", password="root", database="slack")
    cursor=db.cursor()
#    cursor.execute("USE slack")
#    db.commit()

   # sql = "INSERT slack values 0 webhook_url = %s Cname = %s Cid = %s token = %s user = %s"
   # cursor.execute(sql, (webhook_url, Cname, Cid, token, user))
   # cursor.execute("INSERT slack values (0, 'webweb','tokentoken','channelchannnel','useruser');")
    cursor.execute("INSERT INTO slack VALUES (%s, %s, %s, %s, %s, %s, %s)", (0 ,webhook_url, Cname, Cid, token, user, sub_date))
    db.commit()



    return render_template("form.html", webhook_url = webhook_url, Cid = Cid, token = token, user = user, Cname = Cname)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
