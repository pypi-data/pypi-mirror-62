#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CRISPR_TAPE", # Replace with your own username
    version="1.0.1",
    author="Daniel Anderson",
    author_email="danielanderson1@hotmail.com",
    description="A protein-centric CRISPR gRNA design tool for TArgeted Protein Engineering",
    long_description="Existing CRIPSR gRNA design tools target protein-coding regions within genomic loci and non-specifically target the entire input region of DNA. Current tools fail to consider proteomic-based applications, so CRISPR-TAPE has been developed to reduce the substantial time burden associated with manual curation of gRNA libraries and empower the proteomics community." ,
    long_description_content_type="text/markdown",
    url="https://github.com/LaboratoryChild/CRISPR-TAPE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
