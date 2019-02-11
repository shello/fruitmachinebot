"""A FruitMachine client."""

import logging
import os.path
from typing import BinaryIO, Optional

from mastodon import Mastodon, MastodonError

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

        self.authenticate(api_base_url=api_base_url, client_id=client_id,
                          client_secret=client_secret,
                          access_token=access_token)

    def authenticate(self, api_base_url: str = _DEFAULT_API,
                     client_id: Optional[str] = None,
                     client_secret: Optional[str] = None,
                     access_token: Optional[str] = None):
        """Initialise the authentication of the client."""
        if self._masto:
            raise RuntimeError("Client is already initialised.")

        client_cred_file = os.path.join(_BASEDIR, "data", "client_cred.secret")
        access_token_file = os.path.join(_BASEDIR, "data", "user_cred.secret")

        auth_kwargs = {}

        if client_id and client_secret:
            auth_kwargs['client_id'] = client_id
            auth_kwargs['client_secret'] = client_secret
        elif os.path.isfile(client_cred_file):
            auth_kwargs['client_id'] = client_cred_file

        if access_token:
            auth_kwargs['access_token'] = access_token
        elif os.path.isfile(access_token_file):
            auth_kwargs['access_token'] = access_token_file

        if 'client_id' in auth_kwargs and 'access_token' in auth_kwargs:
            self._masto = Mastodon(
                api_base_url=api_base_url,
                **auth_kwargs)

    def post(self, status: str, media_fp: BinaryIO, media_mime_type: str,
             media_description: str):
        """Send a status post with a media file."""
        if not self._masto:
            raise RuntimeError("Unable to post, client isn't initialised.")

        # Upload/post image file
        try:
            media_data = self._masto.media_post(media_fp,
                                                mime_type=media_mime_type,
                                                description=media_description)
        except MastodonError as e:
            logging.error("Error uploading media.")
            logging.error(e)
            raise RuntimeError("Unable to upload media file.") from e

        if not media_data:
            raise RuntimeError("Empty media dict returned from upload.")

        logging.info(f"Uploaded image: {media_data}")

        # Then post the status with the media file
        status_visibility = 'direct' if self.debug else 'public'

        try:
            status_data = self._masto.status_post(status,
                                                  media_ids=[media_data],
                                                  visibility=status_visibility)
        except MastodonError as e:
            logging.error("Error while posting status.")
            logging.error(e)
            raise RuntimeError("Unable to post status") from e

        if not status_data:
            raise RuntimeError("Empty toot dict returned from posting.")

        logging.info(f"Posted {status_visibility} status: {status_data}")
