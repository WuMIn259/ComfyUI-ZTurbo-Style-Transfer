ComfyUI-ZTurbo-Style-Transfer
这是一个专为 z-image-turbo设计的极速风格与色彩迁移一体化插件。

由于 z-image-turbo 等高度蒸馏的模型对文本提示词（Prompt）具有极高的服从性，传统的图生图往往无法有效保留参考图的色彩氛围。本插件通过底层 PyTorch 张量计算实现了一种“色彩基因劫持”机制，能够强行将参考图的色调迁移至新生成的图像中，同时保持构图的自由度。

✨ 核心特性
强制色彩基因匹配 (Color Match Plus)：

内置改进型 AdaIN（自适应实例归一化）算法，直接在像素空间提取参考图的均值与方差。

无视提示词干扰：即便提示词中包含与参考图冲突的颜色描述，插件也能在输出端强制纠正色调。

色彩劫持强度控制 (Strength Control)：

支持 0.0 - 1.0 的平滑混合。

亮度保护机制：有效防止在 Denoise = 1.0 或高强度匹配时出现的画面死黑或过暗现象。

极简一体化流程：

将 VAE 编解码与针对 Turbo 模型优化的采样参数（res_multistep + simple）高度封装。

内置尺寸安全检查，自动拦截 ≥4096px 的输入，保护显存。

零外部依赖：

完全基于原生 PyTorch 实现，不依赖 OpenCV 或 scikit-image，环境极简，即插即用。

📦 安装方法
进入 ComfyUI 的插件目录：

Bash
cd ComfyUI/custom_nodes/
克隆本仓库：

Bash
git clone https://github.com/你的用户名/ComfyUI-ZTurbo-Style-Transfer.git
重启 ComfyUI 即可使用。

🚀 节点说明
在 ComfyUI 中右键搜索 Z-Turbo Style Transfer 即可找到该节点。

输入参数：
style_strength (Denoise)：控制画面结构的保留程度。

0.7 - 0.85：保留原图构图并修改材质/风格。

1.0：配合 ControlNet 使用，实现完全的新构图。

color_match_strength：色彩迁移的权重。

推荐值 0.8：在保持参考图高级色调的同时，保留新图的明暗细节。

1.0：极致的色彩覆盖。

💡 最佳实践
想要“全新构图 + 参考图色调”？

准备一张你想要的构图参考图（线稿或深度图）。

连接 ControlNet (Union/Depth) 到 Z-Turbo Style Transfer 的模型输入。

将 style_strength 设为 1.0。

将本插件的 color_match_strength 设为 0.85。

结果：你将获得一个由 ControlNet 控制构图、由 Prompt 描述内容、但视觉色调完全继承自参考图的神奇效果。

🛠 开发初衷
在 DiT 架构模型（如 SD3, Flux, Z-Image）中，风格迁移一直是难点。本项目旨在通过一种霸道但高效的“数学染色”方案，在不需要训练专属 IP-Adapter 的情况下，赋予用户对极速模型最直观的色彩控制权。