var app = angular.module("myApp", ['ngDialog', 'ngCookies']);

app.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

// app.config(['$httpProvider', function ($httpProvider) {
//   //Reset headers to avoid OPTIONS request (aka preflight)
//   $httpProvider.defaults.headers.common = {};
//   $httpProvider.defaults.headers.post = {"Content-Type":"application/json"};
//   $httpProvider.defaults.headers.put = {};
//   $httpProvider.defaults.headers.patch = {};
// }]);