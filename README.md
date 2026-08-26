<div align="center">

# ⚡ Uni-Face

**Fast · Clean · No-Fuss Face Swapping**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![ONNX Runtime](https://img.shields.io/badge/ONNX_Runtime-1.26-005CED?logo=onnx&logoColor=white)](https://onnxruntime.ai/)
[![TensorRT](https://img.shields.io/badge/TensorRT-Supported-76B900?logo=nvidia&logoColor=white)](https://developer.nvidia.com/tensorrt)
[![CUDA](https://img.shields.io/badge/CUDA-Supported-76B900?logo=nvidia&logoColor=white)](https://developer.nvidia.com/cuda-toolkit)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)

*Uni-Face is a speed-first face swap tool that delivers quality results with minimal configuration overhead. Optimized for NVIDIA GPUs with TensorRT, CUDA, and CPU fallback.*

</div>

---

## ✨ Highlights

| Feature | Detail |
|---|---|
| 🚀 **Speed-first design** | Optimized pipeline with TRT → CUDA → CPU execution provider chain |
| 🖥️ **Web UI** | React 19 + Tailwind CSS frontend, no browser extension needed |
| ⌨️ **CLI** | Full command-line interface for scripting and automation |
| 🔧 **Config-driven** | Swap backends, enhancers, and providers swappable via `uni-face.ini` |
| 🤖 **Multiple swap backends** | inswapper · simswap · hyperswap |
| ✨ **Face enhancement** | GFPGAN · GPEN-BFR · CodeFormer · RestoreFormer++ |
| 🎬 **Image & Video** | Single images or full video files via FFmpeg |

> **Design Philosophy:** Uni-Face trades configuration flexibility for speed. Sensible defaults are pre-baked in — you spend time swapping faces, not tuning parameters.

---

## 📋 Requirements

- **OS:** Windows 10/11 (Linux support planned)
- **GPU:** NVIDIA GPU with CUDA 12.x (recommended)
- **VRAM:** 4 GB minimum, 8 GB+ recommended for video
- **Python:** 3.10+
- **Conda:** Anaconda / Miniconda

---

## 🚀 Quick Start

### 1 — Clone & Setup Environment

```bash
git clone https://github.com/Pakaho-q1/Uni-Face.git
cd uni-face

conda create -n uniface python=3.10 -y
conda activate uniface
```

### 2 — Install Dependencies & WebUI

Run the native installer. It will install all required Python libraries.

```bash
python install.py
```
> **Note:** If you want hardware acceleration, you can run `python install.py cuda` or `python install.py tensorrt`.

### 3 — Download Models

Uni-Face includes an automated model manager that fetches the required models from Hugging Face and verifies their integrity via SHA256 hashes.

```bash
python uni-face.py models install
```

### 4 — Launch Web UI

```bash
# Windows — double-click or run in terminal:
run_uniface.bat

# Or manually via CLI:
conda activate uniface
python uni-face.py webui
```

Then open your browser at **http://localhost:8000**

---

## 🖥️ Web UI

The Web UI is built with **React 19** + **TypeScript** + **Tailwind CSS** + **shadcn/ui** components, served by a **FastAPI** backend.

**Workflow:**
1. Upload a **source face** image
2. Upload a **target** image or video
3. Hit **Swap** — done

No installation of the frontend is required for end users — the built assets are served directly by the API server.

### Dev Mode (contributors)

```bash
cd webui
npm install
npm run dev
```

---

## ⌨️ CLI Usage

```bash
conda activate uniface
python main.py cli --help
```

### Swap a single image

```bash
python main.py cli \
  --source path/to/source.jpg \
  --target path/to/target.jpg \
  --output path/to/output.jpg
```

### Swap a video

```bash
python main.py cli \
  --source path/to/source.jpg \
  --target path/to/video.mp4 \
  --output path/to/output.mp4
```

### Start API server

```bash
python main.py serve --port 8000
```

---

## ⚙️ Configuration

Edit `uni-face.ini` to change global defaults:

```ini
[GLOBAL]
providers = trt cuda cpu          # Execution provider priority
execution_thread_count = 6        # Worker threads
video_encoder = h264_nvenc        # NVIDIA hardware encoder

[PROCESSORS]
processors = swap restore         # Active processors
swap_model = inswapper_128        # Swap backend
swap_weight = 0.80                # Swap blending weight (0.0–1.0)
swap_boost = 512                  # Internal processing resolution
mask_types = box                  # Mask strategy
restore_model = gpen_bfr_256      # Enhancer model
restore_weight = 0.8              # Enhancer blending weight (0.0–1.0)
restore_blend = 100               # Blend strength (0–100)
```

### Execution Providers

Uni-Face automatically falls back through the provider chain:

```
TensorRT  →  CUDA  →  CPU
```

Set `providers` in `uni-face.ini` to restrict or reorder providers.

---

## 🏗️ Architecture

```
uni-face/
├── uniface/              # Main Python Package
│   ├── api/              # FastAPI adapter (HTTP → Service)
│   ├── cli/              # CLI adapter (argparse → Service)
│   ├── core/             # Business logic layer & parallel pipeline
│   ├── modules/          # Deep learning models adapters
│   ├── api_server.py     # FastAPI Server
│   └── main.py           # CLI routing
├── webui/                # React 19 + Vite frontend
├── models/               # ONNX model files (not tracked in git)
├── uni-face.py           # Unified Entrypoint Script
├── uni-face.ini          # User configuration
└── run_uniface.bat       # One-click Windows launcher
```

### Processing Pipeline

```
Input (image / video)
  └─► Detect + Landmark + Recognize   (YOLOFace + 2DFAN4 + ArcFace)
        └─► Face Masking              (xseg_1 occluder + bisenet parser)
              └─► Face Swap           (inswapper / simswap / hyperswap)
                    └─► Face Enhance  (GFPGAN / GPEN / CodeFormer) [optional]
                          └─► Composite  (color match + blend)
                                └─► Output (image / video)
```

---

## 🤝 Contributing

Pull requests are welcome! Please open an issue first to discuss what you would like to change.

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/amazing-feature`
3. Commit your changes: `git commit -m 'feat: add amazing feature'`
4. Push to the branch: `git push origin feat/amazing-feature`
5. Open a Pull Request

---

## ⚖️ Licenses & Terms of Use

The models utilized by this project originate from various open-source projects and research papers. **Their use is strictly bound by the original licenses.**

### Non-commercial research only
The following models are based on or utilize components (e.g., InsightFace) that are restricted to **non-commercial, research, and educational purposes only**:
- `inswapper_128` / `inswapper_128_fp16`
- `simswap_256`
- `hyperswap` series
- `arcface` (`w600k_r50`)
- `gfpgan_1.4`
- `codeformer`
- `RestoreFormerPlusPlus`

### Permissive
- `yoloface_8n` (YOLO variants typically GNU/AGPL or Permissive depending on version)
- `bisenet_resnet_34` (Face parsing)

### Unresolved — no license located
- `xseg_1`
- `gpen_bfr` series

---

## ⚠️ Legal Disclaimer

**Responsibility of Use**: The creators and maintainers of this repository and the Uni-Face project assume absolutely no legal responsibility or liability for how this software and the associated models are used. 

By downloading and using this software, you agree to:
1. Comply with all local, state, and international laws.
2. Strictly adhere to the original licenses of the respective models (especially non-commercial clauses).
3. Never use this software for malicious, defamatory, or non-consensual purposes (e.g., deepfakes without consent).
4. Assume full legal and ethical responsibility for any outputs generated.

---

## 📄 License

This software codebase is licensed under the [MIT License](LICENSE). Note that this license applies **only to the code in this repository**, not to the weights or models downloaded separately.

---

<div align="center">
  Made with ⚡ for speed
</div>
