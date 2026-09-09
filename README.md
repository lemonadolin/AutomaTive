# PC Autopilot

Control common Windows PC actions with natural-language commands and reusable
routines — with the plan always shown **before** anything runs.

> _“Close Discord, open Steam, launch F1 25 and set volume to 40%.”_
>
> PC Autopilot turns that into a reviewable plan, waits for your confirmation,
> then executes it step-by-step with live status.

![icon](pcautopilot/resources/icon.png)

## Screenshots

**Home — type a command, review the plan before it runs:**

![Home](docs/screenshot_home.png)

**Apps — configure programs by picking their executable; live running status:**

![Apps](docs/screenshot_apps.png)

**Routines — build reusable sequences, run or test them:**

![Routines](docs/screenshot_routines.png)

**Activity — a visible log of everything that ran:**

![Activity](docs/screenshot_activity.png)

**Settings — AI provider, theme, safety, startup, history:**

![Settings](docs/screenshot_settings.png)

> **Just want the `.exe`?** See [`HOW_TO_BUILD.md`](HOW_TO_BUILD.md) for a
> no-code, click-by-click guide (GitHub builds it for you).

---

## Highlights

- **Natural-language command box** — type what you want; see the interpreted
  plan (numbered steps) with **Execute / Cancel** before it runs.
- **Reliable Windows actions** via native APIs: launch / close / restart / focus
  apps, open files / folders / URLs, set system volume, mute/unmute, per-app
  playback volume, wait (fixed or *for an app to start*), run a **pre-configured**
  command, check if an app is running.
- **Apps page** — configure applications by **picking the executable** (no
  hard-coded paths), with custom arguments, live running status, and
  launch/close buttons.
- **Routines page** — create, rename, duplicate, delete routines; add / edit /
  reorder / remove / **test** individual actions; run whole routines. Routines
  are also triggerable by name (“get my racing setup ready”).
- **Execution engine** — strictly sequential, live status
  (`✓ / → / ○ / ✗ / ⤼`), dependency-aware failure handling with
  **retry / skip / cancel**.
- **Activity page** — a visible log of every execution (time, command, steps,
  success/failure, error messages); clearable.
- **Settings** — AI provider, theme (dark default + light), confirmation
  behavior, default timeout, startup behavior, activity history, and configured
  commands.
- **Safety first** — sensitive actions (shutdown, restart, sign-out,
  force-closing apps, running commands) always require explicit confirmation.
  The parser can **never** run an arbitrary shell string.

---

## Architecture (core-first, modular)

```
natural-language text
      │
      ▼
 Interpreter (ai/)                deterministic  |  OpenAI-compatible  |  Ollama
      │  produces a structured Plan (list of Actions)
      ▼
 validate_plan (core/plan.py)     ← ALLOWLIST GATE: every action + params
      │                             checked against core/actions.ACTION_REGISTRY
      ▼
 confirmation (UI)                ← plan shown before execution; sensitive
      │                             actions always confirmed
      ▼
 ExecutionEngine (engine/)        ← sequential, live status, retry/skip/cancel
      │  dispatches ONLY allowlisted actions
      ▼
 windows_api (engine/)            ← native Win32 / Core Audio / psutil
```

Key safety property: **the interpretation layer is fully separated from
execution.** The AI/parser only ever emits a structured plan; the engine
re-validates it against a fixed allowlist and dispatches typed actions. There is
no action type that accepts a raw shell command from the model — `run_command`
takes the *name* of a command you authored yourself in Settings.

| Layer | Package | Notes |
|-------|---------|-------|
| Domain / allowlist | `pcautopilot/core/actions.py` | Action types + validation specs |
| Plan + validation | `pcautopilot/core/plan.py` | The security boundary |
| Interpreters | `pcautopilot/ai/` | Deterministic (default, offline), LLM (optional) |
| Secure credentials | `pcautopilot/ai/credentials.py` | Windows Credential Manager via `keyring` |
| Storage | `pcautopilot/storage/` | JSON in `%LOCALAPPDATA%\PC Autopilot` |
| Native ops | `pcautopilot/engine/windows_api.py` | Win32 / pycaw / psutil, graceful fallbacks |
| Execution | `pcautopilot/engine/executor.py` | Sequential engine + failure policy |
| UI | `pcautopilot/ui/` | PySide6, dark/light, 5 pages |

Adding a new PC action later = add one `ActionType` + an `ActionSpec` +
a dispatch branch in the executor + (optionally) parser phrasing. No rewrite.

---

## Running from source (any OS for the offline parts)

```bash
python -m venv .venv
# Windows:  .venv\Scripts\activate       Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt          # add -r requirements-win.txt on Windows
python -m pcautopilot
```

> The deterministic parser, routines, activity log, and full UI work
> everywhere. Native volume control and window-foregrounding require Windows
> (and `requirements-win.txt`).

---

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Covers the parser, plan validation/allowlist, the execution engine (ordering,
live status, retry/skip/cancel, dependency-aware aborts, routine + group
expansion, sensitive-action gating), LLM output parsing/filtering, and
persistence. All engine tests use a fake Windows layer, so they run on any OS.

---

## Building the Windows `.exe`

A Windows executable **must** be built on Windows — a PyInstaller build on Linux
produces a Linux binary, not a `.exe`. Two supported paths:

### 1. GitHub Actions (recommended)
`.github/workflows/build-windows.yml` runs on `windows-latest`: installs deps,
runs the test suite, packages with PyInstaller, **smoke-tests the packaged
exe**, and uploads `PCAutopilot-windows.zip` as a build artifact (and attaches
it to GitHub Releases on `v*` tags). Just push the repo.

### 2. Locally on Windows
```bat
build.bat
```
This creates a venv, installs `requirements-win.txt`, runs `pytest`, packages
with `PCAutopilot.spec`, and self-tests the result.

**Output:** `dist\PCAutopilot\PCAutopilot.exe` (single-folder build — chosen for
reliability and fewer AV false positives; no DLLs are stripped).

See [`docs/PACKAGING.md`](docs/PACKAGING.md) for details.

---

## Privacy & safety

- All automation is **visible** — plans are shown before running and logged
  afterward. No hidden persistence, keylogging, surveillance, or credential
  collection.
- API keys are stored in the **OS credential vault** (Windows Credential
  Manager), never in plain-text project or settings files.
- “Launch at sign-in” uses the visible per-user `Run` registry key and can be
  toggled off at any time.
