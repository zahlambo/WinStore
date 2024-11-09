import { useState } from "react";
import "./Card.css";

interface CardProps {
  id: string;
  name: string;
  icon: string;
}

function Card({ id, name, icon }: CardProps) {
  const [isSelected, setIsSelected] = useState(false);

  const toggleSelection = () => {
    setIsSelected(!isSelected);
  };

  return (
    <div
      className={`border-2 rounded-lg flex flex-col aspect-square w-40 hover:cursor-pointer hover:shadow-lg transition-shadow duration-200 ${
        isSelected ? "border-green-400" : "btn"
      }`}
      onClick={toggleSelection}
    >
      <span className="h-full w-full">
        <div
          className={"flex items-center justify-center h-3/4"}
          dangerouslySetInnerHTML={{ __html: icon } as { __html: string }}
        />
        <div className="flex items-center justify-center h-1/4 border-t-2s">
          <h1>{name}</h1>
        </div>
      </span>
    </div>
  );
}

export default Card;
