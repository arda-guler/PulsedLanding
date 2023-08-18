class Vessel:
    def __init__(self, pos, vel, dry_mass, prop_mass, mdot, thrust):
        self.pos = pos
        self.vel = vel
        self.dry_mass = dry_mass
        self.prop_mass = prop_mass
        self.mdot = mdot
        self.thrust = thrust

        self.throttle = 0 # either 0 or 1 during operation
        self.accel = 0

    def update_physics(self, grav_accel, dt):
        self.vel += grav_accel * dt
        if self.prop_mass > 0:
            self.vel += self.thrust * self.throttle / (self.dry_mass + self.prop_mass) * dt
        self.pos += self.vel * dt

        if self.prop_mass > 0:
            self.prop_mass -= self.mdot * self.throttle * dt
            if self.prop_mass < 0:
                self.prop_mass = 0

    def activate_engine(self):
        self.throttle = 1

    def deactivate_engine(self):
        self.throttle = 0

    def toggle_engine(self):
        if self.throttle:
            self.throttle = 0
        else:
            self.throttle = 1
