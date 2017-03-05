from setuptools import setup


setup(name='apitizer',
    version_format='{tag}.{commitcount}+{gitsha}',
    description='plone.api refactoring helper',
    setup_requires=[
        'setuptools-git >= 0',
        'setuptools-git-version'
    ],
    install_requires=[
        'setuptools',
        'rope',
    ],
    entry_points={
        'console_scripts': [
            'apitizer = apitizer:main',
        ],
    },
)
