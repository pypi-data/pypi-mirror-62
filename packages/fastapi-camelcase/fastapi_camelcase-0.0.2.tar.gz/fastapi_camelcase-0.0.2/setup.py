from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

VERSION = "0.0.2"

setup(
    name="fastapi_camelcase",
    version=VERSION,
    description="Package provides an easy way to have camelcase request/response bodies for Pydantic",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/ahmednafies/fastapi_camelcase",
    author="Ahmed Nafies",
    author_email="ahmed.nafies@gmail.com",
    license="MIT",
    packages=["fastapi_camelcase"],
    install_requires=["pydantic", "pyhumps"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    zip_safe=False,
)
