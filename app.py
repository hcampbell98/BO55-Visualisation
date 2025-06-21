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
    all_makes = df['make'].value_counts()
    top_makes = all_makes.nlargest(12)  # Get top 12 manufacturers
    
    # Calculate "Other" category from remaining manufacturers
    other_count = all_makes.iloc[12:].sum() if len(all_makes) > 12 else 0
    
    # Create the final counts with "Other" at the bottom
    if other_count > 0:
        # Reverse the top makes for display (highest at the top)
        make_counts = top_makes.iloc[::-1]
        # Add "Other" at the bottom (first position after reversal)
        make_counts = pd.concat([pd.Series([other_count], index=['Other']), make_counts])
    else:
        # If no "Other" category needed, just reverse for display
        make_counts = top_makes.iloc[::-1]
      # Set ultra-modern styling with dark background
    plt.style.use('dark_background')  # Start with dark theme
    plt.rcParams.update({
        'font.family': ['Segoe UI', 'Arial'],
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 20,
        'xtick.labelsize': 10,
        'ytick.labelsize': 11,
        'axes.linewidth': 0,
        'axes.spines.left': False,
        'axes.spines.bottom': False,
        'axes.spines.top': False,
        'axes.spines.right': False,
    })
    
    # Set up the figure with dark background
    fig, ax = plt.subplots(figsize=(16, 10), dpi=100)
    fig.patch.set_facecolor('#1a1a1a')  # Dark background
    ax.set_facecolor('#1a1a1a')    # Create a custom color palette that includes #fec72f (yellow/gold)
    start_color = '#fec72f'  # Yellow/gold
    end_color = '#1e88e5'    # Blue
    custom_cmap = mpl.colors.LinearSegmentedColormap.from_list("custom", [start_color, end_color])
    
    # Create colors, with special color for "Other" if it exists
    if 'Other' in make_counts.index:
        colors = [custom_cmap(i) for i in np.linspace(0, 1, len(make_counts)-1)]
        # Add a distinct color for "Other" category
        colors.insert(0, '#666666')  # Gray color for "Other" at the bottom
    else:
        colors = [custom_cmap(i) for i in np.linspace(0, 1, len(make_counts))]
    
    # Create bars with rounded corners effect and shadow
    bars = ax.barh(make_counts.index, make_counts.values, 
                   color=colors[:len(make_counts)], 
                   height=0.7, alpha=0.9,
                   edgecolor='white', linewidth=0.5)
      # Add subtle shadow effect by creating offset bars
    shadow_bars = ax.barh(make_counts.index, make_counts.values, 
                         color='#404040', height=0.7, alpha=0.3,
                         left=make_counts.max() * 0.005)  # Slight offset for shadow
    
    # Move shadow bars behind main bars
    for shadow_bar in shadow_bars:
        shadow_bar.set_zorder(1)
    for bar in bars:
        bar.set_zorder(2)
    
    # Add elegant data labels with better positioning
    for i, (bar, value) in enumerate(zip(bars, make_counts.values)):
        # Add value labels inside bars for better readability
        label_x = bar.get_width() - (bar.get_width() * 0.05)
        ax.text(label_x, bar.get_y() + bar.get_height()/2, 
                f"{value:,}", 
                va='center', ha='right',
                fontsize=11, fontweight='600',
                color='white', alpha=0.95,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.6, edgecolor='none'))
          # Add percentage labels
        percentage = (value / make_counts.sum()) * 100
        ax.text(bar.get_width() + (make_counts.max() * 0.02), 
                bar.get_y() + bar.get_height()/2, 
                f"({percentage:.1f}%)", 
                va='center', ha='left',
                fontsize=10, fontweight='400',
                color='#CCCCCC', alpha=0.8)
    # Remove the frame and add minimal grid lines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid(axis='x', linestyle='-', alpha=0.1, color='#444444', linewidth=0.8)
    ax.set_axisbelow(True)
      # Set title and labels with modern typography
    plt.title('BO55 Plates by Manufacturer', 
              fontsize=24, fontweight='300', pad=30,
              color='#FFFFFF')
    plt.xlabel('Number of Vehicles', fontsize=13, labelpad=15, color='#CCCCCC', fontweight='400')
    plt.ylabel('Manufacturer', fontsize=13, labelpad=15, color='#CCCCCC', fontweight='400')
    
    # Modern tick styling
    ax.tick_params(axis='both', which='major', labelsize=11, colors='#CCCCCC', length=0)
    ax.tick_params(axis='x', pad=8)
    ax.tick_params(axis='y', pad=10)
    
    # Style y-axis labels with better formatting
    for label in ax.get_yticklabels():
        label.set_fontweight('500')
        label.set_color('#FFFFFF')
    
    # Style x-axis labels
    for label in ax.get_xticklabels():
        label.set_fontweight('400')
        label.set_color('#CCCCCC')
    
    # Adjust layout
    plt.tight_layout()
    
    # Add a sleek footer
    plt.figtext(0.5, 0.01, "Lisense Insights - Generated on " + pd.Timestamp.now().strftime("%Y-%m-%d"), 
                ha='center', fontsize=8, alpha=0.7, fontfamily='Arial', fontstyle='italic')    # Add lisense.uk data source attribution
    plt.figtext(0.12, 0.95, "Data Source: lisense.uk", 
                ha='left', fontsize=10, fontweight='bold', 
                color='#fec72f', alpha=0.9, fontfamily='Arial')
    
    # Add total count display in top right
    total_vehicles = len(df)
    plt.figtext(0.88, 0.95, f"Total Vehicles: {total_vehicles:,}", 
                ha='right', fontsize=12, fontweight='bold', 
                color='#FFFFFF', alpha=0.9, fontfamily='Arial')
    
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