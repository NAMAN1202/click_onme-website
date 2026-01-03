from flask import Flask, render_template_string
import os

app = Flask(
    __name__,
    static_folder="static",
    static_url_path="/static"
)

# ================= HOME =================
HTML_HOME = """
<!DOCTYPE html>
<html>
<head>
<title>Birthday 🎉</title>
<style>
body{
  margin:0;
  font-family:Arial;
  background:linear-gradient(270deg,#ff6fb1,#8fd3f4,#fbc2eb);
  background-size:600% 600%;
  animation:bg 10s infinite;
  height:100vh;
  overflow:hidden;
  color:white;
}
@keyframes bg{
  0%{background-position:0%}
  50%{background-position:100%}
  100%{background-position:0%}
}
.center{
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  text-align:center;
}
button{
  padding:16px 36px;
  font-size:20px;
  border:none;
  border-radius:40px;
  cursor:pointer;
  background:linear-gradient(135deg,#ffe259,#ffa751);
  font-weight:bold;
}
#overlay{
  position:fixed;
  inset:0;
  background:black;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:90px;
  z-index:5;
}
</style>
</head>
<body>

<div id="overlay"><span id="count">5</span></div>

<div class="center">
  <h1>🎉 Happy Birthday Didi 🎉</h1>
  <p>Something special is coming 💖</p>
  <button onclick="location.href='/cake'">Tap for Surprise 🎁</button>
</div>

<script>
let c = 5;
let t = setInterval(function(){
  c--;
  document.getElementById("count").innerText = c;
  if(c === 0){
    clearInterval(t);
    document.getElementById("overlay").style.display = "none";
  }
},1000);
</script>

</body>
</html>
"""

# ================= CAKE =================
HTML_CAKE = """
<!DOCTYPE html>
<html>
<head>
<title>Cake 🎂</title>
<style>
body{
  margin:0;
  background:black;
  overflow:hidden;
  color:white;
  font-family:Arial;
}
canvas{position:fixed;inset:0;}
.center{
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  text-align:center;
}
.cake{
  width:260px;
  height:160px;
  background:#ffb347;
  border-radius:25px;
  margin:30px auto;
  position:relative;
}
.candle{
  width:10px;
  height:45px;
  background:white;
  margin:0 8px;
  display:inline-block;
  position:relative;
}
.flame{
  position:absolute;
  top:-18px;
  left:50%;
  transform:translateX(-50%);
  width:16px;
  height:22px;
  background:radial-gradient(circle,#fff700,#ff7b00,#ff0000);
  border-radius:50%;
  animation:flicker .2s infinite alternate;
}
@keyframes flicker{
  from{transform:translateX(-50%) scale(1);}
  to{transform:translateX(-50%) scale(1.4);}
}
.glow{
  box-shadow:0 0 25px gold;
}
button{
  padding:14px 30px;
  border:none;
  border-radius:30px;
  cursor:pointer;
}
</style>
</head>
<body>

<canvas id="fw"></canvas>

<div class="center">
  <h1>🎂 Make a Wish 🎂</h1>

  <div class="cake" id="cake">
    <div style="position:absolute;top:-50px;left:50%;transform:translateX(-50%)">
      <div class="candle"><div class="flame" id="f1"></div></div>
      <div class="candle"><div class="flame" id="f2"></div></div>
      <div class="candle"><div class="flame" id="f3"></div></div>
    </div>
  </div>

  <button onclick="blow()">Blow Candles 🕯️</button><br><br>
  <button onclick="location.href='/memories'">See Memories 📸</button>
</div>

<script>
const canvas = document.getElementById("fw");
const ctx = canvas.getContext("2d");
canvas.width = innerWidth;
canvas.height = innerHeight;

let sparks = [];

function fire(power){
  for(let i=0;i<power;i++){
    sparks.push({
      x:Math.random()*canvas.width,
      y:canvas.height,
      dx:(Math.random()-0.5)*6,
      dy:-Math.random()*10-5,
      life:100
    });
  }
}

setInterval(function(){ fire(6); },300);

function animate(){
  ctx.fillStyle="rgba(0,0,0,0.25)";
  ctx.fillRect(0,0,canvas.width,canvas.height);
  sparks.forEach(function(s,i){
    s.x+=s.dx;
    s.y+=s.dy;
    s.dy+=0.1;
    s.life--;
    ctx.fillStyle="gold";
    ctx.fillRect(s.x,s.y,3,3);
    if(s.life<=0) sparks.splice(i,1);
  });
  requestAnimationFrame(animate);
}
animate();

function blow(){
  document.getElementById("cake").classList.add("glow");
  fire(200);
  ["f1","f2","f3"].forEach(function(id){
    document.getElementById(id).style.display="none";
  });
}
</script>

</body>
</html>
"""

# ================= MEMORIES =================
HTML_MEMORIES = """
<!DOCTYPE html>
<html>
<head>
<title>Memories 💖</title>
<style>
body{
  margin:0;
  background:linear-gradient(135deg,#ff9a9e,#fad0c4);
  overflow:hidden;
  color:white;
  font-family:Arial;
}
.balloon{
  position:absolute;
  bottom:-100px;
  font-size:40px;
  animation:float 10s linear infinite;
}
@keyframes float{
  to{transform:translateY(-120vh);}
}
.center{
  position:absolute;
  top:50%;
  left:50%;
  transform:translate(-50%,-50%);
  text-align:center;
}
.photo{
  width:140px;
  height:140px;
  border-radius:15px;
  overflow:hidden;
  margin:10px;
  display:inline-block;
  background:rgba(255,255,255,.3);
}
.photo img{
  width:100%;
  height:100%;
  object-fit:cover;
}
</style>
</head>
<body>

<div class="balloon" style="left:10%">🎈</div>
<div class="balloon" style="left:30%">🎈</div>
<div class="balloon" style="left:50%">🎈</div>
<div class="balloon" style="left:70%">🎈</div>
<div class="balloon" style="left:90%">🎈</div>

<div class="center">
  <h1>💖 Beautiful Memories 💖</h1>
  <div>
    <div class="photo"><img src="/static/images/photo1.jpeg"></div>
    <div class="photo"><img src="/static/images/photo2.jpeg"></div>
    <div class="photo"><img src="/static/images/photo3.jpeg"></div>
  </div>
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_HOME)

@app.route("/cake")
def cake():
    return render_template_string(HTML_CAKE)

@app.route("/memories")
def memories():
    return render_template_string(HTML_MEMORIES)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
