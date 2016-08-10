#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from Sprite import Sprite


class Enemy( Sprite ):
    def __init__( self, x, y, width, height, fname ):
        Sprite.__init__( self, x, y, width, height )
        bitmap = pygame.image.load( fname ).convert_alpha()
        self.images[ self.UP ] = (
                bitmap.subsurface( ( width * 0, height * 0, width, height ) ),
                bitmap.subsurface( ( width * 0, height * 1, width, height ) )
            )
        self.images[ self.DOWN ] = (
                bitmap.subsurface( ( width * 1, height * 0, width, height ) ),
                bitmap.subsurface( ( width * 1, height * 1, width, height ) )
            )
        self.images[ self.LEFT ] = (
                bitmap.subsurface( ( width * 2, height * 0, width, height ) ),
                bitmap.subsurface( ( width * 2, height * 1, width, height ) )
            )
        self.images[ self.RIGHT ] = (
                bitmap.subsurface( ( width * 3, height * 0, width, height ) ),
                bitmap.subsurface( ( width * 3, height * 1, width, height ) )
            )
        self.setHeading( self.LEFT )
        self.setSteps( 2, 2 )
        self.setUpdateInterval( 32 )
        self.setRefreshInterval( 100 )

    def update( self, keys, bloqueos, target, lastCall ):
        if( not self.canUpdate( lastCall ) ):
            return

        dx = target.x - self.rect.x
        dy = target.y - self.rect.y

        if( self.heading == self.UP ):
            if( dx == 0 ):
                moves = [ self.UP, self.LEFT, self.RIGHT, self.DOWN ]
            elif( dx < 0 ):
                moves = [ self.LEFT, self.UP, self.RIGHT, self.DOWN ]
            else:
                moves = [ self.RIGHT, self.UP, self.LEFT, self.DOWN ]
        elif( self.heading == self.DOWN ):
            if( dx == 0 ):
                moves = [ self.DOWN, self.LEFT, self.RIGHT, self.UP ]
            elif( dx < 0 ):
                moves = [ self.LEFT, self.DOWN, self.RIGHT, self.UP ]
            else:
                moves = [ self.RIGHT, self.DOWN, self.LEFT, self.UP ]
        elif( self.heading == self.LEFT ):
            if( dy == 0 ):
                moves = [ self.LEFT, self.UP, self.DOWN, self.RIGHT ]
            elif( dy < 0 ):
                moves = [ self.UP, self.LEFT, self.DOWN, self.RIGHT ]
            else:
                moves = [ self.DOWN, self.LEFT, self.UP, self.RIGHT ]
        elif( self.heading == self.RIGHT ):
            if( dy == 0 ):
                moves = [ self.RIGHT, self.UP, self.DOWN, self.LEFT ]
            elif( dy < 0 ):
                moves = [ self.UP, self.RIGHT, self.DOWN, self.LEFT ]
            else:
                moves = [ self.DOWN, self.RIGHT, self.UP, self.LEFT ]

        for heading in moves:
            if( self.move( heading, bloqueos ) ):
                break

        self.nextFrame( lastCall )
