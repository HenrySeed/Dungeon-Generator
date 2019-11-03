class Room {
  PVector origin; // the top left corner of a room
  float height;
  float width;
  int entrance;
  float startDistance;
  
  Room sideRooms[];
  
  Room(PVector origin, float height, float width, int entrance, float startDistance) {
    this.origin = origin;
    this.height = height;
    this.width = width;
    this.startDistance = startDistance;
    // the side this room entrances from 0=N, 1=E, 2=S, 3=W
    this.entrance = entrance;
    this.sideRooms = new Room[4];
    
    if(startDistance % 2 == 0){
      // generate a main room at the end of a corridor
      genMainRoom();
    } else {
      // generate the side rooms
      genSideRooms();
    }
  }
  
  void genMainRoom() {
    float newRoomWall = random(40, 80);
    float newRoomDepth = random(40, 80);
    float corridorWidth = this.entrance % 2 == 0 ? this.width : this.height;
    float corridorWallDist = random(0, newRoomWall - corridorWidth);
    
    switch (this.entrance) {
          case 0: // N
            this.sideRooms[0] = new Room(
              new PVector(this.origin.x-corridorWallDist, this.origin.y+this.height), 
              newRoomDepth,
              newRoomWall,
              this.entrance,
              this.startDistance + 1
            );
            break;
            
          case 1: // E
            this.sideRooms[0] = new Room(
              new PVector(this.origin.x-newRoomDepth, this.origin.y-corridorWallDist), 
              newRoomWall,
              newRoomDepth,
              this.entrance,
              this.startDistance + 1
            );
            break;
            
          case 2: // S
            this.sideRooms[0] = new Room(
              new PVector(this.origin.x-corridorWallDist, this.origin.y-newRoomDepth), 
              newRoomDepth,
              newRoomWall,
              this.entrance,
              this.startDistance + 1
            );
            break;
            
          case 3: // W
            this.sideRooms[0] = new Room(
              new PVector(this.origin.x+this.width, this.origin.y-corridorWallDist), 
              newRoomWall,
              newRoomDepth,
              this.entrance,
              this.startDistance + 1
            );
            break;
        }
  }
  
  void genSideRooms(){
    // if we've reached max depth, dont continue
    if(this.startDistance < 4){
      // for each of the directions, generate a corridor
      for(int d = 0; d < 4; d++){
        float corridorWidth = random(10, 20);
        float corridorLength = random(20, 40);
        float corridorStartX;
        float corridorStartY;
        
        //if(d == this.entrance && this.startDistance == 0){
        //  // dont make a corridor exit on the same side as the entrance
        //  continue;
        //}
        
        switch (d) {
          case 0: // N
            corridorStartX = random(this.origin.x, this.origin.x + this.width - corridorWidth);
            corridorStartY = this.origin.y;
            this.sideRooms[d] = new Room(
                new PVector(corridorStartX, corridorStartY-corridorLength), 
                corridorLength, 
                corridorWidth, 
                2, 
                this.startDistance+1
              );
            break;
            
          case 1: // E
            corridorStartY = random(this.origin.y, this.origin.y + this.height - corridorWidth);
            corridorStartX = this.origin.x + this.width;
            this.sideRooms[d] = new Room(
                new PVector(corridorStartX, corridorStartY), 
                corridorWidth, 
                corridorLength, 
                3, 
                this.startDistance+1
              );
            break;
            
          case 2: // S
            corridorStartX = random(this.origin.x, this.origin.x + this.width - corridorWidth);
            corridorStartY = this.origin.y + this.height;
            this.sideRooms[d] = new Room(
                new PVector(corridorStartX, corridorStartY), 
                corridorLength, 
                corridorWidth, 
                0, 
                this.startDistance+1
              );
            break;
            
            
          case 3: // W
            corridorStartY = random(this.origin.y, this.origin.y + this.height - corridorWidth);
            corridorStartX = this.origin.x;
            this.sideRooms[d] = new Room(
                new PVector(corridorStartX-corridorLength, corridorStartY), 
                corridorWidth, 
                corridorLength, 
                1, 
                this.startDistance+1
              );
            break;
            
        }
      }
    }
  }
  
  void render() {
    noStroke();
    fill(0);
    rect(origin.x, origin.y, width, height);
    
    for(int i = 0; i < 4; i++){
      if(this.sideRooms[i] != null){
        this.sideRooms[i].render();
      }
    }
  }
}
