# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: CC-BY-4.0 AND Apache-2.0
#
"""Regression test for platform-specific USD extra dependencies."""

import tomllib
import unittest
from pathlib import Path


class TestPyprojectUsdExtras(unittest.TestCase):
    def test_linux_aarch64_uses_usd_exchange(self):
        pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
        with open(pyproject, "rb") as f:
            data = tomllib.load(f)

        usd = data["project"]["optional-dependencies"]["usd"]
        exchange_specs = [s for s in usd if s.startswith("usd-exchange")]
        core_specs = [s for s in usd if s.startswith("usd-core")]

        self.assertEqual(len(exchange_specs), 1)
        self.assertEqual(len(core_specs), 1)

        exchange_marker = exchange_specs[0].split(";", 1)[1].strip()
        core_marker = core_specs[0].split(";", 1)[1].strip()

        # usd-exchange must be gated to Linux only, not all aarch64.
        self.assertIn("platform_system == 'Linux'", exchange_marker)

        # usd-core must still be selected on a non-Linux aarch64 platform.
        env = {"platform_machine": "aarch64", "platform_system": "Darwin"}
        self.assertTrue(
            eval(core_marker, {"__builtins__": {}}, env),
