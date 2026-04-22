"""Shape tests for Claude Skills — ensures each SKILL.md is well-formed."""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

SKILLS_DIR = Path(__file__).resolve().parents[1] / "src" / "aichesscoach" / "skills"


def _skill_dirs() -> list[Path]:
    return sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())


def _split_frontmatter(text: str) -> tuple[str, str]:
    assert text.startswith("---\n"), "SKILL.md must start with a YAML frontmatter block"
    _, frontmatter, body = text.split("---\n", 2)
    return frontmatter, body


@pytest.fixture(params=_skill_dirs(), ids=lambda p: p.name)
def skill_dir(request: pytest.FixtureRequest) -> Path:
    return request.param


def test_skill_md_exists(skill_dir: Path) -> None:
    assert (skill_dir / "SKILL.md").is_file()


def test_skill_frontmatter_has_required_fields(skill_dir: Path) -> None:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    frontmatter, _ = _split_frontmatter(text)
    data = yaml.safe_load(frontmatter)
    assert isinstance(data, dict)
    assert isinstance(data.get("name"), str) and data["name"]
    assert isinstance(data.get("description"), str) and data["description"]


def test_skill_body_not_empty(skill_dir: Path) -> None:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    _, body = _split_frontmatter(text)
    assert body.strip(), "SKILL.md body must not be empty"
