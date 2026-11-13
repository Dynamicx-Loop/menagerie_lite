"""Catalog checks for the two supported native Unitree G1 models."""

from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from menagerie_x.assets import get_variant, validate_assets

ASSETS = Path(__file__).resolve().parents[1]


class UnitreeG1CatalogTests(unittest.TestCase):
    def test_standard_menagerie_is_default_and_only_boxfeet_is_also_catalogued(self):
        variant = get_variant("unitree_g1", ASSETS)
        self.assertEqual(variant.dof, 29)
        self.assertEqual(variant.default_edition, "menagerie")
        self.assertIsNone(variant.urdf)
        self.assertEqual(variant.mjcf, ASSETS / "unitree_g1/g1.xml")
        self.assertEqual([(edition.id, edition.dof, edition.default) for edition in variant.editions],
                         [("menagerie", 29, True), ("29dof_box_feet", 29, False)])
        self.assertTrue(all(edition.formats == {"urdf": False, "mjcf": True} for edition in variant.editions))
        self.assertEqual(validate_assets(ASSETS), [])

    def test_retained_source_urdfs_still_resolve_their_meshes(self):
        family = ASSETS / "unitree_g1"
        for urdf in (family / "urdf/unitree_g1_29dof_with_hand_rev_1_0.urdf",
                     family / "urdf/for_retargeting/g1.urdf"):
            root = ET.parse(urdf).getroot()
            filenames = [mesh.get("filename") for mesh in root.findall(".//mesh") if mesh.get("filename")]
            self.assertTrue(filenames)
            self.assertTrue(all((urdf.parent / name).resolve().is_file() for name in filenames))
