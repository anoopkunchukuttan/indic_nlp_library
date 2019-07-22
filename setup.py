#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# (C) 2019 Ezhil Language Foundation,
# copied from open-tamil project

from distutils.core import setup
from codecs import open

setup(name='Indic-NLP',
      version='0.5',
      description='The goal of the Indic NLP Library is to build Python based libraries for common'\
      ' text processing and Natural Language Processing in Indian languages.',
      author='Anoop Kunchukuttan',
      author_email='anoop.kunchukuttan@gmail.com',
      url='https://github.com/anoopkunchukuttan/indic_nlp_library',
      packages=['indicnlp','indicnlp.morph','indicnlp.normalize','indicnlp.script',
      'indicnlp.syllable','indicnlp.tokenize','indicnlp.transliterate'],
      package_dir={'indicnlp': 'src/indicnlp'},
      license='GPLv3',
      scripts=[],
      platforms='PC,Linux,Mac',
      classifiers=['Natural Language :: Hindi',
      'Natural Language :: Tamil',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7'],
      long_description=open('README.md','r','UTF-8').read(),
      download_url='https://github.com/anoopkunchukuttan/indic_nlp_library/archive/master.zip',
      )
