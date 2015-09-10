'use strict';

// requirements
var gulp = require('gulp');
var sass = require('gulp-sass');
var process = require('child_process');
var shell = require('gulp-shell');

var runSequence = require('run-sequence');

gulp.task('default', ['start']);

gulp.task('initialize_api', shell.task(['cd api && ./initialize.sh']));
gulp.task('start_api', shell.task(['cd api && . env/bin/activate && python api.py']));
gulp.task('start_web', shell.task(['cd web && . ../api/env/bin/activate && python site.py']));

gulp.task('scss', function() {
	gulp.src('web/static/scss/**/*.scss')
		.pipe(sass().on('error', sass.logError))
		.pipe(gulp.dest('web/static/css/'))
});

gulp.task('scss_watch', function() {
	gulp.watch('web/static/scss/**/*.scss', ['scss']);
});

gulp.task('start', function(done) {
	runSequence('initialize_api', function() {
		gulp.start('start_api');
		gulp.start('start_web');
		gulp.start('scss_watch');

	});
});

// // takes in a callback so the engine knows when it'll be done
// gulp.task('one', function(cb) {
//   // do stuff -- async or otherwise
//   cb(err); // if err is not null and not undefined, the orchestration will stop, and 'two' will not run
// });

// // identifies a dependent task must be complete before this one begins
// gulp.task('two', ['one'], function() {
// 	gulp.start('start_api');
// 	gulp.start('start_web');
// 	gulp.start('scss_watch');
//   // task 'one' is done now
// });

