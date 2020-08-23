#!/usr/bin/env python
import random
import requests
import boto3
import click


def get_drink():
    drink_request = requests.get("https://api.punkapi.com/v2/beers/random")
    return drink_request.json()


def generate_email_body(drink, tip, food):
    email_body = f"Your random drink is {drink[0].get('name')}"
    if tip:
        email_body = (
            email_body
            + f"\n\nHere's a tip for your drink! - {drink[0].get('brewers_tips')}"
        )
    if food:
        email_body = (
            email_body
            + f"\n\nHere's some food to go with it - {random.choice(drink[0].get('food_pairing'))}"
        )
    return email_body


def send_email(body):
    sender = ""
    recipient = ""
    subject = "Your drink for the day!"
    charset = "UTF-8"
    client = boto3.client("ses")
    client.send_email(
        Destination={"ToAddresses": [recipient,],},
        Message={
            "Body": {"Text": {"Charset": charset, "Data": body,},},
            "Subject": {"Charset": charset, "Data": subject,},
        },
        Source=sender,
    )
    print("Email sent!")


@click.command()
@click.option("--tip/--no-tip", default=False)
@click.option("--food/--no-food", default=False)
def main(tip, food):
    drink = get_drink()
    body = generate_email_body(drink, tip, food)
    send_email(body)


if __name__ == "__main__":
    main()
