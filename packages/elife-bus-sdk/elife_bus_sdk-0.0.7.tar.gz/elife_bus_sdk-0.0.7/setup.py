from setuptools import setup

import elife_bus_sdk


setup(
    name='elife_bus_sdk',
    version=elife_bus_sdk.__version__,
    description='This library provides a Python SDK for the eLife Sciences Bus',
    packages=['elife_bus_sdk',
              'elife_bus_sdk.publishers',
              'elife_bus_sdk.queues'],
    include_package_data=True,
    install_requires=[
        "boto3>=1.4.7",
    ],
    license='MIT',
    url='https://github.com/elifesciences/bus-sdk-python.git',
    maintainer='eLife Sciences Publications Ltd.',
    maintainer_email='tech-team@elifesciences.org',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ]

)

