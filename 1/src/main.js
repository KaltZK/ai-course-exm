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

const board = new Board(WIDTH, HEIGHT)
board.on_set = ([x, y], s, ps) => {
    let p = document.getElementById(`b_${x}_${y}`)
    p.classList.remove(PSTAT2CLASS[ps])
    p.classList.add(PSTAT2CLASS[s])
}

const map2stat = {
    ['.']: PosStat.Empty,
    ['X']: PosStat.Edge,
    ['#']: PosStat.Solid,
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


// next_btn.addEventListener('click', ()=>{
//     board.update()
// })
let ivid = null
const ctrl_btn = document.getElementById('ctrl_btn')
ctrl_btn.addEventListener('click', evt => {
    if(ivid){
        clearInterval(ivid)
        ivid = null
        ctrl_btn.textContent = 'START'
    }else{
        ivid = setInterval(() => {
            board.update()
        }, 100)
        ctrl_btn.textContent = 'PAUSE'
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
                board.new_agent([i, j])
            })
            tr.appendChild(td)
        }
        table.appendChild(tr)
    }
    ele.appendChild(table)
}