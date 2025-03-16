from setuptools import setup, find_packages


def read_requirements():
    with open("requirements.txt") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="alloy_eval",
    version="0.1.0",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=read_requirements(),
    description="Alloy specification evaluation benchmark",
    long_description=open("README.md").read(),
    long_description_content_type="markdown",
    author="Shmulik Cohen",
    entry_points={
        "console_scripts": [
            "test_alloy_openai=alloy_eval.openai_cli:main",
        ],
    },
)
