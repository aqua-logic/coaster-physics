from vpython import *

# ---------- Parameters ----------
R = 5           # loop radius
g = 9.81
v0 = 15.55      # initial velocity
dt = 0.001      # time step

# ---------- Scene setup ----------
scene = canvas(title='Looping Roller Coaster',
               width=800, height=600,
               center=vector(0,R,0),
               background=color.white)

# Loop (circle) as curve
theta = [i*0.01 for i in range(0, int(2*pi/0.01)+1)]
loop_curve = curve(color=color.gray(0.5))
for th in theta:
    x = R*sin(th)
    y = R*(1 - cos(th))
    loop_curve.append(pos=vector(x, y, 0))

# Ball
ball = sphere(pos=vector(0,0,0), radius=0.3, color=color.red, make_trail=True, trail_color=color.orange)

# Force vector (blue)
F_arrow = arrow(pos=ball.pos, axis=vector(0,0,0), color=color.blue, shaftwidth=0.1)

# ---------- Initial conditions ----------
theta_ball = 0
falling = False
t = 0

# Run simulation
while True:
    rate(1000)
    
    if not falling:
        # velocity from energy
        v = (v0**2 - 2*g*R*(1 - cos(theta_ball)))**0.5
        # force normal
        F_norm = v**2 / R - g * cos(theta_ball)
        
        if F_norm <= 0:
            falling = True
            # convert to projectile initial velocity
            vx = v*cos(theta_ball + pi/2)
            vy = v*sin(theta_ball + pi/2)
            x0 = R*sin(theta_ball)
            y0 = R*(1 - cos(theta_ball))
            t_proj = t
            
    if not falling:
        # position along loop
        x = R*sin(theta_ball)
        y = R*(1 - cos(theta_ball))
        ball.pos = vector(x, y, 0)
        # update force vector (scaled for visibility)
        F_arrow.pos = ball.pos
        F_arrow.axis = vector(-x/R*F_norm, (R-y)/R*F_norm, 0)*0.3
        theta_ball += v/R * dt
    else:
        # projectile motion
        t_since = t - t_proj
        x = x0 + vx*t_since
        y = y0 + vy*t_since - 0.5*g*t_since**2
        if y < 0:
            y = 0
            ball.pos = vector(x, y, 0)
            F_arrow.axis = vector(0,0,0)
            break
        ball.pos = vector(x, y, 0)
        F_arrow.pos = ball.pos
        F_arrow.axis = vector(0,0,0)  # no contact
    
    t += dt
