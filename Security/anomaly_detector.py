import numpy as np  
from scipy import stats
import pandas as pd 
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt


class AnomalyDetector:
    """
    A class for detecting anomalies in network traffic or system log data using Isolation Forest.
    
    This class provides a complete pipeline for anomaly detection, including data loading,
    preprocessing, model training, anomaly detection, and result visualization.
    """

    def __init__(self, data_src, threshold=0.95):
        """
        Initialize the AnomalyDetector.

        Args:
            data_src (str): Source of the data (e.g., "network_traffic")
            threshold (float): Threshold for anomaly detection (default: 0.95)
        """
        self.data_src = data_src
        self.threshold = threshold
        self.model = IsolationForest(contamination=0.1, random_state=42)

    def load_data(self):
        """
        Load data from the specified source.
        
        Note: This implementation generates synthetic data for demonstration.
        In a real-world scenario, this method should be modified to load actual data.
        """
        np.random.seed(42)
        n_samples = 1000
        normal_data = np.random.normal(loc=0, scale=1, size=(n_samples, 2))
        anomalies = np.random.uniform(low=4, high=4, size=(int(n_samples * 0.1), 2))
        self.data = np.vstack((normal_data, anomalies))

    def preprocess_data(self):
        """
        Preprocess the loaded data by applying z-score normalization.
        """
        self.normalized_data = stats.zscore(self.data)
    
    def train_model(self):
        """
        Train the Isolation Forest model on the preprocessed data.
        """
        self.model.fit(self.normalized_data)
    
    def detect_anomalies(self):
        """
        Detect anomalies in the data using the trained model and specified threshold.
        """
        anomaly_scores = self.model.decision_function(self.normalized_data)
        self.anomalies = anomaly_scores < -self.threshold

    def visualize_results(self):
        """
        Visualize the anomaly detection results using a scatter plot.

        Red points represent detected anomalies, while blue points represent normal data.
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(self.data[~self.anomalies, 0], self.data[~self.anomalies, 1], 
                    label='Normal', alpha=0.7)
        plt.scatter(self.data[self.anomalies, 0], self.data[self.anomalies, 1], 
                    color='red', label='Anomaly', alpha=0.7)
        plt.title('Anomaly Detection Results')
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.legend()
        plt.show()

    def run(self):
        """
        Execute the complete anomaly detection pipeline.

        This method runs all steps of the process: data loading, preprocessing,
        model training, anomaly detection, and result visualization.
        """
        print("Loading Data...")
        self.load_data()

        print("Preprocessing data...")
        self.preprocess_data()

        print("Training model...")
        self.train_model()

        print("Detecting anomalies...")
        self.detect_anomalies()
        
        print("Visualizing results...")
        self.visualize_results()

        anomaly_count = np.sum(self.anomalies)
        print(f"Detected {anomaly_count} anomalies out of {len(self.data)} data points.")


if __name__ == "__main__":
    # Example usage of the AnomalyDetector class
    detector = AnomalyDetector(data_src="network_traffic", threshold=0.95)
    detector.run()
