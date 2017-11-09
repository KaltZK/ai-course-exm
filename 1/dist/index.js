/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, {
/******/ 				configurable: false,
/******/ 				enumerable: true,
/******/ 				get: getter
/******/ 			});
/******/ 		}
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _PSTAT2CLASS, _map2stat;

var _lib = __webpack_require__(1);

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var data = '\n################\n#...........####\n#...........####\n#......O....####\n#...........####\n#..XXXXXX......#\n#..XX..XX......#\n#..XX..XX......#\n#...........####\n#...........####\n#.....###...####\n#.....###...####\n################\n'.split("\n").filter(function (s) {
    return s.length;
});
var WIDTH = 16;
var HEIGHT = 13;

generate_board(document.getElementById('board'), WIDTH, HEIGHT);

var PSTAT2CLASS = (_PSTAT2CLASS = {}, _defineProperty(_PSTAT2CLASS, _lib.PosStat.Empty, 'empty'), _defineProperty(_PSTAT2CLASS, _lib.PosStat.Solid, 'solid'), _defineProperty(_PSTAT2CLASS, _lib.PosStat.Edge, 'edge'), _defineProperty(_PSTAT2CLASS, _lib.PosStat.Agent, 'agent'), _PSTAT2CLASS);

var CLASS2PSTAT = {
    'empty': _lib.PosStat.Empty,
    'solid': _lib.PosStat.Solid,
    'edge': _lib.PosStat.Edge,
    'agent': _lib.PosStat.Agent
};

var board = new _lib.Board(WIDTH, HEIGHT);
board.on_set = function (_ref, s, ps) {
    var _ref2 = _slicedToArray(_ref, 2),
        x = _ref2[0],
        y = _ref2[1];

    var p = document.getElementById('b_' + x + '_' + y);
    p.classList.remove(PSTAT2CLASS[ps]);
    p.classList.add(PSTAT2CLASS[s]);
};

var map2stat = (_map2stat = {}, _defineProperty(_map2stat, '.', _lib.PosStat.Empty), _defineProperty(_map2stat, 'X', _lib.PosStat.Solid), _defineProperty(_map2stat, '#', _lib.PosStat.Edge), _defineProperty(_map2stat, 'O', _lib.PosStat.Agent), _map2stat);
for (var i = 0; i < HEIGHT; i++) {
    for (var j = 0; j < WIDTH; j++) {
        var s = map2stat[data[i][j]];
        if (s == _lib.PosStat.Agent) {
            board.new_agent([i, j]);
        } else {
            board.set([i, j], s);
        }
    }
}

var ivid = null;
var block_type = null;
var ctrl_btn = document.getElementById('ctrl_btn');
var next_btn = document.getElementById('next_btn');

init_select();
set_block_type('agent');

next_btn.style.display = 'block';
next_btn.addEventListener('click', function () {
    board.update();
});

ctrl_btn.addEventListener('click', function (evt) {
    if (ivid) {
        clearInterval(ivid);
        ivid = null;
        ctrl_btn.textContent = 'START';
        next_btn.style.display = 'block';
    } else {
        ivid = setInterval(function () {
            board.update();
        }, 100);
        ctrl_btn.textContent = 'PAUSE';
        next_btn.style.display = 'none';
    }
});

function generate_board(ele, w, h) {
    var table = document.createElement('table');

    var _loop = function _loop(_i) {
        var tr = document.createElement('tr');

        var _loop2 = function _loop2(_j) {
            var td = document.createElement('td');
            td.classList.add('b-pos');
            td.classList.add('empty');
            td.id = 'b_' + _i + '_' + _j;
            td.addEventListener('click', function () {
                if (block_type === 'agent') {
                    board.new_agent([_i, _j]);
                } else {
                    board.set([_i, _j], CLASS2PSTAT[block_type]);
                }
            });
            tr.appendChild(td);
        };

        for (var _j = 0; _j < w; _j++) {
            _loop2(_j);
        }
        table.appendChild(tr);
    };

    for (var _i = 0; _i < h; _i++) {
        _loop(_i);
    }
    ele.appendChild(table);
}

function set_block_type(t) {
    var selected_type = document.getElementById('selected_type');
    selected_type.classList.remove(block_type);
    selected_type.classList.add(t);
    block_type = t;
}
function init_select() {
    document.querySelectorAll('.type-option[value]').forEach(function (s) {
        var val = s.getAttribute('value');
        s.addEventListener('click', function (evt) {
            set_block_type(val);
        });
    });
}

/***/ }),
/* 1 */
/***/ (function(module, exports, __webpack_require__) {

"use strict";


Object.defineProperty(exports, "__esModule", {
    value: true
});

var _slicedToArray = function () { function sliceIterator(arr, i) { var _arr = []; var _n = true; var _d = false; var _e = undefined; try { for (var _i = arr[Symbol.iterator](), _s; !(_n = (_s = _i.next()).done); _n = true) { _arr.push(_s.value); if (i && _arr.length === i) break; } } catch (err) { _d = true; _e = err; } finally { try { if (!_n && _i["return"]) _i["return"](); } finally { if (_d) throw _e; } } return _arr; } return function (arr, i) { if (Array.isArray(arr)) { return arr; } else if (Symbol.iterator in Object(arr)) { return sliceIterator(arr, i); } else { throw new TypeError("Invalid attempt to destructure non-iterable instance"); } }; }();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var PosStat = exports.PosStat = {
    Empty: 0,
    Solid: 1,
    Edge: 2,
    Agent: 3
};

var Direction = exports.Direction = {
    North: 0,
    N: 0,
    East: 1,
    E: 1,
    South: 2,
    S: 2,
    West: 3,
    W: 3
};

var DireDx = [-1, 0, +1, 0];
var DireDy = [0, +1, 0, -1];

var AgentPosNum = 8;
var AgentPosDx = [1, 1, 1, 0, -1, -1, -1, 0];
var AgentPosDy = [1, 0, -1, -1, -1, 0, 1, 1];
var AgentTargetI = [5, 7, 1, 3];
var AgentTarget = [Direction.S, Direction.W, Direction.W, Direction.N, Direction.N, Direction.E, Direction.E, Direction.S];

var Agent = exports.Agent = function () {
    function Agent(_ref) {
        var _ref2 = _slicedToArray(_ref, 2),
            x = _ref2[0],
            y = _ref2[1];

        _classCallCheck(this, Agent);

        this.x = x;
        this.y = y;
    }

    _createClass(Agent, [{
        key: 'next',
        value: function next(stat) {
            for (var i = 0; i < AgentPosNum; i++) {
                if (stat[i] != PosStat.Empty && stat[AgentTargetI[AgentTarget[i]]] == PosStat.Empty) {
                    return AgentTarget[i];
                }
            }
            return AgentTarget[Direction.North];
        }
    }, {
        key: 'move',
        value: function move(_ref3) {
            var _ref4 = _slicedToArray(_ref3, 2),
                tx = _ref4[0],
                ty = _ref4[1];

            var _ref5 = [this.x, this.y],
                fx = _ref5[0],
                fy = _ref5[1];

            this.x = tx;
            this.y = ty;
            // console.log([fx, fy], [tx, ty])
            this.on_move([fx, fy], [tx, ty]);
        }
    }, {
        key: 'on_move',
        value: function on_move(_ref6, _ref7) {
            var _ref9 = _slicedToArray(_ref6, 2),
                fx = _ref9[0],
                fy = _ref9[1];

            var _ref8 = _slicedToArray(_ref7, 2),
                tx = _ref8[0],
                ty = _ref8[1];

            throw new Exception("Unregisted agent.");
        }
    }, {
        key: 'pos',
        value: function pos() {
            return [this.x, this.y];
        }
    }]);

    return Agent;
}();

;

var Board = exports.Board = function () {
    function Board(w, h) {
        var agent_template = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : Agent;

        _classCallCheck(this, Board);

        this.width = w;
        this.height = h;
        this.data_size = w * h;
        this.data = new Array(this.data_size);
        for (var i = 0; i < this.data_size; i++) {
            this.data[i] = PosStat.Empty;
        }
        this.agents = [];
    }

    _createClass(Board, [{
        key: 'new_agent',
        value: function new_agent(_ref10) {
            var _ref11 = _slicedToArray(_ref10, 2),
                x = _ref11[0],
                y = _ref11[1];

            var from = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : Agent;

            var agent = new from([x, y]);
            this.set([x, y], PosStat.Agent);
            this.register_agent(agent);
            return agent;
        }
    }, {
        key: 'state_at',
        value: function state_at(pos) {
            var _pos = _slicedToArray(pos, 2),
                x = _pos[0],
                y = _pos[1];

            if (this.valid_pos([x, y])) {
                return this.data[x * this.width + y];
            } else {
                return PosStat.Edge;
            }
        }
    }, {
        key: 'set',
        value: function set(_ref12, s) {
            var _ref13 = _slicedToArray(_ref12, 2),
                x = _ref13[0],
                y = _ref13[1];

            if (!this.valid_pos([x, y])) return;
            var priv_stat = this.data[x * this.width + y];
            if (priv_stat != PosStat.Empty && !(s == PosStat.Empty && priv_stat == PosStat.Agent)) {
                console.error('W: non-empty chunk changed.');
            }
            this.data[x * this.width + y] = s;
            this.on_set([x, y], s, priv_stat);
        }
    }, {
        key: 'valid_pos',
        value: function valid_pos(_ref14) {
            var _ref15 = _slicedToArray(_ref14, 2),
                x = _ref15[0],
                y = _ref15[1];

            return x >= 0 && x < this.height && y >= 0 && y < this.width;
        }
    }, {
        key: 'erase',
        value: function erase(_ref16) {
            var _ref17 = _slicedToArray(_ref16, 2),
                x = _ref17[0],
                y = _ref17[1];

            this.set([x, y], PosStat.Empty);
        }
    }, {
        key: 'on_set',
        value: function on_set(_ref18, stat) {
            var _ref19 = _slicedToArray(_ref18, 2),
                x = _ref19[0],
                y = _ref19[1];

            var priv_stat = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : PosStat.Empty;

            console.error('W: on_set noe defined');
        }
    }, {
        key: 'register_agent',
        value: function register_agent(agent) {
            var _this = this;

            agent.on_move = function (_ref20, _ref21) {
                var _ref23 = _slicedToArray(_ref20, 2),
                    fx = _ref23[0],
                    fy = _ref23[1];

                var _ref22 = _slicedToArray(_ref21, 2),
                    tx = _ref22[0],
                    ty = _ref22[1];

                _this.erase([fx, fy]);
                _this.set([tx, ty], PosStat.Agent);
            };
            this.agents.push(agent);
        }
    }, {
        key: 'generate_state_at',
        value: function generate_state_at(_ref24) {
            var _ref25 = _slicedToArray(_ref24, 2),
                x = _ref25[0],
                y = _ref25[1];

            var stat = [];
            for (var i = 0; i < AgentPosNum; i++) {
                stat.push(this.state_at([x + AgentPosDx[i], y + AgentPosDy[i]]));
            }
            return stat;
        }
    }, {
        key: 'update',
        value: function update() {
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = this.agents[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var a = _step.value;

                    var p = a.pos();
                    var stat = this.generate_state_at(p);
                    var t = a.next(stat);

                    var _p = _slicedToArray(p, 2),
                        fx = _p[0],
                        fy = _p[1];

                    var tx = fx + DireDx[t];
                    var ty = fy + DireDy[t];
                    if (this.valid_pos([tx, ty])) {
                        a.move([tx, ty]);
                    } else {
                        console.error("Invalid Position");
                    }
                    // console.log(`(${fx}, ${fy}) -> (${tx}, ${ty})`, this.valid_pos([tx, ty]))
                }
            } catch (err) {
                _didIteratorError = true;
                _iteratorError = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion && _iterator.return) {
                        _iterator.return();
                    }
                } finally {
                    if (_didIteratorError) {
                        throw _iteratorError;
                    }
                }
            }
        }
    }]);

    return Board;
}();

;

/***/ })
/******/ ]);