from setuptools import setup

setup(
    name="python-abode",
    version="1.0.0",
    author="Wil Schrader",
    author_email="wilrader@gmail.com",
    description=("A thin Python wrapper for the Abode Alarm Non-Public API"),
    license="MIT License",
    keywords="api wrapper abode alarm goabode",
    url="https://github.com/misterwil/python-abode",
    py_modules=['abode'],
    zip_safe=True,
    install_requires=['requests>=1.6', 'responses'],
)
