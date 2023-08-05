alembic-migrate
=============

alembic-migrate is a framework-independent fork of flask-migrate.

Installation
------------

To install, run `pip install alembic-migrate`

Usage
-----

Create the following file structure:

```bash
model/
  ├── __init__.py
  ├── base.py
  ├── book.py 
```

Then declare your SQLAlchemy Base and connection string in `model/base.py`:

```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_base():
    return {'base': Base, 'sqlalchemy_url': 'sqlite:///demo.db'}
```

Let's add a model in `model/book.py`:
```python
from .base import Base
from sqlalchemy import Integer, String, Column

class Book(Base):
    __tablename__ = 'books'
    name = Column(String, primary_key=True)
    year = Column(Integer)
```

Now `cd ..` so that you are out of the model package and run:
* `alembic-db init` to setup the template
* `alembic-db migrate` to create a migration

### Configuring base module

The base module contains `get_base() -> dict`. By default `model.base` is used but you can change the environment variable:
```python
export ALEMBIC_BASE="my_model.base"
```

### Model import logic

By default, all `*.py` files in the same package as the base will be loaded.
However if you want to split your models in subpackages or have custom logic
you should implement `import_modules` inside your base module.

```python
def import_modules():
   from . import car, book
   from .sub import other_models

def get_base():
    return ...
```