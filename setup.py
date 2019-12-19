import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="indic_nlp_library", # Replace with your own username
    version="0.6",
    author="Anoop Kunchukuttan",
    author_email="anoop.kunchukuttan@gmail.com",
    description="The goal of the Indic NLP Library is to build Python based libraries for common"\
        ' text processing and Natural Language Processing in Indian languages.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anoopkunchukuttan/indic_nlp_library",
    # project_urls={
    #     "Bug Tracker": "https://bugs.example.com/HelloWorld/",
    #     "Documentation": "https://docs.example.com/HelloWorld/",
    #     "Source Code": "https://code.example.com/HelloWorld/",
    # },    
    packages=setuptools.find_packages(),
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
    download_url='https://github.com/anoopkunchukuttan/indic_nlp_library/archive/master.zip',
    install_requires=[
        'morfessor',
        'pandas',
        'numpy',
    ]
)