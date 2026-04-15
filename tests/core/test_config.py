import os
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from app.core.config import Settings, load_settings, settings


class TestSettings:
    def test_settings_creation(self):
        settings = Settings(openai_api_key="test_key")
        assert settings.openai_api_key == "test_key"
        assert isinstance(settings.base_dir, Path)
        assert isinstance(settings.auth_dir, Path)
        assert isinstance(settings.data_dir, Path)

    def test_knowledge_file_path_property(self):
        settings = Settings(openai_api_key="test_key")
        expected = settings.data_dir / "knowledge.json"
        assert settings.knowledge_file_path == expected

    def test_openai_key_file_path_property(self):
        settings = Settings(openai_api_key="test_key")
        expected = settings.auth_dir / "openai_key.txt"
        assert settings.openai_key_file_path == expected


class TestLoadSettings:
    @patch.dict(os.environ, {}, clear=True)
    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="test_key_from_file")
    def test_load_settings_from_file(self, mock_file, mock_exists):
        mock_exists.return_value = True
        result = load_settings()
        assert result.openai_api_key == "test_key_from_file"

    @patch.dict(os.environ, {"OPENAI_API_KEY": "env_key"}, clear=True)
    def test_load_settings_from_env(self):
        result = load_settings()
        assert result.openai_api_key == "env_key"

    @patch.dict(os.environ, {}, clear=True)
    @patch("pathlib.Path.exists")
    def test_load_settings_no_key_raises_error(self, mock_exists):
        mock_exists.return_value = False
        with pytest.raises(ValueError, match="OpenAI API key not found"):
            load_settings()

    @patch.dict(os.environ, {}, clear=True)
    @patch("pathlib.Path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_settings_empty_file_raises_error(self, mock_file, mock_exists):
        mock_exists.return_value = True
        with pytest.raises(ValueError, match="OpenAI API key not found"):
            load_settings()


class TestGlobalSettings:
    def test_settings_global_instance_loaded(self):
        # During testing, settings should be loaded due to conftest setting OPENAI_API_KEY
        from app.core import config
        assert config.settings is not None
        assert config.settings.openai_api_key == "test_key_for_testing"