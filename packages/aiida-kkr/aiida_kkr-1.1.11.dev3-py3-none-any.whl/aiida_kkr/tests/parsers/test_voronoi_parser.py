#!/usr/bin/env python

from __future__ import absolute_import
from builtins import object
import pytest

# tests
@pytest.mark.usefixtures("aiida_env")
class Test_voronoi_parser(object):
    """
    Tests for the voronoi parser
    """

    def test_parse_voronoi_calc(self):
        """
        ...
        """
        from aiida.orm import load_node
        from aiida_kkr.parsers.voro import VoronoiParser
        from aiida.tools.importexport import import_data
        import_data('files/db_dump_vorocalc.tar.gz')
        voro_calc = load_node('559b9d9b-3525-402e-9b24-ecd8b801853c')
        parser = VoronoiParser(voro_calc)
        parser.parse()
