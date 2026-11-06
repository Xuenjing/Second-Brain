'''
run from project root
python -m tests.settings_tests
'''



# verifiera default Top-K = 5
# verifiera default threshold = 0.82
# verifiera att sparade värden läses in igen
# verifiera att giltiga värden sparas
# verifiera att ogiltiga värden inte ändrar sparade settings
# verifiera att reset till default faktiskt sparar 5 och 0.82

import unittest
from unittest.mock import MagicMock, patch

import backend

class TestRagSettings(unittest.TestCase):

    @patch("backend.LocalLLMProvider")
    @patch("backend.get_embedding_model")
    @patch("backend.initialize_database")
    @patch("backend.QSettings")
    def test_default_rag_settings_are_loaded(
        self,
        mock_qsettings,
        mock_initialize_database,
        mock_get_embedding_model,
        mock_localllmprovider,
    ):
        """Test that default RAG settings are loaded."""

        settings = MagicMock()
        mock_qsettings.return_value = settings

        # Everytime backend tries to read a setting: pretend nothing is stored and return default settings.
        settings.value.side_effect = lambda key, default, type=None: default

        app_backend = backend.Backend()

        self.assertEqual(app_backend.rag_top_k, 5)
        self.assertEqual(app_backend.rag_similarity_threshold, 0.82)


    @patch("backend.LocalLLMProvider")
    @patch("backend.get_embedding_model")
    @patch("backend.initialize_database")
    @patch("backend.QSettings")
    def test_saved_rag_settings_are_loaded(
        self,
        mock_qsettings,
        mock_initialize_database,
        mock_get_embedding_model,
        mock_localllmprovider
    ):
        """Test that saved RAG settings are loaded."""
        
        settings = MagicMock()
        mock_qsettings.return_value = settings

        def settings_value(key, default, type=None):
            if key == "rag/top_k":
                return 8
            if key == "rag/similarity_threshold":
                return 0.75

            return default

        settings.value.side_effect = settings_value

        app_backend = backend.Backend()

        self.assertEqual(app_backend.rag_top_k, 8)
        self.assertEqual(app_backend.rag_similarity_threshold, 0.75)


    @patch("backend.LocalLLMProvider")
    @patch("backend.get_embedding_model")
    @patch("backend.initialize_database")
    @patch("backend.QSettings")
    def test_set_rag_settings_saves_values(
        self,
        mock_qsettings,
        mock_initialize_database,
        mock_get_embedding_model,
        mock_localllmprovider
    ):
        """Test that set RAG settings are saved."""

        settings = MagicMock()
        mock_qsettings.return_value = settings

        settings.value.side_effect = lambda key, default, type=None: default

        app_backend = backend.Backend()

        app_backend.set_rag_settings(
            8,
            0.75,
        )

        # Assert that the backend object has changed to these values.
        self.assertEqual(app_backend.rag_top_k, 8)
        self.assertEqual(app_backend.rag_similarity_threshold, 0.75)

        # Assert that the functions received calls like these.
        settings.setValue.assert_any_call("rag/top_k", 8)
        settings.setValue.assert_any_call("rag/similarity_threshold", 0.75)    


    @patch("backend.LocalLLMProvider")
    @patch("backend.get_embedding_model")
    @patch("backend.initialize_database")
    @patch("backend.QSettings")
    def test_invalid_threshold_is_not_saved(
        self,
        mock_qsettings,
        mock_initialize_database,
        mock_get_embedding_model,
        mock_llm_provider,
    ):
        """Test that invalid threshold settings are not saved."""

        settings = MagicMock()
        mock_qsettings.return_value = settings

        settings.value.side_effect = lambda key, default, type=None: default

        app_backend = backend.Backend()

        app_backend.set_rag_settings(
            8,
            1.5
        )

        # Assert that the above function never completes.
        self.assertEqual(app_backend.rag_top_k, 5)
        self.assertEqual(app_backend.rag_similarity_threshold, 0.82)
        settings.setValue.assert_not_called()


    @patch("backend.LocalLLMProvider")
    @patch("backend.get_embedding_model")
    @patch("backend.initialize_database")
    @patch("backend.QSettings")
    def test_invalid_top_k_is_not_saved(
        self,
        mock_qsettings,
        mock_initialize_database,
        mock_get_embedding_model,
        mock_llm_provider,
    ):
        """Test that invalid topK settings are not saved."""

        settings = MagicMock()
        mock_qsettings.return_value = settings

        settings.value.side_effect = lambda key, default, type=None: default

        app_backend = backend.Backend()

        app_backend.set_rag_settings(
            0,
            0.75,
        )

        self.assertEqual(app_backend.rag_top_k, 5)
        self.assertEqual(
            app_backend.rag_similarity_threshold,
            0.82,
        )

        settings.setValue.assert_not_called()

    @patch("backend.LocalLLMProvider")
    @patch("backend.get_embedding_model")
    @patch("backend.initialize_database")
    @patch("backend.QSettings")
    def test_get_rag_settings_emits_current_values(
        self,
        mock_qsettings,
        mock_initialize_database,
        mock_get_embedding_model,
        mock_llm_provider,
    ):
        """Test that RAG settings are being sent to QML."""

        settings = MagicMock()
        mock_qsettings.return_value = settings
        settings.value.side_effect = lambda key, default, type=None: default
        app_backend = backend.Backend()

        # When ragSettingsLoaded are loaded, put the values into a list.
        received_values = []
        app_backend.ragSettingsLoaded.connect(
            lambda top_k, threshold:
                received_values.append((top_k, threshold))
        )

        app_backend.get_rag_settings()

        self.assertEqual(received_values, [(5, 0.82)])


if __name__ == "__main__":
    unittest.main()