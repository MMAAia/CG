void setup() {
  size(800, 800);
}

void draw() {
  background(0,0,0);
  pushMatrix();
  translate(width/2, height/2);
  rotate(frameCount / -85.0);
  float n = round(map(mouseY,0,width,100,400));
  star(0, 0, 30, n, 5); 
  fill(255,255,0);
  popMatrix();  
}
void star(float x, float y, float radius1, float radius2, int npoints) {
  float angle = TWO_PI / npoints;
  float halfAngle = angle/2.0;
  beginShape();
  for (float a = 0; a < TWO_PI; a += angle) {
    float sx = x + cos(a) * radius2;
    float sy = y + sin(a) * radius2;
    vertex(sx, sy);
    sx = x + cos(a+halfAngle) * radius1;
    sy = y + sin(a+halfAngle) * radius1;
    vertex(sx, sy);
  }
  endShape(CLOSE);
}
