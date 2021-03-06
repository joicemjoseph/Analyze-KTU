var autoprefixer = require('gulp-autoprefixer');
var browserSync  = require('browser-sync');
var config       = require('../config').img;
var gulp         = require('gulp');
var handleErrors = require('../utils/handleErrors');

gulp.task('img', function () {
  return gulp.src(config.src)
    .on('error', handleErrors)
    .pipe(gulp.dest(config.dest))
    .pipe(browserSync.reload({stream:true}));
});
