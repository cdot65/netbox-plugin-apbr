from setuptools import find_packages, setup

setup(
    name='apbr',
    version='0.0.1',
    description='A NetBox plugin for managing Juniper\'s APBR policies',
    url='https://gitlab.com/cdot65/netbox/advanced-policy-based-routing',
    author='Calvin Remsburg',
    license='Apache 2.0',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)