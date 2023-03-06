
from pyfluids import Fluid, FluidsList, Input, Mixture, HumidAir, InputHumidAir
import math
import matplotlib.pyplot as plt
import numpy as np

class state_plot():
    def __init__(self, fluid, property_a, property_b, plot_limit_x, plot_limit_y):
        """
        argumentos:
        * fluid: Aquí se debe insertar un objeto como: FluidList.{}
        * property_i: Se debe indicar la propiedad utilizando la función: Input.{}. Además, se puede
        ingresar una lista de objetos.
        """
        self.fluid = fluid
        self.plot_limit_x = plot_limit_x
        self.plot_limit_y = plot_limit_y
        
        if type(property_a) == list:
            self.state = []
            for p in range(len(property_a)):
                self.state.append(Fluid(self.fluid).with_state(property_a[p],property_b[p]))
        else:
            self.state = Fluid(self.fluid).with_state(property_a,property_b)
         # Critical properties   
        self.P_cr = Fluid(self.fluid).critical_pressure
        self.T_cr = Fluid(self.fluid).critical_temperature
        self.v_cr = 1/Fluid(self.fluid).with_state(Input.pressure(self.P_cr),Input.temperature(self.T_cr)).density

def saturation_lines_Tv(self):
    # Saturation lines
    liq_sat = []
    vap_sat = []
    T = []
    for t in range(self.plot_limit_y[0], int(round(self.T_cr,3)*1000), 1000):
        T.append(t/1000)
        saturation_point = Fluid(self.fluid).with_state(Input.temperature(self.plot_limit_y[0]/1000),Input.quality(0))
        liq_sat.append(1/saturation_point.density)
        saturation_point = Fluid(self.fluid).with_state(Input.temperature(self.plot_limit_y[0]/1000),Input.quality(100))
        vap_sat.append(1/saturation_point.density)
    
    return T, liq_sat, vap_sat
        
        
def point_in_Tv(self):
    """
    Esta función imprime un diagrama Tv con las líneas de saturación y el 
    punto o lista de puntos ingresados en la función a través de las dos
    variables de estado.
    Para ingresar las variables se debe utilizar la función Input.{property}
    """
    # Saturation lines
    T, liq_sat, vap_sat = saturation_lines_Tv(self)

    # plot
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()
    ax.plot(liq_sat, T, linewidth=2.0)
    ax.plot(vap_sat, T, linewidth=2.0)
    ax.plot(self.v_cr, self.T_cr, 'o', color='black')
    if type(self.state) == list:
        for _ in range(len(self.state)):
            ax.plot(1/self.state[_].density, self.state[_].temperature, 'ro')
    else:    
        ax.plot(1/self.state.density, self.state.temperature, 'ro')
    plt.xlabel('v, in m3/kg')
    plt.ylabel('T, in °C')
    ax.set(xlim=(self.plot_limit_x[0], self.plot_limit_x[1]),
            ylim=(self.plot_limit_y[0], self.plot_limit_y[1]))
    
    plt.show()