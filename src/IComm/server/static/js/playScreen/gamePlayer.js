$(function() {

var bddCapteurs = new Array ();
var bddActionneurs = new Array ();
var bddAllies = new Array ();
var bddEnemies = new Array ();
var capteurs = new Array ();
var actionneurs = new Array ();
var allies = new Array ();
var enemies = new Array ();
var bddPlayer;
var player;
var map;

//basic function needed 


function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}



function initData (callback)
{
    $.ajax({    
                dataType: 'json',
                url:'/play', 
                type:'POST', 
                async :'false',
                success : function (data) {
                    data = JSON.parse(data);
                    for (var i=0; i<data.length; i++)
                    {
                        console.log(data[i].type);
                        var aDevice = new Object ();
                        aDevice.ident = data[i].ident;
                        aDevice.state = data[i].state;
                        aDevice.coordX = parseInt(data[i].coordX);
                        aDevice.coordY = parseInt(data[i].coordY);
                        if (data[i].type == "Actuator")
                        {
                            bddActionneurs.push(aDevice);
                        }
                        else if (data[i].type == "Temperature")
                        {
                            bddCapteurs.push(aDevice);    
                        }
                        else if (data[i].type == "Switch")
                        {
                            aDevice.detect = 0;
                            bddCapteurs.push(aDevice);
                        }
                        else if (data[i].type == "Position")
                        {

                            if (parseInt(data[i].state) == 1)
                            {
                                bddAllies.push(aDevice);
                            }
                            else if (parseInt(data[i].state) == 2)
                            {
                                bddEnemies.push(aDevice);
                            }

                        }
                        
                    }

                        callback ();    
                    
                }
            });
    
}


function updateData ()
{
    $.ajax({    
                dataType: 'json',
                url:'/play', 
                type:'POST', 
                async :'false',
                success : function (data) {
                    data = JSON.parse(data);
                    for (var i=0; i<data.length; i++)
                    {
                        if (data[i].type == "Position")
                        {

                            if (parseInt(data[i].state) == 1)
                            {
                                for (var j=0; j<bddAllies.length; j++)
                                {
                                    if (data[i].ident == bddAllies[j].ident)
                                    {
                                        bddAllies[j].coordX = data[i].coordX;
                                        bddAllies[j].coordY = data[i].coordY;
                                        allies[j].x = data[i].coordX;
                                        allies[j].y = data[i].coordY;
                                    }
                                }
                            }
                            else if (parseInt(data[i].state) == 2)
                            {
                                for (var j=0; j<bddEnemies.length; j++)
                                {
                                    if (data[i].ident == bddEnemies[j].ident)
                                    {
                                        bddEnemies[j].coordX = data[i].coordX;
                                        bddEnemies[j].coordY = data[i].coordY;
                                        enemies[j].x = data[i].coordX;
                                        enemies[j].y = data[i].coordY;
                                    }
                                }
                            }

                        }
                        else if ((data[i].type == "Switch")||(data[i].type == "Temperature"))
                        {
                            for (var j=0; j<bddCapteurs.length; j++)
                                {
                                    if (data[i].ident == bddCapteurs[j].ident)
                                    {
                                        bddCapteurs[j].state = data[i].state;
                                    }
                                }
                        }
                    }  
                    
                }
            });
    
}


//Fonctions de traitement des events
function canvasClicked ()
{
    for (var i=0; i<bddActionneurs.length; i++)
    {
        if (actionneurs[i].rect().collidePoint(jaws.mouse_x,jaws.mouse_y))
        {
            console.log("Hahaha, bien ouej !");
        }
    }
}


function GamePlayer ()
{
        
    var Eoo = 0;      

    this.setup = function() { 
        var x;
        var y; 
        

        for (var i=0; i<bddCapteurs.length; i++) {
            x = Math.floor((Math.random()*(610-35))+35);
            y = Math.floor((Math.random()*(545-40))+40);
            capteurs[i] = new jaws.Sprite({image:"static/medias/capteur.png"});
            capteurs[i].x = bddCapteurs[i].coordX;
            capteurs[i].y = bddCapteurs[i].coordY;
        }

        for (var i=0 ; i < bddActionneurs.length ; i++) {
            actionneurs[i] = new jaws.Sprite({image:"static/medias/actionneur.png"});
            actionneurs[i].x = bddActionneurs[i].coordX;
            actionneurs[i].y = bddActionneurs[i].coordY;
        }

        for (var i=0 ; i < bddAllies.length ; i++) {
            allies[i] = new jaws.Sprite({image:"static/medias/allies.png"});
            allies[i].x = bddAllies[i].coordX;
            allies[i].y = bddAllies[i].coordY;
            enemies[i] = new jaws.Sprite({image:"static/medias/enemies.png"});
            enemies[i].x = bddEnemies[i].coordX;
            enemies[i].y = bddEnemies[i].coordY;
        }
		

        updateData();
		
		player = new jaws.Sprite({ image:"static/medias/player.png" });

		player.x = allies[0].x;
	    player.y = allies[0].y;
		
        function SendCoordinates() {
        $.post( "play/location", { ident : bddAllies[0].ident, abscissa: player.x, ordinate: player.y }, function( data ) {
                setTimeout(SendCoordinates, 200);
            });
        }  

		SendCoordinates();
		
		/*map = new jaws.Sprite({ image:"../static/medias/plan.svg" });
		map.x = 35;
		map.y = 40;*/
                    
    }   
	

    
    this.update = function() { 
        
        if (Eoo===10)
        {
            Eoo =0;
        }
        else
        {
            Eoo+=1;
        }

        for (var i=0; i<bddCapteurs.length; i++)
        {
            if ((bddCapteurs[i].state == "open")||(bddCapteurs[i].detect>0))
            {
                bddCapteurs[i].detect+=1;
                switch(bddCapteurs[i].detect)
                {
                    case 15 : 
                        capteurs[i].setImage("static/medias/capteurS1.png");
                        break;
                    case 30 : 
                        capteurs[i].setImage("static/medias/capteurS2.png");
                        break;
                    case 45 : 
                        capteurs[i].setImage("static/medias/capteurS3.png");
                        break;
                    case 60 : 
                        capteurs[i].setImage("static/medias/capteur.png");
                        bddCapteurs[i].detect=0;
                        break;
                }
            }
        }
		
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
		
		for (var i=0 ; i < capteurs.length ; i++) {
			jaws.collide(player, capteurs[i], function() { 
				$.post( "play/captor", { captor : bddCapteurs[i].ident }, function( data ) {});
			});
        }

        
        
    }
            
	this.draw = function() { 
        jaws.context.clearRect(0, 0, jaws.width, jaws.height);
                    
		for (var i=0 ; i < capteurs.length ; i++) {
            capteurs[i].draw();
        }
                   
        for (var i=0 ; i < actionneurs.length ; i++) {
            actionneurs[i].draw();
        } 
		for (var i=1 ; i < allies.length ; i++) {
            allies[i].draw();
            enemies[i].draw();
        }
		enemies[0].draw();
		
		player.draw();
		
		//map.draw();
    }
}
     
window.onload = function() {
    jaws.assets.add("static/medias/capteur.png");
    jaws.assets.add("static/medias/capteurS1.png");
    jaws.assets.add("static/medias/capteurS2.png");
    jaws.assets.add("static/medias/capteurS3.png");
    jaws.assets.add("static/medias/actionneur.png");
    jaws.assets.add("static/medias/allies.png");
    jaws.assets.add("static/medias/enemies.png");
	jaws.assets.add("static/medias/player.png");
	
	//jaws.assets.add("../static/medias/map.svg");
    initData(jaws.start(GamePlayer));
};

});