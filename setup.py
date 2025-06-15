from setuptools import setup

setup(
    name='kdzurawskiproject',
    version='1.0',
    description='Package for data analysis',
    py_modules=['analysis', 'alc_data_prep', 'area_data_prep', 'fire_data_prep', 'pop_data_prep', 'main.py'],
    url='https://github.com/grusgemini/NYPD_project/',
    author='Kacper Żurawski',
    install_requires=[
        'pandas', 'numpy', 'openpyxl', 'xlrd'
    ])

