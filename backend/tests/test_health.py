"""
Health Endpoint Tests

Comprehensive tests for the health check API endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import status

from backend.app.main import app


class TestHealthEndpoint:
    """Test cases for the health endpoint"""
    
    def test_health_endpoint_status_code(self, client: TestClient):
        """Test that health endpoint returns 200 status code"""
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
    
    def test_health_endpoint_response_format(self, client: TestClient):
        """Test that health endpoint returns correct JSON format"""
        response = client.get("/health")
        json_response = response.json()
        
        # Check required fields exist
        assert "status" in json_response
        assert "version" in json_response
        
        # Check field types
        assert isinstance(json_response["status"], str)
        assert isinstance(json_response["version"], str)
    
    def test_health_endpoint_response_values(self, client: TestClient):
        """Test that health endpoint returns expected values"""
        response = client.get("/health")
        json_response = response.json()
        
        # Check status value
        assert json_response["status"] == "ok"
        
        # Check version format (should be semantic version-like)
        version = json_response["version"]
        assert version is not None
        assert len(version) > 0
        # Basic version format validation
        assert any(char.isdigit() for char in version), "Version should contain digits"
    
    def test_health_endpoint_content_type(self, client: TestClient):
        """Test that health endpoint returns correct content type"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_endpoint_response_structure(self, client: TestClient):
        """Test complete response structure validation"""
        response = client.get("/health")
        json_response = response.json()
        
        # Should have exactly 2 fields
        assert len(json_response) == 2
        
        # Required fields with correct types
        assert json_response["status"] == "ok"
        assert isinstance(json_response["version"], str)
        assert json_response["version"] != ""
    
    @pytest.mark.asyncio
    async def test_health_endpoint_async_compatibility(self):
        """Test that health endpoint works in async context"""
        from backend.app.api.health import health_check
        
        # Test the actual endpoint function
        result = await health_check()
        
        assert result.status == "ok"
        assert isinstance(result.version, str)
        assert len(result.version) > 0
    
    def test_health_endpoint_multiple_calls(self, client: TestClient):
        """Test that health endpoint is consistent across multiple calls"""
        responses = []
        for _ in range(3):
            response = client.get("/health")
            responses.append(response.json())
        
        # All responses should be identical
        first_response = responses[0]
        for response in responses[1:]:
            assert response == first_response
    
    def test_health_endpoint_with_query_parameters(self, client: TestClient):
        """Test that health endpoint ignores query parameters"""
        response = client.get("/health?test=param")
        assert response.status_code == status.HTTP_200_OK
        
        json_response = response.json()
        assert json_response["status"] == "ok"
    
    def test_health_endpoint_http_methods(self, client: TestClient):
        """Test that health endpoint only accepts GET method"""
        # GET should work
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        
        # POST should not be allowed
        response = client.post("/health")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
        # PUT should not be allowed
        response = client.put("/health")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        
        # DELETE should not be allowed
        response = client.delete("/health")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_health_endpoint_response_time(self, client: TestClient):
        """Test that health endpoint responds quickly"""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Should respond within 1 second (very generous for a health check)
        assert response_time < 1.0
        assert response.status_code == status.HTTP_200_OK


class TestHealthResponseModel:
    """Test cases for the health response model"""
    
    def test_health_response_model_validation(self):
        """Test HealthResponse model validation"""
        from backend.app.api.health import HealthResponse
        
        # Valid data should work
        valid_response = HealthResponse(status="ok", version="1.0.0")
        assert valid_response.status == "ok"
        assert valid_response.version == "1.0.0"
    
    def test_health_response_model_required_fields(self):
        """Test that HealthResponse requires all fields"""
        from backend.app.api.health import HealthResponse
        from pydantic import ValidationError
        
        # Missing status should raise validation error
        with pytest.raises(ValidationError):
            HealthResponse(version="1.0.0")
        
        # Missing version should raise validation error
        with pytest.raises(ValidationError):
            HealthResponse(status="ok")
    
    def test_health_response_model_serialization(self):
        """Test HealthResponse model serialization"""
        from backend.app.api.health import HealthResponse
        
        response = HealthResponse(status="ok", version="1.0.0")
        serialized = response.model_dump()
        
        assert serialized == {"status": "ok", "version": "1.0.0"}
        assert isinstance(serialized, dict)


# Integration test for the complete health check flow
def test_health_integration_flow(client: TestClient):
    """Integration test for complete health check flow"""
    # Make request
    response = client.get("/health")
    
    # Validate response
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"
    
    # Parse and validate JSON
    json_response = response.json()
    assert json_response["status"] == "ok"
    assert isinstance(json_response["version"], str)
    assert len(json_response["version"]) > 0
    
    # Ensure response is properly formatted
    from backend.app.api.health import HealthResponse
    health_response = HealthResponse(**json_response)
    assert health_response.status == "ok"