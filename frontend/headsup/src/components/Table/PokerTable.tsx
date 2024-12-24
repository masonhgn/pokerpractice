import React from 'react';
import Stack from './Stack';
import Card from './Cards';
import VillainAction from './VillainAction';
import AnalysisBox from '../Interface/AnalysisBox';
import { TableProps } from '../../types/game';

const DealerButton: React.FC = () => (
  <div className="relative w-8 h-8">
    <div className="absolute inset-0 rounded-full bg-white shadow-lg flex items-center justify-center">
      <div className="text-gray-900 font-bold text-sm">D</div>
    </div>
    <div className="absolute inset-0 rounded-full bg-gradient-to-t from-transparent to-white opacity-30" />
  </div>
);

const PokerTable: React.FC<TableProps> = ({
  heroCards,
  villainCards,
  heroStack,
  villainStack,
  pot,
  heroPosition,
  villainAction,
  analysisMessages
}) => {
  return (
    <div className="relative w-full max-w-5xl aspect-[2/1.2] rounded-[16rem] overflow-hidden">
      {/* Table border and felt */}
      <div className="absolute inset-0 bg-gray-900 shadow-2xl">
        {/* Felt pattern */}
        <div className="absolute inset-0 bg-[#1a4a2e] opacity-90">
          <div className="absolute inset-0" style={{
            backgroundImage: `
              radial-gradient(circle at 2px 2px, rgba(255,255,255,0.1) 1px, transparent 1px)
            `,
            backgroundSize: '16px 16px'
          }} />
        </div>

        {/* Table content */}
        <div className="relative h-full flex justify-center">
          {/* Main table content */}
          <div className="w-[400px] flex flex-col items-center justify-between p-8">
            {/* Villain section */}
            <div className="flex flex-col items-center relative w-full">
              <Stack amount={villainStack} />
              <div className="flex space-x-2 mt-4 relative">
                {villainCards.map((card, index) => (
                  <Card
                    key={index}
                    suit={card.suit}
                    value={card.value}
                    faceDown={true}
                  />
                ))}
                {villainAction && villainAction.action && (
                  <div className="absolute left-full ml-4 top-1/2 -translate-y-1/2 whitespace-nowrap">
                    <div className="bg-gray-800 text-white px-4 py-2 rounded-lg shadow-lg">
                      {villainAction.action === 'bet' || villainAction.action === 'raise' 
                        ? `${villainAction.action.charAt(0).toUpperCase() + villainAction.action.slice(1)} ${villainAction.amount}BB`
                        : villainAction.action.charAt(0).toUpperCase() + villainAction.action.slice(1)}
                    </div>
                  </div>
                )}
              </div>
              {heroPosition === 'big blind' && (
                <div className="absolute left-60 top-1/2 transform -translate-y-1/2">
                  <DealerButton />
                </div>
              )}
            </div>

            {/* Pot section */}
            <div className="flex flex-col items-center my-4">
              <Stack amount={pot} label="Pot" />
            </div>

            {/* Hero section */}
            <div className="flex flex-col items-center relative w-full">
              <div className="flex space-x-2 mb-6">
                {heroCards.map((card, index) => (
                  <Card
                    key={index}
                    suit={card.suit}
                    value={card.value}
                    faceDown={false}
                  />
                ))}
              </div>
              <Stack amount={heroStack} />
              {heroPosition === 'dealer' && (
                <div className="absolute left-60 top-1/2 transform -translate-y-1/2">
                  <DealerButton />
                </div>
              )}
            </div>
          </div>

          {/* Analysis box section */}
          {analysisMessages && (
            <div className="w-72 py-8 pr-8 flex items-center">
              <AnalysisBox 
                messages={analysisMessages}
                maxHeight="400px"
                className="w-full"
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PokerTable;