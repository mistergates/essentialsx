from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


def reqs():
    with open('requirements.txt', 'r') as f:
        return f.readlines()


setup(
    name="essentials",
    version="0.0.1",
    description="Reusable essentials to be used across Python projects.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/mistergates/essentials",
    author="Mitch Gates",
    author_email="gates55434@gmail.com",
    keywords="core utilities",
    license="MIT",
    packages=["essentials"],
    install_requires=reqs(),
    include_package_data=True
)
