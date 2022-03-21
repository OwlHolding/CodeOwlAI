
import pandas as pd 

def errors_to_train(file_path, target_file_path, rewrite=True):
    db = pd.read_csv("/content/Dataset.csv")
    db.drop(columns=["Unnamed: 0"], inplace=True)
    db.rename(columns={"0": "error"}, inplace=True)
    instances = []
    for i in range(len(db['answer'])):
        instance = f"<s>Error: {db['error'][i]} \n Answer: {db['answer'][i]}</s>" 
        instances.append(instance)
    with open(target_file_path, 'w' if rewrite else 'a') as f:
      f.write('\n'.join(instances).replace("&lt", "").replace("&gt", "").replace("&quot", ""))