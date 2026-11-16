"""Task discovery and balanced completion regressions; not model observations."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]

class JourneySearchTests(unittest.TestCase):
    def test_task_sentences_rank_relevant_routes_without_selecting_authority(self) -> None:
        cases = [
            ("CI is red and the cause is unknown", "diagnose"),
            ("Why did CI fail on this branch?", "diagnose"),
            ("Explain the save path before changing it", "understand"),
            ("Please explain how saving works", "understand"),
            ("Fix this failing test", "diagnose"),
            ("The tests passed yesterday; what needs rerunning?", "verify"),
            ("Finish this PR", "finish-work"),
            ("Check the pull request for defects", "review"),
        ]
        program = """const {searchDiscovery} = require(process.argv[1]);
        const fs = require('fs'); const data = JSON.parse(fs.readFileSync(0, 'utf8'));
        console.log(JSON.stringify(data.cases.map(([q]) => searchDiscovery(data.catalog,q).routes.map(r=>r.id))));"""
        catalog = json.loads((ROOT / 'dist/discovery/catalog.json').read_text())
        # Test current canonical routing independently from a regenerated source pin.
        current = json.loads((ROOT / 'catalog/workflows.json').read_text())
        for route in catalog['routes']:
            route['search_phrases'] = next(r for r in current['routes'] if r['id']==route['id'])['search_phrases']
        result = subprocess.run(['node','-e',program,str(ROOT/'scripts/discovery-ui.js')],
            input=json.dumps({'catalog':catalog,'cases':cases}),text=True,capture_output=True,check=True)
        for (query, expected), actual in zip(cases,json.loads(result.stdout),strict=True):
            with self.subTest(query=query):
                self.assertTrue(actual, 'No route found')
                self.assertEqual(expected,actual[0])

    def test_unknown_query_is_not_a_confident_match(self) -> None:
        program = """const {searchDiscovery} = require(process.argv[1]);
        const fs=require('fs'); const data=JSON.parse(fs.readFileSync(0,'utf8'));
        console.log(JSON.stringify(searchDiscovery(data,'purple marmalade spaceship').routes));"""
        result=subprocess.run(['node','-e',program,str(ROOT/'scripts/discovery-ui.js')],
            input=(ROOT/'dist/discovery/catalog.json').read_text(),text=True,capture_output=True,check=True)
        self.assertEqual([],json.loads(result.stdout))
