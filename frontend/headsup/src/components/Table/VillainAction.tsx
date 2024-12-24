// components/Table/VillainAction.tsx
import React from 'react';
import { Decision as VillainActionType } from '../../types/game';

interface VillainActionProps {
  action: VillainActionType;
}

const VillainAction: React.FC<VillainActionProps> = ({ action }) => {
  if (!action || action.action === null) {
    return null;
  }

  const getActionText = () => {
    switch (action.action) {
      case 'check':
        return 'Check';
      case 'bet':
        return `Bet ${action.amount}BB`;
      case 'raise':
        return `Raise to ${action.amount}BB`;
      case 'call':
        return 'Call';
      case 'fold':
        return 'Fold';
      default:
        return '';
    }
  };

  return (
    <div className="absolute -right-32 top-1/2 transform -translate-y-1/2">
      <div className="bg-gray-800 text-white px-4 py-2 rounded-lg shadow-lg">
        <span className="text-sm font-medium">{getActionText()}</span>
      </div>
    </div>
  );
};

export default VillainAction;