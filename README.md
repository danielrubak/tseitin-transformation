# tseitin-transformation

This repository contains source code of Tseitin Transformation which was developed as part of the course "Functional Programming" at AGH University of Science and Technology in Cracow.

## Installation

### Requirements

- OS: Linux (created on Ubuntu 20.04 LTS)
- Python interpreter: 3.8+
- Installed pip and venv

This project uses the PySAT library and requires some pre-installed components, you can install them all using the following command:

```bash
sudo apt-get install python3 python-dev-is-python2 python3-dev \
    build-essential libssl-dev libffi-dev libxml2-dev \
    libxslt1-dev zlib1g-dev
```

All you need to do next is to execute below set of commands:

```bash
https://github.com/danielrubak/tseitin-transformation
cd tseitin-transformation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To get more information about PySAT library [click here](https://github.com/pysathq/pysat). Advanced documentation can be found [here](https://pysathq.github.io/docs/html/api/solvers.html).

## Usage

### Supported solvers

List of all supported solvers you can find [here](https://pysathq.github.io/docs/html/api/solvers.html).

Just for convenience reason, there are also here (but below list may be not actual):

| Solver                          | Names                                |
| ------------------------------- | ------------------------------------ |
| CaDiCaL SAT solver              | 'cd', 'cdl', 'cadical'               |
| Glucose 3 SAT solver            | 'g3', 'g30', 'glucose3', 'glucose30' |
| Glucose 4.1 SAT solver          | 'g4', 'g41', 'glucose4', 'glucose41' |
| Lingeling SAT solver            | 'lgl', 'lingeling'                   |
| MapleLCMDistChronoBT SAT solver | 'mcb', 'chrono', 'maplechrono'       |
| MapleCM SAT solver              | 'mcm', 'maplecm'                     |
| MapleCOMSPS_LRB SAT solver      | 'mpl', 'maple', 'maplesat'           |
| Minicard SAT solver             | 'mc', 'mcard', 'minicard'            |
| MiniSat 2.2 SAT solver          | 'm22', 'msat22', 'minisat22'         |
| MiniSat SAT solver              | 'mgh', 'msat-gh', 'minisat-gh'       |
