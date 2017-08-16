// MIT License
//
// Copyright (c) 2017 Sedrak Dalaloyan
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

'use strict';

var polyDraw = angular.module('ngPolyDraw', []);

polyDraw.directive('ngPolyDraw', [function () {
    return {
        restrict: 'A',
        scope: {
            imageUrl: '=',
            enabled: '=',
            palette: '=',
            points: '=',
            active: '=',
            width: '=',
            height: '=',
            newPoints: '='
        },
        controller: function () {
            this.dotLineLength = function(x, y, x0, y0, x1, y1, o) {

                function lineLength(x, y, x0, y0) {
                    return Math.sqrt((x -= x0) * x + (y -= y0) * y);
                }

                function find_line_endpoints(x, y, x0, y0, x1, y1) {
                    if (!(x1 - x0)) {
                        return {x: x0, y: y};
                    } else if (!(y1 - y0)) {
                        return {x: x, y: y0};
                    }

                    var left, tg = -1 / ((y1 - y0) / (x1 - x0));

                    return {
                        x: left = (x1 * (x * tg - y + y0) + x0 * (x * - tg + y - y1)) / (tg * (x1 - x0) + y0 - y1),
                        y: tg * left - tg * x + y
                    };
                }

                var alt_o = find_line_endpoints(x, y, x0, y0, x1, y1);
                var min_x = Math.min(x0, x1);
                var max_x = Math.max(x0, x1);
                var min_y = Math.min(y0, y1);
                var max_y = Math.max(y0, y1);

                if (o && !(o = alt_o)) {
                    if (o.x >= min_x && o.x <= max_x && o.y >= min_y && o.y <= max_y) {

                        var l1 = lineLength(x, y, x0, y0);
                        var l2 = lineLength(x, y, x1, y1);

                        return l1 > l2 ? l2 : l1;
                    }
                }

                var a = y0 - y1,
                    b = x1 - x0,
                    c = x0 * y1 - y0 * x1;

                return Math.abs(a * x + b * y + c) / Math.sqrt(a * a + b * b);
            };

            this.hexToRgb = function(hex){
                var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
                return result ? {
                    r: parseInt(result[1], 16),
                    g: parseInt(result[2], 16),
                    b: parseInt(result[3], 16)
                } : null;
            };
            this.getMousePos = function (canvas, evt) {
                var rect = canvas.getBoundingClientRect();
                return {
                    x: evt.clientX - rect.left,
                    y: evt.clientY - rect.top
                };
            };
        },
        link: function(scope, element, attrs, ctrl) {

            var activePoint, settings = {};
            var $canvas, ctx, image;

            if(!scope.points) {
                scope.points = [[]];
            }

            if(!scope.active) {
                scope.active = 0;
            }

            $canvas = $('<canvas>');
            ctx = $canvas[0].getContext('2d');

            scope.$watch('imageUrl', function() {
                if (scope.imageUrl === null) {
                    return;
                }

                settings.imageUrl = scope.imageUrl;
                settings.height = scope.height;
                settings.width = scope.width;

                image = new Image();

                scope.resize = function () {
                    $canvas.attr('height', settings.height).attr('width', settings.width);
                    settings.img_scale_x = this.width / settings.width;
                    settings.img_scale_y = this.height / settings.height;
                };
                $(image).load(scope.resize);

                image.src = settings.imageUrl;

                if (image.loaded) scope.resize();

                $canvas.css({background: 'url(' + image.src + ')'});
                $canvas.css({backgroundSize: 'contain'});
            });

            $(element).append($canvas);

            scope.move = function(e) {
                if(!e.offsetX) {
                    e.offsetX = (e.pageX - $(e.target).offset().left);
                    e.offsetY = (e.pageY - $(e.target).offset().top);
                }
                var points = scope.points[scope.active];
                points[activePoint] = [
                    Math.round(e.offsetX),
                    Math.round(e.offsetY),
                    Math.floor(e.offsetX * settings.img_scale_x),
                    Math.ceil(e.offsetY * settings.img_scale_y)
                ];

                scope.record();
                scope.draw();
            };

            scope.stopdrag = function() {
                element.off('mousemove');
                scope.record();
                activePoint = null;
            };

            scope.rightclick = function(e) {
                e.preventDefault();
                if(!e.offsetX) {
                    e.offsetX = (e.pageX - $(e.target).offset().left);
                    e.offsetY = (e.pageY - $(e.target).offset().top);
                }
                var x = e.offsetX, y = e.offsetY;
                var points = scope.points[scope.active];
                for (var i = 0; i < points.length; ++i) {
                    var dis = Math.sqrt(Math.pow(x - points[i][0], 2) + Math.pow(y - points[i][1], 2));
                    if ( dis < 6 ) {
                        points.splice(i, 1);
                        scope.draw();
                        scope.record();
                        return false;
                    }
                }
                return false;
            };

            scope.mousedown = function(e) {
                if (!scope.enabled || e.which ===3) {
                    return false;
                }
                var points = scope.points[scope.active];
                var x, y, dis, minDis = 0, minDisIndex = -1, lineDis, insertAt = points.length;

                e.preventDefault();
                if(!e.offsetX) {
                    e.offsetX = (e.pageX - $(e.target).offset().left);
                    e.offsetY = (e.pageY - $(e.target).offset().top);
                }

                var mousePos = ctrl.getMousePos($canvas[0], e);
                x = mousePos.x;
                y = mousePos.y;
                for (var i = 0; i < points.length; ++i) {
                    dis = Math.sqrt(Math.pow(x - points[i][0], 2) + Math.pow(y - points[i][1], 2));
                    if(minDisIndex === -1 || minDis > dis) {
                        minDis = dis;
                        minDisIndex = i;
                    }
                }

                // if within 6px of existing point, assume the user wants to move it
                if ( minDis < 6 && minDisIndex >= 0 ) {
                    activePoint = minDisIndex;
                    element.on('mousemove', scope.move);
                    return false;
                }

                points.splice(
                    insertAt,
                    0,
                    [
                        Math.round(x),
                        Math.round(y),
                        Math.floor(x * settings.img_scale_x),
                        Math.ceil(y * settings.img_scale_y)
                    ]
                );
                activePoint = insertAt;
                element.on('mousemove', scope.move);

                scope.draw();
                scope.record();

                return false;
            };

            scope.draw = function() {

                // re-initialize canvas pixels by resetting the width,
                // could use clearRect to just refresh the region
                //noinspection SillyAssignmentJS
                ctx.canvas.width = ctx.canvas.width;

                if(scope.points.length > 0 && scope.active >= 0) {
                    scope.drawSingle(scope.points[scope.active], scope.active);
                }
                for(var p = 0; p < scope.points.length; ++p) {
                    var points = scope.points[p];

                    if (points.length === 0 || scope.active === p) {
                        continue;
                    }

                    scope.drawSingle(points, p);
                }
            };

            scope.drawSingle = function (points, p) {

                ctx.globalCompositeOperation = 'destination-over';
                ctx.fillStyle = 'rgb(255,255,255)';
                ctx.strokeStyle = scope.palette[p % scope.palette.length];
                ctx.lineWidth = 2;

                ctx.beginPath();
                // ctx.moveTo(points[0], points[1]);
                for (var i = 0; i < points.length; ++i) {
                    if (scope.active === p && scope.enabled) {
                        ctx.fillRect(points[i][0] - 2, points[i][1] - 2, 4, 4);
                        ctx.strokeRect(points[i][0] - 2, points[i][1] - 2, 4, 4);
                    }
                    ctx.lineTo(points[i][0], points[i][1]);
                }
                ctx.closePath();

                var fillColor = ctrl.hexToRgb(ctx.strokeStyle);
                ctx.fillStyle = 'rgba(' + fillColor.r + ',' + fillColor.g + ',' + fillColor.b + ',0.2)';
                ctx.fill();
                ctx.stroke();
            };

            scope.record = function() {
                scope.$apply();
            };

            scope.$watch('points', function () {
                scope.draw();
            }, true);

            scope.$watch('active', function (newVal, oldVal) {
                if (newVal != oldVal) scope.draw();
            });

            // setup watch for new_points, these would be updated by the ctrl
            scope.$watch('newPoints', function() {
                var tmp_points = [];

                scope.newPoints.forEach(function(region) {
                    var new_region_points = [];

                    region.forEach(function(p) {
                        new_region_points.push(
                            [
                                Math.floor(p[0] / settings.img_scale_x),
                                Math.floor(p[1] / settings.img_scale_y),
                                p[0],
                                p[1]
                            ]
                        )
                    });

                    tmp_points.push(new_region_points);
                });

                scope.points = tmp_points;
            });

            $canvas.on('mousedown', scope.mousedown);
            $canvas.on('contextmenu', scope.rightclick);
            $canvas.on('mouseup', scope.stopdrag);
        }
    };
}]);
