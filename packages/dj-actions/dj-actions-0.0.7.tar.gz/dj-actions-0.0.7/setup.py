import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dj-actions",
    version="0.0.7",
    author="Christo Crampton",
    author_email="info@38.co.za",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/schoolorchestration/libs/dj-actions",
    include_package_data=True,
    packages=setuptools.find_packages(
        exclude=('example_project', 'example_app',)
    ),
    install_requires=[
        "PyYAML==5.3",
        "jsonschema==3.2.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)