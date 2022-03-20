export type Board = {
    state: number[][];
    isWhiteTurn: boolean;
};

export type Player = string; // Player is identified by their email (can be found in their JWT)

export type Game = {
    id: number;
    board: Board;
    whitePlayer: Player;
    blackPlayer: Player;
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
