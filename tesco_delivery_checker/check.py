"""
.. include:: ../README.md
"""
import requests
from datetime import datetime, timezone, timedelta
import os
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def get_slots_for_date(url, session):
    """
    Provides with a list of available slots so that booking of groceries' delivery
    is possible on a specified day.

    Parameters
    -----------
    url : string
        URL of the slot endpoint
    session : requests.Session
        Instance of Session class to preserve cookie between requests

    Returns
    --------
    slots : list
        List of available slots filtered from the list of all slots approachable on the endpoint

    Examples
    ---------
        >>> get_slots_for_date(
              "https://ezakupy.tesco.pl/groceries/pl-PL/slots/delivery/2020-05-13?slotGroup=2",
              session
            )
    """
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
    """
    Sends an email to address passed as first parameter.
    The message is delivered using SendGrid service. It requires API key determined
    under `SENDGRID_API_KEY` environment variable for successful email's delivery.

    Parameters
    ------------
    email : string
        Recepient's address email
    subject : string
        Subject of message
    message_body : string
        Content of message

    Returns
    -----------
    is_delivered : Boolean

    Examples
    ---------
    >>> send_email(
          "notification@notify.com",
          "Free slots available",
          "Free slots"
        )
    True
    """
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
    """
    Returns a value of the environment variable `EMAIL_NOTIFICATION`
    that indicates the email address which the notification should be sent to.
    However, if this variable is not set,  its value will be an empty string.

    Returns
    ------------
    string
        Value of `EMAIL_NOTIFICATION` or `""`
    """

    return os.environ.get("EMAIL_NOTIFICATION", "")


def check():
    """
    Function examines whether there is at least one available slot on Tesco's website
    and in case of success the value `True` is returned. Except for that the function `send_email()`
    is called so that the notification with desired information about free slots is sent.
    If there are no available slots `False` is returned.

    Returns
    --------
    Boolean
        True if slots are available, otherwise False
    """
    today = datetime.now(timezone(timedelta(hours=2)))
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
            "email": os.environ.get("TESCO_EMAIL", ""),
            "password": os.environ.get("TESCO_PASSWORD", ""),
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
        send_email(
            email_address(), "Free slot available", f"Free slots {len(list_of_slots)}"
        )
        print("Free slot available. ", len(list_of_slots))
        return True
    else:
        print("No available slots")
        return False
