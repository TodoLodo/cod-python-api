from setuptools import setup

requirements = ["asyncio", "aiohttp", "datetime", "requests", "uuid", "urllib3", "enum34"]

setup(
    name="cod_api",
    packages=['cod_api'],
    install_requires=requirements
)
