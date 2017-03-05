from setuptools import setup


readme = open('README.md').read()


setup(name='apitizer',
    version_format='{tag}.{commitcount}+{gitsha}',
    description='plone.api refactoring helper',
    long_description=readme[readme.find('\n\n'):],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    author='Andreas Zeidler',
    author_email='witsch@plone.org',
    url='https://github.com/witsch/apitizer',
    keywords='plone api refactoring',
    setup_requires=[
        'setuptools-git >= 0',
        'setuptools-git-version'
    ],
    install_requires=[
        'setuptools',
        'rope',
        'Products.CMFCore',
    ],
    entry_points={
        'console_scripts': [
            'apitizer = apitizer:main',
        ],
    },
)
