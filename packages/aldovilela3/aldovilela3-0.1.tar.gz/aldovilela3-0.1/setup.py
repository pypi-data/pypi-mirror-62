import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='aldovilela3',
     version='0.1',
     scripts=['aba_noots.py','ler_novo.py','functools.pyi'] ,
     author="Alisson Machado",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )