import dill as pickle
import os

json_path = os.path.join("/home/ubuntu/brain_tumor_seg/output.json")

with open('train_dataset.pkl', 'wb') as f:
    pickle.dump(json_path, f)
    