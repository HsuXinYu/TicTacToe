var game_state = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]];
var turn = 1;
function who_won(game_state) {
    if (game_state[0][0] != -1) {
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
    if (game_state[1][0] != -1) {
        if (game_state[1][0] == game_state[1][1] && game_state[1][0] == game_state[1][2]) {
            return game_state[1][0];
        }
    }
    if (game_state[0][1] != -1) {
        if (game_state[0][1] == game_state[1][1] && game_state[0][1] == game_state[2][1]) {
            return game_state[0][1];
        }
    }
    if (game_state[0][2] != -1) {
        if (game_state[0][2] == game_state[1][1] && game_state[0][2] == game_state[2][0]) {
            return game_state[0][2];
        }
    }
    if (game_state[2][2] != -1) {
        if (game_state[2][2] == game_state[2][1] && game_state[2][2] == game_state[2][0]) {
            return game_state[2][2];
        }
        if (game_state[2][2] == game_state[1][2] && game_state[2][2] == game_state[0][2]) {
            return game_state[2][2];
        }
    }
    const isFinished = (val) => val != -1;
    if (game_state.every(function (arr) {
        return arr.every(function (val) { return val != -1; })
    })) {
        return -2;
    }
    else {
        return -1;
    }
}
function update_html(game_state) {
    var row_id = 0;
    var col_id = 0;
    for (row_id = 0; row_id < 3; row_id++) {
        for (col_id = 0; col_id < 3; col_id++) {
            var div_id = "#cell_" + row_id.toString() + "_" + col_id.toString();
            console.log(div_id + "" + game_state[row_id][col_id].toString());
            switch (game_state[row_id][col_id]) {
                case 1:
                    $(div_id).addClass("angel");
                    // $(div_id).css("background-color","yellow");
                    break;
                case 0:
                    $(div_id).addClass("demon");
                    // $(div_id).css("background-color","blue");
                    break;
                default:
                    $(div_id).css("background-color", "gray");
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
    game_state = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]];
    update_html(game_state);
}


$(document).ready(function () {
    $('.cell').on('click', function (e) {
        console.log(this.id[5]);
        var row_id = parseInt(this.id[5]);
        var col_id = parseInt(this.id[7]);
        if (game_state[row_id][col_id] == -1) {
            game_state[row_id][col_id] = turn;
            turn = 1 - turn;
        }
        update_html(game_state);
        result_val = who_won(game_state);
        switch (result_val) {
            case 1:
                $("#status").html("Player 1 Won.");
                // $("#status").css("background-color","yellow");
                $("#status").addClass("angel");
                break;
            case 0:
                $("#status").html("Player 0 Won.");
                // $("#status").css("background-color","blue");
                $("#status").addClass("demon");
                break;
            case -1:
                $("#status").html("Ongoing...");
                $("#status").css("background-color", "white");
                break;
            case -2:
                $("#status").html("Draw");
                $("#status").css("background-color", "red");
                break;
            default:
                $("#status").html("");
                $("#status").css("background-color", "white");
                break;
        }
    });
    $('#NewGame').on('click',reset_game);
});