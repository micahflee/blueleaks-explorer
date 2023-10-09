import os
import json


def test_api_structures(client, blueleaks_path, dbs_path, structures_paths):
    response = client.get("/api/structures")
    obj = json.loads(response.data)
    assert len(obj["implemented_sites"]) == 1
    assert (
        obj["implemented_sites"][0]["name"]
        == "Northern California Regional Intelligence Center"
    )
    assert len(obj["unimplemented_sites"]) == 120
    assert "arictexas" in obj["unimplemented_sites"]
    assert "houstonhidta" in obj["unimplemented_sites"]
    assert "memiac" in obj["unimplemented_sites"]


# def test_api_structure_create(client, blueleaks_path, dbs_path, structures_paths):
#     pass


# def test_api_structure_get(client, blueleaks_path, dbs_path, structures_paths):
#     pass


# def test_api_structure_post(client, blueleaks_path, dbs_path, structures_paths):
#     pass


# def test_api_sites(client, blueleaks_path, dbs_path, structures_paths):
#     pass


# def test_api_tables(client, blueleaks_path, dbs_path, structures_paths):
#     pass


# def test_api_rows(client, blueleaks_path, dbs_path, structures_paths):
#     pass


# def test_api_search(client, blueleaks_path, dbs_path, structures_paths):
#     pass


# def test_api_item(client, blueleaks_path, dbs_path, structures_paths):
#     pass


# def test_api_join_all(client, blueleaks_path, dbs_path, structures_paths):
#     pass


# def test_api_join(client, blueleaks_path, dbs_path, structures_paths):
#     pass
