/**
 * Gulp Configuration
 *
 * A set of paths and options for Gulp to properly build our application.
 */

// Define Global Variables for our main object
var dest = './analyzer/static/';
var src = './analyzer/dev/';
var bower = './bower_components/';
var temp = './build/';

module.exports = {
  // Define module variables for easy access to source and destination dirs
  src: src,
  dest: dest,

  // BrowserSync allows us to have livereload as we work on files
  browserSync: {
    mode: 'proxy',
    all: {
      port: process.env.PORT || 8000,
      open: true
    },
    debug: {
      logFileChanges: true,
      logLevel: "debug"
    },
    serverOptions: {
      files: [
        dest + "/**",
        "!" + dest + "/**.map"
      ],
    },
    proxyOptions: {
      proxy: '127.0.0.1:8000'
    }
  },

  // Compile our SCSS files
  sass: {
    src: [
      src + 'scss/screen.scss',
      src + 'scss/**/*.scss'
    ],
    dest: temp + 'css',
    settings: {}
  },
  fonts: {
    src: [
      bower + 'miminum/asset/fonts/*'
    ],
    dest: dest + 'fonts'
  },
  img: {
    src: [
      bower + 'miminum/asset/img/*'
    ],
    dest: dest + 'img'
  },
  css: {
    src: [
      bower + 'bootstrap-datepicker/dist/css/bootstrap-datepicker3.min.css',
      bower + 'miminum/asset/css/plugins/icheck/skins/**/_all.css',
      bower + 'miminum/asset/css/plugins/icheck/skins/all.css',
      bower + 'miminum/asset/css/plugins/ionrangeslider/*.css',
      bower + 'miminum/asset/css/plugins/*.css',
      bower + 'miminum/asset/css/*.css',
      temp + 'css/*.css'
    ],
    dest: dest + 'css'
  },
  // Compile our JS files
  js: {
    src: [
      src + 'js/app.js',
      src + 'js/**/*.js',
      bower + 'bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js',
      bower + 'chained/jquery.chained.min.js',
      bower + 'chained/jquery.chained.remote.min.js',
      bower + 'jquery/dist/jquery.min.js',
      bower + 'parselyjs/dist/parsely.min.js',
      bower + 'parselyjs/dist/i18n/en.js',
      bower + 'miminum/asset/js/plugins/**/*.js',
      bower + 'miminum/asset/js/*.js'
    ],
    dest: dest + 'js',
    settings: {
      bare: true
    }
  },

  // Handle minimizing JS Files into a single file
  browserify: {
    extensions: [],
    transform: [],
    bundleConfigs: [
      {
        entries: src + '/js/app.js',
        dest: dest + '/js',
        outputName: 'app.js'
      }
    ]
  },

  // Django Templates
  templates: {
    src: [
      src + '../apps/*/templates/*.html',
      src + '../apps/*/templates/**/*.html',
      src + '../templates/*.html'
    ]
  }
}
