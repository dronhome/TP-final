import { ArrowLeft } from "lucide-react";

interface HeaderProps {
  title: string;
}

export function Header({ title }: HeaderProps) {
  return (
    <header className="fixed top-0 left-0 w-full bg-white border-b z-50">
      <div className="flex items-center gap-3 px-4 py-4 max-w-sm mx-auto">
        <button
          onClick={() => window.history.back()}
          className="!p-2 !rounded-full !bg-transparent !hover:bg-gray-100 !active:bg-gray-200 !transition"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>

        <h2 className="text-xl font-medium">{title}</h2>
      </div>
    </header>
  );
}
