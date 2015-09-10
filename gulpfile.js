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
