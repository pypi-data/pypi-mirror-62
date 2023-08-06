""" Installer
"""
import os
from os.path import join
from setuptools import setup, find_packages

NAME = 'eea.daviz'
PATH = NAME.split('.') + ['version.txt']
VERSION = open(join(*PATH)).read().strip()

setup(name=NAME,
      version=VERSION,
      description=("EEA DaViz is a plone product which uses Exhibit and Google "
                   "Charts API to easily create data visualizations based "
                   "on data from csv/tsv, JSON, SPARQL endpoints and more."
                   ),
      long_description_content_type="text/x-rst",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Zope2",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Zope",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='EEA Add-ons Plone Zope',
      author='European Environment Agency: IDM2 A-Team',
      author_email='eea-edw-a-team-alerts@googlegroups.com',
      url='https://github.com/collective/eea.daviz',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'eea.app.visualization > 11.0',
          'eea.forms >= 5.2',
          'eea.sparql >= 2.4',
          'eea.googlecharts > 16.8',
          'zc.dict',
          'Products.DataGridField',
      ],
      extras_require={
          'full': [
              'eea.relations >= 5.0',
              'eea.cache >= 4.0',
              'eea.depiction >= 5.0',
              ],
          'test': [
              'plone.app.testing',
              ],
          'zope2': [
              'eea.googlecharts [zope2]',
              'eea.app.visualization [zope2]',
          ]
      },

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
