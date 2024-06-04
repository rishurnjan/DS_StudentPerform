# Building a package for this ML Application so that anyone can do the installation and use. 
# from python pipy  (Building our application as a package itself)

from setuptools import find_packages,setup
from typing import List

const='-e.'

def get_requirements(File_path:str)-> List[str]:
    #will return packages from requiremts.txt file as a list

    requirements=[]
    with open(File_path)as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace('\n','') for req in requirements]

        if const in requirements:
            requirements.remove(const)

    return requirements    
        
setup(
    name='DS_proj',
    version='0.0.1',
    author='almaktashi',
    author_email='almaktashi@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)