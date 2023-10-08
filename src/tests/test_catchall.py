import os
import tempfile


def test_blueleaks_path_doesnt_exist(client):
    # Make temporary dir for blueleaks_path
    blueleaks_path = tempfile.TemporaryDirectory()

    # Set environment variables
    os.environ["BLE_BLUELEAKS_PATH"] = os.path.join(
        blueleaks_path.name, "something_fake"
    )

    response = client.get("/")
    assert (
        f"<p>The BlueLeaks data folder {os.environ['BLE_BLUELEAKS_PATH']} isn&#39;t a folder</p>".encode()
        in response.data
    )


def test_missing_blueleaks_data(client):
    # blueleaks_path should be empty when missing data
    blueleaks_path = tempfile.TemporaryDirectory()
    dbs_path = tempfile.TemporaryDirectory()

    # Get the structures paths from the source tree
    structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "structures"
    )
    builtin_structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "structures-builtin",
    )
    default_structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "structures-default",
    )

    # Set environment
    os.environ["BLE_BLUELEAKS_PATH"] = blueleaks_path.name
    os.environ["BLE_DATABASES_PATH"] = dbs_path.name
    os.environ["BLE_STRUCTURES_PATH"] = structures_path
    os.environ["BLE_STRUCTURES_BUILTIN_PATH"] = builtin_structures_path
    os.environ["BLE_STRUCTURES_DEFAULT_PATH"] = default_structures_path

    response = client.get("/")
    assert b"<p>Can&#39;t find the unzipped BlueLeaks dataset." in response.data


def test_not_initialized(client, blueleaks_sites):
    # blueleaks_path should have a folder for each BlueLeaks site
    blueleaks_path = tempfile.TemporaryDirectory()
    for site in blueleaks_sites:
        os.makedirs(os.path.join(blueleaks_path.name, site))

    # dbs_path should be empty before BlueLeaks Explorer is initialized
    dbs_path = tempfile.TemporaryDirectory()

    # Get the structures paths from the source tree
    structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "structures"
    )
    builtin_structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "structures-builtin",
    )
    default_structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "structures-default",
    )

    # Set environment
    os.environ["BLE_BLUELEAKS_PATH"] = blueleaks_path.name
    os.environ["BLE_DATABASES_PATH"] = dbs_path.name
    os.environ["BLE_STRUCTURES_PATH"] = structures_path
    os.environ["BLE_STRUCTURES_BUILTIN_PATH"] = builtin_structures_path
    os.environ["BLE_STRUCTURES_DEFAULT_PATH"] = default_structures_path

    response = client.get("/")
    assert (
        b"<p>SQLite3 databases are missing. You probably haven&#39;t run the initialize.py script yet.</p>"
        in response.data
    )


def test_initialized(client, blueleaks_sites):
    # blueleaks_path should have a folder for each BlueLeaks site
    blueleaks_path = tempfile.TemporaryDirectory()
    for site in blueleaks_sites:
        os.makedirs(os.path.join(blueleaks_path.name, site))

    # dbs_path should have sqlite3 databases after initialization
    dbs_path = tempfile.TemporaryDirectory()
    for site in blueleaks_sites:
        with open(os.path.join(dbs_path.name, f"{site}.sqlite3"), "wb") as f:
            f.write(b"not a real sqlite3 database")

    # Get the structures paths from the source tree
    structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "structures"
    )
    builtin_structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "structures-builtin",
    )
    default_structures_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "structures-default",
    )

    # Set environment
    os.environ["BLE_BLUELEAKS_PATH"] = blueleaks_path.name
    os.environ["BLE_DATABASES_PATH"] = dbs_path.name
    os.environ["BLE_STRUCTURES_PATH"] = structures_path
    os.environ["BLE_STRUCTURES_BUILTIN_PATH"] = builtin_structures_path
    os.environ["BLE_STRUCTURES_DEFAULT_PATH"] = default_structures_path

    response = client.get("/")

    # Should render the frontend, which is the Vue.js app
    assert (
        b"<p><strong>BlueLeaks Explorer requires javascript.</strong></p>"
        in response.data
    )
