from distutils.core import setup

setup(
    name='homotopy',
    version='0.0',
    packages=['homotopy', 'test'],
    url='',
    license='',
    author='Nenad',
    author_email='ahhhhmed@gmail.com',
    description='snippet engine',
    install_requires=[

    ],
    include_package_data=True,
    package_data={'homotopy': ['stdlib/*']},
    entry_points={
        'console_scripts': [
            'homotopy = homotopy.__main__:main'
        ]
    }
)
