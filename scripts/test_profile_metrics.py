"""Regression checks for data completeness, streak boundaries and failed updates."""

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import update_profile as profile


class ProfileMetricsTests(unittest.TestCase):
    def test_daily_counts_are_joined_by_id_and_trimmed_after_today(self):
        parser = profile.CalendarParser()
        parser.feed("""
          <h2 id="js-contribution-activity-description">3 contributions in 2028</h2>
          <div data-graph-url="/users/jamshid-muxsinov/contributions"><table>
            <td id="contribution-day-b" data-date="2028-01-02" data-level="1"></td>
            <td id="contribution-day-a" data-date="2028-01-01" data-level="4"></td>
          </table></div>
          <tool-tip for="contribution-day-a">2 contributions on January 1st.</tool-tip>
          <tool-tip for="contribution-day-b">1 contribution on January 2nd.</tool-tip>
        """)
        self.assertEqual(parser.days(date(2028, 1, 1)), [
            {"date": "2028-01-01", "count": 2, "level": 4},
        ])
        parser.heading = "4 contributions in 2028"
        with self.assertRaisesRegex(ValueError, "disagrees"):
            parser.days(date(2028, 1, 1))
        del parser.tips["contribution-day-b"]
        with self.assertRaisesRegex(ValueError, "tooltips"):
            parser.days(date(2028, 1, 1))

    def test_leap_day_must_be_present_exactly_once(self):
        start, end = date(2028, 1, 1), date(2028, 3, 1)
        days = [{"date": str(start + i * profile.ONE_DAY), "count": 0, "level": 0}
                for i in range((end - start).days + 1)]
        profile.validate_days(days, end)
        days[-2] = days[-3].copy()
        with self.assertRaises(ValueError):
            profile.validate_days(days, end)

    def test_cross_year_streak_and_grace_for_today(self):
        prior = {"days": 2, "start": "2025-12-30", "end": "2025-12-31"}
        history = {"ending": prior, "longest": prior}
        days = [{"date": "2026-01-01", "count": 3}, {"date": "2026-01-02", "count": 0}]
        result = profile.streaks(days, history)
        self.assertEqual(result["current"], {"days": 3, "start": "2025-12-30", "end": "2026-01-01"})
        self.assertEqual(result["longest"], result["current"])
        self.assertEqual(profile.streaks(days, history, allow_today=False)["current"], profile.empty_streak())
        days.append({"date": "2026-01-03", "count": 0})
        self.assertEqual(profile.streaks(days, history)["current"], profile.empty_streak())

    def test_history_cache_expires_and_resets_at_year_boundary(self):
        created, today = date(2025, 1, 1), date(2026, 7, 30)
        cache = {"through": "2025-12-31", "checked_on": "2026-07-24",
                 "ending": profile.empty_streak(), "longest": profile.empty_streak()}
        with patch.object(profile, "read_calendar", return_value=[]) as fetch:
            self.assertIs(profile.history_before_year(created, today, cache), cache)
            fetch.assert_not_called()
            profile.history_before_year(created, date(2026, 7, 31), cache)
            fetch.assert_called_once_with(date(2025, 12, 31))
            fetch.reset_mock()
            cache["checked_on"] = "2026-12-31"
            profile.history_before_year(created, date(2027, 1, 1), cache)
            self.assertEqual([call.args[0].year for call in fetch.call_args_list], [2025, 2026])

    def test_pagination_and_incomplete_commit_search(self):
        def repos(stars, more):
            return {"totalCount": 2, "nodes": [{"stargazerCount": stars}],
                    "pageInfo": {"hasNextPage": more, "endCursor": "A" if more else None}}
        base = {"user": {"login": profile.LOGIN, "createdAt": "2025-01-01T00:00:00Z",
                         "repositories": repos(3, True), "repositoriesContributedTo": {"totalCount": 1}},
                "prs": {"issueCount": 0}, "issues": {"issueCount": 0}}
        tail = {"user": {"repositories": repos(7, False)}}
        with patch.object(profile, "graphql", side_effect=[base, tail, base, tail]), \
             patch.object(profile, "api", side_effect=[{"total_count": 0, "incomplete_results": False},
                                                       {"total_count": 0, "incomplete_results": True}]):
            self.assertEqual(profile.github_metrics(date(2026, 1, 2))[1]["stars"], 10)
            with self.assertRaisesRegex(ValueError, "partial"):
                profile.github_metrics(date(2026, 1, 2))

    def test_remote_failure_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            (output / "snapshot.json").write_text(json.dumps({"sample": True}))
            (output / "statistics.svg").write_text("old image")
            with patch.object(profile, "OUTPUT", output), patch.object(sys, "argv", ["refresh"]), \
                 patch.object(profile, "fetch", side_effect=OSError("offline")) as fetch, \
                 patch("time.sleep"), self.assertRaisesRegex(SystemExit, "Previous images retained"):
                profile.main()
            self.assertEqual(fetch.call_count, 3)
            self.assertEqual((output / "statistics.svg").read_text(), "old image")
            self.assertEqual(json.loads((output / "snapshot.json").read_text()), {"sample": True})

    def test_checked_in_snapshot_reproduces_images_and_text(self):
        source = json.loads((profile.OUTPUT / "snapshot.json").read_text())
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            profile.write_snapshot(source, output)
            summary = (output / "summary.md").read_text()
            self.assertIn(f"| Total contributions | {source['metrics']['contributions']} |", summary)
            self.assertIn(source["as_of"], summary)
            for file in output.iterdir():
                self.assertEqual(file.read_bytes(), (profile.OUTPUT / file.name).read_bytes())


if __name__ == "__main__":
    unittest.main()
