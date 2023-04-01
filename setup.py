from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["urllib3==1.26.15", "requests==2.28.2",
                "git+https://github.com/vmware/vsphere-automation-sdk-python@v8.0.0.1"]

setup(
    name="vmware_wrapper",
    version="1.0.0",
    author="Kanaev Oleg",
    author_email="saga6021@gmail.com",
    description="A package to work with VMware Workstation. Local/vSphere storages",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/Oleggg2000/vmware_wrapper",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.11",
    ],
)