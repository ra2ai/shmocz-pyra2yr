import runpy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from pyra2yr.game import get_compose_dict


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

    def test_bind_host_applies_to_all_published_ports(self):
        args = ([14521, 14522], "local/game")
        default = get_compose_dict(*args)["services"]["tunnel"]["ports"]
        bound = get_compose_dict(*args, bind_host="127.0.0.1")["services"]["tunnel"]["ports"]
        self.assertIn("6081:6081", default)
        self.assertEqual(bound, [f"127.0.0.1:{mapping}" for mapping in default])

    def test_second_desktop_uses_its_own_display_and_ports(self):
        services = get_compose_dict(
            [14521, 14522], "local/game", vnc_port=15901, novnc_port=16081,
            separate_vnc_desktop=True,
        )["services"]
        self.assertIn("15902:15902", services["tunnel"]["ports"])
        self.assertIn("16082:16082", services["tunnel"]["ports"])
        self.assertIn("Xvnc :2 ", services["vnc-1"]["command"])
        self.assertIn("-rfbport=15902 ", services["vnc-1"]["command"])
        self.assertIn("--vnc localhost:15902 --listen 16082", services["novnc-1"]["command"])
        self.assertEqual(services["wm-1"]["environment"]["DISPLAY"], ":2")
