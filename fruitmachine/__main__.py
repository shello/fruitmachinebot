"""CLI Interface to FruitMachine."""

from argparse import ArgumentParser
import logging


def main_local(out_filename: str):
    """CLI for generating Fruit Machines locally."""
    from fruitmachine.fruitmachine import FruitMachine

    fruit_machine = FruitMachine()

    with open(out_filename, mode='wb') as out_file:
        description, status, jackpot = fruit_machine.generate(out_file)

    print(status)
    print("    Image description:", description)
    if jackpot:
        print("    Jackpot!!")


def main_post(debug: bool = False):
    """CLI for posting a random Fruit Machine to the internet."""
    import os
    import tempfile

    from fruitmachine.fruitmachine import FruitMachine
    from fruitmachine.client import Client

    # Set up the client
    env_client_id = os.getenv('FRUITMACHINE_CLIENT_ID')
    env_client_secret = os.getenv('FRUITMACHINE_CLIENT_SECRET')
    env_access_token = os.getenv('FRUITMACHINE_ACCESS_TOKEN')

    auth_params = {}

    if env_client_id and env_client_secret:
        auth_params['client_id'] = env_client_id
        auth_params['client_secret'] = env_client_secret

    if env_access_token:
        auth_params['access_token'] = env_access_token

    client = Client(debug=debug, **auth_params)

    # Let's spin!
    fruit_machine = FruitMachine()

    with tempfile.NamedTemporaryFile(mode='w+b') as image:
        (description, status, jackpot) = fruit_machine.generate(image)

        # Be kind, rewind!
        image.seek(0)

        client.post(status=status, media_fp=image, media_mime_type="image/png",
                    media_description=description, bookmark=jackpot)


def main():
    """Main CLI function."""
    parser = ArgumentParser(description="Generate Fruit Machines.")
    parser.add_argument("-o", "--out", dest="out_filename",
                        help="output the image to FILE", metavar="FILE")
    parser.add_argument("-D", "--debug", dest="debug", action='store_true',
                        default=False, help="Run as debug.")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level="INFO")

    if args.out_filename:
        main_local(args.out_filename)
    else:
        main_post(debug=args.debug)


main()
