import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="env_canada",
    version="0.0.35",
    author="Michael Davie",
    author_email="michael.davie@gmail.com",
    description="A package to access meteorological data from Environment Canada",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaeldavie/env_canada",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['requests>=2.19.1',
                      'geopy>=1.16.0',
                      'imageio>=2.3.0',
                      'requests_futures>=0.9.7',
                      'ratelimit>=2.2.1',
                      'python-dateutil>=2.8.1'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)