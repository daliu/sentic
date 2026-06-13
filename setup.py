try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = ['sentic', 'sentic.babel']

setup(name='sentic',
      version='0.0.9',
      description='Sentic Package for NLP',
      long_description=open('README.md').read(),
      author=u'David Liu',
      author_email='7david12liu@gmail.com',
      url='https://github.com/daliu/sentic/',
      packages=packages,
      package_data={'': ['LICENSE', 'README.md'], 'sentic': ['sentic'], 'sentic.babel': ['babel']},
      package_dir={'sentic': 'sentic', 'sentic.babel': 'sentic/babel'},
      include_package_data=True,
      license='SenticNet License (Non-Commercial; active Sentic Membership required for commercial use)',
      zip_safe=False,
      install_requires=[],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Science/Research',
                   'License :: Other/Proprietary License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries'],
)
