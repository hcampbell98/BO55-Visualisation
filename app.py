import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import numpy as np

def load_vehicle_data(file_path):
    """Load vehicle data from CSV file"""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error loading the CSV file: {e}")
        return None

def plot_vehicle_makes(df):
    """Plot the count of each vehicle make with a modern style"""
    if df is None or df.empty:
        print("No data to plot")
        return
    
    # Count the occurrences of each make and sort for better visualization
    make_counts = df['make'].value_counts().nlargest(15)  # Limit to top 15 for cleaner visualization
    
    # Reverse the order for display (highest at the top)
    make_counts = make_counts.iloc[::-1]
    
    # Set the style and use modern fonts
    plt.style.use('dark_background')
    plt.rcParams['font.family'] = 'Arial'  # Use a clean, modern font
    
    # Set up the figure size with high DPI for better quality
    fig, ax = plt.subplots(figsize=(14, 8), dpi=100)
    
    # Create a custom color palette that includes #fec72f (yellow/gold)
    start_color = '#fec72f'  # Yellow/gold
    end_color = '#1e88e5'    # Blue
    custom_cmap = mpl.colors.LinearSegmentedColormap.from_list("custom", [start_color, end_color])
    colors = [custom_cmap(i) for i in np.linspace(0, 1, len(make_counts))]
    
    # Create a horizontal bar plot with custom styling
    bars = ax.barh(make_counts.index, make_counts.values, color=colors, alpha=0.9)
    
    # Add data labels to the bars
    for i, bar in enumerate(bars):
        ax.text(bar.get_width() + (make_counts.max() * 0.01), 
                bar.get_y() + bar.get_height()/2, 
                f"{make_counts.values[i]:,}", 
                va='center', 
                fontsize=10, 
                fontweight='bold',
                color='white',
                fontfamily='Arial')
    
    # Remove the frame and add minimal grid lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#444444')
    ax.spines['left'].set_color('#444444')
    ax.grid(axis='x', linestyle='--', alpha=0.2)
    
    # Set title and labels with modern typography
    plt.title('BO55 Plates by Manufacturer', fontsize=18, fontweight='bold', pad=20)
    plt.xlabel('Number of Vehicles', fontsize=12, labelpad=10)
    plt.ylabel('Manufacturer', fontsize=12, labelpad=10)
    
    # Add a subtle gradient background
    gradient = np.linspace(0, 1, 100).reshape(1, -1)
    ax.imshow(gradient, aspect='auto', extent=[0, make_counts.max()*1.15, -0.5, len(make_counts)-0.5], 
              alpha=0.1, cmap=custom_cmap)
    
    # Make tick labels more modern
    ax.tick_params(axis='both', which='major', labelsize=10)
    for label in ax.get_yticklabels():
        label.set_fontweight('medium')
    
    # Adjust layout
    plt.tight_layout()
    
    # Add a sleek footer
    plt.figtext(0.5, 0.01, "Lisense Insights - Generated on " + pd.Timestamp.now().strftime("%Y-%m-%d"), 
                ha='center', fontsize=8, alpha=0.7, fontfamily='Arial', fontstyle='italic')
    
    # Add lisense.uk data source attribution
    plt.figtext(0.12, 0.95, "Data Source: lisense.uk", 
                ha='left', fontsize=10, fontweight='bold', 
                color='#fec72f', alpha=0.9, fontfamily='Arial')
    
    # Show and save the plot with high quality
    plt.savefig('vehicle_makes.png', dpi=300, bbox_inches='tight', transparent=False)
    plt.show()

if __name__ == "__main__":
    file_path = 'bo55_plates.csv'
    vehicle_data = load_vehicle_data(file_path)
    
    if vehicle_data is not None:
        print(f"Loaded {len(vehicle_data)} vehicle records")
        print("Vehicle makes in the dataset:", sorted(vehicle_data['make'].unique()))
        plot_vehicle_makes(vehicle_data)