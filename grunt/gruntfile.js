module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            dist: {
                src: ['node_modules/@popperjs/core/dist/umd/popper.min.js', 'node_modules/bootstrap/dist/js/bootstrap.min.js', 'node_modules/lightbox2/dist/js/lightbox.js', 'src/flinthillsparanormal.js'],
                dest: 'dist/flinthillsparanormal.js'
            }
        },
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n',
                mangle: true,
                compress: true,
                beautify: false
        },
        dist: {
            files: {
                //'/home/flinthillsparanormal/sites/flinthillsparanormal/static/js/flinthillsparanormal.min.js': ['<%= concat.dist.dest %>'],
                '../static/js/flinthillsparanormal.min.js': ['<%= concat.dist.dest %>'],
                '../static/js/fontawesome-free.min.js': ['node_modules/@fortawesome/fontawesome-free/js/all.js'],
            }
        }
    },
    sass: {                              // Task
      dist: {                            // Target
        files: {                         // Dictionary of files
          //'/home/flinthillsparanormal/sites/flinthillsparanormal/static/css/flinthillsparanormal.css': 'src/flinthillsparanormal.scss'
          'dist/flinthillsparanormal.css': 'src/flinthillsparanormal.scss'
        }
      }
    },
    cssmin: {
      target: {
        files: [{
          expand: true,
          cwd: 'dist',
          src: ['*.css', '!*.min.css'],
          dest: '../static/css',
          ext: '.min.css'
        }]
      }
    },
    watch: {
      scripts: {
        files: 'src/*.*',
        tasks: ['concat', 'uglify', 'sass', 'cssmin'],
        // tasks: ['sass'],
        options: {
          livereload: true
        },
      },
    }
    });

    // Load the plugins
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Default task(s).

    grunt.registerTask('default', ['concat', 'uglify', 'sass', 'cssmin', 'watch']);
    // grunt.registerTask('default', ['sass', 'watch']);

};