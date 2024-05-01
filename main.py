from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('url', validators=[DataRequired(), URL()])
    open_time = TimeField('open_time', validators=[DataRequired()])
    close_time = TimeField('close_time', validators=[DataRequired()])
    coffee_rating = SelectField('coffee_rating',
                                choices=[("☕️", "☕️"), ("☕️☕️", "☕️☕️"), ("☕️☕️☕️", "☕️☕️☕️"), ("☕️☕️☕️☕️", "☕️☕️☕️☕️"),
                                         ("☕️☕️☕️☕️☕️", "☕️☕️☕️☕️☕️")], validators=[DataRequired()])
    wifi_rating = SelectField('wifi_rating',
                              choices=[("✘", "✘"), ("💪", "💪"), ("💪💪️", "💪💪️"), ("💪💪💪", "💪💪💪️"), ("💪💪💪💪", "💪💪💪💪"),
                                       ("💪💪💪💪💪", "💪💪💪💪💪")], validators=[DataRequired()])
    power_rating = SelectField('power_rating',
                               choices=[("✘", "✘"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌"),
                                        ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")], validators=[DataRequired()])
    submit = SubmitField('Submit')


# ---------------------------------------------------------------------------


# flask routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a", encoding='utf-8') as csv_file:
            csv_file.write(f"\n{form.cafe.data},"
                           f"{form.location.data},"
                           f"{form.open_time.data},"
                           f"{form.close_time.data},"
                           f"{form.coffee_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_rating.data}")
        return redirect("cafes")
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open("cafe-data.csv", newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        del list_of_rows[0]
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
