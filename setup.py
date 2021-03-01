from setuptools import setup

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setup(
    name='HotpepperScrape',
    version='1.1',
    packages=[''],
    url='https://github.com/YutaUtah/Hotpepper_Scraping.git',
    license='',
    author='Yuta Hayashi',
    author_email='yuta.hayashi96@gmail.com',
    description='Scrape Hotpepper',
    install_requires=_requires_from_file('requirements.txt'),
)
