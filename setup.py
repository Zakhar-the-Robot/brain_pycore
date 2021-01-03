from setuptools import setup, find_packages
from info import info

setup(name=info.get("name"),
      version=info.get("version"),
      description=info.get("description"),
      url=info.get("url"),
      author=info.get("author"),
      author_email=info.get("author_email"),
      license=info.get("license"),
      packages=find_packages(),
      install_requires=info.get("install_requires"),
      python_requires=">=3",
      zip_safe=False)
