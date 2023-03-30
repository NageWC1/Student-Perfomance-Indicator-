from setuptools import find_packages, setup
from typing import List
# find_packages : this will automatically findout all the packages that are available in the entire machine learning
# application in the direcory that we created 

HYPEN_E_DOT = '-e .'

def get_requirements(
        file_path:str
)->List[str]:
    '''
    this function will return the list of requiments 
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements = [req.replace("\n","")for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements
      
print(get_requirements('requirements.txt'))
# this will include all the inforamton about the project 
setup(
    name='Student Perfomance Prediction',
    version='0.0.1',
    author='Nagenthiran',
    author_email='Nagenthirannagarajh@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
   

