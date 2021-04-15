
boolean arrastandoP = false;
boolean arrastandoQ = false;
boolean arrastandoR = false;
boolean arrastandoS = false;

  float p1x = 100;
  float p1y = 300;
  float p2x = 300;
  float p2y = 700;
  float p3x = 500;
  float p3y = 100;
  float p4x = 700;
  float p4y = 500;
void setup() {
  size (800, 800);
}

void draw() {
  background(0,255,0);
  
  if(arrastandoP)
  {
    p1x = mouseX;
    p1y = mouseY;
  }
  else if(arrastandoQ)
  {
    p2x = mouseX;
    p2y = mouseY;
  }
   else if(arrastandoR)
  {
    p3x = mouseX;
    p3y = mouseY;
  }
  else if(arrastandoS)
  {
    p4x = mouseX;
    p4y = mouseY;
  }
  noFill();
  beginShape();
  for(float t = 0; t <= 1; t += 0.01)
  {
    float ax = p1x + t*(p2x-p1x);
    float ay = p1y + t*(p2y-p1y);
    float bx = p2x + t*(p3x-p2x);
    float by = p2y + t*(p3y-p2y);
    float cx = p3x + t*(p4x-p3x);
    float cy = p3y + t*(p4y-p3y);
    float dx = ax + t*(bx-ax);
    float dy = ay + t*(by-ay);
    float ex = bx + t*(cx-bx);
    float ey = by + t*(cy-by);
    float fx = dx + t*(ex-dx);
    float fy = dy + t*(ey-dy);

    vertex(fx,fy);
  }
  endShape();
  fill(255, 0, 0);
  circle(p1x, p1y, 10);
  circle(p2x, p2y, 10);
  circle(p3x, p3y, 10);
  circle(p4x, p4y, 10);
}
void mousePressed()
{
    if(dist(p1x,p1y,mouseX,mouseY)<10)
    {
      arrastandoP = true;
    }
    if(dist(p2x,p2y,mouseX,mouseY)<10)
    {
      arrastandoQ = true;
    }
  
    if(dist(p3x,p3y,mouseX,mouseY)<10)
    {
      arrastandoR = true;
    }
    
    if(dist(p4x,p4y,mouseX,mouseY)<10)
    {
      arrastandoS = true;
    }
}

void mouseReleased()
{
  arrastandoP = false;
  arrastandoQ = false;
  arrastandoR = false;
  arrastandoS = false;
}
