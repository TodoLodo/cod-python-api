from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests", "uuid", "urllib3", "enum34"]

setup(
    name="cod_api",
    version="0.0.1",
    author="Todo Lodo",
    author_email="me@todolodo.xyz",
    description="Call Of Duty API",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/TodoLodo2089/cod-python-api.git",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[],
)