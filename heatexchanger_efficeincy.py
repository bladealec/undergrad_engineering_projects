def calculate_heat_exchanger_efficiency(m_dot_cold, T_in_cold, T_out_cold, m_dot_hot, T_in_hot, T_out_hot):
    # Calculate heat gained by the cold fluid
    Q_cold = m_dot_cold * (T_out_cold - T_in_cold)

    # Calculate heat lost by the hot fluid
    Q_hot = m_dot_hot * (T_in_hot - T_out_hot)

    # Calculate efficiency (assuming no heat loss to the environment)
    efficiency = Q_cold / Q_hot

    return efficiency

def main():
    print("Heat Exchanger Efficiency Calculator")
    
    m_dot_cold = float(input("Enter the mass flow rate of the cold fluid (kg/s): "))
    T_in_cold = float(input("Enter the inlet temperature of the cold fluid (°C): "))
    T_out_cold = float(input("Enter the outlet temperature of the cold fluid (°C): "))
    
    m_dot_hot = float(input("Enter the mass flow rate of the hot fluid (kg/s): "))
    T_in_hot = float(input("Enter the inlet temperature of the hot fluid (°C): "))
    T_out_hot = float(input("Enter the outlet temperature of the hot fluid (°C): "))
    
    efficiency = calculate_heat_exchanger_efficiency(m_dot_cold, T_in_cold, T_out_cold, m_dot_hot, T_in_hot, T_out_hot)

    print(f"\nThe efficiency of the heat exchanger is: {efficiency:.2f}")

if __name__ == "__main__":
    main()
