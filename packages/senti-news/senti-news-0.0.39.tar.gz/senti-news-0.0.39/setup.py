import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requirements = [
    'sqlalchemy',
    'numpy',
    'textblob',
    'vaderSentiment',
    'pandas',
    'newsapi-python',
    'python-dateutil',
    'requests',
    'bs4',
    'scrapy',
    'python-dotenv',
    'transformers'
]

setuptools.setup(
    name="senti-news",
    version="0.0.39",
    author="Nicholas Broad",
    author_email="nicholas@nmbroad.com",
    description="News title sentiment analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nbroad1881/senti-news",
    packages=setuptools.find_packages(where='src/'),
    package_dir={'': 'src'},
    install_requires=install_requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
