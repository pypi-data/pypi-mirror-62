import setuptools


with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='dokklib_db',
    author='Agost Biro',
    author_email='agost+dokklib_db@dokknet.com',
    description='DynamoDB Single Table Library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://dokklib.com/libs/db/',
    packages=['dokklib_db'],
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    python_requires='>=3.6',
    install_requires=[
        'boto3>=1.10.34,<2',
        'botocore>=1.13.34,<2',
        'typing-extensions>=3.7.2,<4'
    ],
    data_files=[('', ['LICENSE', 'NOTICE'])],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Database'
    ]
)
