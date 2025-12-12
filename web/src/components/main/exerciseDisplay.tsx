import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { BicepsFlexed, Play } from "lucide-react";
<BicepsFlexed />;
interface Exercise {
  id: number;
  name: string;
  description?: string;
}

interface ExerciseDisplayProps {
  exercises: Exercise[];
}

export function ExerciseDisplay({ exercises }: ExerciseDisplayProps) {
  return (
    <Card className="shadow-lg">
      <CardHeader className="w-full flex items-center gap-2 text-2xl font-semibold">
        <BicepsFlexed />
        Exercises
      </CardHeader>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {exercises.map((exercise) => (
          <Card key={exercise.id} className=" shadow mx-3">
            <CardContent className=" text-center">
              <div className="w-full flex items-center">
                <Play className="mr-1" />
                <h3 className="font-bold text-lg">{exercise.name}</h3>
              </div>

              {exercise.description && (
                <p className="text-sm mt-2">{exercise.description}</p>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </Card>
  );
}
