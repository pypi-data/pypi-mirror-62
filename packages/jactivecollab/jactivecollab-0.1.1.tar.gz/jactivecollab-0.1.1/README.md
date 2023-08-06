# jActivecollab

jActivecollab is the python library for accessing the ETH juniors ActiveCollab. It currently is a collection of useful functions gathered for the jupyter notebooks on jautomatio.ethjuniors.ch.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install jActivecollab in development mode. First, copy the repo. The login for gitlab.ethz.ch is in the jWiki.

```bash
git clone "https://gitlab.ethz.ch/eth-juniors/jactivecollab"
```

Then install the package in development mode. This allows you to simply change the code or pull from gitlab without having to reinstall the package.

```bash
pip install --user -e jactivecollab
```

## Usage
Credentials are on jautomation.ethjuniors.ch

```python
import jActivecollab

ac = jActivecollab.login(
    db_user = '...',
    db_password = '...',
    db_host = '...',
    db_database = '...',
)

# Returns all hours ever tracked on ActiveCollab
time_records(ac)

# TODO: Show rest of the library
```
