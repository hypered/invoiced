from setuptools import setup, find_packages

setup(
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    license='BSD2 License',
    package_data={
    },
    entry_points={
        'console_scripts': [
            'invoiced=invoiced.main:main',
        ],
    },
    install_requires=[
    ],
)
