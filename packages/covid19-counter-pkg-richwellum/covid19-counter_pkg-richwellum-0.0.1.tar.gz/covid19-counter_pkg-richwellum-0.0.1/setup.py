import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covid19-counter_pkg-richwellum",
    version="0.0.1",
    scripts=['covid19_counter'] ,
    author="Richard Wellum",
    author_email="richwellum@gmail.com",
    description="Track some basic covid19 statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RichWellum/covid19",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
