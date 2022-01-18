import smtplib
from email.message import EmailMessage


def get_cpu_image():
    cpu_list = [

    ]


def email_users(recipient, user_points):  # TODO

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
        <img src="https://lh3.googleusercontent.com/-PI4eFXKhlMV0sasSV4Bh-N1XDu8eVW50piS9QkbK9uQzqVIYw2Obkh-tbMe-N2KodvmsY2IxzlV-nHAzyHr4i63tvUWi-GOQEQU19cSorEpygE0xzK7_AYdy-vroq94-P04CuUh1xQ2pcyq43zGKCfbHmDQI_UP-QjzfdvsLijKQt2CKNz6ROa04u95nPqlI5UglG3fipAJls75Hf3f2KHAbhzoaRul8Z-jnDlji-FhH9tjl7-EkCWNJAXDJtFQSTdYMvi5n6a4IXl52Rm6xECUNsRKmIO_QrvId7C2apg9mAI1-RAE0Iu0dj3N6hEaHJDoolWlCJPSF9Ij_COupHjhUgyM2tVzi3R_0r1ylvIRpLoE8HVMmHZYYLnhmM_pLtkEmQDCYAbnhvPPUN3LDOArCqB-qNG_ONmXTND-NRyHYsIZ2aGlLvk8OvBFNlXSVhwIncsbcUqeVs9PviRxuTAR9PEcHikgDN_tLSoX61nqB6xmaMTIdEwQSqN9PmzNN4zSpcSVb42SPKbF6tMWaJHJjmFeJrJi-UmfOxSWwQKdYwsWL548no07gHwOqMASqnSD4QsP0eHtlCCwINnhOefuvK00FXVlBKixq5fnknrOADTYX1ohTl-7JUNGYi2ssggBgd1zxvqyF3wXyOkvYOGUGY0b5SOzTnJ2TxPqgsRKaok2FFeoBM434UD8hTssfBL3aXbLJTnz-ewy=w3360-h946-no" alt="WishTrees Logo" width="90%">
        <br><h1 style="color: #c993dc">Here's your point summary</h1>
        <h2 style="color: #c993dc">""" + str(user_points) + """"</h2>
        <br>
        <h1 style="color: #c993dc">How about a random charity to donate to?</h1>
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


user = "marcushuntlypeck@gmail.com"
points = 1000

email_users(user, points)
