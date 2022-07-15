from setuptools import setup

with open("README.rst", "r") as readme_file:
    readme = readme_file.read()

requirements = ["asyncio", "requests", "uuid", "urllib3", "enum34"]

setup(
    name="cod_api",
    author="Todo Lodo",
    author_email="me@todolodo.xyz",
    maintainer="Engineer15",
    maintainer_email="engineergamer15@gmail.com",
    description="Call Of Duty API",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=['cod_api'],
    install_requires=requirements,
    classifiers=[],
)