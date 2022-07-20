from setuptools import setup

requirements = ["asyncio", "datetime", "requests", "uuid", "urllib3", "enum34", "json", "sys"]

setup(
    name="cod_api",
    packages=['cod_api'],
    install_requires=requirements
)
