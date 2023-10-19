from setuptools import setup, find_packages

setup(
    name="my_clean_folder",
    version="1.0.0",
    description="A tool for cleaning folders",
    url="https://github.com/VladSkopenko/Homework-for-mentor",
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
