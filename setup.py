import setuptools

setuptools.setup(
	name="TP-RequestFlows",
	version="2025.4.30",
	author="TP Cyber Security",
	license="MIT",
	author_email="tpcybersec2023@gmail.com",
	description="A Python library for sending raw HTTP requests in a predefined sequence configured via a rules.json file. Supports automatic re-login when the session token expires",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	install_requires=open("requirements.txt").read().split(),
	url="https://github.com/tpcybersec/TP-RequestFlows",
	classifiers=[
		"Programming Language :: Python :: 3",
	],
	keywords=["TPCyberSec", "TP-RequestFlows", "Request Flows"],
	packages=["TP_RequestFlows"],
)