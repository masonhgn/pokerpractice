import React from 'react';
import { Value, CardType } from '../../types/game';


const suitSymbols = {
  hearts: '♥',
  diamonds: '♦',
  clubs: '♣',
  spades: '♠'
};

const suitColors = {
  hearts: '#ff4d4d',    // Brighter red
  diamonds: '#ff4d4d',  // Brighter red
  clubs: '#ffffff',     // Pure white
  spades: '#ffffff'     // Pure white
};

const valueToDisplay = (value: Value): string => {
  switch (value) {
    case 11: return 'J';
    case 12: return 'Q';
    case 13: return 'K';
    case 14: return 'A';
    default: return value.toString();
  }
};

const Card: React.FC<CardType> = ({ suit, value, faceDown = false }) => {
  if (faceDown) {
    return (
      <div className="relative w-16 h-24 rounded-lg shadow-lg overflow-hidden">
        {/* Base card */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900 to-blue-950 border border-gray-700" />
        
        {/* Pattern overlay */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 opacity-20">
            <div className="absolute inset-0 grid grid-cols-4 gap-1">
              {[...Array(20)].map((_, i) => (
                <div 
                  key={i} 
                  className="h-3 bg-blue-400 transform -rotate-45"
                />
              ))}
            </div>
          </div>
          
          {/* Center emblem */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-700 to-blue-800 flex items-center justify-center">
              <div className="w-8 h-8 rounded-full border-2 border-blue-400 opacity-30" />
            </div>
          </div>
          
          {/* Shine effect */}
          <div className="absolute inset-0 bg-gradient-to-br from-blue-400 to-transparent opacity-5" />
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-16 h-24 rounded-lg bg-gray-900 shadow-lg border border-gray-700">
      <div className="absolute inset-0 p-2 flex flex-col">
        {/* Top section */}
        <div className="flex justify-between items-start">
          <div className="text-base font-bold leading-none" style={{ color: suitColors[suit] }}>
            {valueToDisplay(value)}
          </div>
          <div className="text-base leading-none" style={{ color: suitColors[suit] }}>
            {suitSymbols[suit]}
          </div>
        </div>
        
        {/* Center section */}
        <div className="flex-grow flex items-center justify-center">
          <div className="text-3xl font-bold" style={{ color: suitColors[suit] }}>
            {suitSymbols[suit]}
          </div>
        </div>
        
        {/* Bottom section (rotated) */}
        <div className="flex justify-between items-end transform rotate-180">
          <div className="text-base font-bold leading-none" style={{ color: suitColors[suit] }}>
            {valueToDisplay(value)}
          </div>
          <div className="text-base leading-none" style={{ color: suitColors[suit] }}>
            {suitSymbols[suit]}
          </div>
        </div>
      </div>
      
      {/* Add a subtle highlight effect */}
      <div className="absolute inset-0 rounded-lg bg-white opacity-5 pointer-events-none" />
    </div>
  );
};

// // Example usage component showing a hand of cards
// const CardHand: React.FC<{ cards: Array<{ suit: Suit; value: Value }> }> = ({ cards }) => {
//   return (
//     <div className="flex space-x-2">
//       {cards.map((card, index) => (
//         <Card key={index} suit={card.suit} value={card.value} />
//       ))}
//     </div>
//   );
// };

// // Example usage:
// const ExampleUsage = () => {
//   const heroCards = [
//     { suit: 'hearts' as const, value: 14 as const },  // Ace of Hearts
//     { suit: 'spades' as const, value: 13 as const },  // King of Spades
//   ];

//   return (
//     <div className="p-8 bg-gray-800 flex flex-col space-y-8">
//       <div className="flex flex-col items-center space-y-2">
//         <div className="text-gray-400 text-sm">Hero's Hand</div>
//         <CardHand cards={heroCards} />
//       </div>
      
//       <div className="flex flex-col items-center space-y-2">
//         <div className="text-gray-400 text-sm">Villain's Hand</div>
//         <div className="flex space-x-2">
//           <Card suit="hearts" value={2} faceDown />
//           <Card suit="diamonds" value={3} faceDown />
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ExampleUsage;

export default Card;