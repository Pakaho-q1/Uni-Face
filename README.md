<div align="center">

# ⚡ Uni-Face

**Fast · Clean · No-Fuss Face Swapping & Immich Integration**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-1.26-005CED?logo=onnx&logoColor=white)](https://onnxruntime.ai/)
[![TensorRT](https://img.shields.io/badge/TensorRT-Supported-76B900?logo=nvidia&logoColor=white)](https://developer.nvidia.com/tensorrt)
[![CUDA](https://img.shields.io/badge/CUDA-Supported-76B900?logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)

*Uni-Face is a speed-first face swap tool that delivers quality results with minimal configuration overhead. Optimized for NVIDIA GPUs with TensorRT, CUDA, and CPU fallback, featuring two-way Immich self-hosted photo management integration.*

</div>

---

## ✨ Highlights

| Feature | Detail |
|---|---|
| 🚀 **Speed-First Design** | Optimized pipeline with TensorRT → CUDA → CPU execution provider priority chain |
| ☁️ **Immich 2-Way Integration** | Import and export albums, people, and tags; instant 0 MB filesystem hardlinks; hash deduplication & unbounded pagination |
| 📱 **Mobile & Desktop Responsive** | Adaptive UI layout for smartphones, tablets, and desktop workstations |
| 👥 **Multi-Angle Face Models** | Extract and aggregate embeddings across multiple photos into `.safetensors` face models |
| 🎯 **Specific Face Target Filtering** | Scan targets and swap only selected faces based on cosine similarity threshold |
| 🧠 **Smart Memory Batching** | Dynamic size-based chunk hashing prevents memory overflow on massive datasets |
| 🗂️ **Target Sets & Bulk Exports** | Curate custom target sets; non-blocking streaming ZIP downloads |
| 🤖 **Multiple Swap Backends** | `inswapper_128` · `simswap_256` · `hyperswap` |
| ✨ **Face Enhancers** | `gfpgan_1.4` · `gpen_bfr_256/512` · `codeformer` · `RestoreFormer++` |
| 🎬 **Image & Video Support** | High-performance frame-by-frame video face swapping via FFmpeg (NVENC hardware acceleration) |

> **Design Philosophy:** Uni-Face trades configuration complexity for speed and usability. Sensible defaults are pre-baked in — you spend time swapping faces, not tuning parameters.

---

## 📋 Requirements

- **Operating System:** Windows 10/11 or Linux
- **GPU:** NVIDIA GPU with CUDA 12.x recommended (TensorRT supported)
- **VRAM:** 4 GB minimum (8 GB+ recommended for 4K video)
- **Python:** 3.10 or 3.11
- **Conda:** Miniconda / Anaconda

---

## 🚀 Quick Start

### 1 — Clone & Setup Environment

```bash
git clone https://github.com/Pakaho-q1/Uni-Face.git
cd uni-face

conda create -n uniface python=3.11 -y
conda activate uniface
```

### 2 — Run Native Installer

Install all Python dependencies and the Immich SDK:

```bash
# For NVIDIA GPU (CUDA / TensorRT acceleration):
python install.py cuda

# For CPU only:
python install.py
```

### 3 — Download AI Models

Fetch neural network weights automatically from Hugging Face with SHA-256 integrity verification:

```bash
python uni-face.py models install
```

### 4 — Launch Web UI

```bash
# Windows — Double-click or run:
run_uniface.bat

# Or run via Python:
python uni-face.py webui
```

Then open your browser at **http://localhost:8000** (or your local network IP on mobile devices).

---

## ☁️ Immich Integration

Uni-Face seamlessly connects with your self-hosted **[Immich](https://immich.app/)** server:

- **Target Import:** Browse Albums, Named People, and Tags from Immich and use them as swap targets directly.
- **⚡ Instant 0 MB Hardlinks:** When running on the same machine/drive as Immich, Uni-Face links original media via filesystem hardlinks (`os.link`) without duplicating storage.
- **Auto Deduplication:** Checks MD5 hashes against existing imports to skip re-downloading.
- **Auto-Save Exports:** Automatically upload processed swaps back to Immich with real file timestamps and assign them to custom Albums or Tags.

---

## ⚙️ Configuration (`uni-face.ini`)

Configure global defaults in `uni-face.ini`:

```ini
[GLOBAL]
providers = trt cuda cpu          # Execution provider fallback chain
execution_thread_count = 6        # Worker threads
video_encoder = h264_nvenc        # NVIDIA hardware encoder
server_port = 3000

[PROCESSORS]
processors = swap restore         # Active processors
swap_model = inswapper_128        # Swap backend
swap_weight = 0.80                # Blending weight (0.0–1.0)
swap_boost = 512                  # Processing resolution
mask_types = box                  # Mask strategy
restore_model = gpen_bfr_256      # Enhancer model
restore_weight = 0.8              # Enhancer strength
restore_blend = 100               # Blend strength (0–100)

[IMMICH]
url = http://localhost:2283       # Immich Server URL
api_key = your_immich_api_key     # Immich API Key
local_path = D:\immich\library    # Host path for instant Hardlinks (optional)
auto_save = false
new_album = false
album = 
tags = 
delete_local = false
```

---

## ⌨️ CLI Usage

```bash
conda activate uniface

# Swap single image
python uni-face.py cli --source path/to/source.jpg --target path/to/target.jpg --output output.jpg

# Swap video
python uni-face.py cli --source path/to/source.jpg --target path/to/video.mp4 --output output.mp4

# Start API Server
python uni-face.py serve --port 8000
```

---

## 🏗️ Architecture

```
uni-face/
├── uniface/              # Core Python package
│   ├── api/              # FastAPI routers (swap, jobs, face models, immich)
│   ├── cli/              # Command-line interface
│   ├── core/             # Business logic, pipeline, database, immich sync
│   ├── modules/          # Deep learning model wrappers (detectors, swappers, restorers)
│   └── api_server.py     # FastAPI application server
├── webui/                # React 19 + TypeScript + Tailwind CSS frontend
├── models/               # Model weights and hash integrity files
├── immich_sdk_repo/      # Open-source Immich Python client SDK
├── uni-face.py           # Unified launcher
├── install.py            # Automated installer
├── uni-face.ini          # Configuration file
└── run_uniface.bat       # Windows launcher
```

---

## ⚖️ Licenses & Terms of Use

The models utilized by this project originate from open-source research projects. **Their use is strictly bound by the original licenses.**

### Non-commercial research only
- `inswapper_128` / `inswapper_128_fp16`
- `simswap_256`
- `hyperswap` series
- `arcface` (`w600k_r50`)
- `gfpgan_1.4`
- `codeformer`
- `RestoreFormerPlusPlus`

### Permissive
- `yoloface_8n`
- `bisenet_resnet_34`

---

## ⚠️ Legal Disclaimer

**Responsibility of Use**: The creators and maintainers of this repository assume no liability for how this software is used. By using this tool, you agree to comply with all applicable local, national, and international laws, respect individual privacy and consent, and take full ethical and legal responsibility for generated content.

---

## 📄 License

This software codebase is licensed under the [MIT License](LICENSE).
