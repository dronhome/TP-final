import { Home, BicepsFlexed, User } from "lucide-react";
import { Link, useLocation } from "react-router-dom";

export function BottomNav() {
  const location = useLocation();

  const items = [
    { path: "/", icon: Home },
    { path: "/exercise", icon: BicepsFlexed },
    { path: "/group", icon: User },
  ];

  return (
    <nav className="fixed bottom-3 left-1/2 -translate-x-1/2 w-[92%] rounded-3xl  backdrop-blur-xl shad shadow-gray-400 shadow-xl border border-gray-300 flex justify-around items-center py-3 z-50">
      {items.map(({ path, icon: Icon }) => {
        const active = location.pathname === path;
        return (
          <Link key={path} to={path} className="flex flex-col items-center">
            <Icon
              className={`w-9 h-9 transition-all ${
                active ? "text-blue-600 scale-110" : "text-gray-600"
              }`}
            />
          </Link>
        );
      })}
    </nav>
  );
}
