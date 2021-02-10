

class cMath:
    def __init__(self):
        pass
    
    def Sin(self, xInput):
        xInput *= (-1) ** round(xInput / 3.14)
        
        xInput = (xInput - 1.57) % 3.14 - 1.57
        return xInput - (xInput * xInput * xInput / 6) + (xInput * xInput * xInput * xInput * xInput / 120)


    def MatrixMul(self, xMatrix1, xMatrix2):
        xOutput = []
        
        for yI in range(len(xMatrix1)):
            xBuffer = 0
        
            for xI in range(len(xMatrix1[yI])):
                xBuffer += xMatrix1[yI][xI] * xMatrix2[xI]
                
            xOutput.append(xBuffer)
            
        return xOutput
        
class cRender:
    def __init__(self):
        self.cMath = cMath()
        
        self.xAngle = 0

    def ClacRotation(self, xAngle, xPointBuffer):
        xOutput = [None for x in range(len(xPointBuffer))]
        
        xRotationMatrixY = [
                [self.cMath.Sin(self.xAngle + 1.57), 0, self.cMath.Sin(self.xAngle)],
                [0, 1, 0],
                [-self.cMath.Sin(self.xAngle), 0, self.cMath.Sin(self.xAngle + 1.57)]
            ]

        xRotationMatrixX = [
                [1, 0, 0],
                [0, self.cMath.Sin(self.xAngle + 1.57), -self.cMath.Sin(self.xAngle)],
                [0, self.cMath.Sin(self.xAngle), self.cMath.Sin(self.xAngle + 1.57)]
            ]

        xRotationMatrixZ = [
                [self.cMath.Sin(self.xAngle + 1.57), -self.cMath.Sin(self.xAngle), 0],
                [self.cMath.Sin(self.xAngle), self.cMath.Sin(self.xAngle + 1.57), 0],
                [0, 0, 1]
            ]
        
        for xI in range(len(xPointBuffer)):
            xOutput[xI] =   self.cMath.MatrixMul(xRotationMatrixX,
                            self.cMath.MatrixMul(xRotationMatrixY,
                            self.cMath.MatrixMul(xRotationMatrixZ, xPointBuffer[xI])))

        return xOutput



    def Perspectiv(self, xPointBuffer):
        for xI in range(len(xPointBuffer)):
            xPointBuffer[xI][0] = xPointBuffer[xI][0] / (xPointBuffer[xI][2] / 10 + 1)
            xPointBuffer[xI][1] = xPointBuffer[xI][1] / (xPointBuffer[xI][2] / 10 + 1)
        
        return xPointBuffer
        
    def Projekt(self, xPointBuffer):
        xProjectionMatrix = [
                [0, 1, 0],
                [1, 0, 0]
            ]
        
        return [self.cMath.MatrixMul(xProjectionMatrix, xI) for xI in xPointBuffer]
    
    def Scale(self, xPointBuffer):
        for xI in range(len(xPointBuffer)):
            xPointBuffer[xI][0] = int(xPointBuffer[xI][0] * 10)
            xPointBuffer[xI][1] = int(xPointBuffer[xI][1] * 10)
        
        return xPointBuffer
        
    def Render(self, xPointBuffer):
        return self.Scale(self.Projekt(self.Perspectiv(self.ClacRotation(self.xAngle, xPointBuffer))))
        
        
        
        
        
class cMain:
    def __init__(self):
        self.cR = cRender()
    
    
    
    def PrintMatrix(self, xPointBuffer):
        xFrameBuffer = [[" " for i in range(50)] for y in range(50)]
        
        for yI in range(len(xFrameBuffer)):
            for xI in range(len(xFrameBuffer[yI])):
                if [yI - len(xFrameBuffer) // 2, xI - len(xFrameBuffer[yI]) // 2] in xPointBuffer:
                    xFrameBuffer[yI][xI] = "#"
        
        print("\n".join(["".join(x) for x in xFrameBuffer]))
        
        
    def Main(self):
        xPointBuffer = [
                [-1, -1, -1],
                [1, -1, -1],
                [-1, 1, -1],
                [1, 1, -1],
                [-1, -1, 1],
                [1, -1, 1],
                [-1, 1, 1],
                [1, 1, 1]
            ]
        
        while True:
            self.PrintMatrix((self.cR.Render(xPointBuffer)))
            
        
            #tune these parameters so it works for you
            self.cR.xAngle += 0.01 #increase rotation angle
            for i in range(3000000): pass #wait
        
if __name__ == '__main__':
    cM = cMain()
    cM.Main()