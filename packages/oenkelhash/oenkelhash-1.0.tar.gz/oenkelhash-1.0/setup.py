from distutils.core import setup
setup(
  name = 'oenkelhash',         # How you named your package folder (MyLib)
  packages = ['oenkelhash'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Oenkel Hash',   # Give a short description about your library
  author = 'job',                   # Type in your name
  author_email = 'job@vv32.nl',      # Type in your E-Mail
  url = 'https://github.com/jobfeikens/oenkelhash',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jobfeikens/oenkelhash/archive/v1.0.tar.gz',    # I explain this later on
  keywords = ['oenkel', 'hash'],   # Keywords that define your package best
  install_requires=[],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)
