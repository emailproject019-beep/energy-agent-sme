# agents/models/forecast.py
import torch
import torch.nn as nn

class EnergySpikePredictor(nn.Module):
    """Neural Network targeting future tariff rate spikes."""
    def __init__(self, input_dim=3, hidden_dim=64, num_layers=2):
        super(EnergySpikePredictor, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True)
        # Output layers predicting tariff rate and probability of a spike
        self.fc = nn.Linear(hidden_dim, 1) 
        
    def forward(self, x):
        # x shape: (batch_size, sequence_length, input_features)
        lstm_out, _ = self.lstm(x)
        predictions = self.fc(lstm_out[:, -1, :]) # Take the last time-step
        return predictions

if __name__ == "__main__":
    # Standard training entry point executed by the Gensyn compute node
    print("Gensyn node initialized training loop for SME Energy Agent...")
    # (Data loading, forward pass, loss calculation, backprop happens here)
