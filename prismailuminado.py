from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
from math import *
import sys

a = 0

def calculaNormalFace(v0, v1, v2):
    x = 0
    y = 1
    z = 2
    U = (v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z])
    V = (v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z])
    N = ((U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    NLength = sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return (N[x]/NLength, N[y]/NLength, N[z]/NLength)
    
def prisma():
    raio = 2
    N = 5
    H = 4
    modificador = 1
    pontosBase = []
    angulo = (2*math.pi)/N

    glPushMatrix()
    glTranslatef(0,-2,0)
    glRotatef(a,0.0,1.0,0.0)
    glRotatef(-90,1.0,0.0,0.0)

    # BASE
    glBegin(GL_POLYGON)
    for i in range(0,N):
        x = raio * math.cos(i*angulo)
        y = raio * math.sin(i*angulo)
        pontosBase += [ (x,y) ]
        glVertex3f(x,y,0.0)

    u = (pontosBase[0][0], pontosBase[0][1], 0)
    v = (pontosBase[1][0], pontosBase[1][1], 0)
    p = (pontosBase[2][0], pontosBase[2][1], 0)

    glNormal3fv(calculaNormalFace(u,v,p))
    glEnd()

    # TOPO
    glBegin(GL_POLYGON)
    for x,y in pontosBase:
        glVertex3f(modificador*x,modificador*y, H)
    
    u = (pontosBase[0][0], pontosBase[0][1], H)
    v = (pontosBase[1][0], pontosBase[1][1], H)
    p = (pontosBase[2][0], pontosBase[2][1], H)

    glNormal3fv(calculaNormalFace(u,v,p))
    glEnd()

    # LATERAL
    glBegin(GL_QUADS)
    for i in range(0,N):
        u = (pontosBase[i][0], pontosBase[i][1],0.0)
        v = (modificador*pontosBase[i][0],modificador*pontosBase[i][1],H)
        p = (modificador*pontosBase[(i+1)%N][0],modificador*pontosBase[(i+1)%N][1],H)
        q = (pontosBase[(i+1)%N][0],pontosBase[(i+1)%N][1],0.0)

        glNormal3fv(calculaNormalFace(u,v,q))

        glVertex3fv(u)
        glVertex3fv(v)
        glVertex3fv(p)
        glVertex3fv(q)
    glEnd()

    glPopMatrix()

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(15,timer,1)


def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    a+=1
    prisma()
    glutSwapBuffers()

def reshape(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,float(w)/float(h),0.1,50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(10,0,0,0,0,0,0,1,0)

def init():
    mat_ambient = (0.25, 0.148, 0.06475, 1.0)
    mat_diffuse = (0.4, 0.2368, 0.1036, 1.0)
    mat_specular = (0.774597, 0.458561, 0.200621, 1.0)
    mat_shininess = (50.8)
    light_position = (150.0, 150.0, 150.0, 1.0)
    glClearColor(0.0,0.0,0.0,0.0)
    glShadeModel(GL_SMOOTH)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

# PROGRAMA PRINCIPAL
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Prisma Iluminado")
    glutReshapeFunc(reshape)
    glutDisplayFunc(desenha)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45,800.0/600.0,0.1,100.0)
    glTranslatef(0.0,0.0,-10)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()