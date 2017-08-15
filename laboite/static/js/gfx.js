function printText(x, y, text, color, bg) {
    for(var i = 0; i < text.length; i++) {
        drawChar(x + i*5, y, text[i], color, bg);
    }
}

function reset(){
    for(var i=0; i< matrixWidth*matrixHeight; i++){
        $(".led ul li").eq(i).css("background","#444");
    }
}

function draw(x0, y0, bitmap, width, height, color, bg) {
    for(var y = 0; y <= bitmap.length/height+1; y++) {
        for(var x = 0; x <= width-1; x++) {
            if(bitmap[x+y*width]==1)
                drawPixel(x+x0, y+y0, color);
            else
                drawPixel(x+x0, y+y0, bg);
        }
    }
}

function drawChar(x0, y0, character, color, bg){
    bitmap = font[character.charCodeAt()-32];
    draw(x0, y0, bitmap, 5, 7, color, bg);
}

function fillRect(x0, y0,  width,  height, color) {
    for (var y = y0; y < y0+height; y++) {
        drawFastHLine(x0, y, width, color);
    }
}

function drawRect(x0, y0,  width,  height, color) {
    drawFastHLine(x0, y0, width, color);
    drawFastHLine(x0, y0+height-1, width, color);

    drawFastVLine(x0, y0, height, color);
    drawFastVLine(x0+width-1, y0, height, color);
}

function drawFastHLine(x0, y0, width, color) {
    for (var x = x0; x < x0+width; x++)
        drawPixel(x, y0, color);
}

function drawFastVLine(x0, y0, height, color) {
    for (var y = y0; y < y0+height; y++)
        drawPixel(x0, y, color);
}

function drawPixel(x, y, color) {
    if((x < 0) || (y < 0) || (x >= matrixWidth) || (y >= matrixHeight) || color == "#000") return;

    $(".led ul li").eq(x+matrixWidth*y).css("background",color);
}
