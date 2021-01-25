import plotly.graph_objects as go
import numpy as np
import math
from model import *

class Simulator:
    def __init__(self):
        self.model = Model()
    
        self.dt = 0.01 # in seconds
        self.total_time = 10.0
        
        self.v = [0.0, 0.0]
        self.t = []
        self.u = []
        
    def simulate(self, target):
        kp = 25.0
        kd = 0.1
        ki = 0.0
        
        last_error = 0.0
        I = 0.0
        D = 0.0
    
        for i in range(0, int(self.total_time / self.dt + 2)):
            error = target - self.v[len(self.v) - 1]
            D = (error - last_error) / self.dt
            I += error * self.dt
            
            input = kp * error + kd * D + ki * I
            last_error = error
        
            if input > 12:
                input = 12
            elif input < -12:
                input = -12
        
            self.u.append(input)
            
            self.model.Update(self.dt, input)
            self.v.append(self.model.GetVel())
            self.t.append(i * self.dt)
    
        return self.v[2:], self.u, self.t[:len(self.t) - 1 - 2]
        
        
        
        
sim = Simulator()
input = 0.2 * sim.model.max_speed
v, u, t = sim.simulate(input)
print("goal speed: " + str(input))


vel = go.Figure()
vel.add_trace(go.Scatter(x=t, y=v, name='v vs. t', line=dict(color='firebrick', width=4)))
vel.update_layout(title='v vs. t', xaxis_title='Time (s)', yaxis_title='velocity (rad/s)')

vel.show()

volt = go.Figure()
volt.add_trace(go.Scatter(x=t, y=u, name='V vs. t', line=dict(color='royalblue', width=4)))
volt.update_layout(title='V vs. t', xaxis_title='Time (s)', yaxis_title='Voltage')

volt.show()
