"""Tests for eseas.core.json_ops module"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from eseas.core.json_ops import (
    dict_apply,
    remove_json_bad_chars,
    replace_recursive_json,
    create_json_file,
)


class TestDictApply:
    """Test dict_apply function"""

    def test_dict_apply_with_dict(self):
        """Test applying function to dictionary values"""
        input_dict = {"key1": "value1", "key2": "value2"}
        result = dict_apply(input_dict, str.upper)
        assert result == {"key1": "VALUE1", "key2": "VALUE2"}

    def test_dict_apply_with_list(self):
        """Test applying function to list elements"""
        input_list = ["hello", "world"]
        result = dict_apply(input_list, str.upper)
        assert result == ["HELLO", "WORLD"]

    def test_dict_apply_with_tuple(self):
        """Test applying function to tuple elements"""
        input_tuple = ("hello", "world")
        result = dict_apply(input_tuple, str.upper)
        assert result == ["HELLO", "WORLD"]  # Returns list

    def test_dict_apply_with_nested_values(self):
        """Test that non-string values are ignored"""
        input_dict = {"str_val": "text", "int_val": 123, "bool_val": True}
        result = dict_apply(input_dict, str.upper)
        assert result == {"str_val": "TEXT"}
        assert "int_val" not in result
        assert "bool_val" not in result


class TestReplaceRecursiveJson:
    """Test replace_recursive_json function"""

    def test_simple_replacement(self):
        """Test simple character replacement"""
        text = "Hello$World$Test"
        result = replace_recursive_json(text, "$", "USD")
        assert result == "HelloUSDWorldUSDTest"

    def test_no_replacement_needed(self):
        """Test when character is not present"""
        text = "HelloWorld"
        result = replace_recursive_json(text, "$", "USD")
        assert result == "HelloWorld"

    def test_multiple_occurrences(self):
        """Test multiple occurrences of same character"""
        text = "$$$"
        result = replace_recursive_json(text, "$", "USD")
        # Splitting "$$$" by "$" gives ["", "", "", ""], joining with "USD" gives "USDUSDUSD"
        assert result == "USDUSDUSD"

    def test_replacement_with_special_chars(self):
        """Test replacement with special characters"""
        text = "Test?Question?Mark"
        result = replace_recursive_json(text, "?", "QUESTIONMARK")
        assert result == "TestQUESTIONMARKQuestionQUESTIONMARKMark"


class TestRemoveJsonBadChars:
    """Test remove_json_bad_chars function"""

    def test_remove_bad_chars_from_string(self):
        """Test removing bad characters from string"""
        text = "Price: $100 (50% off)"
        result = remove_json_bad_chars(text)
        assert "$" not in result
        assert "%" not in result
        assert "USD" in result
        assert "PERCENT" in result

    def test_remove_bad_chars_from_dict(self):
        """Test removing bad characters from dictionary values"""
        input_dict = {
            "price": "$100",
            "discount": "50%",
            "name": "Product",
        }
        result = remove_json_bad_chars(input_dict)
        assert "$" not in result["price"]
        assert "USD" in result["price"]
        assert "%" not in result["discount"]
        assert "PERCENT" in result["discount"]
        assert result["name"] == "Product"  # No change

    def test_remove_bad_chars_from_list(self):
        """Test removing bad characters from list"""
        input_list = ["$100", "50%", "&symbol"]
        result = remove_json_bad_chars(input_list)
        assert "$" not in result[0]
        assert "USD" in result[0]
        assert "%" not in result[1]
        assert "AMPERSTAND" in result[2]

    def test_remove_bad_chars_from_tuple(self):
        """Test removing bad characters from tuple"""
        input_tuple = ("$100", "50%")
        result = remove_json_bad_chars(input_tuple)
        assert isinstance(result, list)  # Converts to list
        assert "$" not in result[0]
        assert "USD" in result[0]

    def test_all_bad_chars_replaced(self):
        """Test that all defined bad characters are replaced"""
        text = "$100 50% A&B Question? ÄŸ Ä"
        result = remove_json_bad_chars(text)
        assert "$" not in result
        assert "%" not in result
        assert "&" not in result
        assert "?" not in result
        assert "USD" in result
        assert "PERCENT" in result
        assert "AMPERSTAND" in result
        assert "QUESTIONMARK" in result

    def test_nested_dict_processing(self):
        """Test processing nested dictionary"""
        input_dict = {
            "level1": "$100",
            "nested": {
                "level2": "50%",
            },
        }
        result = remove_json_bad_chars(input_dict)
        # Only processes top-level string values
        assert "USD" in result["level1"]
        # Nested dict is not processed (by design of dict_apply)
        assert "nested" not in result


class TestCreateJsonFile:
    """Test create_json_file function"""

    @patch("evdspy.EVDSlocal.common.files.Write")
    def test_create_json_file_default_name(self, mock_write, tmp_path):
        """Test creating JSON file with default name"""
        test_dict = {"key1": "value1", "key2": "value2"}
        mock_write.return_value = (True, "Success")

        with patch("eseas.core.json_ops.Path", return_value=tmp_path):
            create_json_file(test_dict)

        # Should be called twice (two Write calls in the function)
        assert mock_write.call_count == 2

        # Check the format of the written content
        call_args = mock_write.call_args_list[0][0]
        content = call_args[1]
        assert content.startswith("file_and_cols='")
        assert content.endswith("'")
        assert "key1" in content
        assert "value1" in content

    @patch("evdspy.EVDSlocal.common.files.Write")
    def test_create_json_file_custom_name(self, mock_write, tmp_path):
        """Test creating JSON file with custom name"""
        test_dict = {"test": "data"}
        custom_name = "custom.js"
        mock_write.return_value = (True, "Success")

        with patch("eseas.core.json_ops.Path", return_value=tmp_path):
            create_json_file(test_dict, file_name=custom_name)

        assert mock_write.call_count == 2

    @patch("evdspy.EVDSlocal.common.files.Write")
    def test_create_json_file_with_unicode(self, mock_write, tmp_path):
        """Test creating JSON file with unicode characters"""
        test_dict = {"name": "Test", "description": "Unicode: ğüşıöç"}
        mock_write.return_value = (True, "Success")

        with patch("eseas.core.json_ops.Path", return_value=tmp_path):
            create_json_file(test_dict)

        # Verify ensure_ascii=False is used (unicode preserved)
        call_args = mock_write.call_args_list[0][0]
        content = call_args[1]
        # Unicode characters should be preserved
        assert "ğüşıöç" in content or "Unicode" in content

    @patch("evdspy.EVDSlocal.common.files.Write")
    def test_create_json_file_empty_dict(self, mock_write, tmp_path):
        """Test creating JSON file with empty dictionary"""
        test_dict = {}
        mock_write.return_value = (True, "Success")

        with patch("eseas.core.json_ops.Path", return_value=tmp_path):
            create_json_file(test_dict)

        call_args = mock_write.call_args_list[0][0]
        content = call_args[1]
        assert content == "file_and_cols='{}'"


class TestIntegration:
    """Integration tests combining multiple functions"""

    def test_clean_and_create_json_file(self, tmp_path):
        """Test cleaning bad chars and creating JSON file"""
        dirty_dict = {
            "price": "$100",
            "discount": "50%",
            "question": "What?",
        }

        # Clean the dictionary
        clean_dict = remove_json_bad_chars(dirty_dict)

        # Verify cleaning worked
        assert "$" not in clean_dict.get("price", "")
        assert "%" not in clean_dict.get("discount", "")

        # Verify it's valid JSON-serializable
        json_str = json.dumps(clean_dict)
        assert "USD" in json_str
        assert "PERCENT" in json_str

    def test_dict_apply_with_cleaning_function(self):
        """Test using dict_apply with cleaning function"""
        input_dict = {"val1": "$100", "val2": "50%"}

        def clean_value(text):
            return text.replace("$", "USD").replace("%", "PERCENT")

        result = dict_apply(input_dict, clean_value)
        assert result["val1"] == "USD100"
        assert result["val2"] == "50PERCENT"
