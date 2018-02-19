import math
#import turtle
import matplotlib.pyplot as plt    
import numpy as np    
import matplotlib.animation as animation    

#earthpos = turtle
#moonpos= turtle
#direction = turtle


#class matter:
	
#turtle.screensize(2000, 2000, "black")
#turtle.speed(1000)
#turtle.pencolor("white")
#turtle.hideturtle()
	
	
G = 6.67e-11

class matter:
	def __init__(self,name, index, x,y,z,diameter, mass, density, velocity, v_angle, dStep=1):
		self.name = name
		self.index = index
		self.x = x
		self.y = y
		self.z = z
		self.diameter = diameter
		self.mass = mass
		self.density = density
		self.velocity = velocity
		self.v_angle = v_angle
		self.force = 0
		self.force_angle=0
		self.distance=0
		self.dStep=dStep
		
	def CalForce(self, OtherMatters):
		i=1
		F_acc_x, F_acc_y = 0,0
		n = len(OtherMatters)
		for i in range(n):
			if i != self.index :
				x1=OtherMatters[i].x
				x2=self.x
				y1=OtherMatters[i].y
				y2=self.y
				z1=OtherMatters[i].z
				z2=self.z
				distance= math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1));
				self.distance = distance
				F=(G*OtherMatters[i].mass * self.mass)/ (distance*distance)
				angle = math.atan((F_acc_y)/(F_acc_x))
				if F_acc_x < 0:
					F_angle = math.pi + F_angle
				F_x = math.cos(F)
				F_y = math.sin(F)
				F_acc_x = F_acc_x + F_x
				F_acc_y = F_acc_y + F_y
				print("self#=",self.index, "loop#=",i, "F=",F, "Fx=",F_x, "Fy=",F_y,"F_acc_x=",F_acc_x, "F_acc_y=",F_acc_y)
		F_angle = math.atan((F_acc_y)/(F_acc_x))
		if F_acc_x < 0:
			F_angle = math.pi + F_angle
		self.force = F_acc_y/math.sin(F_angle)
		self.force_angle = F_angle
		print("Accumulated Force =", self.force, "Angle=", self.force_angle)

				#F_angle = math.atan((y2-y1)/(x2-x1))
#				if x2-x1 < 0 :
#						F_angle = math.pi + F_angle
			
				#print("distance=",distance)
				#print("F=",F)
				#print("F_angle=",F_angle)

	def CalVelocity(self):
		F = self.force
		F_angle = self.force_angle
		a_v = (F * math.cos(F_angle+math.pi-self.v_angle))/self.mass #顺着原来速度的分加速度
		a_pv = (F * math.sin(F_angle+math.pi-self.v_angle))/self.mass #垂直原来速度的分加速度 
		
		v1 = self.velocity + self.dStep * a_v # 原来速度+增加的分速度
		self.v_angle = self.v_angle + math.atan(self.dStep * a_pv/v1) # 下一次速度的角度
		self.velocity = v1/(math.cos(math.atan(self.dStep * a_pv/v1)))
		#print("a_v=",a_v)
		#print("a_pv=",a_pv)
		#print("v1=",v1)
		#print("moon.v_angle=",self.v_angle)
		#print("moon.velocity=",self.velocity)	
		
	def Move(self):
		self.x = self.x + self.dStep * self.velocity * math.cos(self.v_angle)
		self.y = self.y + self.dStep * self.velocity * math.sin(self.v_angle)
		#print(self.x,self.y)
		#print("\n")
		
		


def simData(AllMatters):    
	t_max = 10000000 
	dt=1       
	t = 0.0    
	while t < t_max:    
		matters[2].CalForce(AllMatters)
		matters[2].CalVelocity()
		matters[2].Move()
		t = t + dt
		if t % (3600 ) == 0 : 
			#print(moon.x/2000000, moon.y/2000000)
			yield matters[2].x/2000000, matters[2].y/2000000    
	
def simPoints(simData):    
	x, y = simData[0], simData[1]    
	time_text.set_text(time_template%(matters[2].distance))    
	line1.set_data(x, y)
	line2.set_data(matters[1].x,matters[1].y)
	return line1, line2, time_text  


matters = [matter("",0,0,0,0,0,0,0,0,0)]*10

dStep = 10
matters[1]=matter("earth",1,0,0,0,12756e+3,5.965e+24,5507.85, 0, 0,dStep)
matters[2]=matter("moon", 2,363300e+3,0,0,3476.28e+3,7.349e+22,3350,1023,math.pi/2,dStep)
time=0

fig = plt.figure()    
ax = fig.add_subplot(111)    
line1, = ax.plot([], [], 'bo', ms=matters[2].diameter/2000000) # I'm still not clear on this stucture...   
line2, = ax.plot([], [], 'ro', ms=matters[1].diameter/2000000) # I'm still not clear on this stucture...  
line3, = ax.plot([], []) # I'm still not clear on this stucture...  
 
ax.set_ylim(-300, 300)    
ax.set_xlim(-300, 300)
plt.axis('off')

time_template = 'Time = %.1f s'    # prints running simulation time    
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)    


ani = animation.FuncAnimation(fig, simPoints, simData(matters), blit=False, interval=10,    
	repeat=True)    
plt.show() 

#while time<10000000:
#
#	moon.CalForce(earth)
#	moon.CalVelocity()
#	moon.Move()
##	if time % (3600 * 24) == 0 : 
#
#
#		#turtle.clear()
#		
##		earthpos.penup()
##		earthpos.goto((earth.x)/2000000,earth.y/2000000)
##		earthpos.pendown()
##		earthpos.circle(earth.diameter/2000000)
##		
##		moonpos.penup()
##		moonpos.goto((moon.x)/2000000,moon.y/2000000)
##		moonpos.pendown()
##		moonpos.circle(moon.diameter/2000000)
##	
##		direction.penup()
##		direction.goto(200,200)
##		direction.pendown()
##		direction.setheading(moon.v_angle/math.pi*180)
##		direction.forward(50)
##	
#	
#	time=time+1
#
#
#
