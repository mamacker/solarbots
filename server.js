var express = require("express");
var app = express();
var expressWs = require("express-ws")(app);
var path = require("path");
var cookieParser = require("cookie-parser");
var session = require("express-session");
var bodyParser = require("body-parser");
app.listen(80);

process.on("uncaughtException", function (err) {
  if (err.message == "session not found") {
    console.log("Trezor USB disconnected.");
  } else {
    console.log(err);
    //console.error(err.stack);
  }
});

app.use(
  session({
    secret: "0xs###dfji23nlfnalod932flkmnlfaidsjf9092j34rjlkjfj",
    resave: true,
    saveUninitialized: false,
  })
);

app.use(bodyParser.json());
app.use(cookieParser());
app.use("/static", express.static("public"));

app.get("/", function (req, res, next) {
    res.sendFile(path.join(__dirname, "public") + "/index.html");
});

