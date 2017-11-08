
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


let data = 
`################
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
################`.split("\n")

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
setInterval(() => {
    board.update()
}, 100)