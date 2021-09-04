let start = 'bbbbxxxxxxxxwwwwbbbbxxxxxxxxwwwwbbbbxxxxxxxxwwwwbbbbxxxxxxxxwwww'
const board = start.split("")
class Rules {
    constructor(board) {
        this.board = board;
        this.two_space_moves=[10,-10,8,-8,6,-6,4,-4];
        this.one_space_moves=[5,-5,4,-4,3,-3,2,-2];
    }
    initialize_homeboard(color){
    if (color == "b"){
        var homeboard = [0, 1];
        }
    if (color == "w"){
        var homeboard = [2, 3];
        }
    return homeboard;
    }
    check_if_valid(input1, input2, color){
        var invertboard = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15];
        var invertmoves = {'1': 4, '-1': -4, '5': 5, '-5': -5, '4': 1, '-4': -1, '-3': 3, '3': -3, '2': 8, '-2': -8, '10': 10, '-10': -10, '8': 2, '8': -2, '-6': 6, '6': -6};            
        //# dictionary mapping coordinates to an inverted matrix to detect move legality
        var valid_moves = [1, -1, 5, -5, 4, -4, 3, -3, 2, -2, 10, -10, 8, -8, 6, -6, 4, -4];     //#all valid movement vectors

        if (this.board[input1] != color){      //#must select your own color stone
            return false;
        }
        if (~~(input1/16) != ~~(input2/16)){        //# division to see if both inputs are in 4x4 grids
            console.log('input1 and input2 not on same subboard');
            return false;
        }

        var input1 = input1 % 16;
        var input2 = input2 % 16;
        var move = input2 % 16 - input1 % 16;
        if (!(valid_moves.includes(move))){     //#detects if illegal move like a knights move, or something
            console.log('just illegal')
            return false;
        }
        if ((move > 0) && ((input1 + move) % 16 < input1)){  //#if in valid moves, checks if goes off the board for top and bottom edges
            console.log('top')
            return false;
        }
        if (((invertboard[input1 % 16] + invertmoves[move]) % 16) < invertboard[input2 % 16]){   //#checks if goes off the board for left and right edges
            console.log('left')
            return false;
        }
        if ((move < 0) && (input1 + move) % 16 > input1){
            console.log('bottom')
            return false;
        }
        if (((invertboard[input1 % 16]+ invertmoves[move]) % 16) > invertboard[input2 % 16]){
            console.log('check 5')
            return false;
        }
        else{
            return true;
        }
     }
    check_if_pushes(input1,input2,color){          //#checks if a stone is being pushed, returns the location of the stone being pushed
        var move = input2 - input1
        if (this.two_space_moves.includes(move)){
            if ((this.board[parseInt(input1+move/2)] != 'x') && (this.board[input2]=='x')){
                return input1+move/2;    //#if stone moves past another stone, returns location of the stone being jumped over
            }
        
            if ((this.board[parseInt(input1 + move / 2)] == 'x') && (this.board[input2] != 'x')){
                return input2;           //# if stone moves onto other stone, returns location of stone being moved onto
            }
            if ((this.board[parseInt(input1+move/2)] != 'x') && (this.board[input2]!='x')){
                return false;          //# if move both jumps over a stone and lands on a stone, returns false
            }
        }
        if (this.one_space_moves.includes(move)){
            if ((this.board[input2] !='x') && (this.board[input2 + move] == 'x')){ //#checks if one space move lands on enemy stone
                return input2;
            }
        }
        return 'x'      //#shows nothing has been pushed
    }
    passive_move(input1,input2,color){
        var subboard=this.initialize_homeboard(color);
        if ((board[input1] != color) || (board[input2] != 'x')){  //#checks if you select your own color or if you push another stone
            return false;
        }
        if (!(subboard.includes(~~(input1/16)))){                    //#checks if passive move not on passive board
            console.log('move not on ' + color + ' homeboard');
            return false;
        }
        if (!(this.check_if_valid(input1,input2,color))){    //#checks if movement is valid
            console.log('Error: Movement not orthogonally or diagonally adjacent with a scale up to two.');
            return false;
        }
        if (this.check_if_pushes(input1,input2,color)!='x'){  //#checks if a stone is being pushed
            console.log('cannot push a stone on your passive move');
            return false;
        }
        return true;
    }
    aggressive_move(input3,move,color,passive_board){
        var pushed_stone = this.check_if_pushes(input3, input3 + move, color);   //#returns the coordinate of the pushed stone, or 'x' if nothing pushed
        if (this.board[input3] != color){
            console.log('must select your own stone');
            return false;
        }
        if ((passive_board % 2) == ((~~(input3/16)) % 2)){     //#checks if aggressive move on same parity board of passive move
            console.log('move not on opposite colored board');
            return false;
        }
        if (!(this.check_if_valid((input3) % 16, (input3 + move) % 16, color))){ //#checks if aggressive move pushes off board
            console.log('Error: aggressive move out of bounds');
            return false;
        }
        if (this.board[input3+move] == color){
            console.log('you cannot push your own stone');
            return false;
        }
        if (pushed_stone == false){       //#check_if_pushes returns false if two stones are pushed
            console.log('cant push 2 stones');
            return false;
        }
        if (pushed_stone != 'x'){         //#if a stone is being pushed, checks if the stone is your own color
            var pushed_stone = parseInt(pushed_stone);
            if (this.board[pushed_stone]==color){
                console.log('cant push your own stone');
                return false;
            }
        }
        return true;
    }
    passive_aggressive(input1, input2, input3, color){
        var move = input2 - input1;
        var passive_board = ~~(input1/16);
        if (!(this.passive_move(input1, input2, color))){
            console.log('passive move false');
            return false;
        }
        if (!(this.aggressive_move(input3,move,color,passive_board))){
            console.log('aggressive move false');
            return false;
        }
        return true;
    }
    update_board(input1,input2,input3,color,input_board){
        if (color == 'w'){
        var opponent = 'b';
         }
        else{
        var opponent = 'w';
        }
        var updated_board = input_board.slice(0);
        var move = (input2 % 16 - input1 % 16);
        var halfmove = move;
        
        if (!(this.passive_aggressive(input1,input2,input3,color))){     //#verifies the move is legal
            return false;
        }

        updated_board[input1] = 'x';
        updated_board[input2] = color;
        updated_board[input3] = 'x';
        updated_board[input3 + move] = color;
 
        var pushed_stone = this.check_if_pushes(input3, (input3 + move), color)
        if (pushed_stone != 'x'){
            var pushed_stone=parseInt(pushed_stone);
            var pushed_stone = parseInt(pushed_stone);
            if (this.two_space_moves.includes(move)){  //#if move is 2 spaces, creates a 1 space move of same vector
                move = parseInt((input1 + move / 2));
            }
            if (!(this.check_if_valid(pushed_stone, parseInt(input1 + move * 2), color))){ //#checks if stone was pushed off board
                console.log('opponent ' + opponent + ' stone pushed off board from position ' + pushed_stone.toString());
            }
            else{
                updated_board[input3 + move + halfmove] = opponent;
            }
        }
        return updated_board
    }

}
    function convert_to_string(board){ //#converts the board back from a list into a string for readability
        string = board[0];
        for (i=1; i<board.length; i++){
            if (i % 4 == 0){
                // console.log(i + "i value")
                // console.log(string.slice(i-4,i))
                string += "\n";
            }
            if (i % 16 == 0){
                string += "\n \n";
            }
            string += board[i].toString();
            
        }
        return string;
        }


//#testing
const game = new Rules(board);
var updated_board=game.update_board(45,39,28,'w',board);
try{
    console.log(convert_to_string(updated_board));
}
catch (err){
    console.log(err);
}

// test_string = "b"
// console.log(test_string)
// for (i=1; i<board.length; i++){
//     if (i%4 == 0){
//         test_string += "\n"
//     }
//     if (i % 16 == 0){
//         test_string += "\n \n";
//     }
//     test_string += board[i]
// }
// console.log(test_string)