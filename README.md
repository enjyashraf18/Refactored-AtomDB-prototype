# Refactored-AtomDB-prototype

This is a prototype for AtomDB, created to handle and store data about atomic and ionic species. It leverages TinyDB with a unique storage approach that compresses the database into ZIP files.

Clearly, this prototype serves as an initial framework, designed to be straightforward and easy to modify.


## Requirements

To run this application, you need the following Python packages:

- `tinydb`
- `dataclasses` (included in Python 3.7+)

No other external libraries are needed since Python’s built-in modules (json, os, zipfile, logging, shutil, etc.) handle the rest!

You can install the required packages using `pip`

```bash
pip install tinydb
```

## Key Features
- Sharding: Data is split by element, so it’s easy to manage.
- Compression: ZIP files keep things small.
- Logging: The code logs what it’s doing (like "Inserted species...") to help you debug.

