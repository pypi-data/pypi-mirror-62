import setuptools

if __name__ == '__main__':
    with open('README.md', 'r') as fh:
        long_description = fh.read()

    setuptools.setup(
        name='pyjump',
        version='1.3',
        author='opper',
        author_email='alex@opper.nl',
        description=(
            'Utility that builds a 2-level menu based on applications and their available environments.'
        ),
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/opper/jump',
        packages=setuptools.find_packages(),
        classifiers=(
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ),
        entry_points={
            'console_scripts': [
                'jump = jump.menu:main'
            ],
        },
        install_requires=[
            'python-dotenv',
            'pythondialog',
            'requests',
            'click',
        ],
        include_package_data=True
    )
