import runpy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase


class RuntimeTest(TestCase):
    def test_overlay_is_per_instance_and_reversible(self):
        helper = Path(__file__).resolve().parents[3] / "scripts/run-gamemd.py"  # pyra2yr/scripts/run-gamemd.py
        create_symlinks = runpy.run_path(str(helper))["create_symlinks"]
        with TemporaryDirectory() as tmp:
            data, overlay, instance = (Path(tmp) / p for p in ("data", "overlay", "instance"))
            for path in (data, overlay, instance):
                path.mkdir()
            (data / "ddraw.dll").write_bytes(b"original")
            (overlay / "DDRAW.DLL").write_bytes(b"replacement")
            (overlay / "extra.dll").touch()
            (overlay / "ignored.txt").touch()
            create_symlinks(instance, data, overlay)
            self.assertEqual((instance / "ddraw.dll").read_bytes(), b"replacement")
            self.assertEqual((data / "ddraw.dll").read_bytes(), b"original")
            self.assertTrue((instance / "extra.dll").is_file())
            self.assertFalse((instance / "ignored.txt").exists())
            create_symlinks(instance, data)
            self.assertFalse((instance / "extra.dll").exists())
            self.assertEqual((instance / "ddraw.dll").read_bytes(), b"original")
