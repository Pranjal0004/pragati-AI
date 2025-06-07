from setuptools import setup, find_packages

setup(
    name="interview-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.4.2",
        "pydantic-settings>=2.0.3",
        "loguru>=0.7.2",
        "pytest>=7.4.3",
        "httpx>=0.25.0",
        "python-multipart>=0.0.6",
        "hydra-core>=1.3.2",
        "omegaconf>=2.3.0",
        "mongoengine>=0.26.0",
        "pymongo>=4.5.0",
        "pydantic-mongoengine>=0.1.0",
        "pydantic-settings>=2.0.3",
        "pydantic-mongoengine>=0.1.0",
        "pydantic-settings>=2.0.3",
        
    ],
) 