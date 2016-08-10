#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from Sprite import Sprite


class Hero( Sprite ):
    def __init__( self, x, y, width, height, fname ):
        Sprite.__init__( self, x, y, width, height )
        bitmap = pygame.image.load( fname ).convert_alpha()
        self.images[ self.UP ] = (
                bitmap.subsurface( ( width * 0, height * 0, width, height ) ),
                bitmap.subsurface( ( width * 0, height * 1, width, height ) ),
                bitmap.subsurface( ( width * 0, height * 2, width, height ) ),
                bitmap.subsurface( ( width * 0, height * 3, width, height ) )
            )
        self.images[ self.DOWN ] = (
                bitmap.subsurface( ( width * 1, height * 0, width, height ) ),
                bitmap.subsurface( ( width * 1, height * 1, width, height ) ),
                bitmap.subsurface( ( width * 1, height * 2, width, height ) ),
                bitmap.subsurface( ( width * 1, height * 3, width, height ) )
            )
        self.images[ self.LEFT ] = (
                bitmap.subsurface( ( width * 2, height * 0, width, height ) ),
                bitmap.subsurface( ( width * 2, height * 1, width, height ) ),
                bitmap.subsurface( ( width * 2, height * 2, width, height ) ),
                bitmap.subsurface( ( width * 2, height * 3, width, height ) )
            )
        self.images[ self.RIGHT ] = (
                bitmap.subsurface( ( width * 3, height * 0, width, height ) ),
                bitmap.subsurface( ( width * 3, height * 1, width, height ) ),
                bitmap.subsurface( ( width * 3, height * 2, width, height ) ),
                bitmap.subsurface( ( width * 3, height * 3, width, height ) )
            )
        self.setHeading( self.LEFT )
        self.setSteps( 2, 2 )
        self.setUpdateInterval( 16 )
        self.setRefreshInterval( 16 )

    def update( self, keys, bloqueos, target, lastCall ):
        if( not self.canUpdate( lastCall ) ):
            return

        move = False
        if( keys[ pygame.K_UP ] == pygame.KEYDOWN ):
            move = self.move( self.UP, bloqueos )
        elif( keys[ pygame.K_DOWN ] == pygame.KEYDOWN ):
            move = self.move( self.DOWN, bloqueos )
        elif( keys[ pygame.K_LEFT ] == pygame.KEYDOWN ):
            move = self.move( self.LEFT, bloqueos )
        elif( keys[ pygame.K_RIGHT ] == pygame.KEYDOWN ):
            move = self.move( self.RIGHT, bloqueos )
        if( move ):
            self.nextFrame( lastCall )
        else:
            if( self.move( self.heading, bloqueos ) ):
                self.nextFrame( lastCall )
            else:
                self.setHeading( self.heading )
