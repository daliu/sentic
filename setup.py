try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = ['sentic']

setup(name='sentic',
      version='0.0.3',
      description='Sentic Package for NLP',
      long_description=open('README.md').read(),
      author=u'David Liu',
      author_email='7david12liu@gmail.com',
      url='https://github.com/daliu/sentic/',
      packages=['sentic'],
      package_data={'': ['LICENSE', 'README.md'], 'sentic': ['sentic']},
      package_dir={'sentic': 'sentic'},
      include_package_data=True,
      license='MIT',
      zip_safe=False,
      install_requires=[],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Science/Research',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries'],
)
