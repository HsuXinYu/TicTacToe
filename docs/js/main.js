var EMPTY = 1;
var PLAYER_0 = 0;
var PLAYER_1 = 2;
var PLAYERS = [PLAYER_0, PLAYER_1];
var game_state = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]];
var turn = 1;
var game_mode = EMPTY;

function who_won(game_state) {
    if (game_state[0][0] != EMPTY) {
        if (game_state[0][0] == game_state[0][1] && game_state[0][0] == game_state[0][2]) {
            return game_state[0][0];
        }
        if (game_state[0][0] == game_state[1][0] && game_state[0][0] == game_state[2][0]) {
            return game_state[0][0];
        }
        if (game_state[0][0] == game_state[1][1] && game_state[0][0] == game_state[2][2]) {
            return game_state[0][0];
        }
    }
    if (game_state[1][0] != EMPTY) {
        if (game_state[1][0] == game_state[1][1] && game_state[1][0] == game_state[1][2]) {
            return game_state[1][0];
        }
    }
    if (game_state[0][1] != EMPTY) {
        if (game_state[0][1] == game_state[1][1] && game_state[0][1] == game_state[2][1]) {
            return game_state[0][1];
        }
    }
    if (game_state[0][2] != EMPTY) {
        if (game_state[0][2] == game_state[1][1] && game_state[0][2] == game_state[2][0]) {
            return game_state[0][2];
        }
    }
    if (game_state[2][2] != EMPTY) {
        if (game_state[2][2] == game_state[2][1] && game_state[2][2] == game_state[2][0]) {
            return game_state[2][2];
        }
        if (game_state[2][2] == game_state[1][2] && game_state[2][2] == game_state[0][2]) {
            return game_state[2][2];
        }
    }
    if (game_state.every(function (arr) {
        return arr.every(function (val) { return val != EMPTY; })
    })) {
        return -2; //draw
    }
    else {
        return EMPTY; //ongoing
    }
}

function update_html(game_state) {
    var row_id = 0;
    var col_id = 0;
    for (row_id = 0; row_id < 3; row_id++) {
        for (col_id = 0; col_id < 3; col_id++) {
            var div_id = "#cell_" + row_id.toString() + "_" + col_id.toString();
            // console.log(div_id + "" + game_state[row_id][col_id].toString());
            switch (game_state[row_id][col_id]) {
                case PLAYER_1:
                    $(div_id).addClass("angel");
                    break;
                case PLAYER_0:
                    $(div_id).addClass("demon");
                    break;
                default:
                    break;
            }
        }
    }
}

function reset_game(e) {
    $("#status").html("");
    $("#status").removeClass("angel");
    $("#status").removeClass("demon");
    $('.cell').removeClass("angel");
    $('.cell').removeClass("demon");
    game_state = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]];
    turn = 0;
    game_mode = EMPTY;
    update_html(game_state);


}

async function reset_game_0(e) {
    reset_game(e);
    game_mode = PLAYER_0;
    await auto_move();
    update_html(game_state);
}

async function reset_game_1(e) {
    reset_game(e);
    game_mode = PLAYER_1;

}

var models = [];
async function LoadModel(){
    const modelUrl0 = 'models/dqn_ttt0_js/model.json';
    models.push(await tf.loadLayersModel(modelUrl0));

    const modelUrl1 = 'models/dqn_ttt0_js/model.json';
    models.push(await tf.loadLayersModel(modelUrl1));
    // console.log("Model loaded")

    // const sample_inp = tf.tensor3d([0,1,1,1,1,1,1,1,1],[1,1,9]);
    // models[0].predict(sample_inp).print();
    // models[1].predict(sample_inp).print();

}

async function predict(){

    var inp = tf.tensor3d(game_state.flat(),[1,1,9]);
    var valid_action = inp.equal(EMPTY);
    if(game_mode == PLAYER_0){
        var q_action = models[0].predict(inp);
    }
    else{
        var q_action = models[1].predict(inp);
    }
    var action = valid_action.mul(q_action).argMax(axis=2).arraySync()[0][0];
    // console.log(action.arraySync()[0][0]);
    var col_id = action%3;
    var row_id = (action - col_id)/3;
    return [row_id, col_id];
}

async function auto_move(){
    result_val = who_won(game_state);
    if(result_val != EMPTY){
        return;
    }
    if(game_mode != PLAYER_1 && game_mode != PLAYER_0){
        return;
    }
    var [row_id, col_id] = await predict();
    
    if (game_state[row_id][col_id] == EMPTY) {
        game_state[row_id][col_id] = PLAYERS[turn];
        turn = 1 - turn;
    }
    
    
}

async function update(element){
    // console.log(this.id[5]);
    var row_id = parseInt(element.id[5]);
    var col_id = parseInt(element.id[7]);
    if (game_state[row_id][col_id] == EMPTY) {
        game_state[row_id][col_id] = PLAYERS[turn];
        turn = 1 - turn;
    }

    // check for game mode
    await auto_move();
    // Stop game after someone wins
    var cls = String($("#status").attr("class"));
    // console.log(cls);
    if(cls.includes("angel") || cls.includes("demon")){
        return;
    }
    update_html(game_state);
    result_val = who_won(game_state);
    switch (result_val) {
        case PLAYER_1:
            $("#status").html("Won.");
            $("#status").addClass("angel");
            break;
        case PLAYER_0:
            $("#status").html("Won.");
            $("#status").addClass("demon");
            break;
        case EMPTY:
            $("#status").html("Ongoing...");
            break;
        case -2:
            $("#status").html("Draw");
            break;
        default:
            $("#status").html("");
            break;
    }
    
    
}

$(document).ready(function () {
    LoadModel();
    $('.cell').on('click', function (e) {update(this);}
        );
    $('#NewGame').on('click',reset_game);
    $('#NewGame0').on('click',reset_game_0);
    $('#NewGame1').on('click',reset_game_1);
});