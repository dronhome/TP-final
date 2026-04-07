import { useState, useRef, useCallback, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Loader2,
  Upload,
  Save,
  Play,
  Trash2,
  Plus,
  GripVertical,
  AlertCircle,
  CheckCircle,
  Film,
  ChevronRight,
  RotateCcw,
} from "lucide-react";

// ── API config ────────────────────────────────────────────────────
const UPLOAD_API = "http://localhost:7000";
const EDITOR_API = "http://localhost:7001";
const POSES_API  = "http://localhost:8000";

// ── types ─────────────────────────────────────────────────────────
type Frame = {
  idx: number;
  angles: Record<string, number>;
};

type StatusMsg = { type: "success" | "error" | "info"; text: string } | null;

// ── helpers ───────────────────────────────────────────────────────
function angleLabel(angles: Record<string, number>) {
  const entries = Object.entries(angles).slice(0, 3);
  return entries.map(([k, v]) => `${k}: ${Math.round(v)}°`).join("  ·  ");
}

// ── drag-reorder hook ─────────────────────────────────────────────
function useDragReorder<T>(
  items: T[],
  setItems: React.Dispatch<React.SetStateAction<T[]>>
) {
  const dragIdx = useRef<number | null>(null);
  const overIdx = useRef<number | null>(null);

  const onDragStart = (i: number) => { dragIdx.current = i; };
  const onDragEnter = (i: number) => { overIdx.current = i; };
  const onDragEnd   = () => {
    if (dragIdx.current === null || overIdx.current === null) return;
    if (dragIdx.current === overIdx.current) { dragIdx.current = overIdx.current = null; return; }
    setItems((prev) => {
      const next = [...prev];
      const [moved] = next.splice(dragIdx.current!, 1);
      next.splice(overIdx.current!, 0, moved);
      return next;
    });
    dragIdx.current = overIdx.current = null;
  };

  return { onDragStart, onDragEnter, onDragEnd };
}

// ── main component ────────────────────────────────────────────────
export default function ExerciseEditor() {
  const [exerciseId, setExerciseId]   = useState<string | null>(null);
  const [frames, setFrames]           = useState<Frame[]>([]);
  const [poses, setPoses]             = useState<string[]>([]);
  const [status, setStatus]           = useState<StatusMsg>(null);
  const [uploading, setUploading]     = useState(false);
  const [loadingFrames, setLoadingFrames] = useState(false);
  const [saving, setSaving]           = useState(false);
  const [running, setRunning]         = useState(false);
  const [insertingAt, setInsertingAt] = useState<number | null>(null);
  const [deletingAt, setDeletingAt]   = useState<number | null>(null);
  const [selectedPose, setSelectedPose] = useState<Record<number, string>>({});
  const [imageUrls, setImageUrls]     = useState<Record<number, string>>({});
  const [dragOver, setDragOver]       = useState<number | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const drag = useDragReorder(frames, setFrames);

  // ── load poses on mount ───────────────────────────────────────
  useEffect(() => {
    fetch(`${POSES_API}/commands`)
      .then((r) => r.json())
      .then((data) => {
        // backend returns either string[] or {commands: string[]} or object with keys
        if (Array.isArray(data)) setPoses(data);
        else if (data.commands) setPoses(data.commands);
        else setPoses(Object.keys(data));
      })
      .catch(() => {/* poses not critical at startup */});
  }, []);

  // ── load frame images when frames change ─────────────────────
  useEffect(() => {
    if (!exerciseId || !frames.length) return;
    const urls: Record<number, string> = {};
    frames.forEach((f) => {
      urls[f.idx] = `${EDITOR_API}/exercise/${exerciseId}/frame/${f.idx}/image`;
    });
    setImageUrls(urls);
  }, [frames, exerciseId]);

  const showStatus = (type: "success" | "error" | "info", text: string) => {
    setStatus({ type, text });
    if (type !== "error") setTimeout(() => setStatus(null), 4000);
  };

  // ── upload video ──────────────────────────────────────────────
  const handleUpload = useCallback(async (file: File) => {
    if (!file.type.startsWith("video/")) {
      showStatus("error", "Please select a video file.");
      return;
    }
    setUploading(true);
    setStatus(null);
    setFrames([]);
    setExerciseId(null);

    try {
      const fd = new FormData();
      fd.append("video", file);

      const res = await fetch(`${UPLOAD_API}/exercise/from_video`, {
        method: "POST",
        body: fd,
      });
      if (!res.ok) throw new Error(`Upload failed: HTTP ${res.status}`);
      const data = await res.json();
      const id = data.id ?? data.exercise_id ?? data.exerciseId ?? String(data);
      setExerciseId(id);
      showStatus("info", `Exercise created (ID: ${id}). Loading frames…`);
      await loadFrames(id);
    } catch (err) {
      showStatus("error", err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  }, []);

  // ── load frames ───────────────────────────────────────────────
  const loadFrames = useCallback(async (id: string) => {
    setLoadingFrames(true);
    try {
      const res = await fetch(`${EDITOR_API}/exercise/${id}/frames`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      // normalise: expect [{idx, angles}] or [{index, angles}] or [{frame_index, angles}]
      const normalised: Frame[] = (Array.isArray(data) ? data : data.frames ?? []).map(
        (f: any, i: number) => ({
          idx: f.idx ?? f.index ?? f.frame_index ?? i,
          angles: f.angles ?? f.joint_angles ?? {},
        })
      );
      setFrames(normalised);
      showStatus("success", `${normalised.length} frames loaded.`);
    } catch (err) {
      showStatus("error", err instanceof Error ? err.message : "Failed to load frames");
    } finally {
      setLoadingFrames(false);
    }
  }, []);

  // ── insert pose ───────────────────────────────────────────────
  const insertPose = useCallback(async (afterFrameIdx: number, pose: string) => {
    if (!exerciseId) return;
    setInsertingAt(afterFrameIdx);
    try {
      const res = await fetch(`${EDITOR_API}/exercise/${exerciseId}/frame/from_pose`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pose, position: afterFrameIdx + 1 }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      await loadFrames(exerciseId);
      setSelectedPose((prev) => { const n = { ...prev }; delete n[afterFrameIdx]; return n; });
      showStatus("success", `Pose "${pose}" inserted.`);
    } catch (err) {
      showStatus("error", err instanceof Error ? err.message : "Insert failed");
    } finally {
      setInsertingAt(null);
    }
  }, [exerciseId, loadFrames]);

  // ── delete frame ──────────────────────────────────────────────
  const deleteFrame = useCallback(async (frameIdx: number) => {
    if (!exerciseId) return;
    setDeletingAt(frameIdx);
    try {
      const res = await fetch(`${EDITOR_API}/exercise/${exerciseId}/frame/${frameIdx}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setFrames((prev) => prev.filter((f) => f.idx !== frameIdx));
      showStatus("success", "Frame deleted.");
    } catch (err) {
      showStatus("error", err instanceof Error ? err.message : "Delete failed");
    } finally {
      setDeletingAt(null);
    }
  }, [exerciseId]);

  // ── save sequence ─────────────────────────────────────────────
  const saveSequence = useCallback(async () => {
    if (!exerciseId) return;
    setSaving(true);
    try {
      const sequence = frames.map((f) => f.idx);
      const res = await fetch(`${EDITOR_API}/exercise/${exerciseId}/sequence`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sequence }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      showStatus("success", "Sequence saved.");
    } catch (err) {
      showStatus("error", err instanceof Error ? err.message : "Save failed");
    } finally {
      setSaving(false);
    }
  }, [exerciseId, frames]);

  // ── run on robot ──────────────────────────────────────────────
  const runExercise = useCallback(async () => {
    if (!exerciseId) return;
    setRunning(true);
    try {
      const res = await fetch(`${UPLOAD_API}/exercise/${exerciseId}/run`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      showStatus("success", "Exercise sent to robot!");
    } catch (err) {
      showStatus("error", err instanceof Error ? err.message : "Run failed");
    } finally {
      setRunning(false);
    }
  }, [exerciseId]);

  // ── drop zone ─────────────────────────────────────────────────
  const onDropZone = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) handleUpload(file);
  };

  // ── render ────────────────────────────────────────────────────
  return (
    <div className="w-full max-w-7xl mx-auto px-4 py-6 space-y-6">

      {/* ── header ── */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold tracking-tight text-foreground">
            Exercise Editor
          </h1>
          <p className="text-xs text-muted-foreground mt-0.5">
            Upload a video, edit frames, run on robot.
          </p>
        </div>
        {exerciseId && (
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="font-mono text-xs">
              ID: {exerciseId}
            </Badge>
            <Button
              variant="outline"
              size="sm"
              onClick={() => loadFrames(exerciseId)}
              disabled={loadingFrames}
            >
              {loadingFrames
                ? <Loader2 className="h-3.5 w-3.5 animate-spin" />
                : <RotateCcw className="h-3.5 w-3.5" />
              }
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={saveSequence}
              disabled={saving || !frames.length}
            >
              {saving
                ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                : <Save className="h-3.5 w-3.5 mr-1.5" />
              }
              Save
            </Button>
            <Button
              size="sm"
              onClick={runExercise}
              disabled={running || !frames.length}
              className="text-primary-foreground"
            >
              {running
                ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                : <Play className="h-3.5 w-3.5 mr-1.5" />
              }
              Run on Robot
            </Button>
          </div>
        )}
      </div>

      {/* ── status alert ── */}
      {status && (
        <Alert
          variant={status.type === "error" ? "destructive" : "default"}
          className={
            status.type === "success" ? "border-green-500 bg-green-50 dark:bg-green-950/20" :
            status.type === "info"    ? "border-blue-500 bg-blue-50 dark:bg-blue-950/20" : ""
          }
        >
          {status.type === "error"
            ? <AlertCircle className="h-4 w-4" />
            : <CheckCircle className="h-4 w-4 text-green-600" />
          }
          <AlertDescription>{status.text}</AlertDescription>
        </Alert>
      )}

      {/* ── upload zone (shown when no exercise loaded) ── */}
      {!exerciseId && (
        <Card
          className={[
            "border-2 border-dashed transition-colors duration-200 cursor-pointer",
            "hover:border-primary/50 hover:bg-muted/30",
            uploading ? "opacity-60 pointer-events-none" : "",
          ].join(" ")}
          onDragOver={(e) => e.preventDefault()}
          onDrop={onDropZone}
          onClick={() => fileInputRef.current?.click()}
        >
          <div className="flex flex-col items-center justify-center gap-4 py-16 px-8 text-center">
            {uploading ? (
              <>
                <Loader2 className="h-10 w-10 text-primary animate-spin" />
                <p className="text-sm text-muted-foreground">Uploading video…</p>
              </>
            ) : (
              <>
                <div className="w-16 h-16 rounded-2xl bg-muted/50 flex items-center justify-center">
                  <Film className="h-8 w-8 text-muted-foreground" />
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground">Drop a video here</p>
                  <p className="text-xs text-muted-foreground mt-1">or click to browse</p>
                </div>
                <Badge variant="secondary" className="text-xs">MP4 · MOV · AVI · WEBM</Badge>
              </>
            )}
          </div>
          <input
            ref={fileInputRef}
            type="file"
            accept="video/*"
            className="hidden"
            onChange={(e) => { const f = e.target.files?.[0]; if (f) handleUpload(f); }}
          />
        </Card>
      )}

      {/* ── upload new video button when exercise exists ── */}
      {exerciseId && (
        <div className="flex items-center gap-3">
          <button
            className="flex items-center gap-2 text-xs text-muted-foreground hover:text-foreground transition-colors"
            onClick={() => {
              setExerciseId(null);
              setFrames([]);
              setStatus(null);
            }}
          >
            <Upload className="h-3.5 w-3.5" />
            Upload different video
          </button>
        </div>
      )}

      {/* ── loading frames spinner ── */}
      {loadingFrames && (
        <Card className="flex items-center justify-center py-16">
          <div className="flex flex-col items-center gap-3">
            <Loader2 className="h-8 w-8 text-primary animate-spin" />
            <p className="text-sm text-muted-foreground">Loading frames…</p>
          </div>
        </Card>
      )}

      {/* ── frame timeline ── */}
      {!loadingFrames && frames.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
              {frames.length} Frame{frames.length !== 1 ? "s" : ""}
              <span className="ml-2 normal-case font-normal">— drag to reorder</span>
            </p>
          </div>

          {/* horizontal scrollable frame strip */}
          <div className="overflow-x-auto pb-3">
            <div className="flex gap-3 min-w-max">
              {frames.map((frame, i) => (
                <FrameCard
                  key={`${frame.idx}-${i}`}
                  frame={frame}
                  position={i}
                  imageUrl={imageUrls[frame.idx]}
                  poses={poses}
                  selectedPose={selectedPose[frame.idx] ?? ""}
                  onSelectPose={(p) => setSelectedPose((prev) => ({ ...prev, [frame.idx]: p }))}
                  onInsert={(pose) => insertPose(frame.idx, pose)}
                  onDelete={() => deleteFrame(frame.idx)}
                  inserting={insertingAt === frame.idx}
                  deleting={deletingAt === frame.idx}
                  isDragOver={dragOver === i}
                  // drag handlers
                  draggable
                  onDragStart={() => drag.onDragStart(i)}
                  onDragEnter={() => { drag.onDragEnter(i); setDragOver(i); }}
                  onDragEnd={() => { drag.onDragEnd(); setDragOver(null); }}
                  onDragOver={(e: React.DragEvent) => e.preventDefault()}
                />
              ))}
            </div>
          </div>

          {/* bottom action bar */}
          <div className="flex items-center justify-end gap-3 pt-2 border-t border-border/50">
            <span className="text-xs text-muted-foreground mr-auto">
              Drag frames to reorder, then save.
            </span>
            <Button
              variant="outline"
              size="sm"
              onClick={saveSequence}
              disabled={saving}
            >
              {saving
                ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                : <Save className="h-3.5 w-3.5 mr-1.5" />
              }
              Save Sequence
            </Button>
            <Button
              size="sm"
              onClick={runExercise}
              disabled={running}
              className="text-primary-foreground"
            >
              {running
                ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1.5" />
                : <Play className="h-3.5 w-3.5 mr-1.5" />
              }
              Run on Robot
            </Button>
          </div>
        </div>
      )}

      {/* ── empty state after load ── */}
      {!loadingFrames && exerciseId && frames.length === 0 && (
        <Card className="flex flex-col items-center justify-center py-16 gap-3">
          <Film className="h-8 w-8 text-muted-foreground/40" />
          <p className="text-sm text-muted-foreground">No frames found for this exercise.</p>
          <Button variant="outline" size="sm" onClick={() => loadFrames(exerciseId)}>
            Retry
          </Button>
        </Card>
      )}
    </div>
  );
}

// ── FrameCard sub-component ───────────────────────────────────────
type FrameCardProps = {
  frame: Frame;
  position: number;
  imageUrl: string;
  poses: string[];
  selectedPose: string;
  onSelectPose: (p: string) => void;
  onInsert: (pose: string) => void;
  onDelete: () => void;
  inserting: boolean;
  deleting: boolean;
  isDragOver: boolean;
  draggable: boolean;
  onDragStart: () => void;
  onDragEnter: () => void;
  onDragEnd: () => void;
  onDragOver: (e: React.DragEvent) => void;
};

function FrameCard({
  frame,
  position,
  imageUrl,
  poses,
  selectedPose,
  onSelectPose,
  onInsert,
  onDelete,
  inserting,
  deleting,
  isDragOver,
  ...dragProps
}: FrameCardProps) {
  return (
    <div
      {...dragProps}
      className={[
        "w-52 flex-shrink-0 rounded-xl border bg-card shadow-sm",
        "transition-all duration-150 cursor-grab active:cursor-grabbing",
        isDragOver ? "ring-2 ring-primary scale-[1.02] shadow-lg" : "",
        deleting ? "opacity-40 pointer-events-none" : "",
      ].join(" ")}
    >
      {/* frame image */}
      <div className="relative w-full aspect-video bg-muted rounded-t-xl overflow-hidden">
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={`Frame ${frame.idx}`}
            className="w-full h-full object-cover"
            draggable={false}
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Loader2 className="h-5 w-5 text-muted-foreground animate-spin" />
          </div>
        )}

        {/* position badge + drag handle */}
        <div className="absolute top-2 left-2 flex items-center gap-1">
          <span className="bg-black/60 text-white text-[10px] font-mono px-1.5 py-0.5 rounded">
            #{position + 1}
          </span>
        </div>
        <div className="absolute top-2 right-2 text-white/60">
          <GripVertical className="h-4 w-4" />
        </div>

        {/* delete button */}
        <button
          onClick={onDelete}
          disabled={deleting}
          className="absolute bottom-2 right-2 bg-black/60 hover:bg-destructive text-white rounded-md p-1 transition-colors"
          aria-label="Delete frame"
        >
          {deleting
            ? <Loader2 className="h-3.5 w-3.5 animate-spin" />
            : <Trash2 className="h-3.5 w-3.5" />
          }
        </button>
      </div>

      {/* angles */}
      <div className="px-3 pt-2 pb-1">
        <p className="text-[10px] text-muted-foreground font-mono leading-relaxed truncate">
          {Object.keys(frame.angles).length > 0
            ? angleLabel(frame.angles)
            : <span className="italic">no angle data</span>
          }
        </p>
      </div>

      {/* insert pose */}
      <div className="px-3 pb-3 pt-1 flex gap-1.5">
        <Select value={selectedPose} onValueChange={onSelectPose}>
          <SelectTrigger className="h-7 text-xs flex-1 min-w-0">
            <SelectValue placeholder="Add pose…" />
          </SelectTrigger>
          <SelectContent>
            {poses.length === 0 ? (
              <SelectItem value="__none" disabled>No poses loaded</SelectItem>
            ) : (
              poses.map((p) => (
                <SelectItem key={p} value={p} className="text-xs">
                  {p}
                </SelectItem>
              ))
            )}
          </SelectContent>
        </Select>
        <Button
          size="icon"
          variant="outline"
          className="h-7 w-7 flex-shrink-0"
          disabled={!selectedPose || inserting}
          onClick={() => selectedPose && onInsert(selectedPose)}
          aria-label="Insert pose after this frame"
        >
          {inserting
            ? <Loader2 className="h-3 w-3 animate-spin" />
            : <Plus className="h-3 w-3" />
          }
        </Button>
      </div>
    </div>
  );
}