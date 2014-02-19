
function GameMove() {
	// Sprite du personnage avec son image
	  var player = new jaws.Sprite({ image:"../static/medias/player.png" });
	  var playerSpeed = 4;

    // Initialisation de la position du personnage
	  this.setup = function()
	  {
	    player.x = (jaws.width / 2) - (player.width / 2); // Centré sur X
	    player.y = jaws.height - player.height - 10;       // En bas
	  }

    // Affichage
	this.draw = function()
	{
	    jaws.context.clearRect(0, 0, jaws.width, jaws.height);
	    ship.draw();
	}
}

jaws.onload = function() {
      jaws.assets.add("../static/medias/player.png")
      jaws.start(GameMove)
};