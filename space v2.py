#!/usr/bin/python
import math
import time
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
	def __init__(self,index, name, colorshape, x,y,z,diameter, mass, density, velocity, v_angle, dStep=1):
		global max_matter
		self.name = name     	#天体对象名
		self.index = index	 	#天体编号
		self.x = x				#天体x坐标
		self.y = y				#天体y坐标
		self.z = z				#天体z坐标
		self.colorshape = colorshape	#天体的颜色和形状
		self.diameter = diameter		#天体直径
		self.mass = mass				#天体质量
		self.density = density			#天体密度
		self.velocity = velocity		#天体运动速度
		self.v_angle = v_angle			#天体速度方向
		self.force = 0					#天体受力大小
		self.force_angle=0				#天体受力方向
		self.distance=[0]*max_matter					#天体与其他天体之间的距离
		self.dStep=dStep				#
		
	def CalForce(self, OtherMatters):  #天体受力计算
		if self.mass !=0 :
			F_acc_x, F_acc_y, F_angle = 0,0,0
			for i in range(max_matter):
				if i != self.index :
					x1=OtherMatters[i].x
					x2=self.x
					y1=OtherMatters[i].y
					y2=self.y
					#z1=OtherMatters[i].z
					#z2=self.z
					distance= math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1));
					self.distance[i] = distance
					if distance !=0 and OtherMatters[i].mass !=0 :
						F=(G*OtherMatters[i].mass * self.mass)/ (distance*distance)
						if x2-x1 != 0 :
							angle = math.atan((y2-y1)/(x2-x1))
						else:
							if y2-y1 > 0 :
								angle = math.pi/2
							else:
								angle = math.pi + math.pi/2
						if x2-x1 < 0:
							angle = math.pi + angle
						F_x = math.cos(angle)*F
						F_y = math.sin(angle)*F
						F_acc_x = F_acc_x + F_x
						F_acc_y = F_acc_y + F_y
					#print("self#=",self.index, "loop#=",i, "F=",F, "Fx=",F_x, "Fy=",F_y,"angle=",angle, "F_acc_x=",F_acc_x, "F_acc_y=",F_acc_y)
			if F_acc_x != 0 : 
				F_angle = math.atan((F_acc_y)/(F_acc_x))
			else:
				if F_acc_y >0 : F_angle = math.pi/2
				else: F_angle = math.pi*3/2
			#print("self#=",self.index, "loop#=",i, "F=",F, "Fx=",F_x, "Fy=",F_y,"angle=",angle, "F_acc_x=",F_acc_x, "F_acc_y=",F_acc_y)

			if F_acc_x < 0:
				F_angle = math.pi + F_angle
			self.force = math.sqrt(F_acc_x*F_acc_x+F_acc_y*F_acc_y)
			self.force_angle = F_angle
			#print("Accumulated Force =", self.force, "Angle=", self.force_angle)

				#F_angle = math.atan((y2-y1)/(x2-x1))
#				if x2-x1 < 0 :
#						F_angle = math.pi + F_angle
			
				#print("distance=",distance)
				#print("F=",F)
				#print("F_angle=",F_angle)

	def CalVelocity(self):			#天体速度计算
		if self.mass !=0 :
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
		
	def Move(self,OtherMatters):			#天体移动
		if self.mass !=0 :
			x = self.x + self.dStep * self.velocity * math.cos(self.v_angle)
			y = self.y + self.dStep * self.velocity * math.sin(self.v_angle)
			for i in range(1,max_matter) :
				if i!=self.index:
					x1=OtherMatters[i].x
					x2=x
					y1=OtherMatters[i].y
					y2=y
#					z1=OtherMatters[i].z
#					z2=self.z
					distance= math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1));
					if distance <= OtherMatters[i].diameter + self.diameter :
						print(self.index, i, distance, OtherMatters[i].diameter + self.diameter)
						self.velocity = self.velocity - (OtherMatters[i].diameter + self.diameter - distance)
						i = max_matter


			self.x = self.x + self.dStep * self.velocity * math.cos(self.v_angle)
			self.y = self.y + self.dStep * self.velocity * math.sin(self.v_angle)
			#print(self.x,self.y)
			#print("\n")


def simData(AllMatters):    
	t_max = 100000000
	dt=1       
	global t
	time_frame = time.time()*1000
	while t < t_max:
		if not pause:   
			for i in range(1,len(matters)) :
				matters[i].CalForce(AllMatters)
				matters[i].CalVelocity()
				matters[i].Move(AllMatters)
			t = t + dt
		if t % (frame_step) == 0 : 
			#print(t)
			#print("loop period=",(time.time()*1000-time_frame))
			#time_frame = time.time() *1000 
			yield matters,t
		
def simPoints(simData):  
	
	#print(len(simData[0]))

	Mter = simData[0]
	time_text.set_text(time_template%(float(simData[1]*dStep/3600/24),frame_step*dStep/3600/24, Mter[2].x / 1000000000,Mter[2].y/1000000000, Mter[2].distance[1]/1000000000, (Mter[2].diameter + Mter[1].diameter)/1000000000))

	for i in range(1,len(Mter)):
		if i != 3 :
			line[i].set_data(Mter[i].x/dScale,	  Mter[i].y / dScale)
		else: 
			line[i].set_data(Mter[2].x / dScale + (Mter[3].x / dScale - Mter[2].x / dScale)*30, Mter[2].y / dScale + (Mter[3].y / dScale-Mter[2].y / dScale)*30)
	
	line[1].set_markersize(matters[1].diameter/dScale*sunD_scale) 
	for j in range(2,max_matter): 
		line[j].set_markersize(matters[j].diameter/dScale*planetD_scale) 
	
	return line, time_text
	
def onClick(event):
	global pause
	global frame_step  
	global dScale
	#print(event.key)
	if(event.key == " "):
		pause ^= True  
	if(event.key == "f"):
		if(int(frame_step*0.1)<1): frame_step = frame_step +1
		else:  frame_step = int(frame_step*1.1)
	if(event.key == "d"):
		if(int(frame_step*1.1)>1): frame_step = int(frame_step*0.9)
	if(event.key == "i"):
		if(int(dScale*0.1)<1): dScale = dScale+1
		else:  dScale = int(dScale*1.1)
	if(event.key == "k"):
		dScale = int(dScale*0.9)


pause  = False 
t = 0.0  
max_matter = 12
matters = [matter("",0,"",0,0,0,0,0,0,0,0)]*max_matter
line = [0]*max_matter

dStep = 300
frame_step = 90
dScale = 200000000
sunD_scale = 1
planetD_scale = 50

#	              index,name,       cs,  x,y,z,                     diameter,   mass,      density, velocity,   v_angle,  dStep=1):
matters[1]=matter(1,    "sun",      "ro",0,0,0,                     1.392e+9,   1.9891e+30,1408,    0,          math.pi,  dStep)
matters[2]=matter(2,    "earth",    "go",147098074e+3,0,0,          12756e+3,   5.965e+24, 5507.85, 30287,      math.pi/2,dStep)
matters[3]=matter(3,    "moon",     "bo",147098074e+3+ 384400e+3,0,0,3476.28e+3, 7.349e+22, 3350,    30287+1023, math.pi/2,dStep)
matters[4]=matter(4,    "mercury",  "yo",57894376e+3,0,0, 			4878e+3,    3.3022e+23, 5427,   47890, 		math.pi/2,dStep)
matters[5]=matter(5,    "Venus",    "yo",108208930e+3,0,0, 			12103.6e+3, 4.869e+24,  5240,   35030, 		math.pi/2,dStep)
matters[6]=matter(6,    "Mars",     "mo",227936640e+3,0,0, 			6786e+3,    6.4219e+24,  3950,   24130, 	math.pi/2,dStep)
matters[7]=matter(7,    "Jupiter",  "mo",707833000e+3,0,0, 			142984e+3,    1.8987e+27,  1330,   13060, 	math.pi/2,dStep)
matters[8]=matter(8,    "Saturn",   "yo",1426980000e+3,0,0, 		120536e+3,    5.688e+26,  690,   9640, 		math.pi/2,dStep)
matters[9]=matter(9,    "Uranus",   "co",2870990000e+3,0,0, 		51118e+3,    8.6810e+25,  1290,   6810, 	math.pi*3/2,dStep)
matters[10]=matter(10,  "Neptune",  "ko",4504300000e+3,0,0, 		49528e+3,    1.0247e+26,  1640,   5430, 	math.pi/2,dStep)


fig = plt.figure()    

ax = fig.add_subplot(111)
line[1],= ax.plot([], [], 'ro', ms=matters[1].diameter/dScale*sunD_scale) 
for i in range(2,max_matter): 
	line[i],= ax.plot([], [], matters[i].colorshape, ms=matters[i].diameter/dScale*planetD_scale) 
line5, = ax.plot([], []) 
 
ax.set_ylim(-1000, 1000)    
ax.set_xlim(-1000, 1000)
plt.axis('off')


time_template = 'Time= %.1f day, step= %.1f day | earth(x,y)= (%.1f , %.1f) dis_to_sun= %.1f| d = %.1f'    # prints running simulation time    
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)    

fig.canvas.mpl_connect('key_press_event', onClick) 
ani = animation.FuncAnimation(fig, simPoints, simData(matters), blit=False, interval=1,    
	repeat=True)    
plt.show() 
