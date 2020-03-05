const express = require('express');
const app = express();
const logger = require('morgan');

//Log all requests
app.use(logger('combined'))

//Set content directories
app.use('/', express.static(__dirname + '/static'));


var port = process.env.PORT || 5000;
app.listen(port, function() {
  console.log("Listening on " + port);
});
