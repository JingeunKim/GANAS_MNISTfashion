import torch
from torchviz import make_dot
import dataloader
import pytorch_model_summary
from Configure import params_settings
use_mps = torch.backends.mps.is_available()
device = torch.device("mps" if use_mps else "cpu")
print(device)
# model = torch.load("./"+params_settings.model_name+".pt")
# model = model.to(device)
model = torch.load("./"+params_settings.load_model_name+".pt")
print(model)
trainloader, testloader = dataloader.data_loader()
for i, data in enumerate(trainloader, 0):
    inputs, labels = data
    inputs = inputs.to(device)
    labels = labels

make_dot(model(inputs), params=dict(model.named_parameters())).render(params_settings.load_model_name, format="png")

params = model.state_dict()
torch.onnx.export(model, inputs, params_settings.load_model_name+".onnx")

print(pytorch_model_summary.summary(model, inputs, show_input=False))
