#!/usr/bin/python3
"""
Main script.
"""
import logging
from logging.handlers import RotatingFileHandler
import smtplib
from email.mime.text import MIMEText
from api import get_direct, get_all
from storage import Storage
from settings_local import CONF


def main():
    # Setup log.
    logger = logging.getLogger("bostad")
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    handler = RotatingFileHandler("bostad.log",
                maxBytes=1024*100, backupCount=3)
    handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # Setup storage
    storage = Storage.create_or_open("housing.db")

    logger.info("--- START ---")
    result = get_direct()
    logger.info("Retrieved {0} housings".format(len(result)))
    if result:
        body = ""
        for housing in result:
            if not storage.has_address(housing.address):
                logger.info("Address {0} not previously seen".format(housing.address))
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
            logger.info("Connecting to SMTP server")
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.starttls()
            smtp_server.login(CONF["AUTH_USER"], CONF["AUTH_PWD"])
            smtp_server.send_message(msg)
            smtp_server.quit()

            # Commit storage and log
            storage.commit()
            logger.info("Message sent")
        except Exception as exc:
            logger.error("Unhandled exception: {0}".format(exc))
    logger.info("--- END ---")


if __name__ == '__main__':
    main()
