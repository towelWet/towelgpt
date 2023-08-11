# Python towelgpt

This package contains a set of Python bindings around the `llmodel` C-API.

Package on PyPI: https://pypi.org/project/towelgpt/

## Documentation
https://docs.gpt4all.io/towelgpt_python.html

## Installation

```
pip install towelgpt
```

## Local Build Instructions

**NOTE**: If you are doing this on a Windows machine, you must build the towelgpt backend using [MinGW64](https://www.mingw-w64.org/) compiler.

1. Setup `llmodel`

```
git clone --recurse-submodules git@github.com:nomic-ai/gpt4all.git
cd towelgpt/towelgpt-backend/
mkdir build
cd build
cmake ..
cmake --build . --parallel  # optionally append: --config Release
```
Confirm that `libllmodel.*` exists in `towelgpt-backend/build`.

2. Setup Python package

```
cd ../../towelgpt-bindings/python
pip3 install -e .
```

## Usage

Test it out! In a Python script or console:

```python
from towelgpt import towelgpt
model = towelgpt("orca-mini-3b.ggmlv3.q4_0.bin")
output = model.generate("The capital of France is ", max_tokens=3)
print(output)
```

## Troubleshooting a Local Build
- If you're on Windows and have compiled with a MinGW toolchain, you might run into an error like:
  ```
  FileNotFoundError: Could not find module '<...>\towelgpt-bindings\python\towelgpt\llmodel_DO_NOT_MODIFY\build\libllmodel.dll'
  (or one of its dependencies). Try using the full path with constructor syntax.
  ```
  The key phrase in this case is _"or one of its dependencies"_. The Python interpreter you're using
  probably doesn't see the MinGW runtime dependencies. At the moment, the following three are required:
  `libgcc_s_seh-1.dll`, `libstdc++-6.dll` and `libwinpthread-1.dll`. You should copy them from MinGW
  into a folder where Python will see them, preferably next to `libllmodel.dll`.

- Note regarding the Microsoft toolchain: Compiling with MSVC is possible, but not the official way to
  go about it at the moment. MSVC doesn't produce DLLs with a `lib` prefix, which the bindings expect.
  You'd have to amend that yourself.
