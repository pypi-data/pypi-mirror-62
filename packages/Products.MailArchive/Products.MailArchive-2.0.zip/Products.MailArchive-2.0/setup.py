""" MailArchive installer
"""
from os.path import join
from setuptools import setup, find_packages

NAME = 'Products.MailArchive'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description="Browse a mail archive in Unix MBOX format",
      long_description_content_type="text/x-rst",
      long_description=(
          open("README.rst").read() + "\n" +
          open(join("docs", "HISTORY.txt")).read()
      ),
      classifiers=[
           "Framework :: Zope2",
           "Programming Language :: Python",
           "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='eea',
      author='European Environment Agency (EEA)',
      author_email='webadmin@eea.europa.eu',
      url="https://github.com/eea/Products.MailArchive",
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      )
