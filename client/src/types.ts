export type Board = {
    state: number[][];
    isWhiteTurn: boolean;
};

export type Player = string; // Player is identified by their email (can be found in their JWT)

export type Game = {
    id: string;
    board: Board;
    whitePlayer: Player | null;
    blackPlayer: Player | null;
    host: Player;
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
