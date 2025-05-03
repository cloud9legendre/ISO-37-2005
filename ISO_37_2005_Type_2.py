import cadquery as cq
from math import sqrt

def create_iso37_type2():
    # PARAMETERS (mm)
    A, B, C, D, E, F, thickness = 75.0, 12.5, 25.0, 4.0, 8.0, 12.5, 2.0
    hA, hB, hC, hD = A / 2, B / 2, C / 2, D / 2

    # Circle centers for G1 transitions
    C1 = (-hC, hD + F)
    C2_y = hB - E
    dy = C2_y - C1[1]
    Dsum = F + E
    delta = Dsum**2 - dy**2
    if delta < 0:
        raise ValueError("Radii too large or transitions invalid")
    dx = sqrt(delta)
    C2 = (C1[0] - dx, C2_y)

    # Transition points
    t = F / Dsum
    P_gauge = (-hC, hD)
    P_tangent = (C1[0] + (C2[0] - C1[0]) * t, C1[1] + (C2[1] - C1[1]) * t)
    P_end = (C2[0], hB)

    # Mirror helpers
    def mx(pt): return (-pt[0], pt[1])
    def my(pt): return (pt[0], -pt[1])

    # Right side points
    P_gauge_R = mx(P_gauge)
    P_tangent_R = mx(P_tangent)
    P_end_R = mx(P_end)

    # Construct profile clockwise
    prof = (
        cq.Workplane("XY")
        .moveTo(-hA, hB)
        .lineTo(*P_end)
        .radiusArc(P_tangent, E)
        .radiusArc(P_gauge, -F)
        .lineTo(*P_gauge_R)
        .radiusArc(P_tangent_R, -F)
        .radiusArc(P_end_R, E)
        .lineTo(hA, hB)
        .lineTo(hA, -hB)
        .lineTo(P_end_R[0], -hB)
        .radiusArc(my(P_tangent_R), E)
        .radiusArc(my(P_gauge_R), -F)
        .lineTo(my(P_gauge)[0], -hD)
        .radiusArc(my(P_tangent), -F)
        .radiusArc(my(P_end), E)
        .lineTo(-hA, -hB)
        .close()
    )

    # Extrude to thickness
    return prof.extrude(thickness)

# Generate and export STL
result = create_iso37_type2()
cq.exporters.export(result, 'iso37_type2.stl')
