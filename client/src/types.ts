export type Board = {
    state: number[][];
    is_white_turn: boolean;
    moves: Move[];
};

export type Move = {
    from_square: Square;
    to_square: Square;
    promotion: number; // piece
};

export type Square = {
    x: number;
    y: number;
};

export type Player = string; // Player is identified by their email (can be found in their JWT)

export type Game = {
    id: string;
    board: Board;
    white_player: Player | null;
    black_player: Player | null;
    host: Player;
    has_started: boolean;
};

export interface Jwt {
    fresh: boolean;
    iat: number;
    jti: string;
    type: string;
    sub: string;
    nbf: number;
    exp: number;
}

export type GameOverMessage = {
    winner: string;
};

export type OfferDrawMessage = {
    offer_draw_to: string;
};

export type LeaderboardEntry = {
    email: string;
    numWins: number;
};

export type Leaderboard = LeaderboardEntry[];
