/**
 * Single Source of Truth (SSOT) for Model Options, Execution Providers, and Mask Configurations.
 */

export interface ModelOption {
  id: string;
  label: string;
  description?: string;
}

export const SWAP_MODELS: ModelOption[] = [
  { id: 'inswapper_128', label: 'inswapper_128', description: 'Standard 128x128 Face Swap (Fast & Stable)' },
  { id: 'inswapper_128_fp16', label: 'inswapper_128_fp16', description: 'Half-precision 128x128 (Lower VRAM)' },
  { id: 'hyperswap_1b_256', label: 'hyperswap_1b_256', description: 'HyperSwap 256x256 (High Quality)' },
  { id: 'hyperswap_1c_256', label: 'hyperswap_1c_256', description: 'HyperSwap 256x256 Alternate' },
];

export const RESTORE_MODELS: ModelOption[] = [
  { id: 'gfpgan_1.4', label: 'gfpgan_1.4', description: 'GFPGAN 1.4 Face Restoration' },
  { id: 'codeformer', label: 'codeformer', description: 'CodeFormer High-fidelity Face Restorer' },
  { id: 'gpen_bfr_256', label: 'gpen_bfr_256', description: 'GPEN 256px Face Enhancement' },
  { id: 'gpen_bfr_512', label: 'gpen_bfr_512', description: 'GPEN 512px Face Enhancement' },
  { id: 'gpen_bfr_1024', label: 'gpen_bfr_1024', description: 'GPEN 1024px Ultra High-Def' },
  { id: 'restoreformer_plus_plus', label: 'restoreformer_plus_plus', description: 'RestoreFormer++' },
];

export const EXECUTION_PROVIDERS: ModelOption[] = [
  { id: 'cpu', label: 'CPU (Slow)' },
  { id: 'cuda', label: 'CUDA (Nvidia GPU)' },
  { id: 'trt', label: 'TensorRT (Fastest)' },
];

export const MASK_TYPES: ModelOption[] = [
  { id: 'box', label: 'Box (Default)' },
  { id: 'occlusion', label: 'Occlusion (Hands, Hair)' },
  { id: 'region', label: 'Face Region Only' },
  { id: 'eyes', label: 'Priority Eyes (Force)' },
];

export const OCCLUSION_MODELS: ModelOption[] = [
  { id: 'xseg_1', label: 'xseg_1 (General Occlusion)', description: 'Standard balanced mask for hands, hair, and general objects' },
  { id: 'xseg_2', label: 'xseg_2 (Fine Hair & Details)', description: 'Enhanced mask for fine strands of hair and edge details' },
  { id: 'xseg_3', label: 'xseg_3 (Robust Foreground Objects)', description: 'Aggressive mask for microphones, hands, and large occlusions' },
];

export const MASK_REGIONS: ModelOption[] = [
  { id: 'skin', label: 'Skin' },
  { id: 'l_brow', label: 'Left Brow' },
  { id: 'r_brow', label: 'Right Brow' },
  { id: 'l_eye', label: 'Left Eye' },
  { id: 'r_eye', label: 'Right Eye' },
  { id: 'nose', label: 'Nose' },
  { id: 'mouth', label: 'Mouth' },
  { id: 'u_lip', label: 'Upper Lip' },
  { id: 'l_lip', label: 'Lower Lip' },
];

export const PREVIEW_RESOLUTIONS: ModelOption[] = [
  { id: '320', label: '320p (Fastest)' },
  { id: '480', label: '480p' },
  { id: '720', label: '720p (High Quality)' },
];

export const TARGET_GENDERS: ModelOption[] = [
  { id: 'all', label: 'Any (Male & Female)' },
  { id: 'female', label: 'Female Only' },
  { id: 'male', label: 'Male Only' },
];

export const FACE_ORDERS: ModelOption[] = [
  { id: 'largest', label: 'Largest Face (Default)' },
  { id: 'smallest', label: 'Smallest Face' },
  { id: 'highest_score', label: 'Highest Confidence' },
  { id: 'left_to_right', label: 'Left to Right' },
  { id: 'right_to_left', label: 'Right to Left' },
  { id: 'top_to_bottom', label: 'Top to Bottom' },
  { id: 'bottom_to_top', label: 'Bottom to Top' },
];

export const GALLERY_RESOLUTIONS: ModelOption[] = [
  { id: '256', label: '256p (Fastest)' },
  { id: '384', label: '384p (Balanced)' },
  { id: '512', label: '512p (High Quality)' },
  { id: '720', label: '720p (Max Quality)' },
];

