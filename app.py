from flask import Flask, render_template
from forms import CourseForm
import smtplib, os
from flask_recaptcha import ReCaptcha


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

MY_EMAIL = "anthonynolletti@gmail.com"
MY_PASSWORD = os.environ['MY_PASSWORD']
app.config['RECAPTCHA_PUBLIC_KEY']= os.environ['RECAPTCHA_PUBLIC_KEY']
app.config['RECAPTCHA_PRIVATE_KEY']= os.environ['RECAPTCHA_PRIVATE_KEY']

ReCaptcha = ReCaptcha()

@app.route('/', methods=('GET', 'POST'))
def index():
    form = CourseForm()
    if form.validate_on_submit() and ReCaptcha.verify():
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
    
    elif not ReCaptcha.verify():

        return render_template("index.html", form=form, scroll="recaptchaError")

   
    return render_template('index.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
   app.run(debug = True)