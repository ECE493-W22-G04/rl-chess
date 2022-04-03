export type Board = {
    state: number[][];
    is_white_turn: boolean;
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
