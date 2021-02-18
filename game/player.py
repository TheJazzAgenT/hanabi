#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Player:
    def __init__(self, id, game, hand):
        self.id = id
        self.game = game
        self.hand = hand

    def __eq__(self, other):
        return self.id == other.id
