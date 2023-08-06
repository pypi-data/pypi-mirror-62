#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

from onnxmltools import load_model
from onnxmltools import save_model
from onnxmltools.utils import visualize_model
from onnxmltools.utils import convert_float_to_float16

from .quantize import quantize