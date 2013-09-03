import os
from setuptools import setup
from sitetree import VERSION

f = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
readme = f.read()
f.close()

setup(
    name='django-sitka-sitetree',
    version=".".join(map(str, VERSION)),
    description='Package forked from http://github.com/idlesign/django-sitetree, initial authorship courtesy of Igor Starikov.',
    long_description=readme,
    author="Stryder Crown",
    author_email='stryder@sitkatech.com',
    url='http://github.com/firephreek/django-sitetree',
    packages=['sitetree'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
