from sklearn.ensemble import RandomForestClassifier

def create_model():
    """
    Creates and returns the machine learning model.
    
    We are using a RandomForestClassifier for a few key reasons:
    1.  **Powerful:** It's an "ensemble" model (a "forest" of many "trees") 
        and is very effective at finding complex patterns, which is perfect 
        for text classification.
    2.  **Robust:** It's less prone to overfitting on noisy data compared to 
        a single decision tree.
    3.  **Easy to Use:** It doesn't require a lot of complex "hyperparameter tuning"
        to get a good, working result for a first version.
    """
    
    model = RandomForestClassifier(
        n_estimators=100,  # This is the number of "trees" in the forest. 100 is a good default.
        random_state=42,   # This ensures you get the same results every time you run the script.
        n_jobs=-1          # This tells the model to use all available CPU cores to train faster.
    )
    
    return model