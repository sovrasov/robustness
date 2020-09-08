import torch
from torch import nn
ch = torch

class FakeReLU6(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        return input.clamp(min=0, max=6)

    @staticmethod
    def backward(ctx, grad_output):
        return grad_output

class FakeReLU(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input):
        return input.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        return grad_output


class FakeReLU6M(nn.Module):
    def forward(self, x):
        return FakeReLU6.apply(x)


class FakeReLUM(nn.Module):
    def forward(self, x):
        return FakeReLU.apply(x)

class SequentialWithArgs(torch.nn.Sequential):
    def forward(self, input, *args, **kwargs):
        vs = list(self._modules.values())
        l = len(vs)
        for i in range(l):
            if i == l-1:
                input = vs[i](input, *args, **kwargs)
            else:
                input = vs[i](input)
        return input
