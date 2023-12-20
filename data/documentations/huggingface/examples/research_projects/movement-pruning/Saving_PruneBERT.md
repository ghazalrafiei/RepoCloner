# Saving PruneBERT


This notebook aims at showcasing how we can leverage standard tools to save (and load) an extremely sparse model fine-pruned with [movement pruning](https://arxiv.org/abs/2005.07683) (or any other unstructured pruning mehtod).

In this example, we used BERT (base-uncased, but the procedure described here is not specific to BERT and can be applied to a large variety of models.

We first obtain an extremely sparse model by fine-pruning with movement pruning on SQuAD v1.1. We then used the following combination of standard tools:
- We reduce the precision of the model with Int8 dynamic quantization using [PyTorch implementation](https://pytorch.org/tutorials/intermediate/dynamic_quantization_bert_tutorial.html). We only quantized the Fully Connected Layers.
- Sparse quantized matrices are converted into the [Compressed Sparse Row format](https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html).
- We use HDF5 with `gzip` compression to store the weights.

We experiment with a question answering model with only 6% of total remaining weights in the encoder (previously obtained with movement pruning). **We are able to reduce the memory size of the encoder from 340MB (original dense BERT) to 11MB**, which fits on a [91' floppy disk](https://en.wikipedia.org/wiki/Floptical)!

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Floptical_disk_21MB.jpg/440px-Floptical_disk_21MB.jpg" width="200">

*Note: this notebook is compatible with `torch>=1.5.0` If you are using, `torch==1.4.0`, please refer to [this previous version of the notebook](https://github.com/huggingface/transformers/commit/b11386e158e86e62d4041eabd86d044cd1695737).*


```python
# Includes

import h5py
import os
import json
from collections import OrderedDict

from scipy import sparse
import numpy as np

import torch
from torch import nn

from transformers import *

os.chdir("../../")
```

## Saving

Dynamic quantization induces little or no loss of performance while significantly reducing the memory footprint.


```python
# Load fine-pruned model and quantize the model

model = BertForQuestionAnswering.from_pretrained("huggingface/prunebert-base-uncased-6-finepruned-w-distil-squad")
model.to("cpu")

quantized_model = torch.quantization.quantize_dynamic(
    model=model,
    qconfig_spec={
        nn.Linear: torch.quantization.default_dynamic_qconfig,
    },
    dtype=torch.qint8,
)
# print(quantized_model)

qtz_st = quantized_model.state_dict()
```


```python
# Saving the original (encoder + classifier) in the standard torch.save format

dense_st = {
    name: param for name, param in model.state_dict().items() if "embedding" not in name and "pooler" not in name
}
torch.save(
    dense_st,
    "dbg/dense_squad.pt",
)
dense_mb_size = os.path.getsize("dbg/dense_squad.pt")
```


```python
# Elementary representation: we decompose the quantized tensors into (scale, zero_point, int_repr).
# See https://pytorch.org/docs/stable/quantization.html

# We further leverage the fact that int_repr is sparse matrix to optimize the storage: we decompose int_repr into
# its CSR representation (data, indptr, indices).

elementary_qtz_st = {}
for name, param in qtz_st.items():
    if "dtype" not in name and param.is_quantized:
        print("Decompose quantization for", name)
        # We need to extract the scale, the zero_point and the int_repr for the quantized tensor and modules
        scale = param.q_scale()  # torch.tensor(1,) - float32
        zero_point = param.q_zero_point()  # torch.tensor(1,) - int32
        elementary_qtz_st[f"{name}.scale"] = scale
        elementary_qtz_st[f"{name}.zero_point"] = zero_point

        # We assume the int_repr is sparse and compute its CSR representation
        # Only the FCs in the encoder are actually sparse
        int_repr = param.int_repr()  # torch.tensor(nb_rows, nb_columns) - int8
        int_repr_cs = sparse.csr_matrix(int_repr)  # scipy.sparse.csr.csr_matrix

        elementary_qtz_st[f"{name}.int_repr.data"] = int_repr_cs.data  # np.array int8
        elementary_qtz_st[f"{name}.int_repr.indptr"] = int_repr_cs.indptr  # np.array int32
        assert max(int_repr_cs.indices) < 65535  # If not, we shall fall back to int32
        elementary_qtz_st[f"{name}.int_repr.indices"] = np.uint16(int_repr_cs.indices)  # np.array uint16
        elementary_qtz_st[f"{name}.int_repr.shape"] = int_repr_cs.shape  # tuple(int, int)
    else:
        elementary_qtz_st[name] = param
```

    Decompose quantization for bert.encoder.layer.0.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.0.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.0.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.0.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.0.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.0.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.1.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.1.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.1.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.1.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.1.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.1.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.2.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.2.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.2.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.2.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.2.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.2.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.3.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.3.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.3.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.3.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.3.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.3.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.4.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.4.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.4.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.4.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.4.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.4.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.5.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.5.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.5.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.5.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.5.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.5.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.6.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.6.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.6.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.6.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.6.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.6.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.7.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.7.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.7.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.7.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.7.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.7.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.8.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.8.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.8.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.8.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.8.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.8.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.9.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.9.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.9.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.9.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.9.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.9.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.10.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.10.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.10.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.10.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.10.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.10.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.11.attention.self.query._packed_params.weight
    Decompose quantization for bert.encoder.layer.11.attention.self.key._packed_params.weight
    Decompose quantization for bert.encoder.layer.11.attention.self.value._packed_params.weight
    Decompose quantization for bert.encoder.layer.11.attention.output.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.11.intermediate.dense._packed_params.weight
    Decompose quantization for bert.encoder.layer.11.output.dense._packed_params.weight
    Decompose quantization for bert.pooler.dense._packed_params.weight
    Decompose quantization for qa_outputs._packed_params.weight



```python
# Create mapping from torch.dtype to string description (we could also used an int8 instead of string)
str_2_dtype = {"qint8": torch.qint8}
dtype_2_str = {torch.qint8: "qint8"}
```


```python
# Saving the pruned (encoder + classifier) in the standard torch.save format

dense_optimized_st = {
    name: param for name, param in elementary_qtz_st.items() if "embedding" not in name and "pooler" not in name
}
torch.save(
    dense_optimized_st,
    "dbg/dense_squad_optimized.pt",
)
print(
    "Encoder Size (MB) - Sparse & Quantized - `torch.save`:",
    round(os.path.getsize("dbg/dense_squad_optimized.pt") / 1e6, 2),
)
```

    Encoder Size (MB) - Sparse & Quantized - `torch.save`: 21.29



```python
# Save the decomposed state_dict with an HDF5 file
# Saving only the encoder + QA Head

with h5py.File("dbg/squad_sparse.h5", "w") as hf:
    for name, param in elementary_qtz_st.items():
        if "embedding" in name:
            print(f"Skip {name}")
            continue

        if "pooler" in name:
            print(f"Skip {name}")
            continue

        if type(param) == torch.Tensor:
            if param.numel() == 1:
                # module scale
                # module zero_point
                hf.attrs[name] = param
                continue

            if param.requires_grad:
                # LayerNorm
                param = param.detach().numpy()
            hf.create_dataset(name, data=param, compression="gzip", compression_opts=9)

        elif type(param) == float or type(param) == int or type(param) == tuple:
            # float - tensor _packed_params.weight.scale
            # int   - tensor _packed_params.weight.zero_point
            # tuple - tensor _packed_params.weight.shape
            hf.attrs[name] = param

        elif type(param) == torch.dtype:
            # dtype - tensor _packed_params.dtype
            hf.attrs[name] = dtype_2_str[param]

        else:
            hf.create_dataset(name, data=param, compression="gzip", compression_opts=9)


with open("dbg/metadata.json", "w") as f:
    f.write(json.dumps(qtz_st._metadata))

size = os.path.getsize("dbg/squad_sparse.h5") + os.path.getsize("dbg/metadata.json")
print("")
print("Encoder Size (MB) - Dense:             ", round(dense_mb_size / 1e6, 2))
print("Encoder Size (MB) - Sparse & Quantized:", round(size / 1e6, 2))
```

    Skip bert.embeddings.word_embeddings.weight
    Skip bert.embeddings.position_embeddings.weight
    Skip bert.embeddings.token_type_embeddings.weight
    Skip bert.embeddings.LayerNorm.weight
    Skip bert.embeddings.LayerNorm.bias
    Skip bert.pooler.dense.scale
    Skip bert.pooler.dense.zero_point
    Skip bert.pooler.dense._packed_params.weight.scale
    Skip bert.pooler.dense._packed_params.weight.zero_point
    Skip bert.pooler.dense._packed_params.weight.int_repr.data
    Skip bert.pooler.dense._packed_params.weight.int_repr.indptr
    Skip bert.pooler.dense._packed_params.weight.int_repr.indices
    Skip bert.pooler.dense._packed_params.weight.int_repr.shape
    Skip bert.pooler.dense._packed_params.bias
    Skip bert.pooler.dense._packed_params.dtype
    
    Encoder Size (MB) - Dense:              340.26
    Encoder Size (MB) - Sparse & Quantized: 11.28



```python
# Save the decomposed state_dict to HDF5 storage
# Save everything in the architecutre (embedding + encoder + QA Head)

with h5py.File("dbg/squad_sparse_with_embs.h5", "w") as hf:
    for name, param in elementary_qtz_st.items():
        #         if "embedding" in name:
        #             print(f"Skip {name}")
        #             continue

        #         if "pooler" in name:
        #             print(f"Skip {name}")
        #             continue

        if type(param) == torch.Tensor:
            if param.numel() == 1:
                # module scale
                # module zero_point
                hf.attrs[name] = param
                continue

            if param.requires_grad:
                # LayerNorm
                param = param.detach().numpy()
            hf.create_dataset(name, data=param, compression="gzip", compression_opts=9)

        elif type(param) == float or type(param) == int or type(param) == tuple:
            # float - tensor _packed_params.weight.scale
            # int   - tensor _packed_params.weight.zero_point
            # tuple - tensor _packed_params.weight.shape
            hf.attrs[name] = param

        elif type(param) == torch.dtype:
            # dtype - tensor _packed_params.dtype
            hf.attrs[name] = dtype_2_str[param]

        else:
            hf.create_dataset(name, data=param, compression="gzip", compression_opts=9)


with open("dbg/metadata.json", "w") as f:
    f.write(json.dumps(qtz_st._metadata))

size = os.path.getsize("dbg/squad_sparse_with_embs.h5") + os.path.getsize("dbg/metadata.json")
print("\nSize (MB):", round(size / 1e6, 2))
```

    
    Size (MB): 99.41


## Loading


```python
# Reconstruct the elementary state dict

reconstructed_elementary_qtz_st = {}

hf = h5py.File("dbg/squad_sparse_with_embs.h5", "r")

for attr_name, attr_param in hf.attrs.items():
    if "shape" in attr_name:
        attr_param = tuple(attr_param)
    elif ".scale" in attr_name:
        if "_packed_params" in attr_name:
            attr_param = float(attr_param)
        else:
            attr_param = torch.tensor(attr_param)
    elif ".zero_point" in attr_name:
        if "_packed_params" in attr_name:
            attr_param = int(attr_param)
        else:
            attr_param = torch.tensor(attr_param)
    elif ".dtype" in attr_name:
        attr_param = str_2_dtype[attr_param]
    reconstructed_elementary_qtz_st[attr_name] = attr_param
    # print(f"Unpack {attr_name}")

# Get the tensors/arrays
for data_name, data_param in hf.items():
    if "LayerNorm" in data_name or "_packed_params.bias" in data_name:
        reconstructed_elementary_qtz_st[data_name] = torch.from_numpy(np.array(data_param))
    elif "embedding" in data_name:
        reconstructed_elementary_qtz_st[data_name] = torch.from_numpy(np.array(data_param))
    else:  # _packed_params.weight.int_repr.data, _packed_params.weight.int_repr.indices and _packed_params.weight.int_repr.indptr
        data_param = np.array(data_param)
        if "indices" in data_name:
            data_param = np.array(data_param, dtype=np.int32)
        reconstructed_elementary_qtz_st[data_name] = data_param
    # print(f"Unpack {data_name}")


hf.close()
```


```python
# Sanity checks

for name, param in reconstructed_elementary_qtz_st.items():
    assert name in elementary_qtz_st
for name, param in elementary_qtz_st.items():
    assert name in reconstructed_elementary_qtz_st, name

for name, param in reconstructed_elementary_qtz_st.items():
    assert type(param) == type(elementary_qtz_st[name]), name
    if type(param) == torch.Tensor:
        assert torch.all(torch.eq(param, elementary_qtz_st[name])), name
    elif type(param) == np.ndarray:
        assert (param == elementary_qtz_st[name]).all(), name
    else:
        assert param == elementary_qtz_st[name], name
```


```python
# Re-assemble the sparse int_repr from the CSR format

reconstructed_qtz_st = {}

for name, param in reconstructed_elementary_qtz_st.items():
    if "weight.int_repr.indptr" in name:
        prefix_ = name[:-16]
        data = reconstructed_elementary_qtz_st[f"{prefix_}.int_repr.data"]
        indptr = reconstructed_elementary_qtz_st[f"{prefix_}.int_repr.indptr"]
        indices = reconstructed_elementary_qtz_st[f"{prefix_}.int_repr.indices"]
        shape = reconstructed_elementary_qtz_st[f"{prefix_}.int_repr.shape"]

        int_repr = sparse.csr_matrix(arg1=(data, indices, indptr), shape=shape)
        int_repr = torch.tensor(int_repr.todense())

        scale = reconstructed_elementary_qtz_st[f"{prefix_}.scale"]
        zero_point = reconstructed_elementary_qtz_st[f"{prefix_}.zero_point"]
        weight = torch._make_per_tensor_quantized_tensor(int_repr, scale, zero_point)

        reconstructed_qtz_st[f"{prefix_}"] = weight
    elif (
        "int_repr.data" in name
        or "int_repr.shape" in name
        or "int_repr.indices" in name
        or "weight.scale" in name
        or "weight.zero_point" in name
    ):
        continue
    else:
        reconstructed_qtz_st[name] = param
```


```python
# Sanity checks

for name, param in reconstructed_qtz_st.items():
    assert name in qtz_st
for name, param in qtz_st.items():
    assert name in reconstructed_qtz_st, name

for name, param in reconstructed_qtz_st.items():
    assert type(param) == type(qtz_st[name]), name
    if type(param) == torch.Tensor:
        assert torch.all(torch.eq(param, qtz_st[name])), name
    elif type(param) == np.ndarray:
        assert (param == qtz_st[name]).all(), name
    else:
        assert param == qtz_st[name], name
```

## Sanity checks


```python
# Load the re-constructed state dict into a model

dummy_model = BertForQuestionAnswering.from_pretrained("bert-base-uncased")
dummy_model.to("cpu")

reconstructed_qtz_model = torch.quantization.quantize_dynamic(
    model=dummy_model,
    qconfig_spec=None,
    dtype=torch.qint8,
)

reconstructed_qtz_st = OrderedDict(reconstructed_qtz_st)
with open("dbg/metadata.json", "r") as read_file:
    metadata = json.loads(read_file.read())
reconstructed_qtz_st._metadata = metadata

reconstructed_qtz_model.load_state_dict(reconstructed_qtz_st)
```




    <All keys matched successfully>




```python
# Sanity checks on the infernce

N = 32

for _ in range(25):
    inputs = torch.randint(low=0, high=30000, size=(N, 128))
    mask = torch.ones(size=(N, 128))

    y_reconstructed = reconstructed_qtz_model(input_ids=inputs, attention_mask=mask)[0]
    y = quantized_model(input_ids=inputs, attention_mask=mask)[0]

    assert torch.all(torch.eq(y, y_reconstructed))
print("Sanity check passed")
```

    Sanity check passed



```python

```
