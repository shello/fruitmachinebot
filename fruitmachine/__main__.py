"""CLI Interface to FruitMachine."""

from argparse import ArgumentParser
import logging


def main_local(out_filename):
    """CLI for generating Fruit Machines locally."""
    from .resources import Resources
    from .fruitmachine import FruitMachine
    from .phrase_generator import PhraseGenerator

    resources = Resources()
    phrase_generator = PhraseGenerator(resources.get_statuses())

    fruit_machine = FruitMachine(
        machines=resources.get_machines(),
        reels=resources.get_reels())

    with open(out_filename, mode='wb') as out_file:
        description, machine, reels = fruit_machine.generate(out_file)
        status = phrase_generator.generate_phrase(machine=machine, reels=reels)

    print(status)
    print("    Image description:", description)


def main_post(debug=False):
    """CLI for posting a random Fruit Machine to the internet."""
    import os
    from .client import Client

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
    client.post_fruit_machine()


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
