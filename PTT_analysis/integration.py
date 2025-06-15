import matplotlib.pyplot as plt

# turn the analysis data into vector form
def extract(analysis: dict) -> tuple:
    x, y, z = analysis["評論風向"], analysis["氛圍"], analysis["網軍介入可能性"]
    return (x, y, z)

# draw a 3D scatter plot of the analysis data
def plot(data: list) -> None:
    x = [point[0] for point in data]
    y = [point[1] for point in data]
    z = [point[2] for point in data]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='blue', marker='o')

    ax.set_xlabel('Comment Direction')
    ax.set_ylabel('Atmosphere')
    ax.set_zlabel('Troll Interference Probability')
    plt.title("Relationship Scatter Plot of Analysis Data")
    plt.grid(True)

    plt.show()
