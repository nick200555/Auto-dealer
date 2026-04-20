from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in auto_dealer/__init__.py
from auto_dealer import __version__ as version

setup(
	name="auto_dealer",
	version=version,
	description="Automobile Dealership ERP — ERPNext v15+ Custom App",
	author="Seria Internship",
	author_email="admin@seria.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires,
)
