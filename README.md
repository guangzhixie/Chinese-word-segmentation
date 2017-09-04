# Chinese Word Segmentation

Data set downloaded from http://sighan.cs.uchicago.edu/bakeoff2005/

1. cws_maxent.ipynb: Word segmentation implemented using Maximum Entropy model
2. cws_rnn.ipynb: Word segmentation implemented using RNN with bi-directional LSTM
3. cws.ipynb: Cleaned up notebook

Model Accuracy Comparison
| Training Set | Test Set  | Accuracy - MaxEnt  | Accuracy - RNN |
| :----------: | :-------: | :----------------: | :------------: |
| PKU          | PKU       | 0.94               | 0.91           |
| MSR          | MSR       | 0.92               | 0.96           |
| PKU          | MSR       | 0.86               | 0.86           |
| MSR          | PKU       | 0.88               | 0.84           |
| PKU+MSR      | PKU+MSR   | 0.91               | 0.91           |
