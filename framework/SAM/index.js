'use strict'

exports.handler = function(event, context, callback) {
  console.log("env1 = " + process.env.Test1);
  console.log("env2 = " + process.env.Test2);
  callback(null, "Hello World");
}
