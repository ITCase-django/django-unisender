from unisender import __version__
from setuptools import setup

setup(
    name='unisender',
    version=__version__,
    url='http://github.com/ITCase/django-unisender/',
    author='Efimov Alexey',
    author_email='alexey.efimov@itcase.pro',

    packages=['django-unisender', ],
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    license='MIT',
    description='Django admin unisender integration',
    package_data={
        '': ['*.txt', '*.rst', '*.md'],
    },
    long_description='http://github.com/ITCase/unisender/',
    install_requires=[
        'pyunisend',
        'django>=1.4, <1.7',
        'git+git://github.com/ITCase/django-tinymce-4'
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
        'Topic :: Email',
        'License :: Repoze Public License',
    ],
)
