# Session Report — 18.04.2026

## Overview
Full frontend redesign and backend improvements to the NAO robot exercise web app: new page structure, dual navbar, Slovak localisation, AI features (calories, description, voice parsing), voice command fixes, and editor robustness.

---

## 1. App Redesign & Navigation

### Page restructure
- **Home page** (`/`) rewritten to a simple description page with 4 feature cards linking to the main sections
- **Simple Upload** (`/upload`) — video/image upload moved to its own dedicated page
- **Voice Command** (`/voice`) — voice commander moved to its own page
- **Exercises Store** (`/exercises`) — new page listing all saved exercises
- **Editor** (`/edit`) — existing editor kept, added to navbar
- Legacy `/exercise` and `/group` pages kept but hidden from navigation

### Dual navbar
- **PC sidebar** (`sideNav.tsx`) — `hidden md:flex`, left-side vertical nav with active state highlighting; items: Domov, Nahranie, Hlasové príkazy, Cvičenia, Editor
- **Mobile bottom nav** (`bottomNav.tsx`) — `md:hidden`, 5 icons sized to fit; always visible including on the editor page (fixed previous bug where it was hidden)

---

## 2. Exercises Store
- New page listing all saved exercises from `GET /exercise/list`
- Per-exercise: inline rename with pencil icon, Open (→ `/edit?id=<id>`), Run on robot, Delete with confirmation
- Shows frame count, date, calorie estimate with "Odhad AI" badge, and AI-generated description

---

## 3. Editor Improvements

### FPS and max frames controls
- Added two number inputs above the upload zone: **Snímky za sekundu** (default 1) and **Max snímok** (default 8)
- Parameters are sent to the backend as `fps` and `max_frames` in the upload FormData
- Fixed stale closure bug — `handleUpload` deps include `[fps, maxFrames]`
- Fixed hardcoded 8-frame limit in `skeletonFinderAPI` (`if processed > 6: break` removed)
- Backend (`nao_pose_service.py`) updated to read and apply `max_frames`

### Exercise naming
- Inline rename directly in the editor header — pencil icon on hover, Enter to confirm, Escape to cancel
- Saved via `PUT /exercise/<id>/config`

### Insert pose from dropdown
- Each FrameCard has **Pred** and **Za** dropdowns listing all available poses from the registry
- Selecting a pose inserts it at that position via `POST /exercise/<id>/frame/from_pose`
- Mobile: compact inline selects; Desktop: labelled column layout
- Pose names shown in Slovak (`Drep`, `Úklon`, `T-Póza`, etc.)

### Pose images from registry
- Frames inserted from the pose registry display the pose image from `/pose/<name>/image` (served by `voiceCommandAPI`) as fallback when no frame image exists
- Images available for: `wave`, `stand`, `sit`, `hands_up`, `t_pose`, `bow`, `crouch`
- `point_right` / `point_left` fall back gracefully to placeholder icon
- Fixed persistence bug: pose name was stored in `keypoints.pose_name` but `loadFrames` only checked `f.pose_name` — added `f.keypoints?.pose_name` fallback so images survive page reload

### Auto-save drag reorder
- Dragging frames to reorder auto-saves the new sequence immediately
- Implemented via `onReorder` callback in `useDragReorder` hook, called synchronously inside `setItems` with the new array to avoid stale closure

### Angle tooltip
- Joint angles shown as hover tooltip (scrollable popup) instead of always-visible data
- 120ms hide delay via `useRef` timer so the popup doesn't vanish when moving mouse from trigger to popup

---

## 4. Voice Command Page

### Slovak speech recognition
- `rec.lang = "sk-SK"` set on the SpeechRecognition instance
- Slovak aliases added for all poses (`drep`, `stoj`, `zamávaj`, `ruky hore`, etc.)
- Mic icon fixed (was black on dark background) — added `text-white` class

### GPT interpretation
- Replaced keyword-matching with a GPT API call after the mic stops
- GPT maps the transcript to correct backend command keys, handling garbled speech (e.g. "tipos" → `t_pose`, "depóza" → `t_pose`)
- `isInterpreting` spinner shown while GPT processes; execute button disabled during interpretation

### Pose display names in Slovak
- `DISPLAY_NAMES` updated: Wave→Zamávaj, Stand→Stoj, Sit→Sed, Hands Up→Ruky hore, T-Pose→T-Póza, Bow→Úklon, Crouch→Drep, Point Right→Ukáž vpravo, Point Left→Ukáž vľavo

---

## 5. Voice Edit Panel (Editor)

- AI-assisted voice editing of exercise frame sequences
- User speaks (e.g. "vlož drep za snímku 3") → GPT parses pose, frame number, and side (before/after)
- **`pick_pose` phase**: when speech recognition garbles the pose name (e.g. "vložte póze" — "t" absorbed into "vložte"), GPT still extracts frame+side and shows an amber dropdown for the user to pick the pose manually
- Fixed bug: prompt said `{"error": "reason"}` so GPT returned the literal word "reason" — fixed to proper Slovak error text
- System prompt includes Slovak→key hints for all poses and side words (`pred→before`, `za/po→after`)
- Confirmation box shows Slovak pose display names

---

## 6. Nginx Routing Fix for Voice Commands
- `POST /api/command` was routing to `translatorapi` (404) — voice commands never reached the robot; failed instantly making it appear the system wasn't waiting between poses
- Added `location = /command` pointing to `voicecommandapi:8000/command` with `proxy_read_timeout 30s`
- Fixed frontend URL from `/api/command` to `/command`

---

## 7. Robot Execution Analysis
- Confirmed the full pipeline is sequential and blocking:
  - NAO SDK `angleInterpolation(..., True)` blocks until motion completes (~3s/pose)
  - `voiceCommandAPI` awaits NAO response before returning
  - Exercise run loops frames sequentially, one pose at a time
- Root cause of "not waiting" appearance was the 404 routing bug above

---

## 8. AI Calorie Estimation
- `estimateCalories()` runs on exercise load if no estimate is saved
- Sends joint range-of-motion summary to GPT → returns kcal rounded to one decimal
- Persisted to `config.json`, shown in editor header and exercises store with "Odhad AI" badge
- Backend (`storage.py`, `routes/exercise.py`) updated to store and return `calories`

---

## 9. AI-Generated Exercise Description
- `generateDescription()` runs on exercise load if no description is saved
- GPT writes a 1–2 sentence Slovak description of what the exercise looks like and which body parts it involves
- **Regenerates automatically** when a frame is inserted or deleted
- Shown below the exercise name in the editor and as a subtitle in the exercises store
- Fixed white page crash: `generateDescription` was declared after `insertPose`/`deleteFrame` which referenced it in `useCallback` deps arrays — caused a JavaScript temporal dead zone `ReferenceError` on render; fixed by moving the declaration before those hooks

---

## 10. Slovak Localisation
- All UI text across the app translated to Slovak:
  - `ExerciseEditor.tsx`: loading spinner, frame count, empty state, AnglesTooltip, FrameCard labels, VoiceEditPanel
  - `voiceCommander.tsx`: all labels and status text
  - `exercisesStore.tsx`, `mainPage.tsx`, `simpleUploadPage.tsx`, `voiceCommandPage.tsx`, `sideNav.tsx`

---

## Files Modified
| File | Change |
|---|---|
| `web/src/components/main/ExerciseEditor.tsx` | FPS/max frames, insert pose, auto-save reorder, angle tooltip, naming, calorie + description AI, VoiceEditPanel, Slovak translation, crash fix |
| `web/src/components/main/voiceCommander.tsx` | GPT interpretation, Slovak names + aliases, mic icon fix, routing fix |
| `web/src/components/layout/sideNav.tsx` | New PC sidebar nav |
| `web/src/components/layout/bottomNav.tsx` | Mobile bottom nav, always visible, 5 items |
| `web/src/pages/mainPage.tsx` | Rewritten as description/landing page |
| `web/src/pages/exercisesStore.tsx` | New exercises store page |
| `web/src/pages/simpleUploadPage.tsx` | New simple upload page |
| `web/src/pages/voiceCommandPage.tsx` | New voice command page |
| `web/src/App.tsx` | Both navbars, updated routes |
| `web/nginx-conf/default.conf` | `/command` route, 30s timeout |
| `exerciseConfigService/app/storage.py` | `calories` and `description` fields |
| `exerciseConfigService/app/routes/exercise.py` | Accept `calories` and `description` in PUT /config |
| `translator/nao_pose_service.py` | Read and apply `max_frames` param |
| `skeletonFinderAPI/.../pose_estimation_mediapipe.py` | Remove hardcoded 8-frame cap |
