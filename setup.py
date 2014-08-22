import os
from unisender import __version__
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-unisender',
    version=__version__,
    url='http://github.com/ITCase/django-unisender/',
    author='Efimov Alexey',
    author_email='alexey.efimov@itcase.pro',

    packages=['unisender', ],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    license='MIT',
    description='Django admin unisender integration',
    long_description=README,
    package_data={
        '': ['*.txt', '*.rst', '*.md'],
    },
    install_requires=[
        'pyunisend',
        'django',
        'django-filebrowser',
        'pillow',
        'mock',
        'dateutils'
    ],
    dependency_links=[
        'http://github.com/ITCase/django-tinymce-4/tarball/master',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
        'Topic :: Internet',
        'License :: Repoze Public License',
    ],
)
