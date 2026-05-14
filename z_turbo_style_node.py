import torch
import nodes

class ZImageTurboStyleTransfer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "vae": ("VAE",),
                "reference_image": ("IMAGE",),
                "positive_prompt": ("CONDITIONING",),
                "negative_prompt": ("CONDITIONING",),
                # 结构保留强度，建议配合 ControlNet 时拉到 1.0，单纯图生图建议 0.7-0.85
                "style_strength": ("FLOAT", {"default": 0.85, "min": 0.1, "max": 1.0, "step": 0.05}),
                "cfg": ("INT", {"default": 8, "min": 1, "max": 50, "step": 1}),
                "steps": ("INT", {"default": 8, "min": 1, "max": 12, "step": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                # 色彩匹配强度滑块
                "color_match_strength": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.05}),
            }
        }

    # 【修复 1】补全 ComfyUI 必需的节点属性，并清理了分类目录
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "process_style"
    CATEGORY = "Z-Turbo-Tools"

    def match_color_pytorch(self, target_img, ref_img, strength=1.0):
        """
        带有强度控制和基础防过暗保护的 PyTorch 色彩匹配
        """
        if strength == 0.0:
            return target_img

        ref_single = ref_img[0:1] 
        
        # 提取基因
        ref_mean = ref_single.mean(dim=(1, 2), keepdim=True)
        ref_std = ref_single.std(dim=(1, 2), keepdim=True) + 1e-5
        
        target_mean = target_img.mean(dim=(1, 2), keepdim=True)
        target_std = target_img.std(dim=(1, 2), keepdim=True) + 1e-5
        
        # 核心劫持计算
        matched_img = (target_img - target_mean) / target_std * ref_std + ref_mean
        
        # 线性混合 (Linear Blending)
        blended_img = target_img * (1.0 - strength) + matched_img * strength
        
        # 柔性溢出处理
        return torch.clamp(blended_img, 0.0, 1.0)

    # 【修复 2】将接收参数改为 color_match_strength
    def process_style(self, model, vae, reference_image, positive_prompt, negative_prompt, style_strength, cfg, steps, seed, color_match_strength):
        # 1. 尺寸安全限制
        batch_size, height, width, channels = reference_image.shape
        if height >= 4096 or width >= 4096:
            raise ValueError("安全拦截：画布尺寸过大 (≥4096px)。")

        # 2. VAE 编码
        encoded_latent = nodes.VAEEncode().encode(vae, reference_image)[0]

        # 3. KSampler 采样
        sampler = nodes.KSampler()
        sampled_latent = sampler.sample(
            model=model,
            seed=seed,
            steps=steps,
            cfg=cfg,
            sampler_name="res_multistep",
            scheduler="simple",
            positive=positive_prompt,
            negative=negative_prompt,
            latent_image=encoded_latent,
            denoise=style_strength
        )[0]

        # 4. VAE 解码，获得未经色彩修正的基础生成图
        decoded_image = nodes.VAEDecode().decode(vae, sampled_latent)[0]

        # 5. 【修复 3】终极杀招：带有强度的强制色彩劫持，并清理了控制台打印
        if color_match_strength > 0.0:
            print(f"[Z-Turbo Plugin] 正在执行色彩匹配 (强度: {color_match_strength})...")
            final_image = self.match_color_pytorch(decoded_image, reference_image, strength=color_match_strength)
        else:
            final_image = decoded_image

        return (final_image,)
