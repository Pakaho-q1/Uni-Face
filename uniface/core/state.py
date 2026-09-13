import configparser
import argparse
import os
from typing import List
from uniface.core.config import ROOT_DIR

class StateManager:
    def __init__(self):
        self.providers = ["CPUExecutionProvider"]
        self.auth = None
        
        # Add ONNX SessionOptions to prevent thread thrashing
        import onnxruntime
        self.session_options = onnxruntime.SessionOptions()
        # Limit CPU threads used by ONNX internal ops (1 or 2 is ideal when running concurrent pipelines)
        self.session_options.intra_op_num_threads = 1
        self.session_options.inter_op_num_threads = 1
        
        self.processors = ["swap", "restore", "color"]
        self.execution_thread_count = 4
        self.video_encoder = "h264_nvenc"
        self.server_port = 8000
        self.log_level = "warning"
        self._cli_log_level = None
        
        self.swap_model = "inswapper_128"
        self.swap_weight = 0.65
        self.mask_types = ["box"]
        self.occlusion_model = "xseg_1"
        
        self.restore_model = "gfpgan_1.4"
        self.restore_weight = 1.0
        self.restore_blend = 100

        self.source_path = None
        self.target_path = None
        self.output_path = None
        self.mask_types: List[str] = ['box']
        self.mask_regions: List[str] = ['skin', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 'nose', 'mouth', 'u_lip', 'l_lip']
        self.occlusion_model: str = "xseg_1"
        self.target_gender: str = "all"
        self.face_order: str = "largest"
        self.similarity: bool = False
        self.reference_face_ids: List[str] = []
        self.reference_threshold: float = 0.6
        self.face_detector_score: float = 0.65
        self.face_landmark_score: float = 0.50
        
        # Immich Settings
        self.immich_url: str = ""
        self.immich_api_key: str = ""
        self.immich_auto_save: bool = False
        self.immich_new_album: bool = False
        self.immich_album: str = ""
        self.immich_tags: List[str] = []
        self.immich_delete_local: bool = False

    def set_log_level(self, level: str):
        from uniface.core.logging import setup_logging
        self._cli_log_level = level.strip().lower()
        self.log_level = self._cli_log_level
        setup_logging(level=self.log_level)

    def init(self, parse_args=True):
        ini_path = ROOT_DIR / "uni-face.ini"
        config = configparser.ConfigParser()
        if os.path.exists(ini_path):
            config.read(ini_path)
            if "GLOBAL" in config:
                if "providers" in config["GLOBAL"]:
                    self._parse_providers(config["GLOBAL"]["providers"])
                if "execution_thread_count" in config["GLOBAL"]:
                    self.execution_thread_count = int(config["GLOBAL"]["execution_thread_count"])
                if "video_encoder" in config["GLOBAL"]:
                    self.video_encoder = config["GLOBAL"]["video_encoder"]
                if "server_port" in config["GLOBAL"]:
                    self.server_port = int(config["GLOBAL"]["server_port"])
                if "auth" in config["GLOBAL"]:
                    self.auth = config["GLOBAL"]["auth"]
                if "log_level" in config["GLOBAL"] and not self._cli_log_level:
                    self.log_level = config["GLOBAL"]["log_level"].strip().lower()
            if "PROCESSORS" in config:
                p = config["PROCESSORS"]
                if "processors" in p: self.processors = p["processors"].split()
                if "swap_model" in p: self.swap_model = p["swap_model"]
                if "swap_weight" in p: self.swap_weight = float(p["swap_weight"])
                if "mask_types" in p: self.mask_types = p["mask_types"].split()
                if "occlusion_model" in p: self.occlusion_model = p["occlusion_model"]
                if "target_gender" in p: self.target_gender = p["target_gender"]
                if "face_order" in p: self.face_order = p["face_order"]
                if "restore_model" in p: self.restore_model = p["restore_model"]
                if "restore_weight" in p: self.restore_weight = float(p["restore_weight"])
                if "restore_blend" in p: self.restore_blend = int(p["restore_blend"])
                if "face_detector_score" in p: self.face_detector_score = float(p["face_detector_score"])
                if "face_landmark_score" in p: self.face_landmark_score = float(p["face_landmark_score"])
            
            if "IMMICH" in config:
                i = config["IMMICH"]
                if "url" in i: self.immich_url = i["url"].strip()
                if "api_key" in i: self.immich_api_key = i["api_key"].strip()
                if "auto_save" in i: self.immich_auto_save = i["auto_save"].lower() == "true"
                if "new_album" in i: self.immich_new_album = i["new_album"].lower() == "true"
                if "album" in i: self.immich_album = i["album"].strip()
                if "tags" in i: self.immich_tags = [t for t in i["tags"].split(",") if t.strip()]
                if "delete_local" in i: self.immich_delete_local = i["delete_local"].lower() == "true"

        from uniface.core.logging import setup_logging
        setup_logging(level=self.log_level)

        if not parse_args:
            return

        parser = argparse.ArgumentParser(description="Uni-Face Pipeline")
        parser.add_argument("-s", "--source", required=True)
        parser.add_argument("-t", "--target", required=True)
        parser.add_argument("-o", "--output", required=True)
        parser.add_argument("--similarity", action="store_true")
        
        parser.add_argument("--providers", nargs="+")
        parser.add_argument("--execution_thread_count", type=int)
        parser.add_argument("--video_encoder", type=str)
        parser.add_argument("--processors", nargs="+")
        parser.add_argument("--swap_model", type=str)
        parser.add_argument("--swap_weight", type=float)
        parser.add_argument("--mask_types", nargs="+", type=str)
        parser.add_argument("--restore_model", type=str)
        parser.add_argument("--restore_weight", type=float)
        parser.add_argument("--restore_blend", type=int)
        parser.add_argument("--face-detector-score", "--face_detector_score", type=float, dest="face_detector_score")
        parser.add_argument("--face-landmark-score", "--face_landmark_score", type=float, dest="face_landmark_score")
        parser.add_argument("--log-level", choices=["debug", "info", "warning", "error"], type=str.lower)
        parser.add_argument("--log-info", action="store_true", help="Enable INFO logging")
        parser.add_argument("--log-debug", action="store_true", help="Enable DEBUG logging")
        
        args = parser.parse_args()
        
        self.source_path = args.source
        self.target_path = args.target
        self.output_path = args.output
        self.similarity = args.similarity
        
        if args.providers: self._parse_providers(" ".join(args.providers))
        if args.execution_thread_count is not None: self.execution_thread_count = args.execution_thread_count
        if args.video_encoder: self.video_encoder = args.video_encoder
        if args.processors: self.processors = args.processors
        if args.swap_model is not None: self.swap_model = args.swap_model
        if args.swap_weight is not None: self.swap_weight = args.swap_weight
        if args.mask_types is not None: self.mask_types = args.mask_types
        if args.restore_model: self.restore_model = args.restore_model
        if args.restore_weight is not None: self.restore_weight = args.restore_weight
        if args.restore_blend is not None: self.restore_blend = args.restore_blend
        if getattr(args, "face_detector_score", None) is not None: self.face_detector_score = args.face_detector_score
        if getattr(args, "face_landmark_score", None) is not None: self.face_landmark_score = args.face_landmark_score

        if getattr(args, 'log_debug', False):
            self.set_log_level("debug")
        elif getattr(args, 'log_info', False):
            self.set_log_level("info")
        elif getattr(args, 'log_level', None):
            self.set_log_level(args.log_level)

    def parse_providers(self, provider_str: str) -> list:
        mapping = {
            "trt": "TensorrtExecutionProvider",
            "cuda": "CUDAExecutionProvider",
            "cpu": "CPUExecutionProvider"
        }
        import onnxruntime
        cache_path = os.path.join(ROOT_DIR, '.caches', onnxruntime.get_version_string())
        
        providers = []
        for p in provider_str.split():
            provider_name = mapping.get(p.lower())
            if not provider_name:
                continue
                
            if provider_name == 'TensorrtExecutionProvider':
                os.makedirs(cache_path, exist_ok=True)
                trt_options = {
                    'trt_engine_cache_enable': True,
                    'trt_engine_cache_path': cache_path,
                    'trt_timing_cache_enable': True,
                    'trt_timing_cache_path': cache_path,
                    'trt_builder_optimization_level': 4
                }
                cuda_options = {
                    'cudnn_conv_algo_search': 'DEFAULT'
                }
                providers = [(provider_name, trt_options), ('CUDAExecutionProvider', cuda_options), 'CPUExecutionProvider']
                break
            elif provider_name == 'CUDAExecutionProvider':
                cuda_options = {
                    'cudnn_conv_algo_search': 'DEFAULT'
                }
                providers = [(provider_name, cuda_options), 'CPUExecutionProvider']
                break
            else:
                providers = ['CPUExecutionProvider']
                break
                
        if not providers:
            providers = ["CPUExecutionProvider"]
            
        self.providers = providers
        return providers

    def _parse_providers(self, provider_str: str) -> list:
        return self.parse_providers(provider_str)

state = StateManager()

