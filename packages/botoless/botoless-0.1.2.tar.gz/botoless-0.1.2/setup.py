from setuptools import setup, find_packages

try:
    version = open('VERSION').read().strip()
    license = open('LICENSE').read().strip()
except:
    version = "0.1"
    license = "foo"

setup(
    name = 'botoless',
    version = version,
    license = license,
    author = 'Beau Cronin',
    author_email = 'beau.cronin@gmail.com',
    description = 'A smaller view of boto3 intended for serverless application development',
    # long_description = open('README.md').read().strip(),
    long_description = 'A smaller view of boto3 intended for serverless application development',
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/beaucronin/botoless',
    packages = find_packages(),
    install_requires=[
        # put packages here
        'six',
    ],
    # test_suite = 'tests',
    entry_points = {
	    'console_scripts': [
	        'botoless = botoless.__main__:main',
	    ]
	}
)