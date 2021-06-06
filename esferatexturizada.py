import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from png import Reader
from sys import argv
from math import sin, cos, pi

ESCAPE = '\033'

window = 0

# VARIAVEIS DE ROTACAO
left_button = False
alpha = 90.0
beta = 0
delta_alpha = 0.5

# VARIAVEIS DE TRANSLACAO
right_button = False
delta_x, delta_y, delta_z = 0, 0, 0
down_x, down_y = 0, 0

# FIGURA
n = 50
m = 50
radius = 2

def f(i,j):
    theta = ((pi*i) / (n-1)) - (pi/2)
    phi = 2*pi*j/(m-1)
    
    x = radius * cos(theta) * cos(phi)
    y = radius * sin(theta)
    z = radius * cos(theta) * sin(phi)
    s = s_function(phi)
    t = t_function(theta)
    
    return x,y,z,s,t

def s_function(phi):
    return (phi/(2*pi))

def t_function(theta):
    return ((theta + (pi/2))/pi)


# TEXTURE
texture = []

def LoadTextures():
    global texture
    texture = GL.glGenTextures(2)

    ###############################################################################################
    reader = Reader(filename='C:\\Users\\user\\Desktop\\computação grafica\\mapa.png')
    w, h, pixels, metadata = reader.read_flat()

    if(metadata['alpha']):
        modo = GL.GL_RGBA
    else:
        modo = GL.GL_RGB

    GL.glBindTexture(GL.GL_TEXTURE_2D, texture[0])
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL.GL_UNSIGNED_BYTE, pixels.tolist())
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    GL.glTexEnvf(GL.GL_TEXTURE_ENV, GL.GL_TEXTURE_ENV_MODE, GL.GL_DECAL)
    ###############################################################################################

def figure():
    
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)    
    GL.glLoadIdentity()
    GL.glPushMatrix()
    GL.glTranslatef(delta_x, delta_y, delta_z)
    GL.glRotatef(alpha, 0.0, 1.0, 0.0)
    GL.glRotatef(beta, 0.0, 0.0, 1.0)

    GL.glBindTexture(GL.GL_TEXTURE_2D, texture[0])
    for i in range(n):
        GL.glBegin(GL.GL_QUAD_STRIP)
        for j in range(m):
            
            x, y, z, s, t = f(i,j)
            GL.glTexCoord2f(s, t)
            GL.glVertex3f(x,y,z)

            x, y, z, s, t = f(i+1, j)
            GL.glTexCoord2f(s, t)
            GL.glVertex3f(x,y,z)
        GL.glEnd()

    GL.glPopMatrix()

def draw():
    global alpha, left_button, right_button
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    figure()
    alpha = alpha + delta_alpha

    GLUT.glutSwapBuffers()

def timer(i):
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(10, timer, 1)

def key_pressed(key, x, y):
    global delta_alpha

    if key == b'\x1b':
        GLUT.glutLeaveMainLoop()
    elif key == b" ":
        if delta_alpha == 0:
            delta_alpha = 0.5
        else:
            delta_alpha = 0

def mouse_click(button, state, x, y):
    global down_x, down_y, left_button, right_button, delta_z

    down_x, down_y = x, y

    left_button = button == GLUT.GLUT_LEFT_BUTTON and state == GLUT.GLUT_DOWN
    right_button = button == GLUT.GLUT_RIGHT_BUTTON and state == GLUT.GLUT_DOWN

    # ZOOM
    if button == 3 and state == GLUT.GLUT_DOWN:
        delta_z += 1
    elif button == 4 and state == GLUT.GLUT_DOWN:
        delta_z -= 1


def mouse_move(x, y):
    global alpha, beta, down_x, down_y, delta_x, delta_y, delta_alpha

    # ROTACAO
    if left_button:
        delta_alpha = 0

        alpha += ((x - down_x) / 4.0) * -1

        if alpha >= 360:
            alpha -= 360

        if alpha <= 0:
            alpha += 360

        if alpha >= 180:
            beta -= (y - down_y) / 4.0 * -1
        else:
            beta += (y - down_y) / 4.0 * -1

        if beta >= 360:
            beta -= 360

        if beta <= 0:
            beta += 360

    # TRANSLACAO
    if right_button:
        delta_x += -1 * (x - down_x) / 100.0
        delta_y += (y - down_y) / 100.0

    down_x, down_y = x, y

    GLUT.glutPostRedisplay()

def main():    
    GLUT.glutInit(argv)
    GLUT.glutInitDisplayMode(
        GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH | GLUT.GLUT_MULTISAMPLE
    )

    screen_width = GLUT.glutGet(GLUT.GLUT_SCREEN_WIDTH)
    screen_height = GLUT.glutGet(GLUT.GLUT_SCREEN_HEIGHT)

    window_width = round(2 * screen_width / 3)
    window_height = round(2 * screen_height / 3)

    GLUT.glutInitWindowSize(window_width, window_height)
    GLUT.glutInitWindowPosition(
        round((screen_width - window_width) / 2), round((screen_height - window_height) / 2)
    )
    GLUT.glutCreateWindow("Textura Esfera  Globo")

    GLUT.glutDisplayFunc(draw)
    GLUT.glutKeyboardFunc(key_pressed)
    GLUT.glutMouseFunc(mouse_click)
    GLUT.glutMotionFunc(mouse_move)

    LoadTextures()

    GL.glEnable(GL.GL_MULTISAMPLE)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_TEXTURE_2D)

    GL.glClearColor(0.0, 0.0, 0.0, 1)
    GL.glClearDepth(1.0)
    GL.glDepthFunc(GL.GL_LESS)

    GL.glShadeModel(GL.GL_SMOOTH)
    GL.glMatrixMode(GL.GL_PROJECTION)

    # POSICAO DA CAMERA
    GLU.gluPerspective(-45, window_width / window_height, 0.1, 100.0)
    GL.glTranslatef(0.0, 0.0, -10)

    GL.glMatrixMode(GL.GL_MODELVIEW)

    GLUT.glutTimerFunc(10, timer, 1)
    GLUT.glutMainLoop()


if(__name__ == '__main__'):
    main()