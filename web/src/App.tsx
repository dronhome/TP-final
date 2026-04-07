import { Routes, Route } from "react-router-dom";
import MainPage from "./pages/mainPage";
import ExercisePage from "./pages/exercisePage";
import VideoEditor from "./pages/videoEditor";
import GroupPage from "./pages/groupPage";

function App() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/exercise" element={<ExercisePage />} />
        <Route path="/group" element={<GroupPage />} />
        <Route path="/edit" element={<VideoEditor />} />
      </Routes>
    </div>
  );
}

export default App;