var spawn = require("child_process").spawn;
var process = spawn('python3',["./mlwork/start.py", "/tmp/efd6896d531c87e6b9eb41c00"]);
// Takes stdout data from script which executed
// with arguments and send this data to res object
process.stdout.on('data', function(data) {
	console.log(data.toString());
})
// Takes stdout data from script which executed
// with arguments and send this data to res object
process.stderr.on('data', function(data) {
	console.log("err", data.toString());
})
