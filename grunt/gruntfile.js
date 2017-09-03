module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        concat: {
            dist: {
                src: ['node_modules/jquery/dist/jquery.slim.js', 'node_modules/bootstrap/js/dist/util.js', 'node_modules/bootstrap/js/dist/collapse.js', 'src/flinthillsparanormal.js'],
                dest: 'dist/js/flinthillsparanormal.js'
            }
        },
        uglify: {
            options: {
                banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n',
                compress: {},
                beautify: true
        },
        dist: {
            files: {
                //'/mnt/volume-nyc1-01-part2/static/js/fourfridays.min.js': ['<%= concat.dist.dest %>'],
                '../static/js/flinthillsparanormal.min.js': ['<%= concat.dist.dest %>'],
            }
        }
    },
    sass: {                              // Task
      dist: {                            // Target
        files: {                         // Dictionary of files
          //'/mnt/volume-nyc1-01-part2/static/css/fourfridays.css': 'src/fourfridays.scss'
          '../static/css/flinthillsparanormal.css': 'src/flinthillsparanormal.scss'
        }
      }
    },
    cssmin: {
      target: {
        files: [{
          expand: true,
          cwd: '../static/css',
          src: ['*.css', '!*.min.css'],
          dest: '../static/css',
          ext: '.min.css'
        }]
      }
    },
    watch: {
      scripts: {
        files: 'src/*.*',
        tasks: ['concat', 'uglify', 'sass'],
        //tasks: ['sass'],
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
    //grunt.registerTask('default', ['sass', 'watch']);

};