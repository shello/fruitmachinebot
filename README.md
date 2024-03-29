Fruit Machine Mastodon Bot
==========================

Source code for the very silly bot deployed at
[@fruitmachine@botsin.space](https://botsin.space/@fruitmachine).

This codebase includes the [Mastodon](https://joinmastodon.org/) client and
["Fruit Machine"](https://en.wikipedia.org/wiki/Slot_machine) image generator
for the aforementioned bot.


Artwork
-------

As configured, the fruit machine symbols are set to use the fabulous
[Mutant Standard](https://mutant.tech/), an alternative emoji set with great
principles, and a highly readable and all around lovely design language.

If you like what you see, please support their work through
[donations](https://mutant.tech/donate/) or get yourself good
[merch](https://mutant.tech/donate/) from them.

Check the official website for the license of the emoji.

Mastodon Client
---------------

The Mastodon client is built for the purpose of this bot, using
[Mastodon.py](https://github.com/halcy/Mastodon.py)
([PyPI](https://pypi.org/project/Mastodon.py/)).


Operation
---------

### Requirements

- Python 3.6.

### Configuration

The bot's behaviour can be configured through `data/resources.json`.

### Usage

#### Local usage

First you need to populate the `resources/emoji/` directory with a structure of
images as generated by [orxporter](https://github.com/mutantstandard/orxporter).
Check the directory's [README](resources/emoji/README.md) for more details.

Then to generate a Fruit Machine locally:

`$ ./bin/fruitmachine -o <path_for_image>`

The standard output will show a status and image description.

#### Posting to Mastodon

To post to Mastodon, you need to set up the client by one of the following ways:

1. Set the `FRUITMACHINE_CLIENT_ID`, `FRUITMACHINE_CLIENT_SECRET` and
   `FRUITMACHINE_ACCESS_TOKEN` environment variables with the values given on
   the Settings > Development > Your application interface of your Mastodon
   instance;
2. Create a file named `.ENV` in the root directory of the project, with the
   same variables as above in the format `variable_name=value`, one per line.
3. Create two text files, `data/client_cred.secret` and `data/user_cred.secret`.
   The first file should have the "Client ID" in the first line, and the "Client
   Secret" in second line; the second file needs to have the "Access Token" in
   the first line.

Then just use:

`$ ./bin/fruitmachine`

and a fruit machine will be posted to the account. You can use the `-D` switch
to print "debug" data, and the post's visibility will be set to `direct`, i.e.,
only the account posting will be able to see it.


License
-------

The code is licensed under an ISC license. Check [`LICENSE`](LICENSE) for
details.

Check [Mutant Standard](https://mutant.tech/)'s homepage for the emoji's
license.

The [Fruit Machine graphics](data/machines/) are licensed under a
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/80x15.png" />Creative Commons Attribution 4.0 International License</a>.
