import pybullet as p
import time
import pybullet_data
from math import sqrt
from random import random

class CarSim:
  def __init__(self,pitch=0.0):
    self.physics_client = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-10)
    self.plane_id = p.loadURDF("plane.urdf")
    car_start_pos = [0,0,0.5]
    car_start_orn = p.getQuaternionFromEuler([0,pitch,0])
    self.car_id = p.loadURDF("racecar/racecar.urdf",car_start_pos,car_start_orn)
    self.time = 0.0
    self.time_step = 1./240.
    self.steer_offset = -1.0
    self.steer(0.0)
    self.speed(0.0)

  def quit(self):
    p.disconnect()

  def speed(self,speed_cmd):
    max_force=500.0
    self.speed_cmd = speed_cmd
    p.setJointMotorControlArray(self.car_id,[2,3,5,7],p.VELOCITY_CONTROL,
                                targetVelocities=[speed_cmd,
                                                  speed_cmd,
                                                  speed_cmd,
                                                  speed_cmd],
                                forces=[max_force,
                                        max_force,
                                        max_force,
                                        max_force])

  def steer(self,steer_cmd):
    self.steer_cmd = steer_cmd
    p.setJointMotorControlArray(self.car_id,[4,6],p.POSITION_CONTROL,
                                targetVelocities=[steer_cmd+self.steer_offset,
                                                  steer_cmd+self.steer_offset])

  def add_wheel_wobble(self):
    wobble_joint = 2
    wobble_factor = 1.0+0.001*(random()-0.5)
    p.setJointMotorControl2(self.car_id,wobble_joint,p.VELOCITY_CONTROL,
                            wobble_factor*self.speed_cmd)

  def step(self):
    self.add_wheel_wobble()
    p.stepSimulation()
    time.sleep(self.time_step)
    self.time += self.time_step
    self.position, self.orientation = p.getBasePositionAndOrientation(self.car_id)
    self.trans_vel, self.ang_vel = p.getBaseVelocity(self.car_id)

  def heading(self):
    angs = p.getEulerFromQuaternion(self.orientation)
    return(angs[2])

  def pitch(self):
    angs = p.getEulerFromQuaternion(self.orientation)
    return(angs[1])

  def get_speed(self):
    return(sqrt(self.trans_vel[0]**2 + self.trans_vel[1]**2 + self.trans_vel[2]**2))
    
if __name__=='__main__':
  c = CarSim()
  c.speed(5.0)
  c.steer(0.0)
  for t in range(10000):
    c.step()
    print(c.heading())
    print(c.get_speed())
  c.quit()
