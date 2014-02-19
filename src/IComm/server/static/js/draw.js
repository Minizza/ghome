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
    var lastPoint = null;
    var $currentLine = null;
    var nbLines = 0;

    // Get key events
    $(window).keydown(function(event) {
        // On Ctrl press
        if(event.which == 17) {
            ctrlPressed = true;

            if(lastPoint != null && !started) {
                started = true;
                $currentLine = drawLine(lastPoint.x, lastPoint.y, lastPoint.x, lastPoint.y);
                $svg.on("mousemove", mousemove);
            }
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
            if(started && nbLines > 1) {
                started = false;
                $currentLine.remove();
                $currentLine = null;
                $svg.off("mousemove");
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
        var mouse = getMousePos($(this), event);

        // Fire only on left click event
        if(event.which == 1) {

            // Path already started
            if(started) {
                // Continue path
                if(ctrlPressed) {
                    
                    if(shiftPressed) {
                        closestPoint = getClosestPoint(mouse, lastPoint);
                        drawCircle(closestPoint.x, closestPoint.y);
                        $currentLine = drawLine(closestPoint.x, closestPoint.y, closestPoint.x, closestPoint.y);
                        lastPoint = closestPoint;
                    } else {
                        drawCircle(mouse.x, mouse.y);
                        $currentLine = drawLine(mouse.x, mouse.y, mouse.x, mouse.y);
                        lastPoint = mouse;
                    }
                    
                } 
                // Stop path
                else {
                    started = false;

                    if(shiftPressed) {
                        closestPoint = getClosestPoint(mouse, lastPoint);
                        drawCircle(closestPoint.x, closestPoint.y);
                        lastPoint = closestPoint;
                    } else {
                        drawCircle(mouse.x, mouse.y);
                        lastPoint = mouse;
                    }

                    $svg.off("mousemove");
                }
            } 
            // Start path
            else {
                started = true;
                drawCircle(mouse.x, mouse.y);
                $currentLine = drawLine(mouse.x, mouse.y, mouse.x, mouse.y);
                $svg.on("mousemove", mousemove);
                lastPoint = mouse;
                nbLines = 0;
            }

            nbLines++;
        
        }
        
    }

    function mousemove(event) {
        var mouse = getMousePos($(this), event);

        if(shiftPressed) {
            closestPoint = getClosestPoint(mouse, lastPoint);

            $currentLine
                .attr("x2", closestPoint.x)
                .attr("y2", closestPoint.y);

        } else {
            $currentLine
                .attr("x2", mouse.x)
                .attr("y2", mouse.y);
        }
        
    }

    // Get the mouse position being careful of offset
    function getMousePos(dom, event) {
        return {
            'x': event.pageX - dom.offset().left,
            'y': event.pageY - dom.offset().top
        };
    }

    // Get the point to closest straight line
    function getClosestPoint(point2, point1) {
        if(point1 == null) {

            x = point2.x;
            y = point2.y;

        } else {

            diff_x = Math.abs(point2.x - point1.x);
            diff_y = Math.abs(point2.y - point1.y);

            var x, y;

            if(diff_x >= diff_y) {
                x = point2.x;
                y = point1.y;
            } else {
                x = point1.x;
                y = point2.y;
            }
        }

        return {
            'x': x,
            'y': y
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