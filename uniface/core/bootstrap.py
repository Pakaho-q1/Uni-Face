import os
import sys

def initialize_environment():
    """
    Bootstrap runtime environment:
    1. Auto-inject TensorRT library path on Windows into PATH.
    2. Disable BLAS/OMP threading to prevent thread thrashing during concurrent pipeline tasks.
    3. Register NumPy encoders with FastAPI jsonable_encoder if fastapi is present.
    """
    # 1. TRT Support: Auto-inject TensorRT libs into PATH
    if sys.platform == 'win32':
        trt_path = os.path.join(sys.prefix, 'Lib', 'site-packages', 'tensorrt_libs')
        if os.path.exists(trt_path):
            os.environ['PATH'] = trt_path + os.pathsep + os.environ.get('PATH', '')
        else:
            python_id = f"python{sys.version_info.major}.{sys.version_info.minor}"
            trt_path = os.path.join(sys.prefix, 'lib', python_id, 'site-packages', 'tensorrt_libs')
            if os.path.exists(trt_path):
                os.environ['LD_LIBRARY_PATH'] = trt_path + os.pathsep + os.environ.get('LD_LIBRARY_PATH', '')

    # 2. Disable BLAS/OMP threading to prevent CPU thrashing
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
    os.environ["NUMEXPR_NUM_THREADS"] = "1"

    # 3. Register NumPy encoders globally to prevent jsonable_encoder TypeError
    try:
        import numpy as np
        from fastapi.encoders import ENCODERS_BY_TYPE
        ENCODERS_BY_TYPE[np.bool_] = bool
        for _int_t in (np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64):
            ENCODERS_BY_TYPE[_int_t] = int
        for _float_t in (np.float16, np.float32, np.float64):
            ENCODERS_BY_TYPE[_float_t] = float
        ENCODERS_BY_TYPE[np.ndarray] = lambda x: x.tolist()
    except (ImportError, Exception):
        pass
