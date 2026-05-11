import { useState, useEffect } from "react";
import { CheckCircle, AlertCircle, Info, X } from "lucide-react";

type ToastType = "success" | "error" | "info";

interface Toast {
  id: number;
  type: ToastType;
  text: string;
}

let _id = 0;
const listeners: Array<(toasts: Toast[]) => void> = [];
let _toasts: Toast[] = [];

function notify() {
  listeners.forEach((fn) => fn([..._toasts]));
}

function dismiss(id: number) {
  _toasts = _toasts.filter((t) => t.id !== id);
  notify();
}

export function toast(text: string, type: ToastType = "info") {
  const id = ++_id;
  _toasts = [..._toasts, { id, type, text }];
  notify();
  if (type !== "error") setTimeout(() => dismiss(id), 4000);
}

export function Toaster() {
  const [toasts, setToasts] = useState<Toast[]>([]);

  useEffect(() => {
    listeners.push(setToasts);
    return () => {
      const idx = listeners.indexOf(setToasts);
      if (idx !== -1) listeners.splice(idx, 1);
    };
  }, []);

  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
      {toasts.map((t) => (
        <div
          key={t.id}
          className={[
            "flex items-start gap-3 rounded-xl border px-4 py-3 shadow-lg backdrop-blur-sm pointer-events-auto min-w-[240px] max-w-[340px]",
            t.type === "success" ? "bg-green-50 border-green-200 text-green-900" :
            t.type === "error"   ? "bg-red-50 border-red-200 text-red-900" :
                                   "bg-white border-border text-foreground",
          ].join(" ")}
        >
          {t.type === "success" && <CheckCircle className="h-4 w-4 text-green-600 flex-shrink-0 mt-0.5" />}
          {t.type === "error"   && <AlertCircle className="h-4 w-4 text-red-600 flex-shrink-0 mt-0.5" />}
          {t.type === "info"    && <Info className="h-4 w-4 text-blue-500 flex-shrink-0 mt-0.5" />}
          <span className="text-sm flex-1 leading-snug">{t.text}</span>
          <button
            onClick={() => dismiss(t.id)}
            className="flex-shrink-0 opacity-50 hover:opacity-100 transition-opacity"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        </div>
      ))}
    </div>
  );
}
