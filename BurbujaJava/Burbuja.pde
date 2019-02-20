import java.util.List;

static abstract class BaseObject {

  PVector position;
  PVector velocity;
  
  BaseObject(PVector position, PVector velocity) {
    this.position = position;
    this.velocity = velocity;
  }
  
  void move(Float dt) {
    PVector deltaPosition = this.velocity.copy().mult(dt);
    this.position = this.position.copy().add(deltaPosition);
  }
}

class Burbuja extends BaseObject {

  Color fillColor;
  String title;
  Float titleSize;
  String text;
  Float textSize;
  Float radius;
  List<Burbuja> neighbors;
  Boolean isGrowing;
  Boolean isShrinking;
  PFont titleFont;
  PFont contentsFont;
  
  Burbuja(PVector position, PVector velocity, Color fillColor, String title, Float titleSize, String text, Float textSize, Float radius) {
    super(position, velocity);
    this.fillColor = fillColor;
    this.title = title;
    this.titleSize = titleSize;
    this.text = text;
    this.textSize = textSize;
    this.radius = radius;
    this.neighbors = new ArrayList<Burbuja>();
    this.isGrowing = false;
    this.isShrinking = false;
    this.titleFont = null;
    this.contentsFont = null;
  }
  
  void createFonts() {
    this.titleFont = createFont(TITLE_FONT, MIN_TITLE_TEXT_SIZE, true);
    this.contentsFont = createFont(CONTENTS_FONT, MIN_TITLE_TEXT_SIZE, true);
  }
  
  void setTitleFont() {
    if (this.titleFont != null) {
      textFont(this.titleFont);
    }
  }
  
  void setContentsFont() {
    if (this.contentsFont != null) {
      textFont(this.contentsFont);
    }
  } 
  
  void doDraw() {
    fill(255);
    updateRadius();
    strokeWeight(4);
    ellipse(this.position.x, this.position.y, this.radius * 2, this.radius * 2);
    drawTitle();
    drawContents();
  }
  
  void drawTitle() {
    setTitleFont();
    fill(0);
    textAlign(CENTER);
    textSize(MIN_TITLE_TEXT_SIZE + this.radius/TITLE_SCALE_FACTOR);
    Float yCoordinate = this.position.y - this.radius * CONTENTS_SHIFT_Y;
    text(this.title, this.position.x, yCoordinate);
  }
  
  void drawContents() {
    setContentsFont();
    Float textSize = MIN_TEXT_SIZE + (this.radius - MIN_RADIUS) / CONTENTS_SCALE_FACTOR;
    
    if (textSize > 0.0) {
      fill(0);
      textAlign(CENTER);
      float yCoordinate = this.position.y + this.radius * CONTENTS_SHIFT_Y;
      textSize(textSize);
      text(this.text, this.position.x, yCoordinate);
    }
  }
  
  void bounce() {
    edgeBounce();
    neighborBounce();
  }
  
  void edgeBounce() {
    Boolean leftBounce = this.radius < this.position.x;
    Boolean rightBounce = WIDTH - this.radius > this.position.x;
    
    if (!leftBounce || !rightBounce) {
      this.velocity.x *= -1;
      
      if (this.position.x < this.radius) {
        this.position.x = this.radius;
      } else {
        this.position.x = WIDTH - this.radius;
      }
    }    
    
    Boolean upBounce = this.radius < this.position.y;
    Boolean downBounce = HEIGHT - this.radius > this.position.y;
    
    if (!upBounce || !downBounce) {
      this.velocity.y *= -1;
      
      if (this.position.y < this.radius) {
        this.position.y = this.radius;
      } else {
        this.position.y = HEIGHT - this.radius;
      }
    }  
  }
  
  void neighborBounce() {
    
    for (Burbuja neighbor : this.neighbors) {
      PVector deltaPos = neighbor.position.copy().sub(this.position);
      Float diff;

      diff = (this.radius + neighbor.radius - deltaPos.copy().mag()) / deltaPos.copy().mag();
      this.position = this.position.copy().sub(deltaPos.copy().mult(diff));

      Float angle = atan2(deltaPos.y, deltaPos.x);
      Float speed = this.velocity.copy().mag();

      this.velocity.x = -speed * cos(angle);
      this.velocity.y = -speed * sin(angle);
    }
  }
  
  void startGrowth() {
    this.isShrinking = false;
    this.isGrowing = true;
  }
  
  void stopGrowth() {
    this.isShrinking = false;
    this.isGrowing = false;
  }
  
  void startShrinkage() {
    this.isGrowing = false;
    this.isShrinking = true;
  }
  
  void updateRadius() {
    if (this.isGrowing) {
      this.radius += RADIUS_GROWTH;
    } else if (this.isShrinking) {
      this.radius -= RADIUS_GROWTH;
    }
    this.radius = constrain(this.radius, MIN_RADIUS, MAX_RADIUS);
  }
}

static class CollissionChecker {

  static void checkCollisions(List<Burbuja> bList) {
    // Delete all neighbors
    for (Burbuja b : bList) {
      b.neighbors = new ArrayList<Burbuja>();
    }
    Integer iStart = 1;
    Integer bLength = bList.size();
    for (Burbuja b1 : bList.subList(0, bLength)) {
      List<Burbuja> bToCheck = bList.subList(iStart, bLength);
      iStart += 1;
      
      for (Burbuja b2 : bToCheck) {
        Float ballDistance = dist(b1.position.x, b1.position.y, b2.position.x, b2.position.y);
        Float collisionDistance = b1.radius + b2.radius;
        if (collisionDistance >= ballDistance) {
          b1.neighbors.add(b2);
          b2.neighbors.add(b1);
        }
      }
    }
  }
}
