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

var boolIsAllied = true;
var selectedPlayerId;
var selectedPlayerIndex;

// Variable for drawing map
var context;
var image;

//basic function needed 

function changePlayer() {
    selectedPlayerId = $("#playersList").val();
    var trouve = false;
    for(var i=0; i<bddAllies.length; i++) {
        if(bddAllies[i].ident == selectedPlayerId) {
            selectedPlayerIndex = i;
            boolIsAllied = true;
            if (player)
            {
                player.x = allies[i].x;
                player.y = allies[i].y;
            }
            return;
        }
    }

    for(var i=0; i<bddEnemies.length; i++) {
        if(bddEnemies[i].ident == selectedPlayerId) {
            selectedPlayerIndex = i;
            boolIsAllied = false;
            if (player)
            {
                player.x = enemies[i].x;
                player.y = enemies[i].y;
            }
            return;
        }
    }
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}


//Query : get all devices from BDD
function initData (callback)
{
    $.ajax({
                dataType: 'json',
                url:'/play', 
                type:'POST', 
                async :'false',
                success : function (data) {
                    console.log(data);
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

                            if (parseInt(data[i].team) == 1)
                            {
                                bddAllies.push(aDevice);
                            }
                            else if (parseInt(data[i].team) == 2)
                            {
                                bddEnemies.push(aDevice);
                            }

                        }
                        
                    }

                        callback ();    
                    
                }
            });
    
}

//Updating data from BDD
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

                            if (parseInt(data[i].team) == 1)
                            {
                                for (var j=0; j<bddAllies.length; j++)
                                {
                                    if (data[i].ident == bddAllies[j].ident)
                                    {
                                        bddAllies[j].coordX = data[i].state.coordX;
                                        bddAllies[j].coordY = data[i].state.coordY;
                                        allies[j].x = data[i].state.coordX;
                                        allies[j].y = data[i].state.coordY;
                                    }
                                }
                            }
                            else if (parseInt(data[i].team) == 2)
                            {
                                for (var j=0; j<bddEnemies.length; j++)
                                {
                                    if (data[i].ident == bddEnemies[j].ident)
                                    {
                                        bddEnemies[j].coordX = data[i].state.coordX;
                                        bddEnemies[j].coordY = data[i].state.coordY;
                                        enemies[j].x = data[i].state.coordX;
                                        enemies[j].y = data[i].state.coordY;
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

}


//Fonction d'envoi de l'information "capteur detecte"
function Detect ()
{

}

//Fonction d'envoi de l'information "capteur ne detecte plus"

function GamePlayer ()
{
        
    var Eoo = 0;      

    this.setup = function() { 
        var x;
        var y; 
        
		//Captors objects
        for (var i=0; i<bddCapteurs.length; i++) {
            x = Math.floor((Math.random()*(610-35))+35);
            y = Math.floor((Math.random()*(545-40))+40);
            capteurs[i] = new jaws.Sprite({image:"static/medias/capteur.png"});
            capteurs[i].x = bddCapteurs[i].coordX;
            capteurs[i].y = bddCapteurs[i].coordY;
        }

		//Actuators objects
        for (var i=0 ; i < bddActionneurs.length ; i++) {
            actionneurs[i] = new jaws.Sprite({image:"static/medias/actionneur.png"});
            actionneurs[i].x = bddActionneurs[i].coordX;
            actionneurs[i].y = bddActionneurs[i].coordY;
        }

		//Allies and enemies objects
        for (var i=0 ; i < bddAllies.length ; i++) {
            allies[i] = new jaws.Sprite({image:"static/medias/allies.png"});
            allies[i].x = bddAllies[i].coordX;
            allies[i].y = bddAllies[i].coordY;
            enemies[i] = new jaws.Sprite({image:"static/medias/enemies.png"});
            enemies[i].x = bddEnemies[i].coordX;
            enemies[i].y = bddEnemies[i].coordY;
        }
		
		//Current data
        updateData();
		
		//Player object
		player = new jaws.Sprite({ image:"static/medias/player.png" });
		
		//Chose player selected in the list
        changePlayer();

		//If current player is former player's allie
        if(boolIsAllied) {
			//Coordonates taken in the list of allies
            player.x = allies[selectedPlayerIndex].x;
            player.y = allies[selectedPlayerIndex].y;
        }
		//If current player is former player's enemie
        else {
			//Coordonates taken in the list of enemies
            player.x = enemies[selectedPlayerIndex].x;
            player.y = enemies[selectedPlayerIndex].y;
        }
		

        function SendCoordinates() {
        $.post( "play/location", { ident : selectedPlayerId, abscissa: player.x, ordinate: player.y }, function( data ) {
                setTimeout(SendCoordinates, 200);
            });
        }  

		SendCoordinates();
                    
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

		//Please comment this
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
		
        if (boolIsAllied)
        {
            allies[selectedPlayerIndex].x = player.x;
            allies[selectedPlayerIndex].y = player.y;
        }
        else 
        {
            enemies[selectedPlayerIndex].x = player.x;
            enemies[selectedPlayerIndex].y = player.y;
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
		
		//Manage if player crushes a captor (for all captors)
		for (var i=0 ; i < capteurs.length ; i++) {
			if (jaws.collide(player, capteurs[i]))
            {
                console.log('Gogogo !')
                $.post( "play/captor", { captor : bddCapteurs[i].ident }, function( data ) {});
                bddCapteurs[i].active = true;
            }
            else
            {
                console.log('pas glop !')
                if (bddCapteurs[i].active)
                {
                    $.post( "play/nocaptor", { captor : bddCapteurs[i].ident }, function( data ) {});
                    bddCapteurs[i].active = false;

                }
            }
        }

        
        
    }
            
	this.draw = function() { 
        jaws.context.clearRect(0, 0, jaws.width, jaws.height);

        // Draw map
        // context.drawImage(image, 30, 35);
                    
		//Draw all captors
		for (var i=0 ; i < capteurs.length ; i++) {
            capteurs[i].draw();
        }
         
		//Draw all actuators
        for (var i=0 ; i < actionneurs.length ; i++) {
            actionneurs[i].draw();
        } 
		
		//Draw all allies and enemies except player
		for (var i=0 ; i < allies.length ; i++) {
            if(i!=selectedPlayerIndex) {
                allies[i].draw();
                enemies[i].draw();
            } else {
                if(boolIsAllied) {
                    enemies[i].draw();
                } else {
                    allies[i].draw();
                }
            }
            
        }
		
		//Draw player
		player.draw();
    }
}
     
function loadPlay(mapPath) {
    jaws.assets.add("static/medias/capteur.png");
    jaws.assets.add("static/medias/capteurS1.png");
    jaws.assets.add("static/medias/capteurS2.png");
    jaws.assets.add("static/medias/capteurS3.png");
    jaws.assets.add("static/medias/actionneur.png");
    jaws.assets.add("static/medias/allies.png");
    jaws.assets.add("static/medias/enemies.png");
	jaws.assets.add("static/medias/player.png");

    // Obtenir les infos necessaire pour afficher le plan
    $(function() {
        var $canvas = $('#gameCanvas');
        context = $canvas.get(0).getContext('2d');
        image = new Image();

        // L'astuce ci dessous genere un timestamp pour l'ajouter 
        // au nom de l'image pour que le browser ne la mette pas en cache
        // C'est pourri mais ça MMMMAAAAARRRRCCHE !!!! Owi
        var timestamp = new Date().getTime();
        image.src = mapPath + '.svg?' + timestamp;
    });
	
    initData(jaws.start(GamePlayer));
};
