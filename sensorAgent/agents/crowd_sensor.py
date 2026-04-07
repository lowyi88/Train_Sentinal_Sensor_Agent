from anomalib.data import Folder
from anomalib.models import Padim
from anomalib.engine import Engine
from sklearn.metrics import precision_recall_curve
import numpy as np

def main():
    dataset = Folder(
        name="platform",
        root="C:\\Users\\yi_li\\OneDrive\\Desktop\\Train_Sentinal_Sensor_Agent\\platform",
        normal_dir="Normal",      # training images
        abnormal_dir="test\\Abnormal", # optional anomalies for evaluation
        num_workers=23    
    )

    model = Padim()
    engine = Engine(accelerator="cpu", devices=1)
    engine.fit(model=model, datamodule=dataset)

    y_true = []
    y_scores = []

    # Run inference on the test set
    results = engine.predict(datamodule=dataset)
    for batch in results:
        y_true.extend(batch.gt_label.cpu().numpy())     # ground truth labels
        y_scores.extend(batch.pred_score.cpu().numpy()) # anomaly scores

    precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
    f1_scores = np.divide(
        2 * precision * recall,
        precision + recall,
        out=np.zeros_like(precision),
        where=(precision + recall) != 0
    )
    best_threshold = thresholds[np.argmax(f1_scores)]
    print("Best threshold:", best_threshold)
    binary_preds = (np.array(y_scores) >= best_threshold).astype(int)

    for score, label, pred in zip(y_scores, y_true, binary_preds):
        score = float(score)   # convert numpy scalar/array to Python float
        label = int(label)     # ensure label is int
        pred = int(pred)       # ensure prediction is int
        print(f"Score={score:.4f}, True={label}, Pred={pred}")

 
if __name__ == "__main__":
    main()
