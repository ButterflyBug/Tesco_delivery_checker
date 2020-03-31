import requests
from datetime import date, timedelta
import os
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def get_slots_for_date(url, session):
    response = session.get(
        url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Adrum": "isAjax:true",
            "X-Requested-With": "XMLHttpRequest",
        },
    )

    slots = list(
        filter(lambda item: item["status"] != "UnAvailable", response.json()["slots"])
    )

    return slots


def send_email(email, subject, message_body):
    message = Mail(
        from_email="notifications@grocery.com",
        to_emails=email,
        subject=subject,
        plain_text_content=message_body,
    )
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    sg.send(message)
    return True


def email_address():
    return os.environ.get("EMAIL_NOTIFICATION", "")


def check():
    today = date.today()
    second_period = today + timedelta(days=7)
    third_period = second_period + timedelta(days=7)
    periods = list(
        map(
            lambda item: item.strftime("%Y-%m-%d"), [today, second_period, third_period]
        )
    )

    periods_urls = map(
        lambda item: f"https://ezakupy.tesco.pl/groceries/pl-PL/slots/delivery/{item}?slotGroup=2",
        periods,
    )
    url_login = "https://ezakupy.tesco.pl/groceries/pl-PL/login"

    session = requests.Session()

    response_login_form = session.get(url_login)
    soup = BeautifulSoup(response_login_form.content, features="html.parser")
    csrf_token = soup.find(attrs={"name": "_csrf"}).attrs["value"]

    session.post(
        url_login,
        data={
            "onSuccessUrl": "",
            "email": "",
            "password": "",
            "_csrf": csrf_token,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    period_results = map(lambda url: get_slots_for_date(url, session), periods_urls)
    list_of_slots = []

    for period_result in period_results:
        for slot in period_result:
            list_of_slots.append(slot)

    if len(list_of_slots) > 0:
        send_email(email_address(), "Free slot available", "Free slots")
        return True
    else:
        print("No available slots")
        return False
