class Model:
    def __init__(self):
        self.stall_current = 131.227 * 2 # A
        self.free_speed = 558.15 # rad/s; 5330 rpm
        self.G = 5.143 # Gear Ratio
        self.max_speed = self.free_speed / self.G
        self.R = 12.0 / self.stall_current # internal resistance
        self.kv = 0.0211 # back emf constant; V/rad/s
        self.kt = 0.018803 # torque constant
        self.m = 90.72 # kg
        self.radius = 0.1 # meters
        
        self.v = 0.0 # angular velocity
        
    # returns the angular acceleration based on current velocity
    def Update(self, dt, voltage):
        a =  (voltage * self.G * self.kt) / (self.m * self.R * self.radius ** 2) - (self.G ** 2 * self.kt * self.kv * self.v) / (self.m * self.R * self.radius ** 2)

        
        self.v += a * dt
        
        return self.v
        
    def GetVel(self):
        return self.v
        
