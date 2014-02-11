var capteurs = new Array ();
var actionneurs = new Array ();
var allies = new Array ();
var enemies = new Array ();
var player

function GameState ()
{
            

    this.setup = function() { 

        var x;
        var y; 
        for (var i=0; i<2; i++) {
            x = Math.floor((Math.random()*(610-35))+35);
            y = Math.floor((Math.random()*(545-40))+40);
            capteurs[i] = new jaws.Sprite({image:"../static/medias/capteur.png"});
            capteurs[i].x = x;
            capteurs[i].y = y;
        }

        for (var i=0 ; i < 5 ; i++) {
            allies[i] = new jaws.Sprite({image:"../static/medias/allies.png"});
            x = Math.floor((Math.random()*(610-35))+35);
            y = Math.floor((Math.random()*(545-40))+40);
            allies[i].x = x;
            allies[i].y = y;
            enemies[i] = new jaws.Sprite({image:"../static/medias/enemies.png"});
            x = Math.floor((Math.random()*(610-35))+35);
            y = Math.floor((Math.random()*(545-40))+40);
            enemies[i].x = x;
            enemies[i].y = y;
        }
		
		player = new jaws.Sprite({ image:"../static/medias/player.png" });
	    var playerSpeed = 4;
		player.x = 300;
	    player.y = 250;       // En bas
                    
    }   
	
    this.update = function() { 
                    
		for ( var i=0 ; i < allies.length ; i++) {
            allies[i].x += Math.floor((Math.random()*3)-1);
            allies[i].y += Math.floor((Math.random()*3)-1);
            enemies[i].x += Math.floor((Math.random()*3)-1);
            enemies[i].y += Math.floor((Math.random()*3)-1);
        }
    }
            
	this.draw = function() { 
        jaws.context.clearRect(0, 0, jaws.width, jaws.height);
                    
		for (var i=0 ; i < capteurs.length ; i++) {
            capteurs[i].draw();
        }
                    
		for (var i=0 ; i < allies.length ; i++) {
            allies[i].draw();
            enemies[i].draw();
        }
		
		player.draw();
    }
}
     
window.onload = function() {
    jaws.assets.add("../static/medias/capteur.png");
    jaws.assets.add("../static/medias/allies.png");
    jaws.assets.add("../static/medias/enemies.png");
	
    jaws.start(GameState);
};
