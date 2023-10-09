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
    response = client.get("/")
    assert (
        b"<p><strong>BlueLeaks Explorer requires javascript.</strong></p>"
        in response.data
    )


def test_blueleaks_data(
    client,
    stub_blueleaks_path_dir,
    stub_dbs_path_dir,
    stub_structures_path_dirs_from_source,
):
    # Create fake data in ncric folder
    def create_file(filename, content):
        with open(filename, "w") as f:
            f.write(content)

    os.makedirs(os.path.join(stub_blueleaks_path_dir.name, "ncric", "files"))
    create_file(
        os.path.join(stub_blueleaks_path_dir.name, "ncric", "files", "alpha.txt"),
        "this is test file alpha",
    )
    create_file(
        os.path.join(stub_blueleaks_path_dir.name, "ncric", "files", "beta.txt"),
        "this is test file beta",
    )
    create_file(
        os.path.join(stub_blueleaks_path_dir.name, "ncric", "gamma.txt"),
        "this is test file gamma",
    )
    create_file(
        os.path.join(stub_blueleaks_path_dir.name, "ncric", "epsilon.txt"),
        "this is test file epsilon",
    )

    # Directory listing of /ncric
    response = client.get("/blueleaks-data/ncric/")
    assert b"<h1>BlueLeaks directory listing: /ncric/</h1>" in response.data
    assert b'<a href="/blueleaks-data/ncric/files">files</a>' in response.data
    assert (
        b'<a href="/blueleaks-data/ncric/epsilon.txt">epsilon.txt</a>' in response.data
    )
    assert b' <a href="/blueleaks-data/ncric/gamma.txt">gamma.txt</a>' in response.data

    # Directory listing of /ncric/files
    response = client.get("/blueleaks-data/ncric/files")
    assert b"<h1>BlueLeaks directory listing: /ncric/files</h1>" in response.data
    assert (
        b'<a href="/blueleaks-data/ncric/files/alpha.txt">alpha.txt</a>'
        in response.data
    )
    assert (
        b'<a href="/blueleaks-data/ncric/files/beta.txt">beta.txt</a>' in response.data
    )

    # Content of /ncric/files/alpha.txt
    response = client.get("/blueleaks-data/ncric/files/alpha.txt")
    assert response.data == b"this is test file alpha"
