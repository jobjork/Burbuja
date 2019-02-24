import java.util.Arrays;
import java.lang.Math;
import java.util.Random;

PImage bg;
State state;
List<Burbuja> bList;

// Config parameters
final String IMAGE_PATH = "res.jpg";
final String TITLE_FONT = "kenyan_coffee_rg.ttf";
final String CONTENTS_FONT = "Museo300-Regular.otf";
final Integer WIDTH = 1440;
final Integer HEIGHT = 900;
final Float MIN_TITLE_TEXT_SIZE = 12.0;
final Float MIN_TEXT_SIZE = 0.0;
final Float TITLE_SCALE_FACTOR = 9.0;
final Float CONTENTS_SHIFT_Y = 0.1;
final Float MIN_RADIUS = 75.0;
final Float MAX_RADIUS = 180.0;
final Float RADIUS_GROWTH = 0.8;
final Float CONTENTS_SCALE_FACTOR = 3.0;
final Integer VELOCITY_MAX = 70;
final Float DEFAULT_TITLE_TEXT_SIZE = MIN_TITLE_TEXT_SIZE + MIN_RADIUS/TITLE_SCALE_FACTOR;
final Float DEFAULT_CONTENTS_TEXT_SIZE = MIN_TEXT_SIZE + MIN_RADIUS/CONTENTS_SCALE_FACTOR;

void settings() {
  fullScreen();
}

void setup() {

  final List<List<String>> BURBUJAS_LIST = Arrays.asList(
    Arrays.asList("First title text", "First list \nof \ncontents"), 
    Arrays.asList("Second title text", "Second list \nof \ncontents"), 
    Arrays.asList("Third title text", "Third list \nof \ncontents"),
    Arrays.asList("Fourth title text", "Fourth list \nof \ncontents")
  );
  Integer NUM_BURBUJAS = BURBUJAS_LIST.size();
  List<PVector> positions = new ArrayList<PVector>();
  List<PVector> velocities = new ArrayList<PVector>();
  
  for (int i = 0; i < NUM_BURBUJAS; i++) {  
    positions.add(
      new PVector(
        (float)(Math.random() * 0.9 * WIDTH), 
        (float)(Math.random() * 0.9 * HEIGHT)
      )
    );
  }
  Random random = new Random();
  for (int j = 0; j < NUM_BURBUJAS; j++) {
    velocities.add(
      new PVector(
        (float)(random.nextInt(2*VELOCITY_MAX) - VELOCITY_MAX), 
        (float)(random.nextInt(2*VELOCITY_MAX) - VELOCITY_MAX)
      )
    );
  }
  // Default color. Will not be used if background image is in use
  Color c = new Color(192, 0, 210);
  bList = new ArrayList<Burbuja>();
  
  for (int k = 0; k < NUM_BURBUJAS; k++) {
    Burbuja b = new Burbuja(
      positions.get(k), 
      velocities.get(k),
      c, 
      BURBUJAS_LIST.get(k).get(0), 
      DEFAULT_TITLE_TEXT_SIZE, 
      BURBUJAS_LIST.get(k).get(1), 
      DEFAULT_CONTENTS_TEXT_SIZE,
      40.0
    );
    bList.add(b);
  }
  state = new State();
  for (Burbuja b : bList) {
    b.createFonts();
  }
  frameRate(100);
  smooth(80);
  fill(0);
  size(1440, 900);
  bg = loadImage(IMAGE_PATH);
}

void draw() {
  image(bg, 0, 0, 1440, 900);
  state.update();
  state.resizeBallInlist(bList);

  for (Burbuja b : bList) { 
    b.move(state.dtSeconds);
  }
  CollissionChecker.checkCollisions(bList);
  for (Burbuja b : bList) {
    b.bounce();
    b.doDraw();
  }
}
