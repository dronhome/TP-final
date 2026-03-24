# ExerciseConfigService — Progress Report 17 03

**Project:** NAO Social Robot Exercise Control System  
**Status:** Service scaffolded, architecture finalized, Docker environment configured

---

## Current work

The main new addition to the existing system is the **ExerciseConfigService** — a dedicated storage and configuration microservice that decouples exercise data from the orchestration logic.

---

## What Is Done

### Architecture Design
- Finalized a 4-service microservices architecture
- Defined clear responsibility boundaries for each service
- Decided that `translatorAPI` is the **sole orchestrator and single entry point** for the frontend — no other service is exposed to the web layer directly
- Designed the full communication flow for both the upload path and the run path

### ExerciseConfigService — Created
- Flask application scaffolded with app factory pattern (`create_app`)
- `storage.py` written — single module owning all filesystem logic (path helpers, JSON read/write, exercise and frame operations)
- `health.py` route — `GET /health` endpoint that confirms the service is alive and reports how many exercises are stored
- `run.py` entry point — supports both `python run.py` (local dev) and `gunicorn` (Docker)
- `exercise/*` route - endpoints to work with /exercises (create, get, delete, update)
- `Dockerfile` written — Python 3.11 slim, gunicorn, exercises folder created inside `/service/exercises`
- `requirements.txt` — Flask 3.0.3 + gunicorn

### Docker Environment
- `docker-compose.dev.yml` updated — `exerciseconfigservice` added as a proper service on port `7001`, with `env_file`, environment variables, and network config matching the rest of the stack
- `docker-compose.build.yml` updated — `exercise-config-service` added for CI/CD image builds
- `translatorAPI` `depends_on` updated to include `exerciseconfigservice`
- All inter-service URLs configured via environment variables (`SKELETON_API_URL`, `NAO_API_URL`, `EXERCISE_CONFIG_URL`) — no hardcoded addresses

### Storage Design
- Finalized on-disk structure for exercises (see below)
- Designed `config.json` schema including `frame_sequence` for reordering/replaying frames
- Each frame stored as a separate `frame_NNN.json` file containing both raw keypoints and computed NAO angles

---

## System Architecture

### Services

| Service | Internal Port | Host Port | Role |
|---|---|---|---|
| `naorobotapi` | 5000 | 8001 | Controls physical NAO robot joints |
| `skeletonfinderapi` | 6001 | 8002 | Extracts pose keypoints from media (MediaPipe / YOLO) |
| `translatorapi` | 7000 | 8003 | Orchestrator — sole frontend entry point |
| `exerciseconfigservice` | 7001 | 8004 | Storage — exercises, frames, configs |

All services communicate over the internal Docker network `appnet` using container names as hostnames.

### Communication Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND / WEB UI                    │
│              talks ONLY to translatorapi                │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP :7000
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    translatorapi                        │
│              Orchestrator — single entry point          │
└──────┬──────────────────┬──────────────────┬────────────┘
       │                  │                  │
       │ HTTP             │ HTTP             │ HTTP
       ▼                  ▼                  ▼
┌─────────────┐  ┌─────────────────┐  ┌─────────────────┐
│skeletonfinder│  │exerciseconfig   │  │  naorobotapi    │
│api  :6001   │  │service  :7001   │  │     :5000       │
│             │  │                 │  │                 │
│ MediaPipe / │  │ Stores & serves │  │ Executes joint  │
│ YOLO pose   │  │ exercises,      │  │ angles on NAO   │
│ estimation  │  │ frames, configs │  │ robot hardware  │
└─────────────┘  └─────────────────┘  └─────────────────┘

  ← nobody calls these services except translatorapi →
```

### Upload Flow (after redesign)

```
1. Frontend  →  POST /upload                   (translatorapi)
2. translator  →  POST /pose_from_video        (skeletonfinderapi)
                      returns keypoints per frame
3. translator  converts keypoints → NAO joint angles
4. translator  →  POST /exercise/create        (exerciseconfigservice)
                      saves frames + config to disk
5. translator  →  returns exercise ID          (frontend)
```

### Run Flow

```
1. Frontend  →  POST /exercise/{id}/run        (translatorapi)
2. translator  →  GET /exercise/{id}/frames    (exerciseconfigservice)
                      returns frames in frame_sequence order
3. translator  loops over frames × repetitions:
                  POST /setting_pose/setPose   (naorobotapi)
                      {"angles": [f1, f2, f3, f4, f5, f6, f7, f8]}
```

---

## Exercise Storage Structure

Exercises are stored on disk inside the `exerciseconfigservice` container at `/service/exercises`.

```
/service/exercises/
└── a3f9c1d2/                    ← exercise ID (8-char hex)
    ├── config.json
    ├── media/
    │   └── original.mp4         ← original uploaded file
    └── frames/
        ├── frame_000.json
        ├── frame_001.json
        └── frame_002.json
```

### `config.json`

```json
{
  "id": "a3f9c1d2",
  "name": "Arm Wave",
  "created_at": "2026-03-16T12:00:00",
  "pose_engine": "mediapipe",
  "repetitions": 3,
  "frame_sequence": [0, 1, 2, 1, 0]
}
```

**`frame_sequence`** is the key field — it defines playback order independently of the files on disk. This allows:
- Reordering frames without touching files
- Repeating a single frame multiple times: `[0, 1, 1, 1, 2]`
- Reversing an exercise: `[4, 3, 2, 1, 0]`
- Inserting a shared "rest" frame between moves

### `frame_NNN.json`

```json
{
  "frame_index": 0,
  "keypoints": {
    "left_shoulder": [0.45, 0.32, 0.01],
    "right_shoulder": [0.55, 0.32, 0.01],
    "left_elbow": [0.38, 0.50, -0.02],
    "right_elbow": [0.62, 0.50, -0.02]
  },
  "nao_angles": [0.1, -0.2, 0.5, 1.0, -0.1, 0.3, -0.4, 0.8]
}
```

Joint angle order: `LShoulderPitch, LShoulderRoll, LElbowRoll, LElbowYaw, RShoulderPitch, RShoulderRoll, RElbowRoll, RElbowYaw`

Both `keypoints` and `nao_angles` are stored per frame so that angles can be recomputed from keypoints in future without re-uploading media.

---

## Planned API Endpoints (ExerciseConfigService)

These are designed but not yet implemented — CRUD implementation is pending a decision on scope.

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` |  service health + exercise count |
| `POST` | `/exercise/create` | Create exercise from frames + media |
| `GET` | `/exercise/list` | List all exercises (id, name, frame count) |
| `GET` | `/exercise/<id>` | Full exercise detail + config |
| `PUT` | `/exercise/<id>/config` | Update name, repetitions |
| `GET` | `/exercise/<id>/frames` | All frames in sequence order |
| `PUT` | `/exercise/<id>/sequence` | Replace `frame_sequence` (reorder/repeat/remove) |
| `GET` | `/exercise/<id>/frame/<idx>` | Get one frame |
| `PUT` | `/exercise/<id>/frame/<idx>` | Edit one frame's angles manually |
| `POST` | `/exercise/<id>/frame` | Add a new frame |
| `DELETE` | `/exercise/<id>/frame/<idx>` | Remove a frame |
| `DELETE` | `/exercise/<id>` | Delete entire exercise |

---

## Open Questions

- **CRUD scope** — decide which endpoints are actually needed for the first working version vs. later
- **translatorAPI redesign** — upload and run endpoints need to be updated to call `exerciseconfigservice` instead of going directly to `naorobotapi`
- **Frame extraction rate** — currently configurable per upload (`number_frames_per_sec`), needs to be stored in `config.json` for reference
- **Media storage** — original files are stored but not yet served back; may need a `GET /exercise/<id>/media` endpoint for the frontend preview