import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Loader2, Play, Trash2, Pencil, Check, X, AlertCircle, CheckCircle, Film,
} from "lucide-react";

const API = "";

type Exercise = {
  id: string;
  name: string;
  frame_count: number;
  created_at: string;
  repetitions: number;
  calories?: number | null;
  description?: string | null;
};

type StatusMsg = { type: "success" | "error"; text: string } | null;

export default function ExercisesStore() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading]     = useState(true);
  const [status, setStatus]       = useState<StatusMsg>(null);
  const [running, setRunning]     = useState<string | null>(null);
  const [deleting, setDeleting]   = useState<string | null>(null);
  const [renaming, setRenaming]   = useState<string | null>(null);
  const [renameVal, setRenameVal] = useState("");
  const navigate = useNavigate();

  const showStatus = (type: "success" | "error", text: string) => {
    setStatus({ type, text });
    setTimeout(() => setStatus(null), 3500);
  };

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/exercise/list`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setExercises(await res.json());
    } catch {
      showStatus("error", "Načítanie cvičení zlyhalo.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleDelete = async (id: string) => {
setDeleting(id);
    try {
      const res = await fetch(`${API}/exercise/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setExercises((prev) => prev.filter((e) => e.id !== id));
      showStatus("success", "Cvičenie odstránené.");
    } catch {
      showStatus("error", "Odstránenie zlyhalo.");
    } finally {
      setDeleting(null);
    }
  };

  const handleRun = async (id: string) => {
    setRunning(id);
    try {
      const res = await fetch(`${API}/exercise/${id}/run`, { method: "POST" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      showStatus("success", "Cvičenie odoslané robotovi!");
    } catch {
      showStatus("error", "Spustenie zlyhalo.");
    } finally {
      setRunning(null);
    }
  };

  const startRename = (ex: Exercise) => {
    setRenaming(ex.id);
    setRenameVal(ex.name);
  };

  const commitRename = async (id: string) => {
    const name = renameVal.trim();
    if (!name) { setRenaming(null); return; }
    try {
      const res = await fetch(`${API}/exercise/${id}/config`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setExercises((prev) => prev.map((e) => e.id === id ? { ...e, name } : e));
    } catch {
      showStatus("error", "Premenovanie zlyhalo.");
    } finally {
      setRenaming(null);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto px-4 py-6 pb-24 space-y-4">
      <div>
        <h1 className="text-xl font-semibold tracking-tight text-foreground">Cvičenia</h1>
        <p className="text-xs text-muted-foreground mt-0.5">Všetky uložené cvičenia</p>
      </div>

      {status && (
        <Alert variant={status.type === "error" ? "destructive" : "default"}
          className={status.type === "success" ? "border-green-500 bg-green-50 dark:bg-green-950/20" : ""}
        >
          {status.type === "error"
            ? <AlertCircle className="h-4 w-4" />
            : <CheckCircle className="h-4 w-4 text-green-600" />
          }
          <AlertDescription>{status.text}</AlertDescription>
        </Alert>
      )}

      {loading && (
        <div className="flex justify-center py-16">
          <Loader2 className="h-7 w-7 text-primary animate-spin" />
        </div>
      )}

      {!loading && exercises.length === 0 && (
        <Card className="flex flex-col items-center justify-center py-16 gap-3">
          <Film className="h-8 w-8 text-muted-foreground/40" />
          <p className="text-sm text-muted-foreground">Zatiaľ žiadne cvičenia. Nahrajte video pre vytvorenie.</p>
        </Card>
      )}

      {!loading && exercises.map((ex) => (
        <Card key={ex.id} className="p-4 flex items-center gap-3">
          {/* name + meta */}
          <div className="flex-1 min-w-0">
            {renaming === ex.id ? (
              <div className="flex items-center gap-1.5">
                <input
                  autoFocus
                  className="flex-1 text-sm border border-border rounded px-2 py-0.5 bg-background text-foreground"
                  value={renameVal}
                  onChange={(e) => setRenameVal(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") commitRename(ex.id);
                    if (e.key === "Escape") setRenaming(null);
                  }}
                />
                <button onClick={() => commitRename(ex.id)} className="text-green-600 hover:text-green-700">
                  <Check className="h-4 w-4" />
                </button>
                <button onClick={() => setRenaming(null)} className="text-gray-400 hover:text-gray-600">
                  <X className="h-4 w-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-1.5 group">
                <p className="text-sm font-medium text-foreground truncate">{ex.name}</p>
                <button
                  onClick={() => startRename(ex)}
                  className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-gray-600 transition-opacity"
                >
                  <Pencil className="h-3 w-3" />
                </button>
              </div>
            )}
            <p className="text-[11px] text-muted-foreground mt-0.5 flex items-center gap-1.5 flex-wrap">
              <span>{ex.frame_count} snímok</span>
              <span>·</span>
              <span>{new Date(ex.created_at).toLocaleDateString("sk-SK")}</span>
              {ex.calories != null && (
                <>
                  <span>·</span>
                  <span className="font-medium text-foreground">{ex.calories} kcal</span>
                  <span className="bg-violet-100 text-violet-700 dark:bg-violet-900/30 dark:text-violet-400 px-1.5 py-0.5 rounded-full text-[10px]">Odhad AI</span>
                </>
              )}
            </p>
            {ex.description && (
              <p className="text-[11px] text-muted-foreground mt-1 leading-relaxed line-clamp-2">{ex.description}</p>
            )}
          </div>

          {/* actions */}
          <div className="flex items-center gap-2 shrink-0">
            <Button
              size="sm"
              variant="outline"
              onClick={() => navigate(`/edit?id=${ex.id}`)}
            >
              Otvoriť
            </Button>
            <Button
              size="sm"
              onClick={() => handleRun(ex.id)}
              disabled={running === ex.id}
              className="text-primary-foreground"
            >
              {running === ex.id
                ? <Loader2 className="h-3.5 w-3.5 animate-spin" />
                : <Play className="h-3.5 w-3.5" />
              }
            </Button>
            <button
              onClick={() => handleDelete(ex.id)}
              disabled={deleting === ex.id}
              className="text-gray-400 hover:text-red-500 transition-colors disabled:opacity-40"
            >
              {deleting === ex.id
                ? <Loader2 className="h-4 w-4 animate-spin" />
                : <Trash2 className="h-4 w-4" />
              }
            </button>
          </div>
        </Card>
      ))}

    </div>
  );
}
