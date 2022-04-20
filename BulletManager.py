from GameUnit import Bullet
import math

class BulletManager():
    """mainRoot variable is used extraordinary - it is the same as root anywhere else"""
    def __init__(self,mainRoot):
        self.mainRoot = mainRoot

    def add_new_bullet(self, startObject, endPos):
        """Function adds new bullet widget"""
        new_Bullet = Bullet()
        new_Bullet.root = startObject
        new_Bullet.targetMatrix = endPos.matrixPosition.copy()

        startPos = startObject.matrixPosition

        new_Bullet.absoluteBulletStartX = self.mainRoot.gameMapMatrix[startPos[0]][startPos[1]][0]+new_Bullet.root.width*0.5
        new_Bullet.absoluteBulletStartY  = self.mainRoot.gameMapMatrix[startPos[0]][startPos[1]][1]+new_Bullet.root.width*0.5

        targetMatrixPos = new_Bullet.root.target.matrixPosition

        new_Bullet.absoluteTargetX = self.mainRoot.gameMapMatrix[targetMatrixPos[0]][targetMatrixPos[1]][0]
        new_Bullet.absoluteTargetY = self.mainRoot.gameMapMatrix[targetMatrixPos[0]][targetMatrixPos[1]][1]
        new_Bullet.distanceToFly = startObject.shotDistance
        new_Bullet.pos   = [startObject.pos[0]+new_Bullet.root.width*0.5,startObject.pos[1]+new_Bullet.root.width*0.5]
        new_Bullet.id = f"Bullet{self.mainRoot.obj_add_index}"
        new_Bullet.size_hint = (None, None)
        new_Bullet.target = endPos
        new_Bullet.size = (20, 20)
        new_Bullet.selected = False
        new_Bullet.set_image()
        self.mainRoot.bullets.append(new_Bullet)
        self.mainRoot.add_widget(new_Bullet,index=self.mainRoot.ids["SidePanelWidget"].index+1,canvas="after")
        self.mainRoot.obj_add_index += 1
        self.mainRoot.ids["SidePanelWidget"].index = 0

    def bullet_move(self):
        for bullet in self.mainRoot.bullets:
            bulletRootPos = bullet.root.matrixPosition

            if bullet.target == None:
                self.mainRoot.bullets.remove(bullet)
                self.mainRoot.remove_widget(bullet)
                continue
            elif bullet.target.health <= 0:
                self.mainRoot.bullets.remove(bullet)
                self.mainRoot.remove_widget(bullet)
                continue
            distance = math.dist(bullet.root.pos,bullet.target.pos)
            x = abs(bullet.absoluteBulletStartX-bullet.absoluteTargetX)/60
            y = abs(bullet.absoluteBulletStartY-bullet.absoluteTargetY)/60

            if bullet.target.health <= 0 or bullet.target == None or bullet.target == []:
                self.mainRoot.bullets.remove(bullet)
                self.mainRoot.remove_widget(bullet)
                continue
            if bullet.absoluteBulletStartX < bullet.absoluteTargetX:
                try:
                    bullet.x += bullet.speed * x/distance
                    bullet.moveX += bullet.speed*x/distance
                except:
                    pass
            else:
                try:
                    bullet.x -= bullet.speed*x/distance
                    bullet.moveX -= bullet.speed*x/distance
                except:
                    pass

            if bullet.absoluteBulletStartY < bullet.absoluteTargetY:
                try:
                    bullet.y += bullet.speed*y/distance
                    bullet.moveY += bullet.speed*y/distance
                except:
                    pass
            else:
                try:
                    bullet.y -= bullet.speed*y/distance
                    bullet.moveY -= bullet.speed*y/distance
                except:
                    pass
            # Bullet hit
            if bullet.collide_widget(bullet.target):
                bullet.target.health -= bullet.root.firePower
                if self.mainRoot.ids["MenuButton_AddSelect"].selected == False:
                    self.mainRoot.ids["MainMapPicture"].draw_explosion([bullet.absoluteTargetY,bullet.absoluteTargetX],bullet.root)
                self.mainRoot.bullets.remove(bullet)
                self.mainRoot.remove_widget(bullet)

            elif math.dist(bulletRootPos,[bulletRootPos[0]+bullet.moveX//60,bulletRootPos[1]+bullet.moveY//60]) >= bullet.distanceToFly:
                self.mainRoot.bullets.remove(bullet)
                self.mainRoot.remove_widget(bullet)


