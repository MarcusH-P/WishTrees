import smtplib
from email.message import EmailMessage


def email_users(recipient_list):  # TODO

    html_content = ("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1>Head</h1>
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
    email_contents['To'] = ", ".join(recipient_list)  # Makes list into str spaced with ", "

    # If the user blocks HTML emails this text will show
    email_contents.set_content("Please turn on HTML emails")

    # If HTML are allowed the predefined HTML parameter will show
    email_contents.add_alternative(html_content, subtype='html')

    # Logs into Gmail servers and sends an email with SMTP, Port 465
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(email_contents)


user_list = ["wishtrees.contact@gmail.com"]

email_users(user_list)
