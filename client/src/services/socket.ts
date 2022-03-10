import config from '../env';
import { io } from 'socket.io-client';

const socket = io(config.SERVER_ENDPOINT);

export default socket;
