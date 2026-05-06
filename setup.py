"""Setup configuration for neutts TTS package."""

import os
import subprocess
import sys
from pathlib import Path

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


class CMakeBuild(build_ext):
    """Custom build extension that uses CMake to build C++ extensions."""

    def build_extension(self, ext):
        ext_dir = Path(self.get_ext_fullpath(ext.name)).parent.resolve()

        build_type = "Debug" if self.debug else "Release"
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_dir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={build_type}",
        ]

        build_args = ["--config", build_type]

        if sys.platform == "win32":
            cmake_args += ["-A", "x64"]
            build_args += ["--", "/m"]
        else:
            # Use all available cores instead of hardcoded -j4
            import multiprocessing
            jobs = multiprocessing.cpu_count()
            build_args += ["--", f"-j{jobs}"]

        build_temp = Path(self.build_temp) / ext.name
        build_temp.mkdir(parents=True, exist_ok=True)

        source_dir = Path(__file__).parent.resolve()

        subprocess.run(
            ["cmake", str(source_dir)] + cmake_args,
            cwd=build_temp,
            check=True,
        )
        subprocess.run(
            ["cmake", "--build", "."] + build_args,
            cwd=build_temp,
            check=True,
        )


def read_requirements(filename: str) -> list:
    """Read requirements from a file, ignoring comments and empty lines."""
    req_path = Path(__file__).parent / filename
    if not req_path.exists():
        return []
    with open(req_path, "r", encoding="utf-8") as f:
        return [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]


long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="neutts",
    version="0.1.0",
    author="Neuphonic",
    description="A fast, lightweight text-to-speech engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/neuphonic/neutts",
    license="Apache-2.0",
    packages=find_packages(exclude=["tests*", "docs*"]),
    ext_modules=[Extension("neutts._core", sources=[])],
    cmdclass={"build_ext": CMakeBuild},
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "train": [
            "torch>=2.0.0",
            "torchaudio>=2.0.0",
            "tensorboard>=2.13.0",
            "matplotlib>=3.7.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        # Personal note: keeping Python 3.8 compat for my older lab machine
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
