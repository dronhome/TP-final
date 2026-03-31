# Integration Plan — TranslatorAPI ↔ ExerciseConfigService
**Date:** 27 03 2026
**Status:** Done

---

## Context

`exerciseconfigservice` is fully built and tested in isolation (all CRUD endpoints work, media storage works, volume mount works).
`translatorapi` is the sole orchestrator and the only service the frontend talks to.

The goal is to wire them together so the full upload → save → run flow works end to end.

---

## What Was Done

### 1. Added `EXERCISE_CONFIG_URL` to TranslatorAPI ✓

Added to `nao_pose_service.py`:
```python
EXERCISE_CONFIG_URL = os.environ.get("EXERCISE_CONFIG_URL", "http://exerciseconfigservice:7001")
```

Added to `docker-compose.dev.yml` under `translatorapi` environment and `depends_on`.

---

### 2. New TranslatorAPI Endpoints ✓

#### `POST /exercise/from_video` — implemented
```
1. Receive multipart: file="video", fps=1, seconds=-1, name="Exercise Name"
2. Call process_video_bytes → skeletonfinderapi (base64 POST) → valid landmarks[]
3. For each frame: translate_arms(landmarks) → nao_angles
4. POST exerciseconfigservice /exercise/create with frames + raw video bytes
5. Return: exercise config (id, name, frame_sequence, ...)
```

#### `POST /exercise/from_image` — implemented
```
1. Receive multipart: file="image", name="Exercise Name"
2. POST skeletonfinderapi /pose_from_image (base64) → landmarks
3. translate_arms(landmarks) → nao_angles
4. POST exerciseconfigservice /exercise/create with single frame + raw image bytes
5. Return: exercise config
```

#### `POST /exercise/<id>/run` — implemented
```
1. Receive: {repetitions: N}  (optional — defaults to value stored in config)
2. GET exerciseconfigservice /exercise/<id>/frames  → frames in frame_sequence order
3. GET exerciseconfigservice /exercise/<id>         → config (repetitions)
4. Loop repetitions × frames:
       POST naorobotapi /setting_pose/setPose  {"angles": frame["nao_angles"]}
5. Return: {exercise_id, repetitions, frames_per_rep, total_poses_sent, results[]}
```

#### Proxy CRUD endpoints — implemented ✓

| TranslatorAPI endpoint | Forwards to ExerciseConfigService |
|---|---|
| `GET /exercise/list` | `GET /exercise/list` |
| `GET /exercise/<id>` | `GET /exercise/<id>` |
| `DELETE /exercise/<id>` | `DELETE /exercise/<id>` |
| `PUT /exercise/<id>/config` | `PUT /exercise/<id>/config` |
| `GET /exercise/<id>/frames` | `GET /exercise/<id>/frames` |
| `PUT /exercise/<id>/sequence` | `PUT /exercise/<id>/sequence` |

---

### 3. Updated `docker-compose.dev.yml` ✓

- Added `EXERCISE_CONFIG_URL: http://exerciseconfigservice:7001` to `translatorapi` environment
- Added `exercise-config-service` to `translatorapi` `depends_on`
- Added `./data/exercises:/service/exercises` volume mount to `exercise-config-service` so exercises persist on the host at `data/exercises/`

---

### 4. Tests ✓

**Location:** `team-19-social-robot/translator/tests/`

#### `test_arms_translator.py` — 19 unit tests, all passing
- `compute_shoulder_pitch`: arm down → positive, arm up → negative, within NAO limits
- `compute_shoulder_roll`: arm down → ~0, arm sideways → near max, sign per side
- `compute_elbow_roll_2d`: straight → 30°, bent → 88.5°, sign per side
- `compute_elbow_yaw`: always -1.3 (L) / +1.3 (R)
- `translate_arms`: all 8 named keys present, angles array = 22 elements, legs/head = 0.0, missing landmark → KeyError

#### `test_routes.py` — 17 unit tests with mocked services, all passing
- `/arms/from_landmarks`: valid → 200, missing joint → 400, no body → 400
- `/exercise/from_image`: success → 201, no file → 400, incomplete pose → 422
- `/exercise/from_video`: success → 201, no valid frames → 422, no file → 400
- `/exercise/<id>/run`: success → correct counts, repetitions override, not found → 404
- Proxy routes: list, get, delete, get frames

#### `test_integration.py` — 11 end-to-end tests against live services, all passing
- Health check, create from image, create from video, list, get detail, get frames, run image exercise, run video exercise (8 frames), update config, delete
- Uses real `frame_5.jpg` and `video_2.mp4`
- NAO robot not required — run endpoint reports per-frame errors gracefully

**Run all tests:**
```bash
cd team-19-social-robot/translator
python3 -m pytest tests/ -v
```

**Run integration tests only (requires services up):**
```bash
python3 -m pytest tests/test_integration.py -v -s
```

---

## Decisions on Open Questions

1. **Running the robot** — same logic as the existing `/arms/from_image` flow (call `naorobotapi /setting_pose/setPose`), but now frames come from `exerciseconfigservice` instead of being computed on the fly. No changes to how the robot is called.

2. **Media storage** — no shared volume. Translator passes raw video/image bytes to `exerciseconfigservice` via HTTP (multipart). `exerciseconfigservice` owns the file and saves it inside the exercise directory. Already works today.

3. **Skeletonfinderapi** — use POST with base64 body, same as the working curl commands. No file_location path sharing needed.

4. **Frontend** — not in scope. Backend only.
