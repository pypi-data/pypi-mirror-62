from setuptools import setup, find_packages
import os

version = '3.0.0'

setup(
    name='cciaa.intranetworkflow',
    version=version,
    description="Workflow of the CCIAA - C4P project",
    long_description=open("README.rst").read()
    + "\n"
    + open(os.path.join("docs", "HISTORY.rst")).read(),
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        'Framework :: Plone :: 5.1',
        'Framework :: Plone :: 5.2',
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='c2p c3p c4p cciaa workflow',
    author='RedTurtle Technology',
    author_email='sviluppoplone@redturtle.it',
    url='https://github.com/PloneGov-IT/cciaa.intranetworkflow',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['cciaa'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.GenericSetup>=1.8.2',
        'setuptools',
        # 'redturtle.deletepolicy',
        'rt.lastmodifier',
    ],
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
