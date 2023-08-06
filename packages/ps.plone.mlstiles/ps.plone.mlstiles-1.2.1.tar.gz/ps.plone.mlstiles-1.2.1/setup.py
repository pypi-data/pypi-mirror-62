# -*- coding: utf-8 -*-
"""Setup for ps.plone.mlstiles package."""

from setuptools import setup, find_packages

version = '1.2.1'
description = 'Tiles support for the Propertyshelf MLS Plone Embedding.'
long_description = ('\n'.join([
    open('README.rst').read(),
    open('CHANGES.rst').read(),
]))

install_requires = [
    'setuptools',
    # -*- Extra requirements: -*-
    'plone.api >= 1.0',
    'plone.app.registry',
    'plone.app.tiles',
    'plone.subrequest',
    'plone.tiles',
    'ps.plone.mls >= 0.13.dev0',
    'requests',
    'z3c.form',
]

setup(
    name='ps.plone.mlstiles',
    version=version,
    description=description,
    long_description=long_description,
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='plone zope mls listing real estate',
    author='Propertyshelf, Inc.',
    author_email='development@propertyshelf.com',
    url='https://github.com/propertyshelf/ps.plone.mlstiles',
    download_url='http://pypi.python.org/pypi/ps.plone.mlstiles',
    license='GPL',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['ps', 'ps.plone'],
    include_package_data=True,
    zip_safe=False,
    extras_require=dict(
        cover=[
            'collective.cover',
        ],
        mosaic=[
            'plone.app.mosaic',
            'plone.app.standardtiles',
            'plone.supermodel',
        ],
        test=[
            'mock',
            'plone.app.testing',
        ],
        test_cover=[
            'ps.plone.mlstiles [test]',
            'ps.plone.mlstiles [cover]',
            'collective.cover [test]',
        ],
        test_mosaic=[
            'ps.plone.mlstiles [test]',
            'ps.plone.mlstiles [mosaic]',
        ],
    ),
    install_requires=install_requires,
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
