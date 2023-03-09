import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scrapy-settings-log",
    version="1.1",
    author="Roy Healy",
    author_email="roy.healy87@gmail.com",
    description="An extension that allows a user to display all or some of their scrapy spider settings at runtime.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/further-reading/scrapy-settings-log",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'scrapy',
      ],
    python_requires='>=3.6',
    include_package_data=True,
)
