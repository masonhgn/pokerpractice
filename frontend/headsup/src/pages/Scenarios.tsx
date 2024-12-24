import React, { useState } from 'react';
import PokerTable from '../components/Table/PokerTable';
import { GameState, Decision, CardType, Suit, Value, TableProps, Position } from '../types/game';
import AnalysisBox, { AnalysisMessage } from '../components/Interface/AnalysisBox';
const convertPosition = (position: 'IP' | 'OOP'): Position => {
    return position === 'IP' ? 'dealer' : 'big blind';
  };


const Scenario = () => {
  // Initial game state
  const [villainAction, setVillainAction] = useState<Decision>({ action: null });
  const [analysisMessages, setAnalysisMessages] = useState<AnalysisMessage[]>([
    {
      id: '1',
      title: 'Raise 3BB',
      text: 'Raising 3BB preflop heads-up with AKo maximizes its value as a premium hand, applies pressure to weaker holdings, and takes control of the pot. It leverages AKo’s strong equity advantage while maintaining initiative, setting up favorable postflop scenarios regardless of whether the board hits your hand.'
    },

  ]);
  const [gameState, setGameState] = useState<GameState>({
    heroCards: [
      { suit: 'hearts' as Suit, value: 14 as Value },  // Ace of hearts
      { suit: 'spades' as Suit, value: 13 as Value }   // King of spades
    ],
    position: 'IP',
    action: 'firstToAct',
    stackSizes: {
      hero: 100,
      villain: 120
    },
    pot: 15
  });



  const tableProps: TableProps = {
    heroCards: gameState.heroCards,
    villainCards: [
      { suit: 'diamonds' as Suit, value: 2 as Value },
      { suit: 'clubs' as Suit, value: 3 as Value }
    ],
    heroStack: gameState.stackSizes.hero,
    villainStack: gameState.stackSizes.villain,
    pot: gameState.pot,
    heroPosition: convertPosition(gameState.position),
    villainAction,
    analysisMessages, 
  };

  // Action handlers
  const handleDecision = (decision: Decision) => {
    // Handle the decision here
    console.log('Decision made:', decision);
  };

  // Test controls
  const togglePosition = () => {
    setGameState((prev: GameState) => ({
      ...prev,
      position: prev.position === 'IP' ? 'OOP' : 'IP'
    }));
  };

  const cycleAction = () => {
    const actions: GameState['action'][] = ['firstToAct', 'facingRaise', 'facingCall'];
    const currentIndex = actions.indexOf(gameState.action);
    const nextIndex = (currentIndex + 1) % actions.length;
    
    setGameState((prev: GameState) => ({
      ...prev,
      action: actions[nextIndex]
    }));
  };

  const addToPot = () => {
    setGameState((prev: GameState) => ({
      ...prev,
      pot: prev.pot + 10,
      stackSizes: {
        hero: prev.stackSizes.hero - 5,
        villain: prev.stackSizes.villain - 5
      }
    }));
  };


  const cycleVillainAction = () => {
    const actions: Decision[] = [
      { action: 'check' },
      { action: 'bet', amount: 5 },
      { action: 'raise', amount: 15 },
      { action: 'call' },
      { action: 'fold' },
      { action: null }
    ];
    
    setVillainAction(prev => {
      const currentIndex = actions.findIndex(a => a.action === prev.action);
      const nextIndex = (currentIndex + 1) % actions.length;
      return actions[nextIndex];
    });
  };

  return (
    <div className="min-h-screen bg-gray-900 p-4">
      {/* Main content */}
      <div className="max-w-6xl mx-auto">
        <PokerTable {...tableProps} />
      </div>

      {/* Decision interface */}
      <div className="fixed bottom-4 left-1/2 transform -translate-x-1/2 flex gap-4">
        <button
          onClick={() => handleDecision({ action: 'fold' })}
          className="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Fold
        </button>
        <button
          onClick={() => handleDecision({ action: 'call' })}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Call
        </button>
        <button
          onClick={() => handleDecision({ action: 'raise', amount: 20 })}
          className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
        >
          Raise
        </button>
      </div>

      {/* Test controls */}
      <div className="fixed bottom-4 right-4 space-y-2">
        <div className="flex flex-col gap-2">
          <button
            onClick={togglePosition}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Toggle Position
          </button>
          <button
            onClick={cycleAction}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            Cycle Action
          </button>
          <button
            onClick={addToPot}
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Add to Pot (10 BB)
          </button>

          <button
            onClick={cycleVillainAction}
            className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
          >
            Cycle Villain Action
          </button>

        </div>
      </div>
    </div>
  );
};

export default Scenario;