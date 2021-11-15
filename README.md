# lawyertools

A Python library for lawyer tools.

This software is **heavily WIP**, it is **not yet tested** and welcomes anyone's contribution.

- **requires `Python 3.9 or above`**. See also `requirements.txt`

## Purpose

This project's purpose is three-fold:
- allow tech savvy jurists to fiddle around with useful code
- provide a library of tools that can be imported and used in other projects
- provide a modular [FastAPI](https://fastapi.tiangolo.com/) server API to instantly fire up blazing fast web apps

## Installation

### Option A: clone the repository locally

- clone with ssh: `git clone git@gitlab.com:lawengineeringsystems/lawyertools.git`
- or with https: `git clone https://gitlab.com/lawengineeringsystems/lawyertools.git`
- move into the repo: `cd lawyertools`
- install: `pip install -e .` (the `-e` is optional, but it is advised in development environments)
- import and use the tools, e.g.:
  ```python
  from lawyertools.it.compenso_avvocati import calcola_compenso
  ```
  
### Option B: Install from gitlab

If you want to install this directly from git, without cloning it manually on your machine, run:
```shell
pip install git+https://gitlab.com/lawengineeringsystems/lawyertools.git@master#egg=lawyertools`
```

You can also list it like that in your requirements.txt file:
```text
...
pep8==1.7.1
git+https://gitlab.com/lawengineeringsystems/lawyertools.git@master#egg=lawyertools
pydantic==1.8.2
...
```

### Option C: Install with PIP

Feeling lazy, uh?

`pip install lawyertools`

## Run the API server

Either install the library from git or clone it locally, then:

- on your terminal, run `lawyertools <port>`; <port> is optional and will default to 8000
- if you want to run it manually, cd to `lawyertools` (within the library), then run: `uvicorn app:app`
More info [here](https://fastapi.tiangolo.com/deployment/manually/)
  

# TODO:

- write better docs (no shit)
- write tests
- write examples