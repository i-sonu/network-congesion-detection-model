# Network Congestion Detection Model

This project watch the network and tell if it is congested. It ping a machine again and again and note down how long the ping take and how many packets get lost. Then it use that data to train a machine learning model. After training, the model look at live ping numbers and say if network is normal or congested right now. So basically, it is a simple tool that learn from ping data and warn you when the network get busy.
