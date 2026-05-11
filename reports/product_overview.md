# NAO Cvičenia — Product & System Overview

## What it is

NAO Cvičenia is a web-based tool that lets therapists, caregivers, or gym instructors create physical exercise routines and have a humanoid NAO robot perform them live — so seniors or patients can follow along with a real robot instead of a screen or a person.

## The core idea

A caregiver films themselves doing an exercise (or takes photos of key poses). The system automatically extracts the body skeleton from each frame, translates those poses into motor commands the NAO robot understands, and saves the whole routine. The robot can then replay the routine on demand — in the right order, the right number of repetitions.

## What you can do with it

| Feature | What it does |
|---|---|
| **Upload a video or photo** | Drop in a video clip or image of any exercise; the system extracts skeleton keypoints and sends the pose directly to the robot without any editing step |
| **Exercise editor** | Arrange frames into a sequence, reorder them, insert named poses (e.g. "drep", "stoj", "ruky hore"), preview each frame's image |
| **Exercise library** | Browse all saved routines, see their name, frame count, AI-estimated calorie burn, and description; run any of them on the robot with one tap |
| **Live voice control** | Say a pose name out loud — the robot immediately strikes that pose. No buttons needed |
| **Voice frame insertion** | While editing, speak commands like "vlož drep za snímku 3" to rearrange a routine hands-free |
| **AI assistance** | If a GPT key is configured, it generates a calorie estimate and a natural-language description for each exercise automatically. Without a key, calorie and description fields are skipped silently, voice commands fall back to local keyword matching, and voice-driven frame insertion uses a built-in Slovak keyword parser — all other features remain fully functional |

## Who it is for

- Physiotherapists and care home staff who design exercise programs for elderly patients and want the NAO robot to lead the sessions
- Researchers building human-robot interaction studies with seniors
- Anyone operating a NAO robot who needs a simple authoring tool that does not require coding

---

## Architecture

The system is a **microservices application** — 7 independent services, each in its own container, communicating over HTTP. Deployed with **Kubernetes (k8s)**, orchestrated via manifests in `/k8s/` and a `Makefile` for one-command operations.

## Services

| Service | What it does |
|---|---|
| **web** | React + Vite frontend. Single-page app served by Nginx. Nginx also acts as reverse proxy — routes `/api/*` calls to backend services so the browser only talks to one host |
| **team19-web** | Static documentation site (sprint notes, retrospectives, meeting minutes) |
| **naoRobotAPI** | Thin bridge to the physical NAO robot. Receives a pose (joint angles) and sends it over the NAO SDK |
| **skeletonFinderAPI** | Takes an image, runs MediaPipe pose estimation, returns body keypoints (x, y, z per joint) |
| **translator** | Converts keypoints → NAO joint angles. Also handles exercise playback — reads a saved sequence and sends each frame to naoRobotAPI |
| **exerciseConfigService** | CRUD storage for exercises. Stores config.json + per-frame JSON + frame PNG images on a persistent volume |
| **voiceCommandAPI** | Receives a recognized pose name (text), looks it up, forwards joint angles to naoRobotAPI |

## Frontend features

- **Exercise editor** — video upload, frame extraction, frame reordering, named pose insertion, voice-driven editing
- **Exercise library** — browse/delete/run saved exercises, AI-generated calorie estimate and description
- **Voice control** — live voice commands → immediate robot pose (with GPT parsing or keyword fallback)
- **Simple upload** — quick one-shot pose send from video or image, no editing step

## Kubernetes deployment

- Each service has its own **Deployment + ClusterIP Service** manifest in `/k8s/<service>/`
- **exerciseConfigService** uses a **PersistentVolumeClaim** (2Gi) so exercise data survives pod restarts
- The web Nginx ConfigMap routes all `/api/*` paths to the correct k8s service DNS names
- `make k8s-deploy` applies all manifests; `make k8s-logs` / `make k8s-restart` for operations
- Images are pushed to Docker Hub (`dronhome13/*`) and pulled by k8s at deploy time
