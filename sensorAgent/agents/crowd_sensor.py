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

    results1 = engine.predict(data_path="C:\\Users\\yi_li\\OneDrive\\Desktop\\Train_Sentinal_Sensor_Agent\\platform_eval\\Normal")
    for batch in results1:
        # Access the image path
        file_name = batch.image_path
        score = batch.pred_score.item()  # convert tensor to float
        label = batch.pred_label.item()  # 0 = normal, 1 = abnormal

        if (label == 1) or (score > best_threshold):
            print("Best threshold:", best_threshold)
            print("Abnormal detected:", file_name, "with score:", score)
 
if __name__ == "__main__":
    main()
