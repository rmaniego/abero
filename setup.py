import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name = 'abero',
    packages = ["abero"],
    version = '1.0.3',
    license='MIT',
    description = 'Analyze multiple files for similarity and/or uniqueness.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Rodney Maniego Jr.',
    author_email = 'rod.maniego23@gmail.com',
    url = 'https://github.com/rmaniego/abero',
    download_url = 'https://github.com/rmaniego/abero/archive/v1.0.tar.gz',
    keywords = ['Python', 'similarity', 'diff', 'compare', 'files'],
    install_requires=["arkivist"],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers', 
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6'
)