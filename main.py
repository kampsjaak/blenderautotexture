import bpy, math
import mathutils

def RotateCamera(area_index):
    rv3d = bpy.context.screen.areas[area_index].spaces[0].region_3d
    rv3d.view_rotation.rotate(mathutils.Euler((0, 0, 0.1)))
    rv3d.view_location.x += 1.0
    rv3d.view_distance -= 1.0

def GetFaces():
    for obj in bpy.data.objects:
        if type(obj.data) != bpy.types.Mesh:
            continue
        for poly in obj.data.polygons:
            if(len(poly.vertices) == 4):
                # Quad information
                tile = 1
                longEdge = GetLongestEdgeLength(obj.data, poly.vertices)
                shortEdge = GetShortestEdgeLength(obj.data, poly.vertices)
                ratio = longEdge / shortEdge
                tiles = poly.area / tile
                facing = GetFacing(poly.normal)
                print("facing {}, local space {}".format(facing, poly.center))
                print("long {:.2f}, short {:.2f}".format(longEdge, shortEdge))
                print("area {:.2f}, tiles {:.2f}, ratio {:.2f}".format(poly.area, ratio, tiles))

def GetFacing(vec3):
    if (abs(vec3.x) > abs(vec3.y) and abs(vec3.x) > abs(vec3.z)):
        if (vec3.x < 0):
            return "backward"
        else:
            return "forward"
    if (abs(vec3.y) > abs(vec3.x) and abs(vec3.y) > abs(vec3.z)):
        if (vec3.y < 0):
            return "right"
        else:
            return "left"
    if (abs(vec3.z) > abs(vec3.x) and abs(vec3.z) > abs(vec3.y)):
        if (vec3.z < 0):
            return "down"
        else:
            return "up"

def GetEdgeForVerts(edges, p, q):
    # p and q are vertex indicies int 
    for edge in edges:
        if((edge.vertices[0] == p and edge.vertices[1] == q) or (edge.vertices[0] == q and edge.vertices[1] == p)):
            return edge
    return None

def GetLongestEdgeLength(data, indices):
    if(len(data.vertices) <= 1):
        return None
    
    hypotenuse = -1
    dist = hypotenuse
    
    for x in range(0, len(indices)-1):
        edge = GetEdgeForVerts(data.edges, indices[x], indices[x+1])
        if (edge == None):
            continue
        
        hypotenuse = Distance(data.vertices[indices[x]].co, data.vertices[indices[x+1]].co)
        if(hypotenuse > dist):
            dist = hypotenuse
    return dist

def GetShortestEdgeLength(data, indices):
    if(len(data.vertices) <= 1):
        return None
    
    hypotenuse = 9999999999
    dist = hypotenuse
    
    for x in range(0, len(indices)-1):
        edge = GetEdgeForVerts(data.edges, indices[x], indices[x+1])
        if (edge == None):
            continue
        
        hypotenuse = Distance(data.vertices[indices[x]].co, data.vertices[indices[x+1]].co)
        if(hypotenuse < dist):
            dist = hypotenuse
    return dist

def Distance(p, q):
    s_sq_difference = 0
    for p_i,q_i in zip(p,q):
        s_sq_difference += (p_i - q_i)**2
    
    distance = s_sq_difference**0.5
    return distance

GetFaces()
RotateCamera(5)