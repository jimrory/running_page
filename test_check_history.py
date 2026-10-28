"""Verify the guard protects irreplaceable history without blocking new runs."""

import importlib
import sqlite3
from pathlib import Path

import pytest


@pytest.fixture
def history(monkeypatch, tmp_path):
    monkeypatch.syspath_prepend(str(Path(__file__).parent / "run_page"))
    guard = importlib.import_module("check_history")
    database = tmp_path / "history.db"
    monkeypatch.setattr(guard, "SQL_FILE", str(database))
    return guard, database, tmp_path / "snapshot.json"


def run_guard(monkeypatch, guard, mode, snapshot):
    monkeypatch.setattr("sys.argv", ["check_history", mode, str(snapshot)])
    guard.main()


def test_missing_database_is_not_created(history):
    guard, database, _ = history
    with pytest.raises(sqlite3.OperationalError):
        guard.activity_ids()
    assert not database.exists()


def test_empty_database_is_rejected(history):
    guard, database, _ = history
    with sqlite3.connect(database) as db:
        db.execute("CREATE TABLE activities (run_id INTEGER PRIMARY KEY)")
    with pytest.raises(RuntimeError, match="empty"):
        guard.activity_ids()


def test_new_runs_allowed_but_removed_history_rejected(history, monkeypatch):
    guard, database, snapshot = history
    with sqlite3.connect(database) as db:
        db.execute("CREATE TABLE activities (run_id INTEGER PRIMARY KEY)")
        db.executemany("INSERT INTO activities VALUES (?)", [(1,), (2,)])
    run_guard(monkeypatch, guard, "snapshot", snapshot)
    with sqlite3.connect(database) as db:
        db.execute("INSERT INTO activities VALUES (3)")
    run_guard(monkeypatch, guard, "verify", snapshot)
    with sqlite3.connect(database) as db:
        db.execute("DELETE FROM activities WHERE run_id = 1")
    with pytest.raises(RuntimeError, match="historical IDs missing"):
        run_guard(monkeypatch, guard, "verify", snapshot)
