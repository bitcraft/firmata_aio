from setuptools import setup

setup(
    name='firmata_aio',
    version='0.0.1',
    packages=['firmata_aio'],
    install_requires=['pyserial>=2.7'],
    download_url='https://github.com/bitcraft/firmata-aio',
    license='GNU General Public License v3 (GPLv3)',
    author='Leif Theden',
    description='A Python Protocol Abstraction Library For Firmata using Python asyncio',
    keywords=['Firmata', 'Arduino', 'Protocol', 'asyncio'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
        'Topic :: Education',
        'Topic :: Home Automation',
    ],
)
