import os
import tempfile


def test_blueleaks_path_doesnt_exist(client):
    blueleaks_path = tempfile.TemporaryDirectory()
    os.environ["BLE_BLUELEAKS_PATH"] = os.path.join(
        blueleaks_path.name, "something_fake"
    )

    response = client.get("/")
    assert (
        f"<p>The BlueLeaks data folder {os.environ['BLE_BLUELEAKS_PATH']} isn&#39;t a folder</p>".encode()
        in response.data
    )


def test_missing_blueleaks_data(client, stub_structures_path_dirs_from_source):
    # blueleaks_path should be empty when missing data
    blueleaks_path = tempfile.TemporaryDirectory()
    os.environ["BLE_BLUELEAKS_PATH"] = blueleaks_path.name

    dbs_path = tempfile.TemporaryDirectory()
    os.environ["BLE_DATABASES_PATH"] = dbs_path.name

    response = client.get("/")
    assert b"<p>Can&#39;t find the unzipped BlueLeaks dataset." in response.data


def test_not_initialized(
    client, stub_blueleaks_path_dir, stub_structures_path_dirs_from_source
):
    os.environ["BLE_BLUELEAKS_PATH"] = stub_blueleaks_path_dir.name

    # dbs_path should be empty before BlueLeaks Explorer is initialized
    dbs_path = tempfile.TemporaryDirectory()
    os.environ["BLE_DATABASES_PATH"] = dbs_path.name

    response = client.get("/")
    assert (
        b"<p>SQLite3 databases are missing. You probably haven&#39;t run the initialize.py script yet.</p>"
        in response.data
    )


def test_initialized(
    client,
    stub_blueleaks_path_dir,
    stub_dbs_path_dir,
    stub_structures_path_dirs_from_source,
):
    os.environ["BLE_BLUELEAKS_PATH"] = stub_blueleaks_path_dir.name
    os.environ["BLE_DATABASES_PATH"] = stub_dbs_path_dir.name

    response = client.get("/")
    assert (
        b"<p><strong>BlueLeaks Explorer requires javascript.</strong></p>"
        in response.data
    )
