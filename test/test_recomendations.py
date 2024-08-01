import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.repository import repository_recomendations
from app import models, schemas, database

class TestRecomendations(unittest.TestCase):

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
        # Reset mock methods for each test
        self.patcher_create_recomendation = patch('app.repository.repository_recomendations.create_review', self._mock_create_recomendation)
        self.patcher_get_recomendations = patch('app.repository.repository_recomendations.get_unreviewed_locations', self._mock_get_recomendations)
        
        self.mock_create_recomendation = self.patcher_create_recomendation.start()
        self.mock_get_recomendations = self.patcher_get_recomendations.start()

    def tearDown(self):
        self.patcher_create_recomendation.stop()
        self.patcher_get_recomendations.stop()

    def _mock_create_recomendation(self, db, recomendation):
        # Simular una recomendación creada exitosamente
        return {**recomendation.model_dump(), "id": 1}

    def _mock_get_recomendations(self, db):
        # Simular una lista de recomendaciones sin revisar
        return [
            schemas.LocationCategoryReview(id=1, location_id=1, category_id=1, last_review="2024-07-01T00:00:00", review="Excellent place", rating=4.5),
            schemas.LocationCategoryReview(id=2, location_id=2, category_id=2, last_review="2024-07-02T00:00:00", review="Nice spot", rating=3.8)
        ]

    def test_create_recomendation(self):
        response = self.client.post("/recomendations/", json={
            "location_id": 1,
            "category_id": 1,
            "last_review": "2024-07-01T00:00:00",
            "review": "Excellent place",
            "rating": 4.5
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "location_id": 1,
            "category_id": 1,
            "last_review": "2024-07-01T00:00:00",
            "review": "Excellent place",
            "rating": 4.5,
            "id": 1
        })

    def test_get_recomendations(self):
        response = self.client.get("/recomendations/unreviewed")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {
                "id": 1,
                "location_id": 1,
                "category_id": 1,
                "last_review": "2024-07-01T00:00:00",
                "review": "Excellent place",
                "rating": 4.5
            },
            {
                "id": 2,
                "location_id": 2,
                "category_id": 2,
                "last_review": "2024-07-02T00:00:00",
                "review": "Nice spot",
                "rating": 3.8
            }
        ])

if __name__ == "__main__":
    unittest.main()
