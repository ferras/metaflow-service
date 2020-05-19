from distutils.core import setup
setup(
  name = 'test_metadata_service',         # How you named your package folder (MyLib)
  packages = ['test_metadata_service'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='Apache License 2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
  author = 'Machine Learning Infrastructure Team at Netflix',                   # Type in your name
  author_email = 'help@metaflow.org',      # Type in your E-Mail
  url = 'https://github.com/ferras/metaflow-service',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ferras/metaflow-service/archive/v0.1-alpha.tar.gz',    # I explain this later on
  keywords = ['metaflow', 'machinelearning', 'ml'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'aiohttp',
          'aiohttp_swagger',
          'psycopg2',
          'aiopg',
          'boto3',
          'click',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
  ],
)