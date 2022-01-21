import smtplib
from email.message import EmailMessage
import random

from flask import render_template, redirect, url_for
from flask_login import current_user


def get_cpu_image():  # TODO return a random CPU image URL
    cpu_list = [  # List of CPU images here
        "https://lh3.googleusercontent.com/pw/AM-JKLW06QsLA3Fjor8GZSFgLV4VpBa8c6iPHgLfY_mTcNMObz-zO38jooA9PXcPvRIoDOyxzvAHL0nupR5JLsb6zWa0RmG0qoVo3UgoauHEgGf8saF2Q5O00F2CiKQPSHspFXMqVOTXN-eSgkotfB-nQg=w338-h451-no",
        "https://lh3.googleusercontent.com/pw/AM-JKLV8kUOmG8C_ngoJpn1VGLgiqI_60oV7P1kA3Ld2Y8GfT7rVn2xlRr-RcBHDaVaf1fQKrtUx3RFzF-5R-eKUCqP2iLd2HfSHynlaHDCaKip3yJW2Wpbv1ApMAWazGfhLYf2BihJdg4x0RTPbWfs-HA=w338-h451-no",
        "https://lh3.googleusercontent.com/pw/AM-JKLWEdTc8alhDpleJnd7160WxRxLZBDlduOILR47fntpKq5KJ9t5Xx8d8SoOvMOAA4LVtrBOegurFLVAq9rDHVJ3gdNxLexhPCC9a1iHfp1hX5TCzkrviI7rQ8GqPOoxZcISMbf6GAFnPwufl6SjMLQ=w338-h451-no"
    ]

    return random.choice(cpu_list)


def email_users(recipient, user_points):

    html_content = ("""
    <!DOCTYPE html>
    <html>

    <head>

    <style>
    img {
      display: block;
      margin-left: auto;
      margin-right: auto;
    }
    </style>

    </head>

    <body style="background-color: #fff8cd;">
        <! WishTrees Logo >
        <img src="https://lh3.googleusercontent.com/pw/AM-JKLW4VYOR4dU9h4JzJsuNtnrqv2mktXIPtxyobM1uqXIrmN_ylHNYbgbmJ4toX0UCJFkomt_8aHYzdbcmVmFQdveCa8s-I5507xo5cjgscqCtV4XnLzWR9HJcfOas2CDmEEuXbzipnUjlMItej0ojzg=w3360-h946-no" alt="WishTrees Logo" width="90%">
        <br><br><h1 style="color: #c993dc; text-align:center">Here's your point summary</h1>
        <h2 style="color: #c993dc; text-align:center">""" + str(user_points) + """</h2>
        <br><br>
        
        <br><h1 style="color: #c993dc; text-align:center">How about a random charity to donate to?</h1>

        <div class="column">
            <img src=' """ + get_cpu_image() + """ ' alt='email_img'>
            <h1 style="color: #c993dc; text-align:center">Charities will always need your help!</h1>            
        </div>
        
        
    </body>
    </html>
    """)

    email_contents = EmailMessage()  # Sets email parameters

    # Login credentials for sender's email
    email_address = "WishTrees.Send@gmail.com"
    email_password = "hykbi5-hucwer-gabzyK"
    # If I had more time the program could
    # get a login token rather then storing
    # the password here

    email_contents['Subject'] = 'Your WishTrees Update is Here!'
    email_contents['From'] = email_address  # Senders email address
    email_contents['To'] = recipient

    # If the user blocks HTML emails this text will show
    email_contents.set_content("Please turn on HTML emails")

    # If HTML are allowed the predefined HTML parameter will show
    email_contents.add_alternative(html_content, subtype='html')

    # Logs into Gmail servers and sends an email with SMTP, Port 465
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(email_contents)

    # return redirect(url_for('profile'))
