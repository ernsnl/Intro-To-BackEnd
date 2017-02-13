module.exports = function(grunt) {
    grunt.initConfig({
        uglify: {
            dynamic_mappings: {
                files: [{
                    expand: true, // Enable dynamic expansion.
                    cwd: 'src/js/',
                    src: ['*.js'], // Actual pattern(s) to match.
                    dest: 'build/js/', // Destination path prefix.
                    ext: '.min.js', // Dest filepaths will have this extension.
                }, ]
            }
        },
        copy: {
            main: {
                files: [{
                        src: ['bower_components/jquery/dist/jquery.js'],
                        dest: "src/js/jquery.js"
                    },
                    {
                        src: ['bower_components/knockout/dist/knockout.js'],
                        dest: "src/js/knockout.js"
                    },
                    {
                        src: ['bower_components/underscore/underscore.js'],
                        dest: "src/js/underscore.js"
                    },
                    {
                        src: ['bower_components/bootstrap/dist/css/bootstrap.css'],
                        dest: "src/css/bootstrap.css"
                    },
                    {
                        src: ['bower_components/bootstrap/dist/js/bootstrap.js'],
                        dest: "src/js/bootstrap.js"
                    },
                    {
                        src: ['bower_components/font-awesome/css/font-awesome.css'],
                        dest: 'src/css/font-awesome.css'
                    },
                    {
                        expand: true,
                        flatten: true,
                        src: ['bower_components/font-awesome/fonts/*'],
                        dest: 'build/fonts/',
                        filter: 'isFile'
                    }
                ]
            },
        },
        cssmin: {
            dynamic_mappings: {
                files: [{
                    expand: true, // Enable dynamic expansion.
                    cwd: 'src/css/',
                    src: ['*.css'], // Actual pattern(s) to match.
                    dest: 'build/css/', // Destination path prefix.
                    ext: '.min.css', // Dest filepaths will have this extension.
                }, ]
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-copy')
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.registerTask('default', ['copy', 'uglify', 'cssmin']);
};
