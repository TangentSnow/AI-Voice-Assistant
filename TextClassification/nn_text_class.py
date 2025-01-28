import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import joblib


class TextClassificationModel(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(TextClassificationModel, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)
        
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)
        return x
    
class TextClassifier:
    def __init__(self):
        self.vectorizer = joblib.load("TextClassification/models/tfidf_vectorizer.pkl")
        self.label_encoder = joblib.load("TextClassification/models/label_encoder.pkl")
        self.classifier = TextClassificationModel(input_dim=3809, output_dim=81)
        self.classifier.load_state_dict(torch.load('TextClassification/models/nn_text_class.pth', weights_only=True))
        self.classifier.eval()
        
    def preprocess(self, text):
        vectors = self.vectorizer.transform([text]).toarray()
        return torch.tensor(vectors, dtype=torch.float32)
    
    def predict(self, text):
        with torch.no_grad():
            inputs = self.preprocess(text)
            pred = torch.argmax(self.classifier(inputs), dim=1)
            
        return self.label_encoder.inverse_transform(pred.numpy())[0]