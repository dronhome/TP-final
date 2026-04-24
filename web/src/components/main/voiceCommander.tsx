import { useState, useRef, useCallback } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Loader2, CheckCircle2, XCircle, Clock, ChevronRight } from "lucide-react";

const DISPLAY_NAMES: Record<string, string> = {
  wave:        "Zamávaj",
  stand:       "Stoj",
  sit:         "Sed",
  hands_up:    "Ruky hore",
  t_pose:      "T-Póza",
  bow:         "Úklon",
  crouch:      "Drep",
  point_right: "Ukáž vpravo",
  point_left:  "Ukáž vľavo",
};

const ALL_COMMANDS = Object.keys(DISPLAY_NAMES);

const LLM_API_BASE = import.meta.env.VITE_LLM_API_BASE ?? "https://litellm.blockfinlab.xyz";
const LLM_API_KEY  = import.meta.env.VITE_LLM_API_KEY ?? "";
const LLM_MODEL    = "gpt-5.4-fiit";
const LLM_AVAILABLE = !!LLM_API_KEY;

const VOICE_ALIASES: [string, string][] = [
  ["drep", "crouch"],
  ["úklon", "bow"], ["uklon", "bow"],
  ["zamávaj", "wave"], ["zamavaj", "wave"], ["zamávajte", "wave"],
  ["stoj", "stand"],
  ["sed", "sit"], ["sadni", "sit"],
  ["ruky hore", "hands_up"],
  ["t-póza", "t_pose"], ["t póza", "t_pose"], ["tpóza", "t_pose"], ["t poza", "t_pose"],
  ["ukáž vpravo", "point_right"], ["ukaz vpravo", "point_right"],
  ["ukáž vľavo", "point_left"], ["ukaz vlavo", "point_left"],
  ["crouch", "crouch"], ["bow", "bow"], ["wave", "wave"], ["stand", "stand"],
  ["sit", "sit"], ["hands up", "hands_up"], ["t pose", "t_pose"], ["t-pose", "t_pose"],
  ["point right", "point_right"], ["point left", "point_left"],
];

function extractCommandsLocally(transcript: string): string[] {
  const lower = transcript.toLowerCase();
  const seen = new Set<string>();
  const result: string[] = [];
  for (const [alias, cmd] of VOICE_ALIASES) {
    if (!seen.has(cmd) && lower.includes(alias)) { seen.add(cmd); result.push(cmd); }
  }
  return result;
}

async function interpretWithGPT(transcript: string): Promise<string[]> {
  const res = await fetch(`${LLM_API_BASE}/v1/chat/completions`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authorization": `Bearer ${LLM_API_KEY}` },
    body: JSON.stringify({
      model: LLM_MODEL,
      response_format: { type: "json_object" },
      messages: [
        {
          role: "system",
          content: `You are a voice command parser for a NAO robot. The user speaks pose names (possibly in Slovak or with speech recognition errors). Map what they said to one or more of these exact command keys: ${ALL_COMMANDS.join(", ")}. Return ONLY a JSON object: {"commands": ["key1", "key2", ...]}. If nothing matches, return {"commands": []}. Preserve the order the user mentioned them.`,
        },
        { role: "user", content: transcript },
      ],
    }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();
  const parsed = JSON.parse(data.choices?.[0]?.message?.content ?? "{}");
  return Array.isArray(parsed.commands) ? parsed.commands.filter((c: string) => ALL_COMMANDS.includes(c)) : [];
}

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
  const [isInterpreting, setIsInterpreting] = useState(false);
  const [pulseLevel, setPulseLevel] = useState(0);

  const recognitionRef = useRef<any>(null);
  const pulseRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const transcriptRef = useRef("");

  const startListening = useCallback(() => {
    const SR =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SR) {
      alert("Rozpoznávanie hlasu nie je podporované — použite Chrome alebo Edge.");
      return;
    }

    const rec = new SR();
    rec.continuous = false;
    rec.interimResults = true;
    rec.lang = "sk-SK";

    rec.onstart = () => {
      setListening(true);
      setTranscript("");
      setDetected([]);
      transcriptRef.current = "";
      pulseRef.current = setInterval(() => {
        setPulseLevel(Math.floor(Math.random() * 5) + 1);
      }, 150);
    };

    rec.onresult = (e: any) => {
      let final = "";
      let interim = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const t = e.results[i][0].transcript;
        if (e.results[i].isFinal) final += t;
        else interim += t;
      }
      const current = final || interim;
      transcriptRef.current = current;
      setTranscript(current);
    };

    rec.onend = async () => {
      setListening(false);
      if (pulseRef.current) clearInterval(pulseRef.current);
      setPulseLevel(0);
      const text = transcriptRef.current.trim();
      if (!text) return;
      if (!LLM_AVAILABLE) {
        setDetected(extractCommandsLocally(text));
        return;
      }
      setIsInterpreting(true);
      try {
        const cmds = await interpretWithGPT(text);
        setDetected(cmds.length ? cmds : extractCommandsLocally(text));
      } catch {
        setDetected(extractCommandsLocally(text));
      } finally {
        setIsInterpreting(false);
      }
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
        const res = await fetch(`/command`, {
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
            Hlasový príkaz
          </h2>
          {LLM_AVAILABLE
            ? <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-green-100 text-green-700 font-medium">AI aktívna</span>
            : <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-gray-100 text-gray-500 font-medium">Bez AI</span>
          }
        </div>
        <p className="text-xs text-muted-foreground">
          {LLM_AVAILABLE
            ? "Povedzte názov pózy — AI rozpozná aj skomolené slová."
            : "Povedzte názov pózy — detekcia kľúčových slov (bez AI)."}
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
            ? <MicOffIcon className="h-8 w-8 text-white" />
            : <MicIcon className="h-8 w-8 text-white" />
          }
        </button>

        <p className="text-xs text-muted-foreground">
          {listening ? "Počúvam… klepnite pre zastavenie" : isInterpreting ? "Interpretuje sa…" : "Klepnite pre hovorenie"}
        </p>
        {isInterpreting && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            <span>AI rozpoznáva príkazy…</span>
          </div>
        )}
      </div>

      {transcript && (
        <div className="mx-5 mb-4 rounded-lg bg-muted/50 border border-border/50 px-4 py-3">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Zachytené</p>
          <p className="text-sm text-foreground leading-relaxed">"{transcript}"</p>
        </div>
      )}

      {detected.length > 0 && (
        <div className="mx-5 mb-4">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
            Detekované ({detected.length})
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
          variant="default"
            className="w-full"
            size="sm"
            onClick={() => executeQueue(detected)}
            disabled={isProcessing || listening || isInterpreting}
          >
            {isProcessing ? (
              <><Loader2 className="mr-2 h-3.5 w-3.5 animate-spin" />Vykonávanie…</>
            ) : (
              <>Vykonať {detected.length} príkaz{detected.length > 1 ? (detected.length < 5 ? "y" : "ov") : ""}</>
            )}
          </Button>
        </div>
      )}

      {queue.length > 0 && (
        <div className="mx-5 mb-5">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Fronta</p>
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
                <span className="text-xs text-muted-foreground">
                  {item.status === "pending" ? "čaká" : item.status === "running" ? "odosiela…" : item.status === "done" ? "hotovo" : "chyba"}
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
              Vymazať
            </Button>
          )}
        </div>
      )}

      {!transcript && queue.length === 0 && (
        <div className="mx-5 mb-5">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
            Dostupné pózy
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