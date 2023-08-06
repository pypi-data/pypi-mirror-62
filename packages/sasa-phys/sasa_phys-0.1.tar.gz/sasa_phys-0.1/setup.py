import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(

    name='sasa_phys',

    version='0.1',

    author="Tim Luca Turan, Max Bräuer",

    author_email="timturan@web.de",

    description="Semi Analytic Stacking Algorithm for Meta Surface stacks",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/TimLucaTuran/SASA",

    packages=['sasa_phys'],

    license='MIT',

    install_requires=['numpy'],

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

)
