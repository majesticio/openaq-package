from setuptools import setup, find_packages


setup(
    name="openaqreqs",
    version="0.1",
    license="MIT",
    author="Gabe",
    author_email="gabe@openaq.org",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/majesticio/openaq-package",
    keywords="example project",
    install_requires=[
        "pandas",
        "requests",
    ],
)
