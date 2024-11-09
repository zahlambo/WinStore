interface CardProps {
  id: string;
  name: string;
  icon: string;
}

function Card({ id, name, icon }: CardProps) {
  return (
    <div className="border-2 rounded-lg flex flex-col aspect-square w-40 hover:cursor-pointer hover:shadow-lg transition-shadow duration-200">
      <div
        className="flex items-center justify-center h-4/5"
        dangerouslySetInnerHTML={{ __html: icon } as { __html: string }}
      />
      <div className="flex items-center justify-center h-1/5 border-t-2s">
        <h1>{name}</h1>
      </div>
    </div>
  );
}

export default Card;
