import pytest
import requests
import random

BASE_URL = "https://petstore.swagger.io/v2"

class TestPetAPI:
    """Test suite for Pet Store API - Pet endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data"""
        self.pet_id = random.randint(10000, 99999)
        self.pet_data = {
            "id": self.pet_id,
            "name": "Firulais",
            "status": "available",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": ["https://example.com/photo.jpg"],
            "tags": [{"id": 1, "name": "friendly"}]
        }
    
    # ========== POST TESTS ==========
    
    def test_post_create_pet_success(self):
        """POST - Caso positivo: Crear una mascota exitosamente"""
        response = requests.post(f"{BASE_URL}/pet", json=self.pet_data)
        
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == self.pet_id
        assert data["name"] == "Firulais"
        assert data["status"] == "available"
        print(f"Pet created successfully with ID: {self.pet_id}")
    
    def test_post_create_pet_invalid_data(self):
        """POST - Caso negativo: Crear mascota con datos inválidos"""
        invalid_data = {"name": ""}  # Missing required fields
        response = requests.post(f"{BASE_URL}/pet", json=invalid_data)

        assert response.status_code in [400, 405, 500], "Should fail with invalid data"
        print("Invalid pet creation rejected as expected")
    
    def test_post_create_pet_without_body(self):
        """POST - Caso negativo: Crear mascota sin body"""
        response = requests.post(f"{BASE_URL}/pet")

        assert response.status_code in [400, 405, 415], "Should fail without body"
        print("Pet creation without body rejected")
    
    # ========== GET TESTS ==========
    
    def test_get_pet_by_id_success(self):
        """GET - Caso positivo: Obtener mascota por ID existente"""
        # First create a pet
        requests.post(f"{BASE_URL}/pet", json=self.pet_data)
        
        # Then get it
        response = requests.get(f"{BASE_URL}/pet/{self.pet_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.pet_id
        assert data["name"] == "Firulais"
        print(f" Pet retrieved successfully: {data['name']}")
    
    def test_get_pet_by_id_not_found(self):
        """GET - Caso negativo: Buscar mascota con ID inexistente"""
        non_existent_id = 999999999
        response = requests.get(f"{BASE_URL}/pet/{non_existent_id}")
        
        assert response.status_code == 404, "Should return 404 for non-existent pet"
        print(" Non-existent pet returns 404 as expected")
    
    def test_get_pet_invalid_id(self):
        """GET - Caso negativo: ID inválido (string en lugar de número)"""
        response = requests.get(f"{BASE_URL}/pet/invalid_id")
        
        assert response.status_code in [400, 404], "Should fail with invalid ID format"
        print(" Invalid ID format rejected")
    
    def test_get_pets_by_status_success(self):
        """GET - Caso positivo: Obtener mascotas por status"""
        response = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": "available"})
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list), "Should return a list"
        print(f" Found {len(data)} pets with status 'available'")
    
    # ========== PUT TESTS ==========
    
    def test_put_update_pet_success(self):
        """PUT - Caso positivo: Actualizar mascota existente"""
        # Create pet first
        requests.post(f"{BASE_URL}/pet", json=self.pet_data)
        
        # Update pet
        updated_data = self.pet_data.copy()
        updated_data["name"] = "Firulais Updated"
        updated_data["status"] = "sold"
        
        response = requests.put(f"{BASE_URL}/pet", json=updated_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Firulais Updated"
        assert data["status"] == "sold"
        print(" Pet updated successfully")
    
    def test_put_update_nonexistent_pet(self):
        """PUT - Caso negativo: Actualizar mascota que no existe"""
        nonexistent_data = {
            "id": 999999999,
            "name": "Ghost Pet",
            "status": "available"
        }
        response = requests.put(f"{BASE_URL}/pet", json=nonexistent_data)
        
        # API may create it or return error - both are acceptable behaviors
        assert response.status_code in [200, 404, 400]
        print(" Update non-existent pet handled")
    
    def test_put_update_pet_invalid_data(self):
        """PUT - Caso negativo: Actualizar con datos inválidos"""
        invalid_data = {"id": "invalid", "name": 12345}
        response = requests.put(f"{BASE_URL}/pet", json=invalid_data)
        
        assert response.status_code in [400, 405, 500]
        print(" Invalid update data rejected")
    
    # ========== DELETE TESTS ==========
    
    def test_delete_pet_success(self):
        """DELETE - Caso positivo: Eliminar mascota existente"""
        # Create pet first
        requests.post(f"{BASE_URL}/pet", json=self.pet_data)
        
        # Delete it
        response = requests.delete(f"{BASE_URL}/pet/{self.pet_id}")
        
        assert response.status_code == 200
        
        # Verify it's deleted
        get_response = requests.get(f"{BASE_URL}/pet/{self.pet_id}")
        assert get_response.status_code == 404
        print(f" Pet {self.pet_id} deleted successfully")
    
    def test_delete_nonexistent_pet(self):
        """DELETE - Caso negativo: Eliminar mascota que no existe"""
        non_existent_id = 999999999
        response = requests.delete(f"{BASE_URL}/pet/{non_existent_id}")
        
        assert response.status_code in [404, 200]  # Some APIs return 200 even if not found
        print(" Delete non-existent pet handled")
    
    def test_delete_pet_invalid_id(self):
        """DELETE - Caso negativo: Eliminar con ID inválido"""
        response = requests.delete(f"{BASE_URL}/pet/invalid_id")
        
        assert response.status_code in [400, 404]
        print(" Delete with invalid ID rejected")


class TestStoreAPI:
    """Test suite for Pet Store API - Store/Order endpoints"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test data"""
        self.order_id = random.randint(1, 10)
        self.order_data = {
            "id": self.order_id,
            "petId": 123,
            "quantity": 1,
            "shipDate": "2025-10-02T00:00:00.000Z",
            "status": "placed",
            "complete": True
        }
    
    # ========== POST TESTS ==========
    
    def test_post_create_order_success(self):
        """POST - Caso positivo: Crear orden exitosamente"""
        response = requests.post(f"{BASE_URL}/store/order", json=self.order_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.order_id
        assert data["status"] == "placed"
        print(f" Order created successfully with ID: {self.order_id}")
    
    def test_post_create_order_invalid(self):
        """POST - Caso negativo: Crear orden con datos inválidos"""
        invalid_order = {"quantity": "invalid"}
        response = requests.post(f"{BASE_URL}/store/order", json=invalid_order)
        
        assert response.status_code in [400, 405, 500]
        print(" Invalid order rejected")
    
    # ========== GET TESTS ==========
    
    def test_get_order_by_id_success(self):
        """GET - Caso positivo: Obtener orden por ID"""
        # Create order first
        requests.post(f"{BASE_URL}/store/order", json=self.order_data)
        
        response = requests.get(f"{BASE_URL}/store/order/{self.order_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == self.order_id
        print(f" Order retrieved successfully")
    
    def test_get_order_not_found(self):
        """GET - Caso negativo: Orden inexistente"""
        response = requests.get(f"{BASE_URL}/store/order/999999")
        
        assert response.status_code == 404
        print(" Non-existent order returns 404")
    
    def test_get_inventory_success(self):
        """GET - Caso positivo: Obtener inventario"""
        response = requests.get(f"{BASE_URL}/store/inventory")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        print(f" Inventory retrieved: {len(data)} status types")
    
    # ========== DELETE TESTS ==========
    
    def test_delete_order_success(self):
        """DELETE - Caso positivo: Eliminar orden"""
        # Create order first
        requests.post(f"{BASE_URL}/store/order", json=self.order_data)
        
        response = requests.delete(f"{BASE_URL}/store/order/{self.order_id}")
        
        assert response.status_code == 200
        print(f" Order {self.order_id} deleted")
    
    def test_delete_order_not_found(self):
        """DELETE - Caso negativo: Eliminar orden inexistente"""
        response = requests.delete(f"{BASE_URL}/store/order/999999")
        
        assert response.status_code == 404
        print(" Delete non-existent order returns 404")