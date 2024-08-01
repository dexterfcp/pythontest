import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app  
from app.repository import repository_locations
from app import models

class TestLocations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        models.Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        cls.session = cls.SessionLocal()
        cls.client = TestClient(app)
    
    @classmethod
    def tearDownClass(cls):
        models.Base.metadata.drop_all(cls.engine)
        cls.session.close()

    def setUp(self):
        self.mock_repository = {
            'create_location': self._mock_create_location,
            'get_locations': self._mock_get_locations,
            'get_location': self._mock_get_location,
            'get_location_by_name': self._mock_get_location_by_name
        }
        repository_locations.create_location = self.mock_repository['create_location']
        repository_locations.get_locations = self.mock_repository['get_locations']
        repository_locations.get_location = self.mock_repository['get_location']
        repository_locations.get_location_by_name = self.mock_repository['get_location_by_name']

    def _mock_create_location(self, db, location):
        location_id = 1
        return {**location.model_dump(), "id": location_id}

    def _mock_get_locations(self, db):
        return []

    def _mock_get_location(self, db, location_id):
        if location_id == 1:
            return {"name": "Test Location", "description": "Description", "latitude": 0.0, "longitude": 0.0, "city": "City", "id": location_id}
        return None

    def _mock_get_location_by_name(self, db, name):
        if name == "Test Location":
            return {"name": name, "description": "Description", "latitude": 0.0, "longitude": 0.0, "city": "City", "id": 1}
        return None

    def test_create_location(self):
        response = self.client.post("/locations/", json={"name": "Test Location", "description": "Description", "latitude": 0.0, "longitude": 0.0, "city": "City"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "Test Location", "description": "Description", "latitude": 0.0, "longitude": 0.0, "city": "City", "id": 1})

    def test_get_locations(self):
        response = self.client.get("/locations/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_location(self):
        response = self.client.get("/locations/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "Test Location", "description": "Description", "latitude": 0.0, "longitude": 0.0, "city": "City", "id": 1})

    def test_get_location_not_found(self):
        response = self.client.get("/locations/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Location not found"})

    def test_get_location_by_name(self):
        response = self.client.get("/locations/name/Test Location")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "Test Location", "description": "Description", "latitude": 0.0, "longitude": 0.0, "city": "City", "id": 1})

    def test_get_location_by_name_not_found(self):
        response = self.client.get("/locations/name/Unknown Location")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Location not found"})

if __name__ == "__main__":
    unittest.main()
