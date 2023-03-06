
from pyfluids import Fluid, Input # Mixture, HumidAir, InputHumidAir, FluidsList
import matplotlib.pyplot as plt

class state_plot:
    
    def __init__(self, fluid, property_a, property_b, plot_limit_T, plot_limit_P, plot_limit_v):
        """
        argumentos:
        * fluid: Aquí se debe insertar un objeto como: FluidList.{}
        * property_i: Se debe indicar la propiedad utilizando la función: Input.{}. Además, se puede
        ingresar una lista de objetos.
        """
        self.fluid = fluid
        self.plot_limit_T = plot_limit_T
        self.plot_limit_P = plot_limit_P
        self.plot_limit_v = plot_limit_v
        
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
        
    def _saturation_lines_Tv(self):
        # Saturation lines
        liq_sat = []
        vap_sat = []
        T = []
        for t in range(self.plot_limit_T[0]*1000, int(round(self.T_cr,3)*1000), 1000):
            T.append(t/1000)
            saturation_point = Fluid(self.fluid).with_state(Input.temperature(t/1000),Input.quality(0))
            liq_sat.append(1/saturation_point.density)
            saturation_point = Fluid(self.fluid).with_state(Input.temperature(t/1000),Input.quality(100))
            vap_sat.append(1/saturation_point.density)
        
        return T, liq_sat, vap_sat
    
    def _saturation_lines_Pv(self):
        # Saturation lines
        liq_sat = []
        vap_sat = []
        P = []
        for p in range(1000, int(round(self.P_cr,0))-1,100000):
            P.append(p)
            saturation_point = Fluid(self.fluid).with_state(Input.pressure(p),Input.quality(0))
            liq_sat.append(1/saturation_point.density)
            saturation_point = Fluid(self.fluid).with_state(Input.pressure(p),Input.quality(100))
            vap_sat.append(1/saturation_point.density)
        
        return P, liq_sat, vap_sat
            
    def point_in_Tv(self):
        """
        Esta función imprime un diagrama Tv con las líneas de saturación y el 
        punto o lista de puntos ingresados en la función a través de las dos
        variables de estado.
        Para ingresar las variables se debe utilizar la función Input.{property}
        """
        # Saturation lines
        T, liq_sat, vap_sat = state_plot._saturation_lines_Tv(self)

        # plot
        plt.style.use('_mpl-gallery')
        fig, ax = plt.subplots()
        ax.plot(liq_sat, T, linewidth=2.0, color='blue')
        ax.plot(vap_sat, T, linewidth=2.0, color='orange')
        ax.plot(self.v_cr, self.T_cr, 'o', color='black')
        if type(self.state) == list:
            for _ in range(len(self.state)):
                ax.plot(1/self.state[_].density, self.state[_].temperature, 'ro')
        else:    
            ax.plot(1/self.state.density, self.state.temperature, 'ro')
        plt.xlabel('v, in m3/kg')
        plt.ylabel('T, in °C')
        ax.set(xlim=(self.plot_limit_v[0], self.plot_limit_v[1]),
                ylim=(self.plot_limit_T[0], self.plot_limit_T[1]))
        
        return plt.show()
        
    def point_in_Pv(self):
        """
        Esta función imprime un diagrama Tv con las líneas de saturación y el 
        punto o lista de puntos ingresados en la función a través de las dos
        variables de estado.
        Para ingresar las variables se debe utilizar la función Input.{property}
        """
        # Saturation lines
        P, liq_sat, vap_sat = state_plot._saturation_lines_Pv(self)

        # plot
        plt.style.use('_mpl-gallery')
        fig, ax = plt.subplots()
        ax.plot(liq_sat, P, linewidth=2.0, color='blue')
        ax.plot(vap_sat, P, linewidth=2.0, color='orange')
        ax.plot(self.v_cr, self.P_cr, 'o', color='black')
        if type(self.state) == list:
            for _ in range(len(self.state)):
                ax.plot(1/self.state[_].density, self.state[_].pressure, 'ro')
        else:    
            ax.plot(1/self.state.density, self.state.pressure, 'ro')
        plt.xlabel('v, in m3/kg')
        plt.ylabel('P, in Pa')
        ax.set(xlim=(self.plot_limit_v[0], self.plot_limit_v[1]),
                ylim=(self.plot_limit_P[0], self.plot_limit_P[1]))
        
        return plt.show()