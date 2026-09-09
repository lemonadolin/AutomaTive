# How to get the PC Autopilot `.exe`

You do **not** need to be a developer. Pick whichever route fits you.

---

## Route 1 — Let GitHub build it for you (recommended, no tools needed)

This uses the build automation already included in this project
(`.github/workflows/build-windows.yml`). GitHub compiles the real Windows
`.exe` on its own Windows servers.

### Step 1 — Create a repository
1. Go to <https://github.com/new>.
2. Type any **Repository name** (e.g. `pc-autopilot`).
3. Leave it Public or Private — either works.
4. Click **Create repository**.

### Step 2 — Upload the project
On the new empty repo page:
1. Click the link **“uploading an existing file”** (or **Add file ▸ Upload files**).
2. Unzip `PCAutopilot-source.zip` on your computer.
3. Select **all** the files/folders inside and drag them into the browser.
4. Scroll down, click **Commit changes**.

> Tip: make sure the hidden `.github` folder gets uploaded — it contains the
> build recipe. If drag-and-drop skips it, use Route 2 (git), which always
> includes it.

### Step 3 — Wait for the build
1. Click the **Actions** tab at the top of your repo.
2. You'll see a run called **“Build Windows EXE”** with a spinning yellow dot.
3. Wait ~3–5 minutes for it to turn into a green ✓.

### Step 4 — Download the `.exe`
1. Click the finished run.
2. Scroll to the **Artifacts** section at the bottom.
3. Download **`PCAutopilot-windows`** — it's a zip.
4. Unzip it, open the `PCAutopilot` folder, and **double-click `PCAutopilot.exe`**.

That's it. It runs on any Windows 10/11 PC — no Python required.

---

## Route 2 — Push with git (also uses the included history)

This project is already a committed git repository, so:

```bash
cd pc_autopilot
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git branch -M main
git push -u origin main
```

If git asks for a password, paste a GitHub token **into that terminal prompt
only** (never into a webpage or chat). Then follow **Step 3 & 4** above to grab
the `.exe` from the Actions tab.

---

## Route 3 — Build locally on a Windows PC

If you have a Windows PC with Python 3.10–3.12:

1. Unzip the project.
2. Double-click **`build.bat`** (or run it from a terminal).
3. It installs everything, runs the tests, and produces:
   `dist\PCAutopilot\PCAutopilot.exe`

---

## After you have it running

1. **Apps** page → **+ Add App** → **Browse…** and pick each program's `.exe`
   (e.g. `Discord.exe`, `steam.exe`, `F1_25.exe`). One-time setup.
2. **Home** page → type e.g.
   *“Close Discord, open Steam, launch F1 25 and set volume to 40%”* →
   **Interpret** → review the plan → **Execute**.
3. **Routines** page → build reusable sequences, then trigger them by name:
   *“get my racing setup ready.”*
4. **Activity** page → see everything that ran.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| No **Actions** run appears | The `.github/workflows/` folder didn't upload. Use Route 2 (git), or re-upload including hidden folders. |
| Build fails on `pytest` | Read the failing test in the Actions log; the build intentionally stops if tests fail. |
| Windows SmartScreen warning on first run | The `.exe` is unsigned. Click **More info ▸ Run anyway** (code-signing needs a paid certificate). |
| Volume/foreground actions do nothing | Ensure you built with `requirements-win.txt` (Route 1 and `build.bat` do this automatically). |
| “App has no configured executable” | Add the app on the **Apps** page and pick its `.exe` first. |
