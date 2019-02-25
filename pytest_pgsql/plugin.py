"""This forms the core of the pytest plugin."""

import pytest
from pgtest.pgtest import PGTest

from pytest_pgsql import database
from pytest_pgsql import ext


def pytest_addoption(parser):
    """Add configuration options for pytest_pgsql."""
    parser.addini(
        name='pg_ctl',
        help='Location for pg_ctl executable. Example: /usr/lib/postgresql/9.6/bin/pg_ctl',
        default='/usr/lib/postgresql/9.6/bin/pg_ctl'
    )

    parser.addoption(
        '--pg-ctl',
        action='store',
        metavar='path',
        dest='pg_ctl',
        help='Location for pg_ctl executable. Example: /usr/lib/postgresql/9.6/bin/pg_ctl'
    )

    parser.addini(
        name='pg_extensions',
        help='A comma-separated list of PostgreSQL extensions to install at '
             'the beginning of the session for use by all tests. Example: '
             'pg_extensions=uuid-ossp,pg_tgrm,pgcrypto',
    )

    parser.addoption(
        '--pg-extensions',
        action='store',
        default='',
        dest='pg_extensions',
        help='A comma-separated list of PostgreSQL extensions to install at '
             'the beginning of the session for use by all tests. Example: '
             '--pg-extensions=uuid-ossp,pg_tgrm,pgcrypto'
    )


@pytest.fixture(scope='session')
def database_uri(request):
    """A fixture giving the connection URI of the session-wide test database."""
    pg_ctl = request.config.getoption('--pg-ctl') or request.config.getini('pg_ctl')
    with PGTest(pg_ctl=pg_ctl) as pgdb:
        yield pgdb.url


#: A SQLAlchemy engine shared by the transacted and non-transacted database fixtures.
#:
#: .. seealso:: `pytest_pgsql.ext.create_engine_fixture`
# pylint: disable=invalid-name
pg_engine = ext.create_engine_fixture('pg_engine', scope='session')
# pylint: enable=invalid-name


@pytest.fixture(scope='session')
def database_snapshot(pg_engine):
    """Create one database snapshot for the session.

    The database will be restored to this state after each test.

    .. note ::

        This is an implementation detail and should not be used directly except
        by derived fixtures.
    """
    return database.create_database_snapshot(pg_engine)


# pylint: disable=invalid-name

#: Create a test database instance and cleans up after each test finishes.
#:
#: You should prefer the `transacted_postgresql_db` fixture unless your test
#: cannot be run in a single transaction. The `transacted_postgresql_db` fixture
#: leads to faster tests since it doesn't tear down the entire database between
#: each test.
postgresql_db = \
    database.PostgreSQLTestDB.create_fixture('postgresql_db')


#: Create a test database instance that rolls back the current transaction after
#: each test finishes, verifying its integrity before returning.
#:
#: Read the warning in the main documentation page before using this fixture.
transacted_postgresql_db = \
    database.TransactedPostgreSQLTestDB.create_fixture('transacted_postgresql_db')

# pylint: enable=invalid-name
