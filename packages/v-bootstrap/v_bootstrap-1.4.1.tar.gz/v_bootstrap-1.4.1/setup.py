""" Unit bootstrap tool
--------------------------
The tool that helps to provision units to the cloud
"""

from setuptools import setup
from v_bootstrap import __version__


def get_required_pkgs():
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    return required


setup(
    name="v_bootstrap",
    version=__version__,
    license="Apache License 2.0",
    author="EPAM Systems",
    author_email="support@aoscloud.io",
    description="Units bootstrap tool",
    long_description=__doc__,
    packages=["v_bootstrap", "v_bootstrap.onboard", "v_bootstrap.utils"],
    zip_safe=False,
    include_package_data=True,
    install_requires=get_required_pkgs(),
    platforms="any",
    entry_points={
        'console_scripts': [
            'v-bootstrap=v_bootstrap.onboard.boot:run_cli'
        ]
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ]
)
