#!/usr/bin/env python3
"""Apply the repeatable MTA redesign after crawling and cleanup."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SCRIPT = Path(__file__).with_name("static-redesign.py")
spec = spec_from_file_location("mta_static_redesign", SCRIPT)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Unable to load {SCRIPT}")
module = module_from_spec(spec)
spec.loader.exec_module(module)
module.build()
