function Card() {
  return (
    <div className="border-2 rounded-lg flex flex-col aspect-square w-40 hover:cursor-pointer hover:shadow-lg transition-shadow duration-200">
        <p className="h-4/5">A Card</p>
        <div className="flex items-center justify-center h-1/5 border-t-2s">
          <h1>Card</h1>
        </div>
    </div>
  );
}

export default Card;
