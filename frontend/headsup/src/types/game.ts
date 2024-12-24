// types/game.ts


export type Suit = 'hearts' | 'diamonds' | 'clubs' | 'spades';
export type Value = 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14;
export type Position = 'dealer' | 'big blind';
import { AnalysisMessage } from '../components/Interface/AnalysisBox';
export interface CardType {
  suit: Suit;
  value: Value;
  faceDown?: boolean;
  // 11=J, 12=Q, 13=K, 14=A
}



export interface TableProps { 
  heroCards: Array<{ suit: Suit; value: Value }>;
  villainCards: Array<{ suit: Suit; value: Value }>;
  heroStack: number;
  villainStack: number;
  pot: number;
  heroPosition: Position;
  villainAction?: Decision;
  analysisMessages?: AnalysisMessage[];
}


export interface GameState {
  heroCards: CardType[];
  position: 'IP' | 'OOP';
  action: 'firstToAct' | 'facingRaise' | 'facingCall';
  stackSizes: {
    hero: number;
    villain: number;
  };
  pot: number;
}


export interface Decision {
  action: 'check' | 'bet' | 'raise' | 'call' | 'fold' | null;
  amount?: number;
}

