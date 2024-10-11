import pathlib

import setuptools

# REFERENCE VIDEO : https://www.youtube.com/watch?v=WGsMydFFPMk

setuptools.setup(
    name="aio_straico",
    version="0.0.8",
    description="An unofficial async/sync client library for Straico API",
    long_description=pathlib.Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url="https://github.com/jayrinaldime/aio-straico",
    author="Jay Rinaldi",
    author_email="jrinaldi@jayrinaldi.me",
    project_urls={
        "Source": "https://github.com/jayrinaldime/aio-straico",
        "Documentation": "https://github.com/jayrinaldime/aio-straico?tab=readme-ov-file#readme",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Communications :: Chat",
        "Topic :: Adaptive Technologies",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.9,<=3.13",
    install_requires=["httpx>=0.27.0"],
    packages=setuptools.find_packages(),
    include_package_data=True,
)
# Build step
# python -m build
# Push to pypi
# python -m twine upload --repository testpypi dist/*
