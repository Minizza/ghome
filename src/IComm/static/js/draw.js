(function($){

    $svg = $("#plan");

    drawCircle(50,50);

    $svg
        .on("mousedown", mousedown)
        .on("contextmenu", function(event) {     // Prevent context menu on right click
            event.preventDefault();
        });

    var $line;
    var $circle1;
    var $circle2;

    // Javascript function to get the context of SVG
    function SVG(tag) {
       return document.createElementNS('http://www.w3.org/2000/svg', tag);
    }

    function mousedown(event) {
        var mouse = getMousePos($(this), event);

        // Fire only on left click event
        if(event.which == 1) {

            $line = drawLine(mouse.x, mouse.y, mouse.x, mouse.y);

            $circle1 = drawCircle(mouse.x, mouse.y);
            $circle2 = drawCircle(mouse.x, mouse.y);

            $svg.on("mousemove", mousemove);
        }
        
    }

    function mousemove(event) {
        var mouse = getMousePos($(this), event);

        $line
            .attr("x2", mouse.x)
            .attr("y2", mouse.y);

        $circle2
            .attr("cx", mouse.x)
            .attr("cy", mouse.y)
            .attr("r", 5);
    }

    function mouseup(event) {
        var mouse = getMousePos($(this), event);

        $circle2
            .attr("cx", mouse.x)
            .attr("cy", mouse.y)
            .attr("r", 5);

        $svg.off("mousemove");
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
                .appendTo($svg)
                .on("mouseover", function() {
                    $(this).attr("r", 10)
                })
                .on("mouseout", function() {
                    $(this).attr("r", 5)
                });

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

    $export_button = $('#export');
    $export_button.click(function() {
        console.log($svg);
    });
    
})(jQuery);