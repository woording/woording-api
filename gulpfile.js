'use strict';

// requirements
var gulp = require('gulp');
var sass = require('gulp-sass');
var process = require('child_process');
var shell = require('gulp-shell');

gulp.task('default', ['start_api', 'start_web', 'scss_watch']);

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


