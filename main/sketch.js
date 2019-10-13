var Engine = Matter.Engine,
    Render = Matter.Render,
    World = Matter.World,
    Bodies = Matter.Bodies;

var engine;
var world;
var circle = [];
var boundaries = [];
var k = 0;
var c = 0;
function setup() {
  createCanvas(400, 600);
  engine = Engine.create();
  world = engine.world;
  var options = {
    isStatic: true
  }

  boundaries.push(new Boundary(40, 200, width * 0.8, 20, 30*2*3.14/360));
  boundaries.push(new Boundary(365, 200, width * 0.8, 20, -30*2*3.14/360));

}
// boundaries.push(new Boundary(65, 200, width * 0.8, 20, 0.8));
// boundaries.push(new Boundary(335, 200, width * 0.8, 20, -0.8));
//function mouseDragged() {
//  circle.push(new Circle(mouseX, mouseY, random(5, 7)));
//}

function draw() {
  if (circle.length <300) {
    circle.push(new Circle(random(50,350),50,random(5,8)))
  }
  background(51);
  Engine.update(engine);
  for (var i = 0; i < circle.length; i++) {
    circle[i].show();
    if (circle[i].isOffScreen()) {
      k++;
      circle[i].removeFromWorld();
      circle.splice(i, 1);
      i--;
    }
    if (frameCount%300==0) {
      console.log(k/5);
      k=0;
    }
  }

  for (var i = 0; i < boundaries.length; i++) {
    boundaries[i].show();
  }

}
