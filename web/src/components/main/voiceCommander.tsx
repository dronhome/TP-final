import { useState, useRef, useCallback } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, CheckCircle2, XCircle, Clock, ChevronRight } from "lucide-react";

const COMMAND_MAP: Record<string, string[]> = {
  wave:        ["wave", "hello", "hi", "greet", "hey"],
  stand:       ["stand", "standing", "up", "upright"],
  sit:         ["sit", "sitting", "down", "seat"],
  hands_up:    ["hands up", "raise", "surrender", "reach", "arms up"],
  t_pose:      ["t pose", "t-pose", "tpose", "spread", "cross"],
  bow:         ["bow", "bowing", "curtsy", "curtsey"],
  crouch:      ["crouch", "crouching", "duck", "ducking", "squat"],
  point_right: ["point right", "right", "pointing right"],
  point_left:  ["point left", "left", "pointing left"],
};

const DISPLAY_NAMES: Record<string, string> = {
  wave:        "Wave",
  stand:       "Stand",
  sit:         "Sit",
  hands_up:    "Hands Up",
  t_pose:      "T-Pose",
  bow:         "Bow",
  crouch:      "Crouch",
  point_right: "Point Right",
  point_left:  "Point Left",
};

const API_BASE_URL = "/api";

function MicIcon({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
      className={className}>
      <path d="M12 2a3 3 0 0 1 3 3v7a3 3 0 0 1-6 0V5a3 3 0 0 1 3-3Z" />
      <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
      <line x1="12" x2="12" y1="19" y2="22" />
    </svg>
  );
}

function MicOffIcon({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
      className={className}>
      <line x1="2" x2="22" y1="2" y2="22" />
      <path d="M18.89 13.23A7.12 7.12 0 0 0 19 12v-2" />
      <path d="M5 10v2a7 7 0 0 0 12 5" />
      <path d="M15 9.34V5a3 3 0 0 0-5.68-1.33" />
      <path d="M9 9v3a3 3 0 0 0 5.12 2.12" />
      <line x1="12" x2="12" y1="19" y2="22" />
    </svg>
  );
}

function extractCommands(transcript: string): string[] {
  const lower = transcript.toLowerCase();
  const candidates: { index: number; command: string }[] = [];

  for (const [cmd, aliases] of Object.entries(COMMAND_MAP)) {
    for (const alias of aliases) {
      const idx = lower.indexOf(alias);
      if (idx !== -1) {
        candidates.push({ index: idx, command: cmd });
        break;
      }
    }
  }

  candidates.sort((a, b) => a.index - b.index);
  const added = new Set<string>();
  const found: string[] = [];
  for (const { command } of candidates) {
    if (!added.has(command)) {
      found.push(command);
      added.add(command);
    }
  }
  return found;
}

type QueueItem = {
  id: string;
  command: string;
  status: "pending" | "running" | "done" | "error";
  error?: string;
};

export function VoiceCommander() {
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [detected, setDetected] = useState<string[]>([]);
  const [queue, setQueue] = useState<QueueItem[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [pulseLevel, setPulseLevel] = useState(0);

  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const pulseRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const startListening = useCallback(() => {
    const SR =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SR) {
      alert("Speech recognition not supported — use Chrome or Edge.");
      return;
    }

    const rec = new SR();
    rec.continuous = false;
    rec.interimResults = true;
    rec.lang = "en-US";

    rec.onstart = () => {
      setListening(true);
      setTranscript("");
      setDetected([]);
      pulseRef.current = setInterval(() => {
        setPulseLevel(Math.floor(Math.random() * 5) + 1);
      }, 150);
    };

    rec.onresult = (e: SpeechRecognitionEvent) => {
      let final = "";
      let interim = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const t = e.results[i][0].transcript;
        if (e.results[i].isFinal) final += t;
        else interim += t;
      }
      const current = final || interim;
      setTranscript(current);
      setDetected(extractCommands(current));
    };

    rec.onend = () => {
      setListening(false);
      if (pulseRef.current) clearInterval(pulseRef.current);
      setPulseLevel(0);
    };

    rec.onerror = () => {
      setListening(false);
      if (pulseRef.current) clearInterval(pulseRef.current);
      setPulseLevel(0);
    };

    recognitionRef.current = rec;
    rec.start();
  }, []);

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
  }, []);

  const executeQueue = useCallback(async (commands: string[]) => {
    if (!commands.length) return;

    const items: QueueItem[] = commands.map((cmd) => ({
      id: `${cmd}-${Date.now()}-${Math.random()}`,
      command: cmd,
      status: "pending",
    }));

    setQueue(items);
    setIsProcessing(true);

    for (let i = 0; i < items.length; i++) {
      setQueue((prev) =>
        prev.map((item, idx) => (idx === i ? { ...item, status: "running" } : item))
      );

      try {

            console.log("SEND!")
        const res = await fetch(`${API_BASE_URL}/command`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ command: items[i].command }),
        });

        if (!res.ok) {
          const data = await res.json().catch(() => ({}));
          throw new Error(data.detail || data.message || `HTTP ${res.status}`);
        }

        setQueue((prev) =>
          prev.map((item, idx) => (idx === i ? { ...item, status: "done" } : item))
        );
      } catch (err) {
        setQueue((prev) =>
          prev.map((item, idx) =>
            idx === i
              ? { ...item, status: "error", error: err instanceof Error ? err.message : "Unknown error" }
              : item
          )
        );
      }
    }

    setIsProcessing(false);
  }, []);

  const bars = Array.from({ length: 7 });
  const barHeights = [3, 5, 7, 9, 7, 5, 3];

  return (
    <Card className="shadow-lg overflow-hidden">
      <div className="px-5 pt-5 pb-4 border-b border-border/50">
        <div className="flex items-center gap-2 mb-0.5">
          <h2 className="text-sm font-semibold tracking-wide uppercase text-foreground/80">
            Voice Commander
          </h2>
        </div>
        <p className="text-xs text-muted-foreground">
          Speak a pose name — detected commands are queued and sent to the API.
        </p>
      </div>

      <div className="flex flex-col items-center gap-4 px-5 py-6">
        <div className="flex items-center justify-center gap-[3px] h-10">
          {bars.map((_, i) => (
            <div
              key={i}
              className="w-[3px] rounded-full transition-all duration-100"
              style={{
                height: `${
                  listening && pulseLevel > 0
                    ? Math.max(4, Math.floor(Math.random() * 10 * pulseLevel)) * 2
                    : barHeights[i] * 2
                }px`,
                backgroundColor: listening
                  ? "hsl(var(--primary))"
                  : "hsl(var(--muted-foreground) / 0.3)",
              }}
            />
          ))}
        </div>

        <button
          onClick={listening ? stopListening : startListening}
          disabled={isProcessing}
          className={[
            "relative w-20 h-20 rounded-full flex items-center justify-center",
            "transition-all duration-200 shadow-md",
            listening
              ? "bg-destructive hover:bg-destructive/90 shadow-lg scale-105"
              : "bg-primary hover:bg-primary/90",
            "disabled:opacity-50 disabled:cursor-not-allowed",
          ].join(" ")}
          aria-label={listening ? "Stop listening" : "Start listening"}
        >
          {listening && (
            <span className="absolute inset-0 rounded-full bg-destructive/40 animate-ping" />
          )}
          {listening
            ? <MicOffIcon className="h-8 w-8" />
            : <MicIcon className="h-8 w-8" />
          }
        </button>

        <p className="text-xs text-muted-foreground">
          {listening ? "Listening… tap to stop" : "Tap to speak"}
        </p>
      </div>

      {transcript && (
        <div className="mx-5 mb-4 rounded-lg bg-muted/50 border border-border/50 px-4 py-3">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Heard</p>
          <p className="text-sm text-foreground leading-relaxed">"{transcript}"</p>
        </div>
      )}

      {detected.length > 0 && (
        <div className="mx-5 mb-4">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
            Detected ({detected.length})
          </p>
          <div className="flex flex-wrap gap-2 mb-3">
            {detected.map((cmd) => (
              <Badge key={cmd} variant="secondary" className="gap-1.5 py-1 px-2.5 text-xs font-medium">
                <ChevronRight className="h-3 w-3" />
                {DISPLAY_NAMES[cmd] ?? cmd}
              </Badge>
            ))}
          </div>
          <Button 
          variant="primary"
            className="w-full"
            size="sm"
            onClick={() => executeQueue(detected)}
            disabled={isProcessing || listening}
          >
            {isProcessing ? (
              <><Loader2 className="mr-2 h-3.5 w-3.5 animate-spin" />Executing…</>
            ) : (
              <>Execute {detected.length} Command{detected.length > 1 ? "s" : ""}</>
            )}
          </Button>
        </div>
      )}

      {queue.length > 0 && (
        <div className="mx-5 mb-5">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Queue</p>
          <div className="flex flex-col gap-1.5">
            {queue.map((item) => (
              <div
                key={item.id}
                className={[
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors duration-200 border",
                  item.status === "running" ? "bg-primary/10 border-primary/20" : "",
                  item.status === "done"    ? "bg-green-500/10 border-green-500/20" : "",
                  item.status === "error"   ? "bg-destructive/10 border-destructive/20" : "",
                  item.status === "pending" ? "bg-muted/40 border-border/40" : "",
                ].join(" ")}
              >
                <span className="flex-shrink-0">
                  {item.status === "pending" && <Clock        className="h-3.5 w-3.5 text-muted-foreground" />}
                  {item.status === "running" && <Loader2      className="h-3.5 w-3.5 text-primary animate-spin" />}
                  {item.status === "done"    && <CheckCircle2 className="h-3.5 w-3.5 text-green-500" />}
                  {item.status === "error"   && <XCircle      className="h-3.5 w-3.5 text-destructive" />}
                </span>
                <span className="font-medium flex-1">{DISPLAY_NAMES[item.command] ?? item.command}</span>
                <span className="text-xs text-muted-foreground capitalize">
                  {item.status === "running" ? "sending…" : item.status}
                </span>
                {item.error && (
                  <span className="text-xs text-destructive truncate max-w-[120px]" title={item.error}>
                    {item.error}
                  </span>
                )}
              </div>
            ))}
          </div>
          {!isProcessing && (
            <Button
              variant="ghost" size="sm"
              className="w-full mt-2 text-xs"
              onClick={() => { setQueue([]); setTranscript(""); setDetected([]); }}
            >
              Clear
            </Button>
          )}
        </div>
      )}

      {!transcript && queue.length === 0 && (
        <div className="mx-5 mb-5">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
            Available poses
          </p>
          <div className="flex flex-wrap gap-1.5">
            {Object.values(DISPLAY_NAMES).map((name) => (
              <span key={name} className="text-xs bg-muted/50 text-muted-foreground border border-border/50 rounded px-2 py-0.5">
                {name}
              </span>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
}