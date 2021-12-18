var express = require("express");
var app = express();
var expressWs = require("express-ws")(app);
var path = require("path");
var cookieParser = require("cookie-parser");
var session = require("express-session");
var bodyParser = require("body-parser");
var spawn = require("child_process").spawn;

const formidable = require('formidable');

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

let userCt = 0;
app.get("/", function (req, res, next) {
  userCt++;
  if (userCt % 10 == 0) {
    console.log("Users:", userCt);
  }
  res.sendFile(path.join(__dirname, "public") + "/index.html");
});

app.get("/translate", function (req, res, next) {
  userCt++;
  if (userCt % 10 == 0) {
    console.log("Users:", userCt);
  }
  res.sendFile(path.join(__dirname, "public") + "/translate.html");
});

app.post('/api/upload', (req, res, next) => {
  const form = formidable({ multiples: true });

  form.parse(req, (err, fields, files) => {
    if (err) {
      next(err);
      return;
    }

    try {
      console.log("processing: ", files.someExpressFiles.filepath);
      var process = spawn('python3',["./mlwork/start.py", files.someExpressFiles.filepath]);
    
      // Takes stdout data from script which executed
      // with arguments and send this data to res object
      process.stdout.on('data', function(data) {
        console.log(data.toString());
        res.send(data.toString());
      })
      process.stderr.on('data', function(data) {
        console.log("err", data.toString());
        res.send(data.toString());
      })
    } catch(ex) {
      console.log(ex);
      res.send("error");
    }
  });
});

