import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='django-authorizeapi',
    version='1.0',
    packages=find_packages(),
    description='Custom authorization for group level',
    long_description=README,
    author='Merilent',
    author_email='svc_jobs@merilent.com',
    url='https://github.com/yourname/django-authorizeapi/',
    install_requires=[
        'Django>=1.6',
    ],
    classifiers=[
	'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)