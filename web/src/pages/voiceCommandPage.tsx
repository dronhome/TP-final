import { VoiceCommander } from "@/components/main/voiceCommander";

export default function VoiceCommandPage() {
  return (
    <div className="w-full max-w-xl mx-auto px-4 py-6 pb-24 space-y-4">
      <div>
        <h1 className="text-xl font-semibold tracking-tight text-foreground">Hlasové príkazy</h1>
        <p className="text-xs text-muted-foreground mt-0.5">Ovládajte robota NAO hlasom.</p>
      </div>
      <VoiceCommander />
    </div>
  );
}
