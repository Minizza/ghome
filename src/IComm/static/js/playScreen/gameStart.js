var capteurs = new Array ();
var actionneurs = new Array ();
var allies = new Array ();
var enemies = new Array ();
var player

function updateData ()
{
    $.ajax({    
                dataType: "json",
                url:"/launchGame", 
                type:"POST", 
                mimeType : "application/json",
                success : function (data) {}
            });
}



function GameState ()
{
            

    this.setup = function() { 

        var x;
        var y; 

        updateData();

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
		player.x = 300;
	    player.y = 250;
                    
    }   
	
    this.update = function() { 
                    
		for ( var i=0 ; i < allies.length ; i++) {
            allies[i].x += Math.floor((Math.random()*3)-1);
            allies[i].y += Math.floor((Math.random()*3)-1);
            enemies[i].x += Math.floor((Math.random()*3)-1);
            enemies[i].y += Math.floor((Math.random()*3)-1);
        }
		
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
