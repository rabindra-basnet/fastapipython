from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='fastapiBlog',  
    version='0.1.0',  
    author='Rabindra Basnet', 
    author_email='rabindraabasnet@gmail.com',  
    description='This project is about the blog api and a sample api way to create',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/rabindra-basnet/fastapipython.git',  
    packages=find_packages(), 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
    install_requires=read_requirements(),
)
