import unittest
import json
import io
from unittest.mock import patch, MagicMock
from uniface.core.immich_sync import (
    test_immich_connection as sdk_test_conn,
    get_immich_albums_list,
    get_immich_tags_list,
    get_immich_people_list,
    get_immich_category_assets,
    import_immich_assets,
    sync_to_immich
)

class DummyHTTPResponse:
    def __init__(self, data: dict | list):
        self.data_bytes = json.dumps(data).encode("utf-8")
        self.io = io.BytesIO(self.data_bytes)

    def read(self):
        return self.io.read()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class TestImmichIntegration(unittest.TestCase):

    @patch('urllib.request.urlopen')
    def test_connection_success(self, mock_urlopen):
        mock_urlopen.return_value = DummyHTTPResponse({"name": "Test User", "email": "test@test.com"})

        res = sdk_test_conn("http://localhost:2283", "dummy_key")
        self.assertTrue(res["success"])
        self.assertIn("Test User", res["message"])

    @patch('urllib.request.urlopen')
    def test_get_albums_success(self, mock_urlopen):
        mock_urlopen.return_value = DummyHTTPResponse([{"id": "album-123", "albumName": "Vacation", "assetCount": 5}])

        res = get_immich_albums_list("http://localhost:2283", "dummy_key")
        self.assertTrue(res["success"])
        self.assertEqual(len(res["albums"]), 1)
        self.assertEqual(res["albums"][0]["name"], "Vacation")

    @patch('urllib.request.urlopen')
    def test_get_tags_success(self, mock_urlopen):
        mock_urlopen.return_value = DummyHTTPResponse([{"id": "tag-123", "name": "Family"}])

        res = get_immich_tags_list("http://localhost:2283", "dummy_key")
        self.assertTrue(res["success"])
        self.assertEqual(len(res["tags"]), 1)
        self.assertEqual(res["tags"][0]["name"], "Family")

    @patch('urllib.request.urlopen')
    def test_get_people_filters_unnamed(self, mock_urlopen):
        mock_urlopen.return_value = DummyHTTPResponse({
            "people": [
                {"id": "p-1", "name": "Alice", "thumbnailPath": "/thumb/p1.jpg"},
                {"id": "p-2", "name": ""},
                {"id": "p-3", "name": "   "},
                {"id": "p-4", "name": "Bob", "thumbnailPath": ""}
            ]
        })

        res = get_immich_people_list("http://localhost:2283", "dummy_key")
        self.assertTrue(res["success"])
        self.assertEqual(len(res["people"]), 2)
        names = [p["name"] for p in res["people"]]
        self.assertEqual(names, ["Alice", "Bob"])

    @patch('urllib.request.urlopen')
    def test_get_category_assets_people(self, mock_urlopen):
        mock_urlopen.return_value = DummyHTTPResponse({
            "assets": {
                "items": [
                    {
                        "id": "asset-99",
                        "originalFileName": "photo_1.jpg",
                        "type": "IMAGE",
                        "duration": None
                    }
                ]
            }
        })

        res = get_immich_category_assets("http://localhost:2283", "dummy_key", "people", "3fa85f64-5717-4562-b3fc-2c963f66afa6")
        self.assertTrue(res["success"])
        self.assertEqual(len(res["assets"]), 1)
        self.assertEqual(res["assets"][0]["id"], "asset-99")
        self.assertEqual(res["assets"][0]["filename"], "photo_1.jpg")

if __name__ == '__main__':
    unittest.main()
