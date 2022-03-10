import config from '../config';
import { io } from 'socket.io-client';

const socket = io(config.SERVER_ENDPOINT);

export default socket;
