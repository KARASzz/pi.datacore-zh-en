import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

import 更新资料 as updater


class _Response:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return b"ok"


class UpdaterTests(unittest.TestCase):
    def setUp(self):
        updater._CTX_INSECURE = None
        updater._ALLOW_INSECURE = False

    def test_certificate_failure_is_rejected_by_default(self):
        with mock.patch(
            "更新资料.urllib.request.urlopen",
            side_effect=urllib.error.URLError("CERTIFICATE_VERIFY_FAILED"),
        ) as urlopen:
            with self.assertRaisesRegex(RuntimeError, "--allow-insecure"):
                updater.http_get("https://example.invalid")
        urlopen.assert_called_once()

    def test_insecure_retry_requires_explicit_opt_in(self):
        calls = []

        def fake_urlopen(request, timeout, context):
            calls.append(context)
            if len(calls) == 1:
                raise urllib.error.URLError("CERTIFICATE_VERIFY_FAILED")
            return _Response()

        with mock.patch(
            "更新资料.urllib.request.urlopen", side_effect=fake_urlopen
        ), mock.patch(
            "更新资料.ssl._create_unverified_context", return_value="insecure"
        ):
            self.assertEqual(
                updater.http_get("https://example.invalid", allow_insecure=True),
                b"ok",
            )
        self.assertEqual(calls, [updater._ssl_context(), "insecure"])

    def test_translation_status_becomes_stale_when_source_hash_changes(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            translation_root = root / "translations"
            translation_root.mkdir()
            translation_file = translation_root / updater.TRANSLATION_FILES["quickstart"]
            translation_file.write_text("English\n中文\n", encoding="utf-8")
            status_file = root / "翻译状态.json"
            source_key = "repo:packages/coding-agent/docs/quickstart.md"

            with mock.patch.object(updater, "ROOT", root), \
                    mock.patch.object(updater, "TRANSLATION_ROOT", translation_root), \
                    mock.patch.object(updater, "TRANSLATION_STATUS", status_file):
                first_report = []
                self.assertTrue(
                    updater.translation_status(
                        {source_key: "source-v1"}, first_report
                    )
                )
                first_state = json.loads(status_file.read_text(encoding="utf-8"))
                self.assertEqual(
                    first_state["documents"]["quickstart"]["status"], "CURRENT"
                )

                second_report = []
                self.assertTrue(
                    updater.translation_status(
                        {source_key: "source-v2"}, second_report
                    )
                )
                second_state = json.loads(status_file.read_text(encoding="utf-8"))
                quickstart = second_state["documents"]["quickstart"]
                self.assertEqual(quickstart["status"], "STALE")
                self.assertEqual(quickstart["translation_source_hash"], "source-v1")

                updater.translation_status(
                    {source_key: "source-v2"}, [], mark_current=True
                )
                current_state = json.loads(status_file.read_text(encoding="utf-8"))
                quickstart = current_state["documents"]["quickstart"]
                self.assertEqual(quickstart["status"], "CURRENT")
                self.assertEqual(quickstart["translation_source_hash"], "source-v2")
                self.assertIsNotNone(quickstart["translation_updated_at"])


if __name__ == "__main__":
    unittest.main()
