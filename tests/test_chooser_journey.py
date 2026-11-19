"""Task discovery and balanced completion regressions; not model observations."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
from typing import Any, cast
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import discovery  # noqa: E402


def current_catalog() -> dict[str, Any]:
    """Exercise canonical routes before their generated source pin is updated."""
    catalog = cast(dict[str, Any], json.loads((ROOT / discovery.EXPORT).read_text()))
    registry = json.loads((ROOT / discovery.REGISTRY).read_text())
    for route in registry['routes']:
        route['search_skills'] = discovery.route_skill_ids(route)
    catalog['routes'] = registry['routes']
    return catalog


def search_routes(queries: list[str], catalog: dict[str, Any] | None = None) -> list[list[str]]:
    program = """const {searchDiscovery} = require(process.argv[1]);
    const fs = require('node:fs'); const data = JSON.parse(fs.readFileSync(0, 'utf8'));
    console.log(JSON.stringify(data.queries.map(q =>
      searchDiscovery(data.catalog, q).routes.map(r => r.id))));"""
    result = subprocess.run(
        ['node', '-e', program, str(ROOT / 'scripts/discovery-search.js')],
        input=json.dumps({'catalog': catalog if catalog is not None else current_catalog(),
                          'queries': queries}),
        text=True, capture_output=True, check=True,
    )
    return cast(list[list[str]], json.loads(result.stdout))


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
            ("code review", "review"),
            ("pull request review", "review"),
            ("review this PR", "review"),
            ("Please review this PR before we merge", "review"),
        ]
        for (query, expected), actual in zip(cases, search_routes([q for q, _ in cases]), strict=True):
            with self.subTest(query=query):
                self.assertTrue(actual, 'No route found')
                self.assertEqual(expected, actual[0])

    def test_more_specific_contained_phrase_wins_without_changing_equal_ties(self) -> None:
        catalog = {'skills': [], 'routes': [
            {'id': 'review', 'label': 'Review a change',
             'search_phrases': ['code review'], 'search_skills': []},
            {'id': 'prepare-review', 'label': 'Prepare a change for review',
             'search_phrases': ['prepare my change for code review'], 'search_skills': []},
            {'id': 'same-specificity', 'label': 'Prepare a review packet',
             'search_phrases': ['prepare my change for code review'], 'search_skills': []},
        ]}
        queries = ['Please prepare my change for code review.', 'code review']
        self.assertEqual([
            ['prepare-review', 'same-specificity', 'review'],
            ['review', 'prepare-review', 'same-specificity'],
        ], search_routes(queries, catalog))

    def test_review_lifecycle_intents_select_the_matching_task(self) -> None:
        cases = [
            ('Prepare my change for review', 'prepare-review'),
            ('Please prepare my change for code review.', 'prepare-review'),
            ('Prepare a review packet for this patch', 'prepare-review'),
            ('request-review', 'prepare-review'),
            ('Address review feedback', 'resolve-feedback'),
            ('Please assess the code review feedback before editing.', 'resolve-feedback'),
            ('A reviewer says this needs fixing', 'resolve-feedback'),
            ('address comments', 'resolve-feedback'),
            ('address-review', 'resolve-feedback'),
            ('systems thinking', 'assess-impact'),
            ('What else might break?', 'assess-impact'),
            ('Which callers depend on this?', 'assess-impact'),
            ('assess-change-impact', 'assess-impact'),
            ('What worked after launch?', 'learn-release'),
            ('postlaunch feedback', 'learn-release'),
            ('learn-after-launch', 'learn-release'),
            ('Two reviewers disagree about the trust boundary.', 'resolve-review-conflict'),
            ('Maintain this draft PR', 'maintain-pr'),
        ]
        for (query, expected), actual in zip(cases, search_routes([q for q, _ in cases]), strict=True):
            with self.subTest(query=query):
                self.assertTrue(actual, 'No route found')
                self.assertEqual(expected, actual[0])

    def test_new_journey_requests_preserve_their_read_only_authority(self) -> None:
        routes = {r['id']: r for r in current_catalog()['routes']}
        expected = {
            'prepare-review': ('request-review', 'Return the packet here', 'assign reviewers'),
            'resolve-feedback': ('address-review', 'Return a findings ledger and draft responses here', 'resolve threads'),
            'assess-impact': ('assess-change-impact', 'Confirmed, Possible or Cleared', 'run jobs'),
            'learn-release': ('learn-after-launch', 'observed outcomes', 'message users'),
        }
        for identity, (skill, output, forbidden_action) in expected.items():
            with self.subTest(route=identity):
                route = routes[identity]
                self.assertEqual(skill, route['primary_skill'])
                self.assertEqual(['assess'], [mode['id'] for mode in route['modes']])
                mode = route['modes'][0]
                self.assertEqual(skill, mode['command_skill'])
                self.assertIn('Read-only', mode['scope'])
                for client, prompt in mode['prompts'].items():
                    with self.subTest(route=identity, client=client):
                        self.assertIn(output, prompt)
                        self.assertIn('Do not edit, run tests or builds', prompt)
                        boundary = prompt[prompt.index('Do not edit, run tests or builds'):]
                        self.assertIn(forbidden_action, boundary)
                        self.assertIn('Do not install skills, change billing, run paid evaluations, merge, deploy, or release.', prompt)
                        if client in ('antigravity', 'chatgpt', 'claude-web'):
                            self.assertTrue(prompt.startswith('In [REPOSITORY]'))

    def test_unknown_query_is_not_a_confident_match(self) -> None:
        self.assertEqual([[], [], []], search_routes([
            'purple marmalade spaceship',
            'There is a reviewer waiting elsewhere.',
            'I already checked something else.',
        ]))
