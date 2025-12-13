import { useState } from "react";
import { FileUpload } from "@/components/ui/file-upload";
import { ExerciseDisplay } from "@/components/main/exerciseDisplay";
import { Button } from "@/components/ui/button";
import { BottomNav } from "../components/layout/bottomNav";
import { Card } from "@/components/ui/card";

export default function MainPage() {
  const [file, setFile] = useState<File | null>(null);
  console.log(file);

  const handleFileUpload = (files: File[]) => {
    if (files.length > 0) {
      setFile(files[0]);
      console.log(files[0]);
    }
  };
  const exerciseList = [
    { id: 1, name: "Push-ups", description: "Do 20 reps" },
    { id: 2, name: "Squats", description: "Do 15 reps" },
    { id: 3, name: "Plank", description: "Hold for 60s" },
    { id: 4, name: "Push-ups", description: "Do 20 reps" },
    { id: 5, name: "Squats", description: "Do 15 reps" },
  ];

  return (
    <div className="w-full max-w-sm rounded-md ">
      <Card className="mb-3 shadow-lg">
        <FileUpload onChange={handleFileUpload} />

        <Button variant="default" size="lg" className=" text-white  mx-2 ">
          Create New Exercise
        </Button>
      </Card>
      <ExerciseDisplay exercises={exerciseList} />
      <BottomNav />
    </div>
  );
}


