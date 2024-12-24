import React from 'react';

interface StackProps {
  amount: number;  // Amount in big blinds
  label?: string;  // Optional label (e.g., "Pot" or "Stack")
}

const Stack: React.FC<StackProps> = ({ amount, label }) => {
  // Calculate number of visible chips (max 8 for visual clarity)
  const getVisibleChips = (bbAmount: number) => {
    if (bbAmount <= 0) return 0;
    if (bbAmount <= 10) return 2;
    if (bbAmount <= 25) return 3;
    if (bbAmount <= 50) return 4;
    if (bbAmount <= 100) return 5;
    if (bbAmount <= 200) return 6;
    if (bbAmount <= 500) return 7;
    return 8;
  };

  const visibleChips = getVisibleChips(amount);

  const Chip: React.FC<{ index: number; total: number }> = ({ index, total }) => {
    // Calculate offset for stacking effect
    const offsetY = -index * 4;
    
    return (
      <div 
        className="absolute left-0 right-0"
        style={{ 
          transform: `translateY(${offsetY}px)`,
          zIndex: index
        }}
      >
        <div className="relative mx-auto w-12 h-12">
          {/* Base chip circle */}
          <div className="absolute inset-0 rounded-full bg-gradient-to-br from-gray-700 to-gray-900 border-2 border-gray-600 shadow-lg" />
          
          {/* Inner ring */}
          <div className="absolute inset-2 rounded-full border-2 border-gray-600" />
          
          {/* Center dot */}
          <div className="absolute inset-4 rounded-full bg-gray-600" />
          
          {/* Shine effect */}
          <div className="absolute inset-0 rounded-full bg-gradient-to-t from-transparent to-white opacity-10" />
        </div>
      </div>
    );
  };

  return (
    <div className="relative flex flex-col items-center">
      <div className="relative w-full">
        {/* Chip stack */}
        <div className="relative h-20">
          {Array.from({ length: visibleChips }).map((_, index) => (
            <Chip key={index} index={index} total={visibleChips} />
          ))}
        </div>
        
        {/* Amount display - positioned closer to chips */}
        <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
          <div className="bg-gray-800 bg-opacity-50 px-3 py-1 rounded-full flex flex-col items-center">
            <span className="text-yellow-400 font-bold">
              {amount} BB
            </span>
            {label && (
              <span className="text-gray-400 text-xs">
                {label}
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// // Example usage
// const ExampleStacks = () => {
//   const examples = [
//     { amount: 5, label: "Small Stack" },
//     { amount: 25, label: "Medium Stack" },
//     { amount: 100, label: "Large Stack" },
//     { amount: 500, label: "Pot" },
//   ];

//   return (
//     <div className="p-8 bg-gray-900 grid grid-cols-4 gap-8">
//       {examples.map((example, index) => (
//         <div key={index} className="flex justify-center">
//           <Stack {...example} />
//         </div>
//       ))}
//     </div>
//   );
// };

// export default ExampleStacks;

export default Stack;