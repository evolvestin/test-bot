from setuptools import setup
setup(
    name='evolve-telegram-objects',
    version='0.1.0',
    description='some telegram objects',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/steve10live/evolve-telegram-objects/',
    author='evolvestin',
    packages=['objects'],
    author_email='evolvestin@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='objects',
    package_dir={'objects': 'objects'},
    package_data={'objects': ['LICENSE.txt']},
    install_requires=['heroku3', 'aiogram', 'pyTelegramBotApi', 'requests', 'bs4', 'Unidecode']
)
