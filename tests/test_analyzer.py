import pytest
from src.model_analyzer.analyzer import ModelOutputAnalyzer
import numpy as np
from PIL import Image
import io

@pytest.fixture
def analyzer():
    return ModelOutputAnalyzer()

@pytest.fixture
def sample_image_bytes():
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def test_analyzer_initialization(analyzer):
    assert analyzer.threshold == 0.85
    assert analyzer.supported_formats == {'png', 'jpg', 'jpeg'}

def test_analyze_output_success(analyzer, sample_image_bytes):
    result = analyzer.analyze_output(sample_image_bytes)
    assert result["status"] == "success"
    assert "metrics" in result
    assert "image_shape" in result

def test_analyze_output_invalid_image():
    analyzer = ModelOutputAnalyzer()
    with pytest.raises(Exception):
        analyzer.analyze_output(b"invalid image data")
