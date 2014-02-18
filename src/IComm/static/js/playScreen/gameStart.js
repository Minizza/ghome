var bddCapteurs = new Array ();
var bddActionneurs = new Array ();
var bddAllies = new Array ();
var bddEnemies = new Array ();
var capteurs = new Array ();
var actionneurs = new Array ();
var allies = new Array ();
var enemies = new Array ();
var player;

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
                url:'/launchGame', 
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
                url:'/launchGame', 
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
                                for (var j=0; i<bddAllies.length; j++)
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
                                for (var j=0; i<bddEnemies.length; j++)
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
                            for (var j=0; i<bddCapteurs.length; j++)
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


function GameStart ()
{
        
    var Eoo = 0;        

    this.setup = function() { 
        var x;
        var y; 
        

        for (var i=0; i<bddCapteurs.length; i++) {
            x = Math.floor((Math.random()*(610-35))+35);
            y = Math.floor((Math.random()*(545-40))+40);
            capteurs[i] = new jaws.Sprite({image:"../static/medias/capteur.png"});
            capteurs[i].x = bddCapteurs[i].coordX;
            capteurs[i].y = bddCapteurs[i].coordY;
        }

        for (var i=0 ; i < bddActionneurs.length ; i++) {
            actionneurs[i] = new jaws.Sprite({image:"../static/medias/actionneur.png"});
            actionneurs[i].x = bddActionneurs[i].coordX;
            actionneurs[i].y = bddActionneurs[i].coordY;
        }

        for (var i=0 ; i < bddAllies.length ; i++) {
            allies[i] = new jaws.Sprite({image:"../static/medias/allies.png"});
            allies[i].x = bddAllies[i].coordX;
            allies[i].y = bddAllies[i].coordY;
            enemies[i] = new jaws.Sprite({image:"../static/medias/enemies.png"});
            enemies[i].x = bddEnemies[i].coordX;
            enemies[i].y = bddEnemies[i].coordY;
        }

		player = new jaws.Sprite({ image:"../static/medias/player.png" });
	    var playerSpeed = 4;
		player.x = 300;
	    player.y = 250;


        updateData();
                    
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

        
        if (Eoo===60)
        {
            Eoo =0;
            updateData();
        }
        else
        {
            Eoo+=1;
        }

        for (var i=0; i<bddCapteurs.length; i++)
        {
            if ((bddCapteurs[i].state == "True")||(bddCapteurs[i].detect>0))
            {
                bddCapteurs[i].detect+=1;
                switch(bddCapteurs[i].detect)
                {
                    case 15 : 
                        capteurs[i].setImage("../static/medias/capteurS1.png");
                        break;
                    case 30 : 
                        capteurs[i].setImage("../static/medias/capteurS2.png");
                        break;
                    case 45 : 
                        capteurs[i].setImage("../static/medias/capteurS3.png");
                        break;
                    case 60 : 
                        capteurs[i].setImage("../static/medias/capteur.png");
                        bddCapteurs[i].detect=0;
                        break;
                }
            }
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
		for (var i=0 ; i < allies.length ; i++) {
            allies[i].draw();
            enemies[i].draw();
        }
		
		player.draw();
    }
}
     
window.onload = function() {
    jaws.assets.add("../static/medias/capteur.png");
    jaws.assets.add("../static/medias/capteurS1.png");
    jaws.assets.add("../static/medias/capteurS2.png");
    jaws.assets.add("../static/medias/capteurS3.png");
    jaws.assets.add("../static/medias/actionneur.png");
    jaws.assets.add("../static/medias/allies.png");
    jaws.assets.add("../static/medias/enemies.png");
    jaws.assets.add("../static/medias/player.png");
    initData(jaws.start(GameStart));
};
