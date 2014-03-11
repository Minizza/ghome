var patternJerome = "jerome";
var nbLettresJerome = 0;

function lancerJerome() {
	alert("mettre ici la chanson");
}

function traitement(touche) {
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