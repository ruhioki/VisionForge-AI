# ONNX image-classification model compatibility

VisionForge's optional `classify` command is an inference wrapper for compatible image-classification models. It does not train models, download weights, or include model files.

## Expected model interface

The current preprocessing is designed for ImageNet-style classifiers:

- One float32 input tensor in NCHW layout: `[1, 3, height, width]`.
- Three RGB channels.
- RGB values scaled to 0..1, then normalized with ImageNet mean `[0.485, 0.456, 0.406]` and standard deviation `[0.229, 0.224, 0.225]`.
- A classification output containing one score per class for a batch of one image.
- A separate UTF-8 text file with exactly one class label per line, in the same order as the model output.

Fixed spatial dimensions are read from the model input. If height or width is dynamic, VisionForge uses 224 for that dimension. Models that expect different color conventions, normalization, input layouts, multiple required inputs, or specialized postprocessing are not compatible without changing the preprocessing code.

## Run classification

Install the optional CPU runtime:

```powershell
python -m pip install -e ".[onnx]"
```

Prepare your own compatible ONNX model and matching labels file, then run:

```powershell
visionforge classify "images\\sample.jpg" --model "models\\classifier.onnx" --labels "models\\labels.txt" --top-k 5 --provider auto
```

The JSON output contains class index, label, and normalized confidence for each top prediction. The confidence is derived by applying softmax to the model's output scores, so use it only when that interpretation is appropriate for your model.

## CPU and CUDA

- `--provider cpu`: use the CPU execution provider.
- `--provider auto`: prefer CUDA if the installed ONNX Runtime exposes `CUDAExecutionProvider`, otherwise use CPU.
- `--provider cuda`: require CUDA and return a clear error if the provider is unavailable.

For CUDA, install an `onnxruntime-gpu` build compatible with your operating system, GPU driver, CUDA, and cuDNN versions. Replace the CPU `onnxruntime` package rather than installing both packages into the same environment. Consult the official ONNX Runtime installation and compatibility documentation for your platform before changing packages.

## Model and label licensing

Model weights, label maps, and training datasets may have separate licenses and restrictions. Check the license, attribution requirements, permitted use, and redistribution terms for every file you obtain. Keep large model files out of Git unless their license and repository size make that appropriate.

## Troubleshooting

- **Output class count does not match labels:** use the exact class list associated with the model, preserving its class order.
- **Unexpected predictions:** verify preprocessing, class order, input resolution, and whether the model outputs logits or probabilities.
- **CUDA provider unavailable:** confirm that the GPU runtime and its CUDA/cuDNN dependencies match your system; otherwise use `--provider cpu`.
- **Input shape error:** this command currently expects a single-image, four-dimensional NCHW model input.
