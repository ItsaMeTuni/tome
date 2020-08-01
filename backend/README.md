# Development: Backend

First read the general [instructions](../README.md#Development) in the project root.

The backend is written in [Python](https://www.python.org/) using
[Starlette](https://starlette.io). You'll also need to be fairly familiar with
[asyncio](https://docs.python.org/tutorial/asyncio.html).

[PostgreSQL](https://www.postgresql.org) is used for the database.

## Warning!

(This should go without saying, but:)

**Do not store important data in your development database! It is easy to wipe out a
whole load of data in the blink of an eye!**

Run a separate, stable(r) instance of Tome if you want to use it for note-taking while
you develop. And take regular backups!

*<sub>Yes, I have been burned by this before. How on earth could you tell? /s</sub>* 

## Common Tasks

Here are some common tasks you may want to run during development.

- Code Format
- Lint
- Type Check
- Full Check
- Run Unit Tests
- Run Database Migrations
- Create a Database Migration

### Code Format
(Using [Black](https://github.com/psf/black) and
[isort](https://github.com/timothycrosley/isort))

```bash
sudo docker-compose exec backend poetry run scripts/format
```

---

### Lint
(using [Flake9](https://gitlab.com/retnikt/flake9))

```bash
sudo docker-compose exec backend poetry run flake8
```

The following Flake8 plugins are used:
- The default Flake8 ones (pycodestyle, pyflakes, mccabe)
- OpenStack [Hacking](https://github.com/openstack/hacking)
- [BugBear](https://github.com/PyCQA/flake8-bugbear)

---

### Type Check
(using [mypy](https://github.com/python/mypy))

```bash
sudo docker-compose exec backend poetry run scripts/mypy
```

---

### Full Check
(using all of the above)

```bash
sudo docker-compose exec backend poetry run scripts/check
```

---

### Run Unit Tests
(using [pytest](https://docs.pytest.org))

```bash
sudo docker-compose exec backend poetry run python -m pytest
```

---

### Run Database Migrations
(using the custom system)

```bash
sudo docker-compose exec backend poetry run python -m migrations
```

---

### Get a Database Console
(using [PostgreSQL](https://www.postgresql.org))

either:
```bash
sudo docker-compose exec db psql -U tome
```

Or, if you've published the correct port on the db container, and have `psql` installed
on your host machine:
```bash
psql -h localhost -U tome
```
This has the advantage of not requiring root.

---

### Create a Database Migration
(using the custom system and [PostgreSQL](https://www.postgresql.org))

If you are adding a feature that requires additional data to be stored in the database,
you will need to create a migration.

1. Create a file with in the correct sequence in the `migrations` directory (e.g.
`ver_000_162.py`)
2. Copy and paste in the contents from
[`_version_template.py`](./migrations/_version_template.py)
3. Edit the docstring at the top of the file to describe what the migration does (e.g.
`"""add quantity column to the sausages table""""`)
4. Write some code that upgrades the database, using the given database connection
object, for example:

    ```python
    async def upgrade(conn: asyncpg.Connection):
        await conn.execute(
            """
            alter table sausages create column quantity;
            """
        )
    ```
   
5. Write corresponding downgrade code, for example:

    ```python
    async def upgrade(conn: asyncpg.Connection):
        await conn.execute(
            """
            alter table sausages drop column quantity;
            """
        )
    ```
   
Do not worry, migrations are done in a transaction so if something goes wrong it will
all be rolled back.
   
#### Please follow the following SQL code style rules:
- Lowercase everything unless necessary
    - A good IDE should detect that it's SQL and highlight it for you (PyCharm
    Professional and VSCode can do this)
- Put semicolons after every statement, even if it's the last one in a sequence
- Always use `create table` rather than `create table if not exists`, etc.
- (exception to above) If a database extension is required as part of the migration, use
`create extension if not exists` when upgrading, and **do not** drop it when downgrading
- If a column is altered, make sure that no existing data will be lost in the process
(unless it is a downgrade, of course)
- If adding comments to your queries, add them in the SQL (the syntax is:
`-- this is a comment`) rather than in Python

---
