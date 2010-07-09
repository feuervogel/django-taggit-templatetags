from setuptools import setup, find_packages
import sys, os

from taggit_templatetags import VERSION

setup(name='django-taggit-templatetags',
      version=".".join(map(str, VERSION)),
      description="Templatetags for django-taggit.",
      long_description=open("README.rst", "r").read(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='django taggit tags tagcloud taglist',
      author='Julian Moritz',
      author_email='jumo@gmx.de',
      url='http://github.com/feuervogel/django-taggit-templatetags',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'django>=1.1',
          'django-taggit>=0.8',
          'django-templatetag-sugar=>0.1'          
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
