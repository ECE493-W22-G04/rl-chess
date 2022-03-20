export interface Jwt {
    fresh: boolean;
    iat: number;
    jti: string;
    type: string;
    sub: string;
    nbf: number;
    exp: number;
}
