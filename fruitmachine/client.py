"""A FruitMachine client."""

import collections.abc as abc
import logging
import os.path
import random
import tempfile
from typing import Optional
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
    debug: bool
    _masto: Mastodon

    def __init__(self, debug: bool = False, api_base_url: str = _DEFAULT_API,
                 client_id: Optional[str] = None,
                 client_secret: Optional[str] = None,
                 access_token: Optional[str] = None):
        """Initialise FruitMachine."""
        self.debug = debug
        self._masto = None

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
            api_base_url=api_base_url,
            **masto_auth_params
        )

        self.resources = Resources()
        self.phrase_generator = PhraseGenerator(self.resources.get_statuses())

    def post_fruit_machine(self):
        """Post a fruit machine."""
        fruit_machine = FruitMachine(
            machines=self.resources.get_machines(),
            reels=self.resources.get_reels())

        status_visibility = 'direct' if self.debug else 'public'

        with tempfile.NamedTemporaryFile(mode='w+b') as image:
            (description, machine, reels) = fruit_machine.generate(image)

            # Be kind, rewind!
            image.seek(0)

            # Upload/post image file
            media_data = self._masto.media_post(image,
                                                mime_type='image/png',
                                                description=description)
            logging.info(f"Uploaded image {image.name}: {media_data}")

            # Then post the status with the media file
            status = self.phrase_generator.generate_phrase(machine=machine,
                                                           reels=reels)

            status_data = self._masto.status_post(status,
                                                  media_ids=[media_data],
                                                  visibility=status_visibility)
            logging.info(f"Posted {status_visibility} status: {status_data}")
