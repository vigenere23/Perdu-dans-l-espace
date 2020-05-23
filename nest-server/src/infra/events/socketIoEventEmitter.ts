import { Server, Namespace } from 'socket.io'
import { Service } from 'typedi'
import { EventEmitter as GamesEventEmitter } from '../../domain/events/gamesEventEmitter'
import { Player } from '../../domain/players/player'
import { PlayerId } from '../../domain/players/playerId'

@Service()
export class SocketIoGamesEventEmitter implements GamesEventEmitter {
    private io: Namespace

    constructor(io: Server) {
        this.io = io.of('/games')
    }

    sendStartGame(world: string, socketIds: Array<string>): void {
        socketIds.forEach(socketId => {
            this.io.to(socketId).emit('start', {
                world
            })
        })
    }

    sendPlayerUpdate(player: Player, socketIds: Array<string>): void {
        socketIds
            .filter(socketId => !PlayerId.fromSocketId(socketId).equals(player.id))
            .forEach(socketId => {
                this.io.to(socketId).emit('update', {
                    username: player.id.toString(),
                    ...player.position
                })
            })
    }
}