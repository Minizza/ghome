var bddCapteurs = new Array ();
var bddActionneurs = new Array ();
var bddAllies = new Array ();
var bddEnemies = new Array ();
var capteurs = new Array ();
var actionneurs = new Array ();
var allies = new Array ();
var enemies = new Array ();
var boutonActiver = new Object ();
var infosActuator = new Object ();
var infosParty = new Object ();
var pingSound;

infosParty.team = parseInt(myGame());

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
                url:'/game', 
                type:'POST', 
                async :'false',
                success : function (data) {
                    data = JSON.parse(data);
                    //Stockage des infos capteurs/joueurs
                    for (var i=1; i<data.length; i++)
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
                            if (infosParty.team == 0)
                            {
                                if (parseInt(data[i].state) == 1)
                                {
                                    bddAllies.push(aDevice);
                                }
                                else 
                                {
                                    bddEnemies.push(aDevice);
                                }
                            }
                            else
                            {
                                if (parseInt(data[i].state) == infosParty.team)
                                {
                                    bddAllies.push(aDevice);
                                }
                                else
                                {
                                    bddEnemies.push(aDevice);
                                }
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
                url:'/game', 
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


function actiActiv (theAct)
//Fonction d'envoi d'info lorsqu'un un actuator est activé
{
    $.ajax({    
                dataType: 'json',
                url:'/game/activated', 
                type:'POST', 
                async :'false',
                data : { ident : theAct.ident, anX : theAct.coordX, anY : theAct.coordY }
                });
}

//Fonctions de traitement des events
function canvasClicked ()
{
    if (typeof canvasClicked.selectedA == 'undefined') {canvasClicked.selectedA = -1}


    if ((boutonActiver.isActive==true)&&(boutonActiver.image.rect().collidePoint(jaws.mouse_x,jaws.mouse_y)))
    {
        actiActiv(bddActionneurs[canvasClicked.selectedA]);
        return;
    }
    if (canvasClicked.selectedA != -1)
    {
        actionneurs[canvasClicked.selectedA].setImage("../static/medias/actionneur.png");
        boutonActiver.isActive = false;
        boutonActiver.textId1.set({text : "", x : 690, y :120});
        boutonActiver.textState1.set({text : "", x : 690, y :170});
        boutonActiver.textCoord1.set({text : "", x : 690, y :220});
        canvasClicked.selectedA = -1;
    }
    for (var i=0; i<bddActionneurs.length; i++)
    {
        if (actionneurs[i].rect().collidePoint(jaws.mouse_x,jaws.mouse_y))
        {
            canvasClicked.selectedA = i;
            actionneurs[i].setImage("../static/medias/sel_actionneur.png");
            boutonActiver.isActive = true;
            boutonActiver.textId1.set({text : bddActionneurs[i].ident, x : 690, y :120});
            boutonActiver.textState1.set({text : bddActionneurs[i].state, x : 690, y :170});
            boutonActiver.textCoord1.set({text : bddActionneurs[i].coordX+","+bddActionneurs[i].coordY, x : 690, y :220});
            return;
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
        }
        for (var i=0; i < bddEnemies.length ; i++) {
            enemies[i] = new jaws.Sprite({image:"../static/medias/enemies.png"});
            enemies[i].x = bddEnemies[i].coordX;
            enemies[i].y = bddEnemies[i].coordY;
        }


        //Les infos concernant l'actuator selectionne

        //Le bouton d'activation d'actuator
        boutonActiver.image = 	new jaws.Sprite({image:"../static/medias/butActiver.png"});
        boutonActiver.image.moveTo(683,480);
        boutonActiver.textId = new jaws.Text({text : "Id :", x : 680, y : 100});
        boutonActiver.textState = new jaws.Text({text : "State :", x : 680, y : 150});
        boutonActiver.textCoord = new jaws.Text({text : "Coord :", x : 680, y : 200});
        boutonActiver.textId1 = new jaws.Text({text : "", x : 690, y : 120});
        boutonActiver.textState1 = new jaws.Text({text : "", x : 690, y : 170});
        boutonActiver.textCoord1 = new jaws.Text({text : "", x : 690, y : 220});
        boutonActiver.isActive  = false;	

        //Le son de ping
        pingSound = new Audio("../static/medias/ping.wav");

        updateData();
    }   
	

    
    this.update = function() { 
            
        if (Eoo===15)
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
            if (bddCapteurs[i].ident == "0001B592")
            {
                console.log(bddCapteurs[i].state);
            }
            if ((bddCapteurs[i].state == "open")||(bddCapteurs[i].detect>0))
            {

                bddCapteurs[i].detect+=1;
                switch(bddCapteurs[i].detect)
                {
                    case 15 :
                        //pingSound.play();
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

        boutonActiver.textId.draw();
        boutonActiver.textState.draw();
        boutonActiver.textCoord.draw();
        boutonActiver.textId1.draw();
        boutonActiver.textState1.draw();
        boutonActiver.textCoord1.draw();
                    
		for (var i=0 ; i < capteurs.length ; i++) {
            capteurs[i].draw();
        }
                   
        for (var i=0 ; i < actionneurs.length ; i++) {
            actionneurs[i].draw();
        } 
		for (var i=0 ; i < allies.length ; i++) {
            allies[i].draw();
        }
        if (infosParty.team==0)
        {
            for (var i=0 ; i < enemies.length ; i++) {
                enemies[i].draw();
            }
        }

        if (boutonActiver.isActive)
        {
            boutonActiver.image.draw();
            
        }
    }
}
     
window.onload = function() {
    jaws.assets.add("../static/medias/capteur.png");
    jaws.assets.add("../static/medias/capteurS1.png");
    jaws.assets.add("../static/medias/capteurS2.png");
    jaws.assets.add("../static/medias/capteurS3.png");
    jaws.assets.add("../static/medias/actionneur.png");
    jaws.assets.add("../static/medias/sel_actionneur.png");
    jaws.assets.add("../static/medias/allies.png");
    jaws.assets.add("../static/medias/enemies.png");
    jaws.assets.add("../static/medias/butActiver.png");
    initData(jaws.start(GameStart));
};
