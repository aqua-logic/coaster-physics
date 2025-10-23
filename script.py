# Animação: loop circular de montanha-russa (sem atrito)
# Requisitos: numpy, matplotlib
# Em Jupyter: o FuncAnimation aparece inline. Em script .py podes salvar como GIF/MP4 removendo a parte de display.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import FancyArrow
from IPython.display import HTML

# --------- parâmetros ajustáveis ----------
R = 5.0
g = 9.81
v0 = 10.55
T = 4.0
dt = 0.01
# -----------------------------------------

# coordenadas do loop
theta_track = np.linspace(0, 2*np.pi, 400)
x_track = R * np.sin(theta_track)
y_track = R * (1 - np.cos(theta_track))

# listas para trajetória
x_history, y_history, v_history, F_norm_history = [], [], [], []

theta = 0.0
t = 0.0
falling = False
v = v0

while t < T:
    if not falling:
        # velocidade escalar pelo princípio da energia
        v2 = v0**2 - 2*g*R*(1 - np.cos(theta))
        v = np.sqrt(max(v2,0))
        # força normal
        F_norm = v**2 / R - g*np.cos(theta)
        if F_norm <= 0:
            # força normal zero ou negativa → inicia queda
            falling = True
            x0 = R*np.sin(theta)
            y0 = R*(1-np.cos(theta))
            vx = v * np.cos(theta + np.pi/2)
            vy = v * np.sin(theta + np.pi/2)
            t_proj = t
    if not falling:
        x = R*np.sin(theta)
        y = R*(1-np.cos(theta))
        x_history.append(x)
        y_history.append(y)
        v_history.append(v)
        F_norm_history.append(F_norm)
        dtheta = v/R*dt
        theta += dtheta
    else:
        # queda livre
        t_since = t - t_proj
        x = x0 + vx*t_since
        y = y0 + vy*t_since - 0.5*g*t_since**2
        v = np.sqrt(vx**2 + (vy - g*t_since)**2)
        F_norm = 0
        if y < 0:
            y = 0
            x_history.append(x)
            y_history.append(y)
            v_history.append(v)
            F_norm_history.append(F_norm)
            break
        x_history.append(x)
        y_history.append(y)
        v_history.append(v)
        F_norm_history.append(F_norm)
    t += dt

x_history = np.array(x_history)
y_history = np.array(y_history)
v_history = np.array(v_history)
F_norm_history = np.array(F_norm_history)

# normalizar força normal para visualização de seta
F_max = np.max(F_norm_history)
F_norm_scaled = F_norm_history / F_max * 1.0  # comprimento máximo 1.0

# --- animação ---
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal')
ax.plot(x_track, y_track, linestyle='--', color='gray')
ax.set_xlim(-1.5*R, 1.5*R)
ax.set_ylim(-0.5, 2.5*R)
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')
ax.set_title('Loop circular com queda instantânea quando F ≤ 0')

cart_point, = ax.plot([], [], marker='o', markersize=12)
time_text = ax.text(0.02,0.95,'',transform=ax.transAxes)
speed_text = ax.text(0.02,0.90,'',transform=ax.transAxes)
arrow = None  # placeholder para a seta

def init():
    cart_point.set_data([], [])
    time_text.set_text('')
    speed_text.set_text('')
    return cart_point, time_text, speed_text

def animate(i):
    global arrow
    cart_point.set_data(x_history[i], y_history[i])
    # cor do carrinho
    if F_norm_history[i]>0:
        cart_point.set_color('green')
    else:
        cart_point.set_color('red')
    # remover seta anterior
    if arrow:
        arrow.remove()
    if F_norm_history[i]>0:
        # seta azul proporcional à força normal
        scale = F_norm_scaled[i]
        dx = -x_history[i]/R * scale
        dy = (R - y_history[i])/R * scale
        arrow = FancyArrow(x_history[i], y_history[i], dx, dy,
                           width=0.05*scale, color='blue')
        ax.add_patch(arrow)
    time_text.set_text(f't = {i*dt:.2f} s')
    speed_text.set_text(f'|v| = {v_history[i]:.2f} m/s')
    return cart_point, time_text, speed_text, arrow

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=len(x_history), interval=dt*1000, blit=True)


anim.save('loop_animation.mp4', fps=int(1/dt))
