# Top Drawer

Ever had trouble finding a valid name for that new package ? 

`top-drawer` is command line tool to help with that by searching for synonyms
of a word and validate if they are available on pypi or npm.

### Install

Python >= 3.6:

`$ pip install top-drawer`

### Usage

```
$ top-drawer --help
usage: top-drawer [-h] [-v] [--log-file LOG_FILE] [--quiet] [-c CONFIG_FILE]
                  [--api-key API_KEY]
                  ...

    Thesaurus search and availability validators to find new package names.
    

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         - (default: False)
  --log-file LOG_FILE
  --quiet
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Config file path (default: None)
  --api-key API_KEY     Your bighugelabs.com api key (default: None)

Commands:
  
    search              Search for valid words from the thesaurus definition.
    validate            Validate a word is available.
    thesaurus           Get the thesaurus definition from Big Huge Thesaurus.
    clear-cache         Clear the validations cache.
```

```
$ top-drawer search --help                                                                                                                                      ✔  17:37 
usage: top-drawer search [-h] [-c {snakecase,spinalcase}] [--pypi] [--npm] [-f]
                         [-w {noun,verb,adjective} [{noun,verb,adjective} ...]]
                         [-m {syn,ant,usr,sim,rel} [{syn,ant,usr,sim,rel} ...]]
                         word

Search for valid words from the thesaurus definition.

positional arguments:
  word                  The word to search.

optional arguments:
  -h, --help            show this help message and exit
  -c {snakecase,spinalcase}, --casing {snakecase,spinalcase}
                        The casing to apply to synonyms. (default: spinalcase)
  --pypi                Disable validation on pypi. (default: True)
  --npm                 Disable validation on npm. (default: True)
  -f, --full            Include the invalids in the output. (default: False)
  -w {noun,verb,adjective} [{noun,verb,adjective} ...], --word-type {noun,verb,adjective} [{noun,verb,adjective} ...]
                        Type of words to use. (default: None)
  -m {syn,ant,usr,sim,rel} [{syn,ant,usr,sim,rel} ...], --mode {syn,ant,usr,sim,rel} [{syn,ant,usr,sim,rel} ...]
```

## Links

- [Big Huge Thesaurus](https://words.bighugelabs.com/)
- [precept](https://github.com/T4rk1n/precept)
