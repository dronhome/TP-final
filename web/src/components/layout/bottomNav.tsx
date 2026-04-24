import { Home, Upload, Mic, Library, FilmIcon } from "lucide-react";
import { Link, useLocation } from "react-router-dom";

const items = [
  { path: "/", icon: Home },
  { path: "/upload", icon: Upload },
  { path: "/voice", icon: Mic },
  { path: "/exercises", icon: Library },
  { path: "/edit", icon: FilmIcon },
];

export function BottomNav() {
  const location = useLocation();

  return (
    <nav className="md:hidden fixed bottom-3 left-1/2 -translate-x-1/2 w-[92%] rounded-3xl backdrop-blur-xl shadow-gray-400 shadow-xl border border-gray-300 flex justify-around items-center py-3 z-50 bg-background/80">
      {items.map(({ path, icon: Icon }) => {
        const active = location.pathname === path;
        return (
          <Link key={path} to={path} className="flex flex-col items-center">
            <Icon className={`w-7 h-7 transition-all ${active ? "text-blue-600 scale-110" : "text-gray-600"}`} />
          </Link>
        );
      })}
    </nav>
  );
}
