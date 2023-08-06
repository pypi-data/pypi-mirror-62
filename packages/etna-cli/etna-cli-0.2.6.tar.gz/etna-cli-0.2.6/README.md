# pytna
[![PyPI version](https://badge.fury.io/py/etna-cli.svg)](https://badge.fury.io/py/etna-cli)

Python tool for my school

### Usage

```
Usage: etna.py [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version  print version
  --help         Show this message and exit.

Commands:
  config        Init, edit or delete etna config.
  conversation  Conversations on intranet.
  event         Events.
  gitlab        Gitlab.
  project       Projects.
  rank          rank by promotion.
  student       Student stuff.
  task          Add quests and projects to TaskWarrior
```


### Installation

Make sure to have `taskwarrior` installed to task related stuff

#### Git{hub/tea} repository
```bash
$ git clone https://github.com/matteyeux/etna-cli
$ cd etna-cli
$ poetry install
```

#### PyPI
`pip3 install etna-cli`


### Setup

If you run etna-cli for the first time you may run `etna config init` to set credentials and optional Gitlab Token.
```
$ etna config init
ETNA username : demo_t
Password:
Add Gitlab API token ? [Y/n]: Y
Gitlab API token :
```

Password and Gitlab token are not printed to STDOUT.


### Credits
Powered by [etnawrapper](https://github.com/tbobm/etnawrapper)


