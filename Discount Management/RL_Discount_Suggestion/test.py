# import torch.nn as nn

# class SimpleModel(nn.Module):
#     def __init__(self):
#         super(SimpleModel, self).__init__()
#         self.fc = nn.Linear(10, 1)

#     def forward(self, x):
#         return self.fc(x)

# model = SimpleModel()
# print("✅ Simple model works fine")

import torch
print(torch.__version__)
print(torch.cuda.is_available())  # Check if CUDA is detected (if using GPU)
