# Agent instructions

- Use English for agent instructions, code identifiers, tests, commit messages,
  and pull request titles. Use Brazilian Portuguese for user-facing text,
  README content, architecture decisions, issues, milestones, and PR descriptions.
- Read the relevant issue and architecture decisions in `docs/adr/` before making changes.
- Keep the core data model country-neutral. Treat Brazilian administrative
  divisions (UF) and IBGE identifiers as country-specific data. See ADR 0002.
- Update `pyproject.toml` and `uv.lock` together when changing Python dependencies.
- Verify API changes with `uv run --locked python -m pytest -q`.
- Report which checks ran and whether they passed.
