import matplotlib.pyplot as plt

# turn the analysis data into vector form
def convert(analysis: dict) -> tuple:
    x, y, z = analysis["評論風向"], analysis["氛圍"], analysis["網軍介入可能性"]
    
    # map the adjectives to numerical values
    mapping = {"正面": 1, "負面": 0, "中立": 0.5, 
               "和諧": 1, "正常": 0.6, "緊張": 0.3, "對立": 0}
    
    x = mapping.get(x, 0.5)  # Default to 0.5 if not found
    y = mapping.get(y, 0.5)  # Default to 0.5 if not found

    return (x, y, z)

# draw a 3D scatter plot of the analysis data
def plot(data: list) -> None:
    x = [point[0] for point in data]
    y = [point[1] for point in data]
    z = [point[2] for point in data]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='blue', marker='o')

    ax.set_xlabel('Comment Direction (Negative=0, Neutral=0.5, Positive=1)')
    ax.set_ylabel('Atmosphere (Confrontation=0, Tension=0.3, Normal=0.6, Harmony=1)')
    ax.set_zlabel('Troll Interference Probability(0~1)')
    plt.title("Relationship Scatter Plot of Analysis Data")
    plt.grid(True)

    plt.show()