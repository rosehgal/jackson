import setuptools
with open('./README.md') as f:
    long_description = f.read()


setuptools.setup(
    name='JackSON',
    version='0.1.2',
    author='Rohit Sehgal',
    author_email='rohitsehgal1994@gmail.com',
    description='JSON secrets keeper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/r0hi7/jackson',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    )
)
