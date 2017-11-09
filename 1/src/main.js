'use strict';
import {Board, PosStat} from './lib.js'
const data = `
################
#...........####
#...........####
#......O....####
#...........####
#..XXXXXX......#
#..XX..XX......#
#..XX..XX......#
#...........####
#...........####
#.....###...####
#.....###...####
################
`   .split("\n")
    .filter(s => s.length)
const WIDTH = 16;
const HEIGHT = 13;

generate_board(document.getElementById('board'), WIDTH, HEIGHT)

const PSTAT2CLASS = {
    [PosStat.Empty]: 'empty',
    [PosStat.Solid]: 'solid',
    [PosStat.Edge]: 'edge',
    [PosStat.Agent]: 'agent'
}

const CLASS2PSTAT = {
    'empty': PosStat.Empty,
    'solid': PosStat.Solid,
    'edge' : PosStat.Edge,
    'agent': PosStat.Agent
}

const board = new Board(WIDTH, HEIGHT)
board.on_set = ([x, y], s, ps) => {
    let p = document.getElementById(`b_${x}_${y}`)
    p.classList.remove(PSTAT2CLASS[ps])
    p.classList.add(PSTAT2CLASS[s])
}

const map2stat = {
    ['.']: PosStat.Empty,
    ['X']: PosStat.Solid,
    ['#']: PosStat.Edge,
    ['O']: PosStat.Agent,
}
for(let i=0; i<HEIGHT; i++){
    for(let j=0; j<WIDTH; j++){
        let s = map2stat[data[i][j]]
        if(s == PosStat.Agent){
            board.new_agent([i, j])
        }else{
            board.set([i,j], s)
        }
    }
}


let ivid = null
let block_type = null
const ctrl_btn = document.getElementById('ctrl_btn')
const next_btn = document.getElementById('next_btn')

init_select()
set_block_type('agent')

next_btn.style.display = 'block'
next_btn.addEventListener('click', ()=>{
    board.update()
})

ctrl_btn.addEventListener('click', evt => {
    if(ivid){
        clearInterval(ivid)
        ivid = null
        ctrl_btn.textContent = 'START'
        next_btn.style.display = 'block'
    }else{
        ivid = setInterval(() => {
            board.update()
        }, 100)
        ctrl_btn.textContent = 'PAUSE'
        next_btn.style.display = 'none'
    }
})

function generate_board(ele, w, h){
    const table = document.createElement('table')
    for(let i=0; i<h; i++){
        let tr = document.createElement('tr')
        for(let j=0; j<w; j++){
            let td = document.createElement('td')
            td.classList.add('b-pos')
            td.classList.add('empty')
            td.id = `b_${i}_${j}`
            td.addEventListener('click', () => {
                if(block_type === 'agent'){
                    board.new_agent([i, j])
                }else{
                    board.set([i, j], CLASS2PSTAT[block_type])
                }
            })
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    ele.appendChild(table)
}

function set_block_type(t){
    const selected_type = document.getElementById('selected_type')
    selected_type.classList.remove(block_type)
    selected_type.classList.add(t)
    block_type = t
}
function init_select(){
    document.querySelectorAll('.type-option[value]').forEach(s => {
        let val = s.getAttribute('value')
        s.addEventListener('click', evt => {
            set_block_type(val)
        })
    })
}