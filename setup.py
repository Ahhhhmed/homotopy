from distutils.core import setup
import os

setup(
    name='homotopy',
    version='0.1.dev2',
    packages=['homotopy'],
    license='MIT',
    author='Nenad Vasic',
    author_email='ahhhhmed@gmail.com',
    url='https://github.com/Ahhhhmed/homotopy',
    description='Homotopy snippet engine',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    install_requires=[],
    python_requires='>=3.3',
    include_package_data=True,
    package_data={'homotopy': ['stdlib/*']},
    entry_points={
        'console_scripts': [
            'homotopy = homotopy.__main__:main'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development',
        'Topic :: Software Development :: Compilers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Programming Language :: Java',
    ],
    test_suite='test',
)
