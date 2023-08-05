YTScraper
=========
Scrape available movies from `yts.mx`_ with their respective IMDB score and 720p and 1080p torrent links. Scraped data are dumped inside this folder `Genre`.

.. _yts.mx: https://yts.mx/

Installing
----------
This current version is made up of a **Python Package**, which can be installed with

.. code-block:: bash

	pip install YTScraper

If you want to install it in a virtual environment, just run before installing:

.. code-block:: bash

	pip3 install virtualenv
	virtualenv venv
	source venv/bin/activate

You can leave virtual environment by running:

.. code-block:: bash

	deactivate venv

Getting Started
---------------
For instance, running this command would download every 1080p sci-fi movie and their posters with an IMDb score of 8 or higher, and store them in rating>genre structured subdirectories.

.. code-block:: bash

	sudo ytscraper -q 720p -g action -r 8 -c genre -b

Available Commands
------------------

- `-h` or `--help` (Prints help text. Also prints out all the available optional arguments)
- `-o` or `--output` (Output directory)
- `-b` or `--background` (Append "-b" to download movie posters. This will pack .torrent file and the image together in a folder)
- `-m` or `--multiprocess` (Append -m to download using multiprocessor. This option makes the process significantly faster but is prone to raising flags and causing server to deny requests)
- `-i` or `--imdb-id` (Append -i to append IMDb ID to filename.)
- `-q` or `--quality` (Video quality. Available options are: "all", "720p", "1080p", "3d")
- `-g` or `--genre` (Movie genre. Available options are: "all", "action", "adventure", "animation", "biography", "comedy", "crime", "documentary", "drama", "family", "fantasy", "film-noir", "game-show", "history", "horror", "music", "musical", "mystery", "news", "reality-tv", "romance", "sci-fi", "sport", "talk-show", "thriller", "war", "western")
- `-r` or `--rating` (Minimum rating score. Enter an integer between 0 and 9)
- `-s` or `--sort-by` (Download order. Available options are: "title", "year", "rating", "latest", "peers", "seeds", "download_count", "like_count", "date_added")
- `-c` or `--categorize-by` (Creates a folder structure. Available options are: "rating", "genre", "rating-genre", "genre-rating")
- `-p` or `--page` (Can be used to skip ahead an amount of pages)

License
-------
License stuff is `here`_.

.. _here: https://gist.github.com/0xnu/d11da49c85eeb7272517a9010bbdf1ab

Caution
-------
Don't forget to use a `VPN`_ before running the script. Torrenting is illegal in most countries! Don't get caught!

.. _VPN: https://www.expressrefer.com/refer-friend?referrer_id=15890185&utm_campaign=referrals&utm_medium=copy_link&utm_source=referral_dashboard