'use strict';
const PosStat = {
    Empty: 0,
    Solid: 1,
    Edge:  2,
    Agent: 3,
};

const Direction = {
    North: 0,
    N: 0,
    East:  1,
    E: 1,
    South: 2,
    S: 2,
    West:  3,
    W: 3
};

const DireDx = [-1, 0, +1,  0];
const DireDy = [ 0, +1, 0, -1];

const AgentPosNum= 8
const AgentPosDx = [ 1,  1,  1,  0, -1, -1, -1,  0];
const AgentPosDy = [ 1,  0, -1, -1, -1,  0,  1,  1];
const AgentTargetI = [5, 7, 1, 3]
const AgentTarget= [
    Direction.S,
    Direction.W,
    Direction.W,
    Direction.N,
    Direction.N,
    Direction.E,
    Direction.E,
    Direction.S
];

class Agent{
    constructor([x, y]){
        this.x = x
        this.y = y
    }
    next(stat){
        for(let i=0; i<AgentPosNum; i++){
            if(stat[i] != PosStat.Empty && stat[AgentTargetI[AgentTarget[i]]] == PosStat.Empty){
                return AgentTarget[i]
            }
        }
        return AgentTarget[Direction.North]
    }
    move([tx, ty]){
        const [fx, fy] = [this.x, this.y]
        this.x = tx
        this.y = ty
        // console.log([fx, fy], [tx, ty])
        this.on_move([fx, fy], [tx, ty])
    }
    on_move([fx, fy], [tx, ty]){
        throw new Exception("Unregisted agent.")
    }
    pos(){
        return [this.x, this.y]
    }
};

class Board{
    constructor(w, h, agent_template = Agent){
        this.width = w
        this.height= h
        this.data_size = w * h
        this.data  = new Array(this.data_size)
        for(let i=0; i<this.data_size; i++){
            this.data[i] = PosStat.Empty
        }
        this.agents = []
    }
    new_agent([x, y], from = Agent){
        const agent = new from([x, y])
        this.set([x, y], PosStat.Agent)
        this.register_agent(agent)
        return agent
    }
    state_at(pos){
        let [x, y] = pos
        if(this.valid_pos([x, y])){
            return this.data[x*this.width + y]
        }else{
            return PosStat.Edge
        }   
    }
    set([x, y], s){
        if( !this.valid_pos([x, y]) )
            return;
        let priv_stat = this.data[x*this.width + y]
        this.data[x*this.width + y] = s
        this.on_set([x, y], s, priv_stat)
    }
    valid_pos([x, y]){
        return x >= 0 && x < this.height && y >= 0 && y < this.width;
    }
    erase([x, y]){
        this.set([x, y], PosStat.Empty)
    }
    on_set([x, y], stat, priv_stat = PosStat.Empty){
        console.error('W: on_set noe defined')
    }
    register_agent(agent){
        agent.on_move = ([fx, fy], [tx, ty]) => {
            this.erase([fx, fy])
            this.set([tx, ty], PosStat.Agent)
        }
        this.agents.push(agent)
    }
    generate_state_at([x, y]){
        let stat = []
        for(let i=0; i<AgentPosNum; i++){
            stat.push(this.state_at([
                x + AgentPosDx[i],
                y + AgentPosDy[i]
            ]))
        }
        return stat
    }
    update(){
        for(let a of this.agents){
            let p = a.pos()
            let stat = this.generate_state_at(p)
            let t = a.next(stat)
            console.log(stat, "NESW"[t])
            let [fx, fy] = p
            let tx = fx + DireDx[t]
            let ty = fy + DireDy[t]
            if(this.valid_pos([tx, ty])){
                a.move([tx, ty])
            }else{
                console.error("Invalid Position")
            }
            console.log(`(${fx}, ${fy}) -> (${tx}, ${ty})`, this.valid_pos([tx, ty]))
        }
    }
};
