from flask import Flask, render_template, redirect, url_for, request, abort
from forms import CourseForm
import smtplib, os
import requests



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

MY_EMAIL = "anthonynolletti@gmail.com"
MY_PASSWORD = os.environ['MY_PASSWORD']
VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

app.config['RECAPTCHA_PUBLIC_KEY']= os.environ['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY']= os.environ['RECAPTCHA_PRIVATE_KEY']

RECAPTCHA_PUBLIC_KEY= os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY= os.environ['RECAPTCHA_PRIVATE_KEY']

@app.route('/', methods=('GET', 'POST'))
def index():
    form = CourseForm()

    if request.method == 'POST':
        secret_response = request.form['g-recaptcha-response']

        verify_response = requests.post(url=f'{VERIFY_URL}?secret={RECAPTCHA_PRIVATE_KEY}&response={secret_response}').json()

        if verify_response['success'] == False:
            return render_template('invalid.html', form=form)


        sender_name = form.name.data
        sender_email = form.email.data
        message = form.message.data

        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=[MY_EMAIL, sender_email],
                 msg=f"Subject:{sender_name}'s Inquiry\n\nHello {sender_name}, \n\nBelow is the inquiry you submitted on my site:\n\n*****************************\n\n{message}\n\n*****************************\n\nI will get back to you shortly! \n\nSincerely,\n\nAnthony"
        )

        return render_template("success.html", sender_name=sender_name, sender_email=sender_email, message=message)
    
    return render_template('index.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
   app.run(debug = True)