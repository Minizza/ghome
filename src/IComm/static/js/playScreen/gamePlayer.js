$(function() {

function GamePlayer() {

	//Creation of player
	this.setup = function()
	  {
	    player = new jaws.Sprite({ image:"../static/medias/player.png" });
	    var playerSpeed = 4;
		
		//Player up in the middle
		player.x = 300;
	    player.y = 40;
		
		function SendCoordinates() {
			$.post( "testplayer/location", { abscissa: player.x, ordinate: player.y }, function( data ) {
				setTimeout(SendCoordinates, 2000);
			});
		}
		
		SendCoordinates();
	  }

	this.update = function() { 

		//Moves if button pressed
		if (jaws.pressed("left")) {
	      player.x -= 3;
	    }
	    if (jaws.pressed("right")) {
	      player.x += 3;
	    }
		if (jaws.pressed("up")) {
	      player.y -= 3;
	    }
	    if (jaws.pressed("down")) {
	      player.y += 3;
	    }
		
		//Player can't leave square
		if (player.x < 35)
	    {
			player.x = 35;
	    }
		if (player.x > 610)
	    {
			player.x = 610;

	    }
		if (player.y < 40)
	    {
			player.y = 40;
	    }
		if (player.y > 545)
	    {
			player.y = 545;
	    }
		
	}
	
	//Draw !
	this.draw = function()
	  {
	    jaws.context.clearRect(0, 0, jaws.width, jaws.height);
	    player.draw();
	  }
	
}

//When the page is loaded : image and function loaded too
jaws.onload = function() {
      jaws.assets.add("../static/medias/player.png");
      jaws.start(GamePlayer);
	  
};
});