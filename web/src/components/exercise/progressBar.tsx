import { Progress } from "@/components/ui/progress"

export function ProgressBar() {
  return (
    <div className="px-4 mt-12">
      <p className="mb-8 font-medium">Motivácia: Skvelá práca!</p>

      <div className="p-4 rounded-xl border bg-card text-card-foreground shadow-sm">
        <p className="text-sm text-left mb-2">Progress bar</p>
        <Progress value={40} />
      </div>
    </div>
  )
}