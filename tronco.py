from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math

a = 0

cores = ( (1,0,0),(1,1,0),(0,1,0),(0,1,1),(0,0,1),(1,0,1),(0.5,1,1),(1,0,0.5) )

def prisma():
    raio = 1.5
    R = 3
    N = 5
    H = 4
    pontosBase = []
    pontosbase2 =[]
    angulo = (2*math.pi)/N

    glPushMatrix()
    glTranslatef(0,-2,0)
    glRotatef(a,0.0,1.0,0.0)
    glRotatef(-110,1.0,0.0,0.0)
    glColor3fv(cores[0])

    # BASE
    glBegin(GL_POLYGON)
    for i in range(0,N):
        x = R * math.cos(i*angulo)
        y = R * math.sin(i*angulo)
        pontosBase += [ (x,y) ]
        glVertex3f(x,y,0.0)
    glEnd()
    glBegin(GL_POLYGON)
    for i in range(0,N):
        m = raio * math.cos(i*angulo)
        n = raio * math.sin(i*angulo)
        pontosbase2 += [ (m,n) ]
        glVertex3f(m,n,H)
    glEnd()

    # LATERAL
    glBegin(GL_QUADS)
    for i in range(0,N):
        glColor3fv(cores[(i+1)%len(cores)])
        glVertex3f(pontosBase[i][0],pontosBase[i][1],0.0)
        glVertex3f(pontosBase[(i+1)%N][0],pontosBase[(i+1)%N][1],0.0)
        #glVertex3f(pontosbase2[i][0],pontosbase2[i][1],H)
        glVertex3f(pontosbase2[(i+1)%N][0],pontosbase2[(i+1)%N][1],H)
        glVertex3f(pontosbase2[i][0],pontosbase2[i][1],H)
        
    glEnd()
    glPopMatrix()


def desenha():
    global a
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    prisma()
    a+=1
    glutSwapBuffers()
  
def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

# PROGRAMA PRINCIPAL
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
glutInitWindowSize(800,600)
glutCreateWindow("prisma")
glutDisplayFunc(desenha)
glEnable(GL_MULTISAMPLE)
glEnable(GL_DEPTH_TEST)
glClearColor(0,0,0,1)
gluPerspective(45,800.0/600.0,0.1,100.0)
glTranslatef(0.0,0.0,-10)
glutTimerFunc(5,timer,1)
glutMainLoop()