from distutils.core import setup

setup(name='SphericalCow',
      version='0',
      description='A Python 2D Physics Engine',
      author='Dominic Adams',
      author_email='dominic_adams@brown.edu',
      url='https://github.com/NicoAdams/SphericalCow',
      packages=['sphericalcow'],
      package_dir={'sphericalcow' : '.'},
      install_requires=[
        "numpy",
      ],
     )