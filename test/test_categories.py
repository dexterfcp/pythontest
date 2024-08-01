import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.repository import repository_categories
from app import models, schemas, database

class TestCategories(unittest.TestCase):

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
        self.patcher_create_category = patch('app.repository.repository_categories.create_category', self._mock_create_category)
        self.patcher_get_categories = patch('app.repository.repository_categories.get_categories', self._mock_get_categories)
        self.patcher_get_category = patch('app.repository.repository_categories.get_category', self._mock_get_category)
        self.patcher_get_category_by_name = patch('app.repository.repository_categories.get_category_by_name', self._mock_get_category_by_name)
        
        self.mock_create_category = self.patcher_create_category.start()
        self.mock_get_categories = self.patcher_get_categories.start()
        self.mock_get_category = self.patcher_get_category.start()
        self.mock_get_category_by_name = self.patcher_get_category_by_name.start()

    def tearDown(self):
        self.patcher_create_category.stop()
        self.patcher_get_categories.stop()
        self.patcher_get_category.stop()
        self.patcher_get_category_by_name.stop()

    def _mock_create_category(self, db, category):
        # Simular una categoría creada exitosamente
        return {**category.model_dump(), "id": 1}

    def _mock_get_categories(self, db):
        # Simular un listado de categorías
        return [
            schemas.Category(id=1, name="Food", description="All about food"),
            schemas.Category(id=2, name="Travel", description="Travel and adventure")
        ]

    def _mock_get_category(self, db, category_id):
        # Simular la obtención de una categoría por ID
        if category_id == 1:
            return schemas.Category(id=1, name="Food", description="All about food")
        return None

    def _mock_get_category_by_name(self, db, category_name):
        # Simular la obtención de una categoría por nombre
        if category_name == "Food":
            return schemas.Category(id=1, name="Food", description="All about food")
        return None

    def test_create_category(self):
        response = self.client.post("/categories/", json={
            "name": "Food",
            "description": "All about food"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "name": "Food",
            "description": "All about food",
            "id": 1
        })

    def test_get_categories(self):
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [
            {"id": 1, "name": "Food", "description": "All about food"},
            {"id": 2, "name": "Travel", "description": "Travel and adventure"}
        ])

    def test_get_category(self):
        response = self.client.get("/categories/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1,
            "name": "Food",
            "description": "All about food"
        })

    def test_get_category_not_found(self):
        response = self.client.get("/categories/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Category not found"})

    def test_get_category_by_name(self):
        response = self.client.get("/categories/name/Food")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "id": 1,
            "name": "Food",
            "description": "All about food"
        })

    def test_get_category_by_name_not_found(self):
        response = self.client.get("/categories/name/Unknown")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Category not found"})

if __name__ == "__main__":
    unittest.main()
