#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Juego simple tipo PacMan.


http://opengameart.org/content/alternate-lpc-character-sprites-george


"""

import pygame
import pytmx
from pytmx.util_pygame import load_pygame

from Hero import Hero
from Enemy import Enemy

class Game():
    def __init__( self ):
        pygame.init()
        pygame.key.set_repeat( 5, 5 )
        self.screenSize = ( 608, 608 )
        self.screen = pygame.display.set_mode( self.screenSize )
        self.camera = pygame.Rect( ( 0, 0 ), self.screenSize )
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.done = False
        self.fontMonoSpace = pygame.font.SysFont( 'monospace', 14 )

        self.world = load_pygame( 'maps/Mapa.tmx' )
        self.worldSize = ( self.world.width * self.world.tilewidth, self.world.height * self.world.tileheight )

        self.bloqueos = []
        muros = self.world.get_layer_by_name( 'Muros' )
        for x, y, image in muros.tiles():
            r = image.get_rect()
            r.x = x * self.world.tilewidth
            r.y = y * self.world.tileheight
            self.bloqueos.append( r )

        self.premios = []
        premios = self.world.get_layer_by_name( 'Premios' )
        for premio in premios:
            self.premios.append( premio )

        self.hero = Hero( 32*9, 32*6, 32, 32, 'images/George.png' )
        self.ghost1 = Enemy( 32*7, 32*10, 32, 32, 'images/Ghost.png' )
        self.ghost2 = Enemy( 32*9, 32*11, 32, 32, 'images/Ghost.png'  )
        self.ghost3 = Enemy( 32*11, 32*10, 32, 32, 'images/Ghost.png'  )
        self.sprites = [ self.hero, self.ghost1, self.ghost2, self.ghost3 ]

    def events( self ):
        self.keys = [ 0 ] * 350
        for event in pygame.event.get():
            if( event.type == pygame.QUIT ):
                self.done = True
            elif( event.type == pygame.KEYDOWN ):
                self.keys[ event.key ] = pygame.KEYDOWN
            elif( event.type == pygame.KEYUP ):
                self.keys[ event.key ] = pygame.KEYUP
        if( self.keys[ pygame.K_ESCAPE ] == pygame.KEYDOWN ):
            self.done = True

    def update( self, lastCall ):
        for sprite in self.sprites:
            sprite.update( self.keys, self.bloqueos, self.hero.getRect(), lastCall )
            r = sprite.getRect()
            if( r.x + r.width - 8 < 0 ):
                sprite.setPos( self.screenSize[1] - 8, r.y, sprite.LEFT )
            elif( r.x + 8 > self.screenSize[1] ):
                sprite.setPos( 0, r.y, sprite.RIGHT )

        hr = self.hero.getRect()
        hr.x = hr.x + 8
        hr.y = hr.y + 8
        hr.width = hr.width -16
        hr.height = hr.height -16
        killed = False
        for sprite in self.sprites:
            if( sprite != self.hero and hr.colliderect( sprite.getRect() ) ):
                killed = True
                break
        if( killed ):
            self.done = True

        for premio in self.premios:
            pr = premio.image.get_rect()
            pr.x = premio.x
            pr.y = premio.y
            if( hr.colliderect( pr ) ):
                self.premios.remove( premio )
                break

    def updateCamera( self ):
        r = self.hero.getRect()
        x = r.x + r.width/2 - self.screenSize[ 0 ]/2
        if( x < 0 ):
            x = 0
        else:
            xx = self.worldSize[ 0 ] - self.screenSize[ 0 ]
            if( x > xx ):
                x = xx
        self.camera.x = x
        y = r.y + r.height/2 - self.screenSize[ 1 ] /2
        if( y < 0 ):
            y = 0
        else:
            yy = self.worldSize[ 1 ] - self.screenSize[ 01]
            if( y > yy ):
                y = yy
        self.camera.y = y

    def render( self ):
        self.updateCamera()
        self.screen.fill( ( 0, 0, 0 ) )
        for layer in self.world.visible_layers:
            if( isinstance( layer, pytmx.TiledTileLayer ) ):
                for x, y, image in layer.tiles():
                    r = image.get_rect()
                    r.x = x * self.world.tilewidth
                    r.y = y * self.world.tileheight
                    if( self.camera.colliderect( r ) ):
                        self.screen.blit( image, ( r.x - self.camera.x, r.y - self.camera.y ) )

        for premio in self.premios:
            r = premio.image.get_rect()
            r.x = premio.x
            r.y = premio.y
            if( self.camera.colliderect( r ) ):
                self.screen.blit( premio.image, ( r.x - self.camera.x, r.y - self.camera.y ) )

        for sprite in self.sprites:
            r = sprite.getRect()
            self.screen.blit( sprite.getImage(), ( r.x, r.y ) )

    def flip( self ):
        fps = self.clock.get_fps()
        if( fps == 0 ):
            fps = 1
        t = 1000./fps
        msg = 'Esperado: %04.1f FPS, Real: %04.1f FPS %04.1f ms' % ( self.fps, fps, t )
        txt = self.fontMonoSpace.render( msg, 10, ( 0, 0, 0 ) )
        self.screen.blit( txt, ( 0, self.screenSize[1] - 20 ) )
        pygame.display.flip()

    def run(self):
        lastCall = 0
        while not self.done:
            self.events()
            self.update( lastCall )
            self.render()
            self.flip()
            lastCall = self.clock.tick( self.fps )

###
if( __name__ == '__main__' ):
    myGame = Game()
    myGame.run()
