import unittest

from .sample_unit_tests import LoadSampleTestCase
from .gating_unit_tests import GatingMLTestCase
from .prog_gating_unit_tests import GatingTestCase
from .export_gml_unit_tests import ExportGMLTestCase
from .matrix_unit_tests import MatrixTestCase
from .string_repr_tests import StringReprTestCase
from .session_unit_tests import SessionTestCase

if __name__ == "__main__":
    unittest.main()
