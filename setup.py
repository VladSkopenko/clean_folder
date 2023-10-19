from setuptools import setup, find_packages

setup(
    name="clean_folder",
    version="1.1.0",
    description="A tool for cleaning folders",
    url="https://github.com/VladSkopenko/clean_folder",
    author="Skopenko_Vladislav",
    author_email="skopirka2k17@gmail.com",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts':[
            'clean-folder=clean_folder.clean:start',
        ],
    }
)
