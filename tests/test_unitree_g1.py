"""Regression checks for standard Menagerie G1 and ProtoMotions boxfeet."""

import hashlib
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from menagerie_x.assets import get_variant
from menagerie_x.commands.mjcf import list_managed_candidates
from menagerie_x.commands.mujoco import check_mujoco

ROOT = Path(__file__).resolve().parents[1]
FAMILY = ROOT / "unitree_g1"


class UnitreeG1ImportTests(unittest.TestCase):
    def test_menagerie_default_names_the_standard_upstream_source(self):
        variant = get_variant("unitree_g1", ROOT)
        self.assertEqual(variant.source_provenance["repository"],
                         "https://github.com/google-deepmind/mujoco_menagerie")
        self.assertEqual(variant.source_provenance["source_path"], "unitree_g1/g1.xml")
        self.assertEqual(variant.source_provenance["revision"], "370c43965323c0944b433b202aac5058b5f907a9")
        self.assertEqual(list_managed_candidates("unitree_g1", ROOT), [])

    def test_boxfeet_provenance_and_retargeting_source_are_preserved(self):
        variant = get_variant("unitree_g1", ROOT)
        boxfeet = next(edition for edition in variant.editions if edition.id == "29dof_box_feet")
        self.assertEqual(boxfeet.mjcf, FAMILY / "unitree_g1_29dof_box_feet.xml")
        self.assertEqual(boxfeet.source_provenance["repository"], "https://github.com/NVlabs/ProtoMotions")
        self.assertEqual(boxfeet.source_provenance["source_path"], "protomotions/data/assets/mjcf/g1_bm_box_feet.xml")
        self.assertEqual(hashlib.sha256(boxfeet.mjcf.read_bytes()).hexdigest(),
                         boxfeet.source_provenance["packaged_sha256"])
        urdf = boxfeet.source_provenance["retargeting_urdf"]
        self.assertEqual(hashlib.sha256((FAMILY / urdf["packaged_path"]).read_bytes()).hexdigest(),
                         urdf["packaged_sha256"])
        for notice in ("LICENSE.Unitree", "LICENSE.ProtoMotions", "NOTICE.ProtoMotions", "LICENSE.Menagerie"):
            self.assertTrue((FAMILY / notice).is_file())

    def test_archived_variants_retain_their_original_bytes(self):
        record = json.loads((FAMILY / "provenance/retired_variants/files.json").read_text())
        for item in record["files"]:
            with self.subTest(path=item["archived_path"]):
                self.assertEqual(hashlib.sha256((FAMILY / item["archived_path"]).read_bytes()).hexdigest(),
                                 item["sha256"])

    def test_boxfeet_snapshot_and_mesh_dependencies_remain_available(self):
        path = FAMILY / "mjcf/unitree_g1_29dof_box_feet.xml"
        root = ET.parse(path).getroot()
        self.assertIsNotNone(root.find(".//site[@name='imu']"))
        filenames = [mesh.get("file") for mesh in root.findall("asset/mesh")]
        self.assertTrue(filenames)
        self.assertTrue(all((FAMILY / "meshes" / name).is_file() for name in filenames))

    def test_both_published_native_models_compile(self):
        result = check_mujoco("unitree_g1", ROOT)
        self.assertEqual(result["variant"], "unitree_g1")
        self.assertEqual(int(result["nq"]), 36)
        result = check_mujoco(mjcf_path=FAMILY / "unitree_g1_29dof_box_feet.xml")
        self.assertEqual(int(result["nq"]), 36)
