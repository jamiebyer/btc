from setuptools import find_packages
from cx_Freeze import setup, Executable


options = {
    'build_exe': {
        'includes': [
            'cx_Logging', 'idna',
        ],
        'packages': [
            'asyncio', 'flask', 'jinja2', 'dash', 'plotly', 'waitress'
        ],
        'excludes': ['tkinter']
    }
}

executables = [
    Executable('./src/server.py',
               base='console',
               #targetName='btc_dash.exe'
               )
]

setup(
    name='btc_dash',
    packages=find_packages(),
    version='0.4.0',
    description='rig',
    executables=executables,
    options=options
)