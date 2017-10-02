var config      = require('../config');
var del         = require('del');
var gulp        = require('gulp');
var outputLogo  = require('../utils/outputLogo');

outputLogo();

gulp.task('build', ['javascript', 'browserify', 'sass', 'css','fonts', 'img'], function(){
  global.isBuilding = false;
});
