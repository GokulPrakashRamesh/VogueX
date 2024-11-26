import pytest
from unittest.mock import Mock
from website.shopping import Shopping

def test_shopping_results_new():
    image_url = "https://www-whattowearonvacation-com.exactdn.com/wp-content/uploads/2019/09/good-walking-shoes-for-Japan.jpg"
    
    # Mock the Shopping class and its method
    s = Shopping()
    s.shopping_results = Mock(return_value=["Item1", "Item2", "Item3"])
    
    # Call the method
    results = s.shopping_results(image_url)
    
    # Assert the results are as expected
    assert isinstance(results, list)
    assert len(results) > 0
    assert "Item1" in results