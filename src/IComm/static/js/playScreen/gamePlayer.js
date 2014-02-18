var player;

function GamePlayer() {

	this.setup = function()
	  {
	    player = new jaws.Sprite({ image:"../static/medias/player.png" });
	    var playerSpeed = 4;
		player.x = 300;
	    player.y = 40;
	  }

	this.update = function() { 

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
	
	this.draw = function()
	  {
	    jaws.context.clearRect(0, 0, jaws.width, jaws.height);
	    player.draw();
	  }
	
}

jaws.onload = function() {
      jaws.assets.add("../static/medias/player.png")
      jaws.start(GamePlayer)
};