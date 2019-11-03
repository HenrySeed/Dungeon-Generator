Room rootRoom;

void genDungeon() {  
  // build base room
  rootRoom = new Room(new PVector(width/2, height/2), 100, 100, 2, 1);
}

void setup() {
  size(1000, 800);
  background(100);
  genDungeon();
}

void draw() {
  rootRoom.render();
}

void mouseClicked() {
  clear();
  background(100);
  genDungeon();
}
