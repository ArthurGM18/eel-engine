cdef extern from "<GL/gl.h>":
    int GL_POINTS
    int GL_LINE_LOOP
    int GL_COLOR_BUFFER_BIT
    int GL_DEPTH_BUFFER_BIT
    int GL_PROJECTION
    int GL_POLYGON
    int GL_QUADS
    int GL_TEXTURE_2D
    int GL_LINE
    int GL_BLEND
    int GL_SRC_ALPHA
    int GL_ONE_MINUS_SRC_ALPHA
    int GL_RGB
    int GL_UNSIGNED_BYTE
    int GL_TEXTURE_MAG_FILTER
    int GL_TEXTURE_MIN_FILTER
    int GL_NEAREST
    int GL_TEXTURE_WRAP_S
    int GL_TEXTURE_WRAP_T
    int GL_CLAMP_TO_EDGE