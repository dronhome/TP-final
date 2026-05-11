import { useState, useEffect } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { toast } from "@/components/ui/toaster";
import { Loader2, X } from "lucide-react";

const API_BASE_URL = "/api";

export default function SimpleUploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    return () => { if (previewUrl) URL.revokeObjectURL(previewUrl); };
  }, [previewUrl]);

  const handleFileUpload = (files: File[]) => {
    if (!files.length) return;
    const selected = files[0];
    setFile(selected);
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(URL.createObjectURL(selected));
  };

  const clearFile = () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setFile(null);
    setPreviewUrl(null);
  };

  const sendToBackend = async () => {
    if (!file) { toast("Najprv vyberte súbor", "error"); return; }
    setIsUploading(true);
    try {
      const isVideo = file.type.startsWith("video/");
      const isImage = file.type.startsWith("image/");
      if (!isVideo && !isImage) throw new Error("Nahrajte platný video alebo obrázkový súbor");

      const formData = new FormData();
      if (isVideo) {
        formData.append("video", file);
        formData.append("fps", "1");
        formData.append("seconds", "-1");
      } else {
        formData.append("image", file);
      }

      const response = await fetch(isVideo ? `${API_BASE_URL}/arms/from_video` : `${API_BASE_URL}/arms/from_image`, {
        method: "POST",
        body: formData,
      });

      let responseData: any = null;
      try { responseData = await response.json(); } catch {}

      if (!response.ok) {
        const details = [responseData?.detail, responseData?.error, responseData?.message].filter(Boolean);
        throw new Error(`Chyba servera (${response.status}): ${details.join(" | ") || response.statusText}`);
      }

      toast(`${isVideo ? "Video" : "Obrázok"} úspešne nahraný!`, "success");
    } catch (error) {
      toast(error instanceof Error ? error.message : "Nahranie súboru zlyhalo", "error");
    } finally {
      setIsUploading(false);
    }
  };

  const isVideo = file?.type.startsWith("video/");

  return (
    <div className="w-full max-w-xl mx-auto px-4 py-6 pb-24 space-y-4">
      <div>
        <h1 className="text-xl font-semibold tracking-tight text-foreground">Jednoduché nahranie</h1>
        <p className="text-xs text-muted-foreground mt-0.5">Nahrajte video alebo obrázok a odošlite ho do API robota.</p>
      </div>

      <Card className="shadow-sm">
        <FileUpload onChange={handleFileUpload} />

        {file && previewUrl && (
          <div className="px-4 pb-4 space-y-3">
            <div className="relative bg-gray-100 rounded-lg overflow-hidden">
              <button onClick={clearFile} className="absolute top-2 right-2 z-10 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors">
                <X className="h-4 w-4" />
              </button>
              {isVideo
                ? <video src={previewUrl} controls className="w-full max-h-80 object-contain" />
                : <img src={previewUrl} alt="Náhľad" className="w-full max-h-80 object-contain" />
              }
            </div>
            <p className="text-xs text-muted-foreground">
              {file.name} · {(file.size / 1024 / 1024).toFixed(2)} MB · {isVideo ? "Video" : "Obrázok"}
            </p>
            <Button onClick={sendToBackend} disabled={isUploading} className="w-full text-white">
              {isUploading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />Nahrávanie…</> : "Odoslať do API"}
            </Button>
          </div>
        )}

      </Card>
    </div>
  );
}
