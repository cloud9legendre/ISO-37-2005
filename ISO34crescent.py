import cadquery as cq
from math import sqrt
import numpy as np
import math
import sympy as sp

def circle_intersections(c1, r1, c2, r2):
    x1, y1 = c1
    x2, y2 = c2
    d = sp.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    a = (r1**2 - r2**2 + d**2)/(2*d)
    h = sp.sqrt(r1**2 - a**2)
    x3 = x1 + a*(x2 - x1)/d
    y3 = y1 + a*(y2 - y1)/d
    rx =  h*(y1 - y2)/d
    ry =  h*(x2 - x1)/d
    p1 = (sp.simplify(x3 + rx), sp.simplify(y3 + ry))
    p2 = (sp.simplify(x3 - rx), sp.simplify(y3 - ry))
    return [p1, p2]

def tangents_to_circle(c, r, p):
    x0, y0 = c
    x3, y3 = p
    x, y = sp.symbols('x y', real=True)
    eq1 = sp.Eq((x - x0)**2 + (y - y0)**2, r**2)
    eq2 = sp.Eq((x - x0)*(x3 - x) + (y - y0)*(y3 - y), 0)
    return sp.solve([eq1, eq2], [x, y])

def internal_tangent_points(c1, r1, c2, r2):
    x1, y1 = c1
    x2, y2 = c2
    dx = x2 - x1
    dy = y2 - y1
    d = sp.sqrt(dx**2 + dy**2)
    k = (r1 + r2)/d
    if sp.Abs(k) > 1:
        return []
    alpha = sp.acos(k)
    theta = sp.atan2(dy, dx)
    pts = []
    for s in (1, -1):
        ang = theta + s*alpha
        x_t1 = x1 + r1*sp.cos(ang)
        y_t1 = y1 + r1*sp.sin(ang)
        x_t2 = x2 - r2*sp.cos(ang)
        y_t2 = y2 - r2*sp.sin(ang)
        pts.append(((sp.simplify(x_t1), sp.simplify(y_t1)),
                    (sp.simplify(x_t2), sp.simplify(y_t2))))
    return pts

def create_iso34_crescent():
    # PARAMETERS (m)
    h_A = 25e-3
    h_B = 10.5e-3
    l_A = 110e-3
    l_B = 68e-3
    l_C = 45e-3
    r_A = 9.0e-3
    r_B = 43e-3
    r_C = 12.5e-3
    r_D = 7.5e-3
    
    Ca = [-l_C/2,(h_A/2)-r_A]
    Cb = [0,r_B-h_B]
    Cc = [0,r_C]
    Cd = [-l_C/2,-h_A/2]
    
    c1 = (Ca[0], Ca[1])
    r1 = r_A
    c2 = (Cc[0], Cc[1])
    r2 = r_C
    pts = internal_tangent_points(c1, r1, c2, r2)
    t1 = pts[0]
    t2 = pts[1]
    
    c3 = (Cd[0],Cd[1])
    r3 = r_D
    p3 = (-l_B/2,-h_A/2)
    tang1,tang2 = tangents_to_circle(c3, r3, p3)
    
    c4 = (Cb[0],Cb[1])
    r4 = r_B
    p4,p5 = circle_intersections(c3, r3, c4, r4)
    # Construct profile clockwise
    prof = (
        cq.Workplane("XY")
        .moveTo(-l_A/2,0)#(-55,0)
        .lineTo(-l_A/2,h_A/2)#(-55,12.5)
        .lineTo(-l_C/2,h_A/2)#(-32.5,12.5)
        .moveTo(Ca[0],Ca[1])
        .circle(r_A, forConstruction=True)
        .moveTo(Cc[0],Cc[1])
        .circle(r_C, forConstruction=True)
        .moveTo(t1[0][0],t1[0][1])
        .lineTo(t1[1][0],t1[1][1])
        .moveTo(-l_C/2,h_A/2)
        .radiusArc((t1[0][0],t1[0][1]),r_A)
        .moveTo(t1[1][0],t1[1][1])
        .radiusArc((0,0),-r_C)
        .moveTo(-l_A/2,0)
        .lineTo(-l_A/2,-h_A/2)
        .lineTo(-l_B/2,-h_A/2)
        .moveTo(Cb[0],Cb[1])
        .circle(r_B,forConstruction=True)
        .moveTo(Cd[0],Cd[1])
        .circle(r_D,forConstruction=True)
        .moveTo(-l_B/2,-h_A/2)
        .lineTo(tang2[0],tang2[1])
        .moveTo(p4[0],p4[1])
        .lineTo(p5[0],p5[1])
        .moveTo(tang2[0],tang2[1])
        .radiusArc(p4,r_D)
        .moveTo(p5[0],p5[1])
        .radiusArc((0,-h_B),-r_B)
        .mirrorY()
        .extrude(2e-3)
        )
    nick = (
        cq.Workplane("XY")
        .rect(1.0e-3,2e-3)
        .extrude(2.1e-3)
        )
    result = prof.cut(nick)

    # Extrude to thickness
    return result#.extrude(thickness)

# Generate and export STL
result = create_iso34_crescent()
show_object(result)