import React from 'react';

export interface AnalysisMessage {
  id: string;
  title: string;
  text: string;
}

interface AnalysisBoxProps {
  messages: AnalysisMessage[];
  maxHeight?: string;
  className?: string;
}

const AnalysisBox: React.FC<AnalysisBoxProps> = ({ 
  messages, 
  maxHeight = "300px",
  className = "" 
}) => {
  return (
    <div className={`bg-gray-800 rounded-lg shadow-lg p-4 ${className}`}>
      <h3 className="text-white text-lg font-semibold mb-3 border-b border-gray-700 pb-2">
        Analysis
      </h3>
      
      <div 
        className="space-y-3 overflow-y-auto"
        style={{ maxHeight }}
      >
        {messages.map((message) => (
          <div
            key={message.id}
            className="bg-gray-700 rounded-lg p-3 text-white"
          >
            <h4 className="font-bold text-sm text-emerald-400 mb-1">
              {message.title}
            </h4>
            <p className="text-sm">{message.text}</p>
          </div>
        ))}
        
        {messages.length === 0 && (
          <div className="text-gray-500 text-sm italic text-center py-4">
            No analysis messages yet
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalysisBox;