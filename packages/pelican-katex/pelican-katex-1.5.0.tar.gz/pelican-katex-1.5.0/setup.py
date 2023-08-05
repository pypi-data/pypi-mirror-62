from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pelican-katex",
    version="1.5.0",
    author="Marten Lienen",
    author_email="marten.lienen@gmail.com",
    description="LaTeX pre-rendering for pelican",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cqql/pelican-katex",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pelican", "docutils"],
    extras_require={"markdown": ["markdown"]},
    tests_require=["pytest", "markdown"],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Framework :: Pelican :: Plugins",
    ],
)
