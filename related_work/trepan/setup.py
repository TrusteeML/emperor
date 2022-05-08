import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trepan",  # Replace with your own username
    version="0.0.1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="git@github.com:abarthakur/trepan_python.git",
    packages=setuptools.find_packages(),
    install_requires=["graphviz"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
