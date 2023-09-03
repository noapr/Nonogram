from random import random, randint, uniform

from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QWidget


class FireworksWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.particles = []

    def start_animation(self):
        self.timer = self.startTimer(50)  # Timer to update the animation

    def timerEvent(self, event):
        self.create_particle()

        # Update and animate particles
        for particle in self.particles:
            particle.update()

        # Remove expired particles
        self.particles = [particle for particle in self.particles if not particle.is_expired()]

        self.update()  # Trigger a repaint

    def create_particle(self):
        x = randint(0, self.width())
        y = self.height()
        particle = Particle(x, y)
        self.particles.append(particle)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(self.rect())

        for particle in self.particles:
            particle.draw(painter)


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = randint(5, 15)
        self.color = QColor(randint(0, 255), randint(0, 255), randint(0, 255))
        self.speed = randint(2, 5)
        self.angle = uniform(0, 2 * 3.141592)

    def update(self):
        self.x += self.speed * 0.5 * 0.5 * 0.5
        self.y -= self.speed * 0.5 * 0.5 * 0.5
        self.speed -= 0.1

    def draw(self, painter):
        painter.setBrush(self.color)
        painter.drawEllipse(int(self.x), int(self.y), int(self.radius), int(self.radius))

    def is_expired(self):
        return self.radius <= 0
