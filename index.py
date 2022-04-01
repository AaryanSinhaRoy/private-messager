from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from password_generator import PasswordGenerator
import clipboard

app = Flask(__name__)

app.secret_key='private-msgs'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///saver.db'
app.config['SECRET_KEY'] = "boat"
db=SQLAlchemy(app)

pwo=PasswordGenerator()

class msgs(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    themsg=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    linkid=db.Column(db.String(100),nullable=False)



@app.route('/')
def home():
	return render_template("index.html")


@app.route('/newmsg',methods=["GET","POST"])
def newmsg():
	themsg=request.form['themsg']
	password=request.form['password']
	pwo.maxschars=0
	pwo.minlen=10
	linkid=pwo.generate()
	message=msgs(themsg=themsg,password=password,linkid=linkid)
	db.session.add(message)
	db.session.commit()
	linkid="http://localhost:5000/viewmsg/"+linkid
	return render_template("index.html",linkid=linkid)


@app.route('/viewmsg/<linkid>')
def viewmsg(linkid):
	link=linkid
	res=msgs.query.filter_by(linkid=link).all()
	msg=""
	password=""
	if int(len(res))>=1:
		for x in res:
			msg=str(x.themsg)
			password=str(x.password)
		return render_template("showmessage.html",msg=msg,password=password,linkid=linkid)
	else:
		return " the msg is either destroyed or the link is invalid"

@app.route('/deletelink/<linkid>')
def deletelink(linkid):
	linktodel=msgs.query.filter_by(linkid=linkid).all()
	for x in linktodel:
		db.session.delete(x)
	db.session.commit()
	return redirect(url_for("home"))


@app.route('/copytoclipboard/<linkid>')
def copytoclipboard(linkid):
	clipboard.copy(str(linkid))
	return redirect(url_for("home"))


if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)