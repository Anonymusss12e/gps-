import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches

# Creare figura
fig, ax = plt.subplots(figsize=(12, 8))

# Configurare curte și clădiri
class Factory:
    def __init__(self):
        # Dimensiuni curte
        self.yard_width = 10
        self.yard_height = 8
        
        # Configurare hale
        self.halls = {
            'Hala 1': {'pos': (2, 4), 'size': (1.5, 1), 'color': 'lightblue'},
            'Hala 2': {'pos': (5, 4), 'size': (1.5, 1), 'color': 'lightgreen'},
            'Hala 3': {'pos': (8, 4), 'size': (1.5, 1), 'color': 'salmon'}
        }
        
        # Configurare drum și parcare
        self.road_width = 1
        self.parking_spots = [(x, 1.5) for x in np.linspace(2, 8, 6)]

    def draw(self):
        # Desenare curte
        yard = patches.Rectangle((0, 0), self.yard_width, self.yard_height,
                               fill=False, color='green', linewidth=2)
        ax.add_patch(yard)
        
        # Desenare hale
        for hall_name, hall_data in self.halls.items():
            hall = patches.Rectangle(hall_data['pos'], 
                                  hall_data['size'][0], hall_data['size'][1],
                                  fill=True, color=hall_data['color'])
            ax.add_patch(hall)
            # Adăugare etichete pentru hale
            ax.text(hall_data['pos'][0] + 0.5, hall_data['pos'][1] + 0.5, 
                   hall_name, ha='center')
        
        # Desenare drum
        road = patches.Rectangle((0, 2), self.yard_width, self.road_width,
                               color='gray', alpha=0.3)
        ax.add_patch(road)
        
        # Desenare locuri de parcare
        for spot in self.parking_spots:
            parking = patches.Rectangle((spot[0]-0.3, spot[1]-0.3), 0.6, 0.6,
                                     fill=False, color='black', linewidth=1)
            ax.add_patch(parking)

# Configurare oameni
class People:
    def __init__(self, num_people, factory):
        self.num_people = num_people
        self.factory = factory
        # Poziții inițiale
        self.positions = np.zeros((num_people, 2))
        self.positions[:, 0] = -1  # Toți încep din afara curții
        self.positions[:, 1] = np.random.uniform(2, 3, num_people)
        
        # Asignare hale pentru fiecare persoană
        self.targets = np.random.choice(list(factory.halls.keys()), num_people)
        
        # Stare pentru fiecare persoană (0=merge spre hală, 1=a ajuns)
        self.states = np.zeros(num_people)
        
        # Culori pentru fiecare persoană bazate pe hala țintă
        self.colors = [factory.halls[target]['color'] for target in self.targets]

    def update_positions(self):
        for i in range(self.num_people):
            if self.states[i] == 0:
                target_hall = self.factory.halls[self.targets[i]]
                target_pos = target_hall['pos']
                
                # Calculare direcție
                dx = target_pos[0] - self.positions[i, 0]
                dy = target_pos[1] - self.positions[i, 1]
                
                # Mișcare
                speed = 0.1
                if abs(dx) > 0.1 or abs(dy) > 0.1:
                    self.positions[i, 0] += np.sign(dx) * speed
                    if self.positions[i, 0] > 0:  # Dacă a intrat în curte
                        self.positions[i, 1] += np.sign(dy) * speed
                else:
                    self.states[i] = 1  # A ajuns la destinație

# Inițializare
factory = Factory()
people = People(15, factory)  # 15 oameni

# Funcții pentru animație
def init():
    factory.draw()
    return []

def animate(frame):
    people.update_positions()
    
    # Șterge doar scatter plot-ul anterior, nu și restul elementelor
    for collection in ax.collections:
        collection.remove()
    
    # Desenează oamenii
    scatter = ax.scatter(people.positions[:, 0], people.positions[:, 1],
                        c=people.colors, s=100, alpha=0.6)
    
    # Adaugă informații despre progres
    ax.set_title(f'Simulare fabrică - {int(np.sum(people.states))}/{people.num_people} persoane au ajuns')
    
    return [scatter]

# Configurare plot
ax.set_xlim(-2, factory.yard_width + 1)
ax.set_ylim(-1, factory.yard_height + 1)
ax.set_aspect('equal')

# Creare animație
anim = animation.FuncAnimation(fig, animate, init_func=init,
                             frames=200, interval=50, blit=True)

plt.show()