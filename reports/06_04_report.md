# Report — 06.04.2026

## Overview

Testing and integration session. All existing services were verified, two new features were added, and everything was committed to a new branch `kandr-2`.

---

## 1. Environment Setup

- Project running on Ubuntu VM with Docker
- Robot (NAO/Choregraphe) on localhost (`127.0.0.1:9559`)
- Services started via `docker compose -f docker-compose.dev.yml up -d`
- **Issue found:** `exercise-config-service` volume was mounted from VMware shared folder (`/mnt/hgfs/`) which Docker containers cannot write to (permission denied)
- **Fix:** Volume remounted from local Ubuntu path `/home/ubuntu/exercises` instead

---

## 2. Testing

All 47 tests run and passing.

### Unit Tests — `test_arms_translator.py` (19 tests)
Mathematical translation from human body landmarks to NAO joint angles:
- Shoulder pitch/roll, elbow roll/yaw calculations
- Limit enforcement, sign correctness per side
- Full `translate_arms()` output (22-angle array, legs/head zero)
- Missing landmark error handling

### Route Tests — `test_routes.py` (17 tests)
HTTP endpoints with mocked external services:
- Health check, `/arms/from_landmarks`, `/exercise/from_image`, `/exercise/from_video`
- Exercise run with repetitions override
- Proxy routes to exerciseConfigService

### Integration Tests — `test_integration.py` (11 tests)
End-to-end against live containers:
- **Issue found:** Translator container was running an old pulled image from Docker Hub, missing the `/exercise/*` routes
- **Fix:** Rebuilt translator image from local source
- All 11 tests passing after fix: health, create from image/video, list, get, frames, run, update config, delete

---

## 3. New Features

### 3.1 voiceCommandAPI Integration

Pulled `voiceCommandAPI` from `kandr` branch into `kandr-2`.

The service receives a pose name and sends hardcoded joint angles directly to the NAO robot. Supported poses: `stand`, `t_pose`, `hands_up`, `sit`, `wave`, `bow`, `crouch`, `point_right`, `point_left` plus aliases.

**New endpoint added to voiceCommandAPI:**
```
GET /pose/<name>
```
Returns pose angles and description without executing on the robot. Used by other services to look up pose data.

**Added to docker-compose:** `voicecommandapi` service on port `8000`.

---

### 3.2 Insert Pose from Registry into Exercise

New endpoint in `exerciseConfigService`:
```
POST /exercise/<id>/frame/from_pose
Body: { "pose_name": "wave", "position": 2 }
```

Flow:
1. Calls `voiceCommandAPI GET /pose/<name>` to get angles
2. Inserts a new frame at the specified position in the exercise's `frame_sequence`
3. Returns the inserted frame with pose name and description

New `insert_frame()` function in `storage.py` handles writing the frame file and inserting its index at the correct position in `frame_sequence` (clamped to valid range).

---

### 3.3 Per-Frame Images for Video Exercises

When a video is processed, skeleton visualization images (PNG with pose overlay) are now stored per frame and served via API.

**New endpoints in `exerciseConfigService`:**
```
GET  /exercise/<id>/frame/<idx>/image   → returns PNG image
POST /exercise/<id>/frame/<idx>/image   → upload PNG image
```

**Translator change:** `exercise_from_video` now enables `attach_visualization=True` when calling the skeleton finder. After the exercise is created, frame images are uploaded to `exerciseConfigService` (best-effort, does not fail the request if image upload fails).

Images are stored at: `/service/exercises/{id}/frames/frame_000.png`

---

## 4. API Summary

| Method | URL | Service | Description |
|--------|-----|---------|-------------|
| GET | `/pose/<name>` | voicecommandapi:8000 | Get pose angles without executing |
| GET | `/commands` | voicecommandapi:8000 | List all poses and aliases |
| POST | `/exercise/<id>/frame/from_pose` | exerciseconfigservice:7001 | Insert pose from registry at position |
| GET | `/exercise/<id>/frame/<idx>/image` | exerciseconfigservice:7001 | Get frame PNG image |
| POST | `/exercise/<id>/frame/<idx>/image` | exerciseconfigservice:7001 | Upload frame PNG image |

---

## 5. Git

All changes committed and pushed to branch `kandr-2` on GitHub.

```
commit 3493761
Branch: kandr-2
Files changed: 10
```
