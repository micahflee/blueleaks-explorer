import os
import tempfile


def test_blueleaks_path_doesnt_exist(client):
    # Make temporary dirs for blueleaks_path, dbs_path, and structures_path
    blueleaks_path = tempfile.TemporaryDirectory()
    dbs_path = tempfile.TemporaryDirectory()
    structures_path = tempfile.TemporaryDirectory()

    # Set environment variables for blueleaks_path, dbs_path, and structures_path
    os.environ["BLE_BLUELEAKS_PATH"] = os.path.join(
        blueleaks_path.name, "something_fake"
    )
    os.environ["BLE_DATABASES_PATH"] = dbs_path.name
    os.environ["BLE_STRUCTURES_PATH"] = structures_path.name

    response = client.get("/")
    assert (
        f"<p>The BlueLeaks data folder {os.environ['BLE_BLUELEAKS_PATH']} isn&#39;t a folder</p>".encode()
        in response.data
    )
