import { useEffect, useState } from "react";
import { getTypeHobbies, createHobby, addUserHobby } from "../api/hobbiesApi";
import type { TypeHobby } from "../api/types";
import EmojiPicker from "emoji-picker-react";
import { HexColorPicker } from "react-colorful";

interface AddHobbyModalProps {
  onClose: () => void;
  onCreated: () => void;
}

export const AddHobbyModal = ({ onClose, onCreated }: AddHobbyModalProps) => {
  const [types, setTypes] = useState<TypeHobby[]>([]);
  const [typeId, setTypeId] = useState("");
  const [name, setName] = useState("");
  const [emoji, setEmoji] = useState("🎨");
  const [color, setColor] = useState("#a5b4fc");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);

  // Загружаем категории (типы хобби)
  useEffect(() => {
    getTypeHobbies().then(setTypes).catch(console.error);
  }, []);

  const handleSave = async () => {
    if (!typeId || !name) return;
    setLoading(true);
    try {
      const newHobby = await createHobby({
        name,
        emoji,
        color,
        type_id: Number(typeId),
      });
      await addUserHobby({
        hobby_id: newHobby.id,
        description,
      });
      onCreated();
      onClose();
    } catch (err) {
      console.error("Ошибка при создании хобби:", err);
      alert("Не удалось создать хобби. Проверьте данные.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl w-[90%] max-w-sm p-5 shadow-xl overflow-y-auto max-h-[90vh]">
        <h2 className="text-lg font-semibold mb-4 text-center text-gray-900">
          Создать хобби
        </h2>

        {/* Тип хобби */}
        <div className="mb-3">
          <label className="block text-sm font-medium mb-1 text-gray-700">
            Тип хобби
          </label>
          <select
              value={typeId}
              onChange={(e) => setTypeId(e.target.value)}
              className="w-full border rounded-xl p-2 text-sm"
          >
            <option value="">Выберите тип</option>
            {types.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
            ))}
          </select>
        </div>

        {/* Название */}
        <div className="mb-3">
          <label className="block text-sm font-medium mb-1 text-gray-700">
            Название
          </label>
          <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Например: Плавание"
              className="w-full border rounded-xl p-2 text-sm"
          />
        </div>

        {/* Эмодзи */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1 text-gray-700">
            Эмодзи
          </label>
          <div className="border rounded-xl p-2 bg-gray-50">
            <EmojiPicker
                onEmojiClick={(e) => setEmoji(e.emoji)}
                width="100%"
                height={260}
                searchDisabled
                skinTonesDisabled
                previewConfig={{showPreview: false}}
                emojiStyle="EmojiStyle.APPLE"
            />
          </div>
          <p className="text-center mt-2 text-2xl">{emoji}</p>
        </div>

        {/* Цвет */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1 text-gray-700">
            Цвет
          </label>
          <div className="border rounded-xl p-3 flex flex-col items-center">
            <HexColorPicker color={color} onChange={setColor}/>
            <p className="text-sm mt-2 text-gray-600">{color}</p>
          </div>
        </div>

        {/* Описание */}
        <div className="mb-5">
          <label className="block text-sm font-medium mb-1 text-gray-700">
            Описание (необязательно)
          </label>
          <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Например: играю с друзьями по выходным"
              className="w-full border rounded-xl p-2 text-sm resize-none h-20"
          />
        </div>

        {/* Кнопки */}
        <div className="flex justify-between">
          <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-100 rounded-xl hover:bg-gray-200 active:scale-[0.98] transition"
          >
            Отмена
          </button>
          <button
              onClick={handleSave}
              disabled={!typeId || !name || loading}
              className={`px-4 py-2 rounded-xl text-white transition active:scale-[0.98] ${
                  !typeId || !name || loading
                      ? "bg-gray-300 cursor-not-allowed"
                      : "bg-[#2a5885] hover:bg-[#244a75]"
              }`}
          >
            {loading ? "Создание..." : "Создать"}
          </button>
        </div>
      </div>
    </div>
  );
};
