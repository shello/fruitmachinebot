"""A FruitMachine client."""

import collections.abc as abc
import logging
import os.path
import random
import tempfile
from datetime import date

from .fruitmachine import FruitMachine
from .resources import Resources
from .phrase_generator import PhraseGenerator

from mastodon import Mastodon

_DEFAULT_API = 'https://botsin.space'

_BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class Client:
    """FruitMachine client."""

    client_name = 'Fruit Machine Bot'
    api_base_url: str
    client_cred: str
    access_token: str
    _masto: Mastodon

    def __init__(self, api_base_url=_DEFAULT_API, debug=False,
                 client_id=None, client_secret=None, access_token=None):
        """Initialise FruitMachine."""
        self.debug = debug
        self._masto = None
        self.api_base_url = api_base_url

        client_cred_file = os.path.join(_BASEDIR, "data", "client_cred.secret")
        access_token_file = os.path.join(_BASEDIR, "data", "user_cred.secret")

        masto_auth_params = {}

        if client_id and client_secret:
            masto_auth_params['client_id'] = client_id
            masto_auth_params['client_secret'] = client_secret
        elif os.path.isfile(client_cred_file):
            masto_auth_params['client_id'] = client_cred_file
        else:
            raise RuntimeError("Client ID file or client_id and client_secret"
                               "parameters missing.")

        if access_token:
            masto_auth_params['access_token'] = access_token
        elif os.path.isfile(access_token_file):
            masto_auth_params['access_token'] = access_token_file
        else:
            raise RuntimeError("Access token not provided and file not found.")

        self._masto = Mastodon(
            **masto_auth_params,
            api_base_url=self.api_base_url
        )

        self.resources = Resources()
        self.phrase_generator = PhraseGenerator(self.resources.get_statuses())

    def get_random_status(self, machine, reels):
        """Get a random status."""
        phrase = random.choice(self.resources.get_statuses())

        if isinstance(phrase, abc.Iterable) and not isinstance(phrase, str):
            phrase = ' '.join(random.choice(s) for s in phrase)

        payline = tuple(r[1].description for r in reels)
        outside_payline = [r[0].description for r in reels] \
            + [r[2].description for r in reels]

        params = {
            'machine': machine.description,
            'payline': payline,
            'random_payline': random.choice(payline),
            'outside_payline': outside_payline,
            'random_outside_payline': random.choice(outside_payline),
            'month': format(date.today(), "%B"),
            'weekday': format(date.today(), "%A")
        }

        return phrase.format(**params)

    def post_fruit_machine(self):
        """Post a fruit machine."""
        fruit_machine = FruitMachine(
            machines=self.resources.get_machines(),
            reels=self.resources.get_reels())

        status_visibility = 'private' if self.debug else 'public'

        with tempfile.NamedTemporaryFile(mode='w+b') as image:
            (description, machine, reels) = fruit_machine.generate(image)

            # Be kind, rewind!
            image.seek(0)

            media_data = self._masto.media_post(image,
                                                mime_type='image/png',
                                                description=description)
            logging.info(f"Uploaded image {image.name}: {media_data}")

            status = self.phrase_generator.generate_phrase(machine=machine,
                                                           reels=reels)

            status_data = self._masto.status_post(status,
                                                  media_ids=[media_data],
                                                  visibility=status_visibility)
            logging.info(f"Posted {status_visibility} status: {status_data}")
