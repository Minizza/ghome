$(function() {

    $svg = $(".plan");

    $svg
        .on("mousedown", mousedown)
        .on("contextmenu", function(event) {     // Prevent context menu on right click
            event.preventDefault();
        });

    var ctrlPressed = false;
    var shiftPressed = false;
    var started = false;
    var mouse = null;
    var $currentLine = null;

    // Get key events
    $(window).keydown(function(event) {
        // On Ctrl press
        if(event.which == 17) {
            ctrlPressed = true;
        }
        // On shift press
        if(event.which == 16) {
            shiftPressed = true;
        }
    }).keyup(function(event) {
        // On Ctrl release
        if(event.which == 17) {
            ctrlPressed = false;

            // Stop drawing if drawing started
            if(started) {
                started = false;
                $currentLine = null;
            }
        }
        // On shift release
        if(event.which == 16) {
            shiftPressed = false;
        }
    });

    // Javascript function to get the context of SVG
    function SVG(tag) {
       return document.createElementNS('http://www.w3.org/2000/svg', tag);
    }

    function mousedown(event) {
        var currentMouse = getMousePos($(this), event);

        // Fire only on left click event
        if(event.which == 1) {

            drawCircle(currentMouse.x, currentMouse.y);         

            if(started) {
                if(ctrlPressed) {
                    $currentLine = drawLine(currentMouse.x, currentMouse.y, currentMouse.x, currentMouse.y);
                } else {
                    started = false;
                    $svg.off("mousemove");
                }
            } else {
                started = true;
                $currentLine = drawLine(currentMouse.x, currentMouse.y, currentMouse.x, currentMouse.y);
                $svg.on("mousemove", mousemove);
            }

            mouse = currentMouse;
        
        }
        
    }

    function mousemove(event) {
        var currentMouse = getMousePos($(this), event);
        $currentLine
            .attr("x2", currentMouse.x)
            .attr("y2", currentMouse.y);
    }

    function getMousePos(dom, event) {
        return {
            'x': event.pageX - dom.offset().left,
            'y': event.pageY - dom.offset().top
        };
    }

    function drawCircle(x, y) {
        var $circle =
            $(SVG('circle'))
                .attr('cx', x)
                .attr('cy', y)
                .attr('r', 5)
                .attr('fill', '#14029D')
                .attr('stroke', 'black')
                .attr('stroke-width', 5)
                .appendTo($svg);

        return $circle;
    }

    function drawLine(x1, y1, x2, y2) {
        var $line =
            $(SVG('line'))
                .attr('x1', x1)
                .attr('y1', y1)
                .attr('x2', x2)
                .attr('y2', y2)
                .attr('stroke', 'black')
                .attr('stroke-width', 5)
                .appendTo($svg);

        return $line;
    }

    function clearCanvas() {
        $svg.empty();
    }

    // Export Button
    $export_button = $('#export');
    $export_button.click(function() {
        var html = $('<svg>').append($svg.clone()).html();
        $.post( "/draw", { svg: html }, function(data) {
            clearCanvas();
            setNotification("Succès export","Le plan a été exporté.", "success");
        });
    });

    // Clear Button
    $clear_button = $('#clear');
    $clear_button.click(function() {
        clearCanvas();
        started = false;
    });

});