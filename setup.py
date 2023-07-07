from setuptools import setup, find_packages

requirements = [
    "requests",
    "websocket-client",
    "setuptools"
]

long_description ="""By: nxslayer\nInstall: pip install user_discord"""

setup(
    name="user_discord",
    license="MIT",
    author="nxSlayer",
    version="2.0.6",
    author_email="princediscordslay@gmail.com",
    description="Library for discord bots.",
    url="https://github.com/nxSlayer/user-discord",
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    install_requires=requirements,
    keywords=[
        'user_discord',
        'user-discord',
    ],
    python_requires='>=3.8',
)