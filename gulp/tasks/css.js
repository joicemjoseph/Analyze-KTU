var autoprefixer = require('gulp-autoprefixer');
var browserSync  = require('browser-sync');
var config       = require('../config').css;
var gulp         = require('gulp');
var handleErrors = require('../utils/handleErrors');

gulp.task('css', function () {
  return gulp.src(config.src)
    .on('error', handleErrors)
    .pipe(gulp.dest(config.dest))
    .pipe(browserSync.reload({stream:true}));
});
