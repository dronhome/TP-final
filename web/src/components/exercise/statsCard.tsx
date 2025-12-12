import {
  Card,
  CardContent,
} from "@/components/ui/card"

export function StatsCard() {
  return (
    <Card className="w-full shadow">
        <CardContent className="py-4 px-6 grid grid-cols-3 text-center gap-4">
            <div>
                <p className="text-sm">Repetície:</p>
                <p className="font-bold">5 / 15</p>
            </div>
            <div>
                <p className="text-sm">Čas:</p>
                <p className="font-bold">00:50</p>
            </div>
            <div>
                <p className="text-sm">Kalórie:</p>
                <p className="font-bold">12 kcal</p>
            </div>
        </CardContent>
    </Card>
  )
}
