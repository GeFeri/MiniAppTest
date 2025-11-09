import { useState, useRef, useEffect } from "react";
import { ChevronRight, ChevronDown } from "lucide-react";

interface HobbyBlockProps {
  hobby: {
    id: number;
    name: string;
    emoji?: string;
    color?: string;
  };
  description?: string;
}

export const HobbyBlock = ({ hobby, description }: HobbyBlockProps) => {
  const [open, setOpen] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState("0px");

  useEffect(() => {
    if (open && contentRef.current) {
      setHeight(`${contentRef.current.scrollHeight}px`);
    } else {
      setHeight("0px");
    }
  }, [open]);

  return (
    <div
      className="w-full rounded-2xl transition-all duration-300 overflow-hidden shadow-sm"
      style={{
        background: `linear-gradient(135deg, ${hobby.color || "#a5b4fc"}22, white 90%)`,
        border: `1px solid ${hobby.color || "#a5b4fc"}33`,
      }}
    >
      {/* Верхняя строка */}
      <div
        onClick={() => setOpen((p) => !p)}
        className="flex items-center justify-between p-3 cursor-pointer active:scale-[0.98] transition"
      >
        <div className="flex items-center gap-3">
          <div
            className="w-10 h-10 flex items-center justify-center rounded-full text-lg"
            style={{
              backgroundColor: `${hobby.color || "#a5b4fc"}33`,
              color: hobby.color || "#6366f1",
            }}
          >
            {hobby.emoji || "🎨"}
          </div>
          <span className="font-medium text-gray-900 text-[15px]">
            {hobby.name}
          </span>
        </div>
        {open ? (
          <ChevronDown className="text-gray-500" size={18} />
        ) : (
          <ChevronRight className="text-gray-400" size={18} />
        )}
      </div>

      {/* Описание */}
      <div
        ref={contentRef}
        style={{ height }}
        className="overflow-hidden transition-[height] duration-300"
      >
        <div className="px-4 py-3 text-sm text-gray-700 bg-white/60 backdrop-blur rounded-b-2xl">
          {description || "Нет описания"}
        </div>
      </div>
    </div>
  );
};
