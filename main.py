import os
import random
from dotenv import load_dotenv, find_dotenv
import smtplib
import datetime as dt
import pandas

load_dotenv(find_dotenv())

MY_EMAIL = os.environ.get("FROM_ADDR")
PASSWORD = os.environ.get("PASSWORD")


data = pandas.read_csv("birthdays.csv")

now = dt.datetime.now()

# -------- Constants ----------#
PLACEHOLDER = "[NAME]"
CHECK_DAY = (data.day == now.day) & (data.month == now.month)

# -------- related birthday -------#
birthday_email = data.loc[CHECK_DAY, 'email'].item()
birthday_name = data.loc[CHECK_DAY, 'name'].item()
is_birthday = CHECK_DAY.any()


if is_birthday:
    random_number = random.randint(1, 4)
    with open(f"./letter_templates/letter_{random_number}.txt") as birthday_letter:
        birthday_letter_content = birthday_letter.read()
        new_birthday_letter = birthday_letter_content.replace(PLACEHOLDER, birthday_name)

    TO_ADDRS = birthday_email

    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=MY_EMAIL, password=PASSWORD)
    connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=TO_ADDRS,
            msg=f"Subject:Happy Birthday\n\n{new_birthday_letter}"
        )
    connection.close()

