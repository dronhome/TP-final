import { Button } from "@/components/ui/button"

export function ExerciseControls() {
  return (
    <div className="flex justify-center gap-4 mt-12 p-4 rounded-xl border bg-card text-card-foreground shadow-sm">
      <Button variant="default" className="!bg-yellow-500 text-white px-6">Pause</Button>
      <Button variant="default" className="!bg-red-500 text-white px-6">Stop</Button>
      <Button variant="default" className="!bg-green-500 text-white px-6">Next</Button>
    </div>
  )
}