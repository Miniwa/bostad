#!/usr/bin/python3
"""
Main script.
"""
import smtplib
from email.mime.text import MIMEText
from api import get_direct, get_all
from storage import Storage
from settings_local import CONF


def main():
    storage = Storage.create_or_open("housing.db")
    result = get_direct()

    if result:
        body = ""
        for housing in result:
            if not storage.has_address(housing.address):
                body += housing.address
                body += "\nHyra: {0}kr".format(housing.rent)
                body += "\nURL: {0}\n\n".format(housing.url)
                storage.insert_address(housing.address)

        # Cancel if all housings were already registered
        if not body:
            return

        # Create message
        msg = MIMEText(body)
        msg["Subject"] = CONF["SUBJECT"]
        msg["From"] = CONF["FROM"]
        msg["To"] = CONF["TO"]

        try:
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.starttls()
            smtp_server.login(CONF["AUTH_USER"], CONF["AUTH_PWD"])
            smtp_server.send_message(msg)
            smtp_server.quit()
        except Exception as exc:
            print(exc)


if __name__ == '__main__':
    main()
