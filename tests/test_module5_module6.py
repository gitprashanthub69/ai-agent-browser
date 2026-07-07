from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from final_project.module5_cross_module.command_parser import parse_command, is_cross_module
from final_project.module6_memory import memory_store


def test_parse_command_creates_multi_step_plan():
    steps = parse_command(
        "Apply to this internship, add deadline to calendar, email my mentor I applied"
    )

    assert len(steps) >= 3
    assert any(step["module"] == "form" for step in steps)
    assert any(step["module"] == "calendar" for step in steps)
    assert any(step["module"] == "email" for step in steps)
    assert is_cross_module("Apply to this internship and email my mentor")


def test_memory_store_persists_notes(tmp_path, monkeypatch):
    monkeypatch.setattr(memory_store, "DB_PATH", tmp_path / "memory.db")
    memory_store.init_db()

    note_id = memory_store.save_note("Applied to internship", title="internship")
    assert note_id > 0

    notes = memory_store.get_notes(limit=5)
    assert any(note["content"] == "Applied to internship" for note in notes)

    search_results = memory_store.search_history("internship")
    assert any(result["content"] == "Applied to internship" for result in search_results)
