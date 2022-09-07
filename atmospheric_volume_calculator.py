import math


class AtmosphericVolumeCalculator:
    def __init__(self, surface_area, air_pressure, temperature, relative_humidity):
        # Temperature in Celsius
        # surface_area in m^2
        # air press in pascal
        # RH: in %
        self.surface_area = surface_area
        self.air_pressure = air_pressure
        self.temperature = temperature
        self.relative_humidity = relative_humidity

    def get_saturation_vapour_pressure(self):
        # Magnus formula
        # Returns in Pascal
        some_constant = 6.1078
        exp_value_num = 7.5*self.temperature
        exp_value_denum = self.temperature + 237.3
        exp_value = exp_value_num/exp_value_denum
        pressure_hPa = some_constant * (10**exp_value)
        pressure_Pa = pressure_hPa*100
        print("Press of Sat", pressure_Pa)
        return pressure_Pa

    def get_vapour_pressure_of_water(self):
        saturation_vapour_pressure = self.get_saturation_vapour_pressure()
        vapour_pressure_of_water = saturation_vapour_pressure * (self.relative_humidity/100)
        print("Press of VP", vapour_pressure_of_water)
        return vapour_pressure_of_water

    def get_pressure_of_dry_air(self):
        vapour_pressure_of_water = self.get_vapour_pressure_of_water()
        pressure_of_dry_air = self.air_pressure - vapour_pressure_of_water
        print("Press of Dry air", pressure_of_dry_air)
        return pressure_of_dry_air

    def get_density_of_atmosphere(self):
        temperature_in_kelvin = self.temperature + 273.15
        # Dry air
        Rd_dry_air = 287.058
        dry_air_num = self.get_pressure_of_dry_air()
        dry_air_denum = Rd_dry_air * temperature_in_kelvin
        dry_air_density = dry_air_num/dry_air_denum
        # water Vapour
        Rd_vapour = 461.495
        vapour_num = self.get_vapour_pressure_of_water()
        vapour_denum = Rd_vapour * temperature_in_kelvin
        vapour_density = vapour_num / vapour_denum
        print("dry air den", dry_air_density)
        print("vap den", vapour_density)
        return dry_air_density + vapour_density

    def get_mass_by_area(self):
        g = 9.806
        mass_by_area = self.air_pressure / g
        return mass_by_area

    def get_volume(self):
        mass_by_area = self.get_mass_by_area()
        mass_of_air = mass_by_area * self.surface_area
        print("Mass by area", mass_by_area)
        print("Mass of the air", mass_of_air)
        density_of_the_air = self.get_density_of_atmosphere()
        volume = mass_of_air/density_of_the_air
        return volume

if __name__ == "__main__":
    # # vol_obj = AtmosphericVolumeCalculator(106*10**6, 100400, 25, 90)
    # vol_obj = AtmosphericVolumeCalculator(510.1*(10**6)*(10**6), 101325, 14.85, 80)
    # print(vol_obj.get_volume()/(10**9))
    # new york state
    vol_obj = AtmosphericVolumeCalculator(141300*(10**6), 101325, 4, 70.7)
    print(vol_obj.get_volume()/(10**9))





