"""maze_pillow.py - a maze drawing module
Copyright 2022 by Eric Conrad

DESCRIPTION

    This is a filter for maze sketching using PIL.

IMPLEMENTS

    class MazeSketcher

REFERENCES

    [1] Jamis Buck.  Mazes for programmers.  2015, the Pragmatic
        Bookshelf.  ISBN-13: 978-1-68050-055-4.

LICENSE

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see
        <https://www.gnu.org/licenses/>.
"""
from math import sqrt, ceil, sin, cos, pi
from PIL import Image, ImageFont, ImageDraw

class MazeSketcher(object):
    """MazeSketcher - control for sketching a maze using PIL"""

    def __init__(self, maze, *args, **kwargs):
        """constructor"""
        self.maze = maze
        self.args = args
        self.kwargs = kwargs
        self.img = None
        self.settings = {}
        maze.sketcher = self

    def open(self, width=800, height=600, margins=[20,10,10,10],
             **gobblekwargs):
        """start a sketch

        The margins, in order, are [top, bottom, left, right].

        Saved in settings:
            width, height, margins
        """
        self.settings['width'] = width        # excluding margins
        self.settings['height'] = height
        margins = [margins] * 4 if isinstance(margins, int) \
            else list(margins)
        top, bottom, left, right = self.settings['margins'] = margins
        canvasHeight = height + top + bottom
        canvasWidth = width + left + right
        self.img = Image.new("RGB", (canvasWidth, canvasHeight))

        self.canvas = img1 = ImageDraw.Draw(self.img)
        shape = [(0, 0), (canvasWidth, canvasHeight)]
        img1.rectangle(shape, fill="white", outline="yellow")
        shape = [(left, top), (left+width, top+height)]
        img1.rectangle(shape, fill="lightslategray", outline="black")

        title = self.kwargs.get('title')
        if title:
            self.entitle(title)

    def entitle(self, text, fontname="arial", fontsize=16):
        """put a title in the top margin"""
        fontinfo = ImageFont.truetype(fontname + ".ttf", fontsize)
        self.canvas.text((20,0), text, (0,0,0), font=fontinfo)

    def _transform(self, x, y):
        """transform (x,y) coordinates"""
        # width = self.settings['width']
        height = self.settings['height']
        # top, bottom, left, right = self.settings['margins']
        top = self.settings['margins'][0]
        left = self.settings['margins'][2]

        u = left + x
        v = top + (height - y)
        return (u, v)

    def draw_polygon(self, vertices, color):
        """draw a filled polygon"""
        polygon = []
        for vertex in vertices:
            vx, vy = vertex           # unpack
            vt = self._transform(vx, vy)
            polygon.append(vt)
        self.canvas.polygon(polygon, fill=color, outline=color)

    def draw_line_segments(self, segments, fill=None):
        """draw a collection of line segments"""
        for segment in segments:
            source, sink = segment    # unpack endpoints
            self.draw_line_segment(source, sink, fill=fill)

    def draw_line_segment(self, source, sink, fill=None,
                          thickness=None):
        """draw a single line segment"""
        (x1, y1), (x2, y2) = source, sink   # unpack endpoints
        u1, v1 = self._transform(x1, y1)
        u2, v2 = self._transform(x2, y2)
        if not thickness:
            thickness = 0
        if not fill:
            fill = 'black'
        self.canvas.line([(u1, v1), (u2, v2)], fill=fill,
                         width=thickness)

    def draw_ellipse(self, diagonal, outline="black", fill="white"):
        """draw an ellipse with axes parallel to the coordinate axes

        The PIL ellipse method only draws ellipses with axes parallel
        to coordinate axes.
        """
        (x1, y1), (x2, y2) = diagonal       # unpack endpoints
        u1, v1 = self._transform(x1, y1)
        u2, v2 = self._transform(x2, y2)
        xy = ((u1, v1), (u2, v2))
        self.canvas.ellipse(xy, fill=fill, outline=outline, width=1)

    def draw_circle(self, center, r, outline="black", fill="white"):
        """draw a circle

        PIL seems to prefer piecharts and ellipses with axes parallel
        to the coordinate axes.  When in Rome...
        """
        (x, y) = center
        diagonal = ((x-r, y+r), (x+r, y-r))
        self.draw_ellipse(diagonal, outline=outline, fill=fill)

    def draw_segment(self, center, r1, r2, theta1, theta2,
                          fill="white", outline=None):
        """draw an annular segment

        r1 > r2

        thetas in revolutions (pi/2 = 90 degrees = 1/4 rev)

        PIL seems to prefer piecharts and ellipses with axes parallel
        to the coordinate axes.  When in Rome...
        """
        (x, y) = center
        assert r1>r2
        diagonal1 = ((x-r1, y+r1), (x+r1, y-r1))
        diagonal2 = ((x-r2, y+r2), (x+r2, y-r2))

        (x11, y11), (x12, y12) = diagonal1        # unpack endpoints
        u11, v11 = self._transform(x11, y11)
        u12, v12 = self._transform(x12, y12)
        xy1 = (u11, v11, u12, v12)                # outer diagonal
        # self.canvas.arc(xy1, 0, 360, fill="grey", width=4)

        (x21, y21), (x22, y22) = diagonal2        # unpack endpoints
        u21, v21 = self._transform(x21, y21)
        u22, v22 = self._transform(x22, y22)
        xy2 = (u21, v21, u22, v22)                # inner diagonal
        # self.canvas.arc(xy2, 0, 360, fill="green", width=4)

        width = ceil(max(u21-u11, v21-v11))

        if outline and outline != fill:
            self.canvas.arc(xy1, theta1*360, theta2*360,
                            fill=outline, width=2)
            u11 += 1
            v11 += 1
            u12 -= 1
            v12 -= 1
            xy1 = (u11, v11, u12, v12)                # outer diagonal
            self.canvas.arc(xy1, theta1*360, theta2*360,
                            fill=fill, width=width-1)
            u11 += width-1
            v11 += width-1
            u12 -= width-1
            v12 -= width-1
            xy1 = (u11, v11, u12, v12)                # outer diagonal
            self.canvas.arc(xy1, theta1*360, theta2*360,
                            fill=outline, width=1)

            x3 = x + r1 * cos(theta1*2*pi)
            y3 = y - r1 * sin(theta1*2*pi)

            x4 = x + r2 * cos(theta1*2*pi)
            y4 = y - r2 * sin(theta1*2*pi)
            self.draw_line_segment((x3,y3), (x4,y4), fill=outline,
                                   thickness=1)

            x3 = x + r1 * cos(theta2*2*pi)
            y3 = y - r1 * sin(theta2*2*pi)

            x4 = x + r2 * cos(theta2*2*pi)
            y4 = y - r2 * sin(theta2*2*pi)
            self.draw_line_segment((x3,y3), (x4,y4), fill=outline,
                                   thickness=1)
        else:
            self.canvas.arc(xy1, theta1*360, theta2*360, fill=fill,
                            width=width)

    def draw_text(self, location, text, fontname="arial", fontsize=16):
        """draw a collection of line segments"""
        x, y = location           # unpack point
        u, v = self._transform(x, y)
        fontinfo = ImageFont.truetype(fontname + ".ttf", fontsize)
        self.canvas.text((u,v), text, (0,0,0), font=fontinfo)

    def close(self, filename=None, show=True, **gobblekwargs):
        """complete a sketch"""
        if filename:
            self.img.save(filename)
        if show:
            self.img.show()
        self.img = None

# end of maze_pillow.py
