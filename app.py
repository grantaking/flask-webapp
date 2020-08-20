# app.py
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///schools'
db = SQLAlchemy(app)

db.Model.metadata.reflect(db.engine)

class School(db.Model):
    __tablename__ = 'schools-geocoded'
    __table_args__ = {'extend_existing': True}
    LOC_CODE = db.Column(db.Text, primary_key=True)

@app.route("/")
def index():
    school_count = School.query.count()
    schools = School.query.all()
    return render_template("list.html", count=school_count, schools=schools, location="New York City")

@app.route('/city/')
def city_list():
    # Get the unique city values from the database
    cities = School.query.with_entities(School.City).distinct().all()
    # They're in a weird list of one-element lists
    # So we'll take them out of that, also making all title case
    cities = [city[0].title() for city in cities]
    #deduping New York
    cities = sorted(list(set(cities)))
    return render_template("cities.html", cities=cities)

@app.route('/city/<cityname>')
def city(cityname):
    cityname=cityname.replace("-", " ")
    schools = School.query.filter_by(City=cityname.upper()).all()
    return render_template("list.html", schools=schools, count=len(schools), location=cityname)

@app.route('/zip/')
def zip_list():
    #Get the unique zip values from the database
    zips = School.query.with_entities(School.ZIP).distinct().all()
    zips = [zip[0] for zip in zips]
    zips = sorted(list(set(zips)))
    return render_template("zips.html", zips=zips)

@app.route('/zip/<zipcode>')
def zip(zipcode):
    schools = School.query.filter_by(ZIP=zipcode).all()
    return render_template("list.html", schools=schools, count=len(schools), location=zipcode)

@app.route('/schools/<slug>')
def detail(slug):
    school = School.query.filter_by(LOC_CODE=slug).first()
    return render_template("detail.html", school=school)


if __name__ == '__main__':
    app.run(debug=True)