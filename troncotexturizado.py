from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import png
import math

ESCAPE = '\033'

window = 0

a = 0

# VARIAVEIS DE ROTACAO
left_button = False
alpha = 90.0
beta = 0
delta_alpha = 0.5

# VARIAVEIS DE TRANSLACAO
right_button = False
delta_x, delta_y, delta_z = 0, 0, 0

down_x, down_y = 0, 0

# BACKGROUND
background_color = (0.0, 0.0, 0.0, 1)

# VARIAVEIS DA FIGURA
vertices = 4
radius = 2
prism_height = 3
piramid_modifier = 0.5

texture = []

# TEXTURE
texture = []
def LoadTextures():
    global texture
    texture = glGenTextures(2) # GERA 2 IDS PARA AS TEXTURAS

    #######################################################################################
    reader = png.Reader(filename='C:\\Users\\user\\Desktop\\computação grafica\\textura.png')
    w, h, pixels, metadata = reader.read_flat()

    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB

    glBindTexture(GL_TEXTURE_2D, texture[0])
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    #######################################################################################

def troncoDePiramide():
    pontosBase = []
    angulo = (2*math.pi)/vertices

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    glTranslatef(0.0, 1.5, -15)
    glRotatef(90,1.0,0.0,0.0)
    glRotatef(20,1.0,0.0,0.0)
    glTranslatef(delta_x, delta_y, delta_z)
    glRotatef(alpha, 0.0, 0.5, 1.0)

    glBindTexture(GL_TEXTURE_2D, texture[0])

    # BASES
    glBegin(GL_POLYGON)
    for i in range(vertices):
        x = radius * math.cos(i*angulo)
        y = radius * math.sin(i*angulo)
        pontosBase += [ (x,y) ]
        glTexCoord2f(x, y); glVertex3f(x,y,0.0)
    glEnd()


    glBegin(GL_POLYGON)
    for x,y in pontosBase:
        glTexCoord2f(x, y); glVertex3f(piramid_modifier*x,piramid_modifier*y, prism_height)
    glEnd()

    # LATERAL
    glBegin(GL_QUADS)
    for i in range(vertices):
        glTexCoord2f(0.0, 0.0); glVertex3f(pontosBase[i][0],pontosBase[i][1],0)
        glTexCoord2f(0.0, 1.0); glVertex3f(piramid_modifier*pontosBase[i][0],piramid_modifier*pontosBase[i][1],prism_height)

        glTexCoord2f(1.0, 1.0); glVertex3f(piramid_modifier*pontosBase[(i+1)%vertices][0],piramid_modifier*pontosBase[(i+1)%vertices][1],prism_height)
        glTexCoord2f(1.0, 0.0); glVertex3f(pontosBase[(i+1)%vertices][0],pontosBase[(i+1)%vertices][1],0)
    glEnd()

    glPopMatrix()

    glutSwapBuffers()

def desenha():
    global alpha, left_button, right_button
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    troncoDePiramide()

    alpha+=delta_alpha
  
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(15,timer,1)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
 
    screen_width = glutGet(GLUT_SCREEN_WIDTH)
    screen_height = glutGet(GLUT_SCREEN_HEIGHT)

    window_width = round(2 * screen_width / 3)
    window_height = round(2 * screen_height / 3)

    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(round((screen_width - window_width) / 2), round((screen_height - window_height) / 2))
    glutCreateWindow("Tronco Textura de Pedra")
    glutDisplayFunc(desenha)
    LoadTextures()
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(*background_color)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(-15,window_width/window_height,0.1,100.0)
    glTranslatef(0.0,0.0,-10)
    glutTimerFunc(50,timer,1)
    glMatrixMode(GL_MODELVIEW)
    glutMainLoop()

main()