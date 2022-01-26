#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This is a JavaScript injection model."""
from abc import abstractmethod, ABCMeta

__author__ = 'GZhY'
__version__ = 1.0


class JSCode:
    __metaclass__ = ABCMeta

    finished_sign = "Hi, I completed the JS injection!"
    finished_code = "document.title += '" + finished_sign + "';"

    @abstractmethod
    def get_jscode(self):
        return ""


class Scroll2Bottom(JSCode):
    def get_jscode(self):
        return """(function () {
            var y = 0;
            var step = 100;
            var height = document.body.scrollHeight;
            function f() {
                //if (y < document.body.scrollHeight) {
                if (y < height) { 
                    y += step;
                    //window.document.body.scrollTop = y;
                    window.scrollTo(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scrollTo(0, 0);""" + self.finished_code + """
                }
            }
            setTimeout(f, 1000);
        })();"""
