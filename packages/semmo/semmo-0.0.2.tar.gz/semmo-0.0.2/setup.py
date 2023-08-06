import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Bram van Es,...",
    author_email="bramiozo@gmail.com",
    name='semmo',
    license="GNU GPLv3",
    description='Semmo, your simple semantic friend',
    version='v0.0.2',
    long_description=README,
    url='https://github.com/bramiozo/semmo',
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=['numpy'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Science/Research',
    ],
)