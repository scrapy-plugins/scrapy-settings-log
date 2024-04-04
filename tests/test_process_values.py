from src.scrapy_settings_log import prepare_for_json_serialization


def test_prepare_for_json_serialization_with_set():
    """Test processing a set value."""
    obj = {1, 2, 3}
    result = prepare_for_json_serialization(obj)
    assert result == [1, 2, 3]


def test_prepare_for_json_serialization_with_class_object():
    """Test processing a class object."""

    class DummyClass:
        pass

    result = prepare_for_json_serialization(DummyClass)
    assert result == "DummyClass"


def test_prepare_for_json_serialization_dict_with_class_as_key():
    """Test processing a dictionary with a class object as a key."""

    class DummyClass:
        pass

    result = prepare_for_json_serialization({DummyClass: "foo"})
    assert result == {"DummyClass": "foo"}


def test_prepare_for_json_serialization_with_nested_objects():
    """Test processing nested objects."""
    obj = {
        "foo": {
            "bar": {
                1,
                2,
                3,
            }
        }
    }
    result = prepare_for_json_serialization(obj)
    assert result == {"foo": {"bar": [1, 2, 3]}}
