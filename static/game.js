$(document).ready(function(e){
  $('.game_slot').on('click', MakeGameMove);
});


function MakeGameMove() {
	var thisMove = $(this);
	var move = thisMove.attr('data-id');
	var moveUrl = '/move/' + move;
	var boardState = getBoardState();

  // If first move, show user's move before response is given
  var first = true;
  for (i=0; i<9; i++) {
    console.log(boardState)
    if (boardState[i] !== '') {
      first = false;
    }
  }
  if (first === true) {
    console.log('first one')
    thisMove.text('X');
  }

	var submitMove = $.post(moveUrl, boardState);
	submitMove.done(updateBoard);
}

function updateBoard(data) {
  boardData = data['board_state'];

  function updateValues(boardData, marker) {
    var slotSelector = '*[data-id="#"]';
    for (i=0; i<9; i++) {
      var thisSlotSelector = slotSelector.replace('#', i);
      var currentVal = $(thisSlotSelector).text();
      var newVal = boardData[i]['marker'];
      // If new value found, update board slot
      if (currentVal === '' & newVal === marker) {
        $(thisSlotSelector).text(newVal);
      }
    }
  }

  function highlightWinValues(boardData) {
    var slotSelector = '*[data-id="#"]';
    for (j=0; j<9; j++) {
      var thisSlotSelector = slotSelector.replace('#', j);
      // If board slots are winning, highlight them
      if (boardData[j]['winning']) {
        $(thisSlotSelector).addClass('winning');
      }
    }
  }

  // Make user's move
  updateValues(boardData, 'X');
  
  // Check for tie
  if (data['tie'] === 'True') {
    setTimeout(function() {
      $('.game_slot').addClass('tie');
      $('.results').removeClass('hide');
    }, 500);
  } else {
    // Delay computer move by 2 seconds
    setTimeout(function() {
      updateValues(boardData, 'O');
    }, 1000);
  }

  if (data['winner'] === 'X' | data['winner'] === 'O') {
    setTimeout(function() {
      highlightWinValues(boardData);
      $('.results').removeClass('hide');
    }, 2000);
  }
}

function getBoardState() {
	var boardState = {};
	$('.game_slot').each(function() {
		boardState[$(this).attr('data-id')] = $(this).text();
	});
	return boardState;
}

