var patternJerome = "jerome";
var nbLettresJerome = 0;

function lancerJerome() {
	alert("mettre ici la chanson");
}

function traitement(touche) {
	console.log(touche.which);
	console.log(patternJerome.charCodeAt(nbLettresJerome));
		console.log(touche.which == patternJerome.charCodeAt(nbLettresJerome));
	if (touche.which != patternJerome.charCodeAt(nbLettresJerome++)) {
		nbLettresJerome = 0;
	}

	if(nbLettresJerome == patternJerome.length) {
		nbLettresJerome = 0;
		lancerJerome();
	}
}

$(function() {
	$(document).keypress(traitement);
});