#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame


class Sprite():
    UP      = 1
    DOWN    = 2
    LEFT    = 3
    RIGHT   = 4

    def __init__( self, x, y, width, height ):
        self.images = {}
        self.images[ self.UP ] = ()
        self.images[ self.DOWN ] = ()
        self.images[ self.LEFT ] = ()
        self.images[ self.RIGHT ] = ()
        self.rect = pygame.Rect( x, y, width, height )

    def getRect( self ):
        return self.rect.copy()

    def getImage( self ):
        return self.image

    def setSteps( self, stepX, stepY ):
        self.stepX = stepX
        self.stepY = stepY

    def setUpdateInterval( self, updateInterval ):
        self.updateInterval = updateInterval
        self.lastUpdate = 0

    def setRefreshInterval( self, refreshInterval ):
        self.refreshInterval = refreshInterval
        self.lastRefresh = 0

    def setPos( self, x, y, heading ):
        self.rect.x = x
        self.rect.y = y
        self.setHeading( heading )

    def setHeading( self, heading ):
        self.idx = 0
        self.heading = heading
        self.image = self.images[ self.heading ][ self.idx ]

    def move( self, heading, bloqueos ):
        r = self.rect.copy()
        if( heading == self.UP ):
            r.y = r.y - self.stepY
        elif( heading == self.DOWN ):
            r.y = r.y + self.stepY
        elif( heading == self.LEFT ):
            r.x = r.x - self.stepX
        elif( heading == self.RIGHT ):
            r.x = r.x + self.stepX

        if( r.collidelist( bloqueos ) == -1 ):
            self.rect = r
            if( self.heading != heading ):
                self.setHeading( heading )
            return True
        else:
            return False

    def nextFrame( self, lastCall ):
        self.lastRefresh = self.lastRefresh + lastCall
        if( self.lastRefresh >= self.refreshInterval ):
            self.lastRefresh = 0
            self.idx = self.idx + 1
            if( self.idx >= len( self.images[ self.heading ] ) ):
                self.idx = 0
            self.image = self.images[ self.heading ][ self.idx ]

    def canUpdate( self, lastCall ):
        self.lastUpdate = self.lastUpdate + lastCall
        if( self.lastUpdate >= self.updateInterval ):
            self.lastUpdate = 0
            return True
        else:
            return False

    def update( self ):
        pass
