# ComfyUI-ZTurbo-Style-Transfer
ComfyUI-ZTurbo-Style-Transfer 这是一个专为 z-image-turbo设计的极速风格与色彩迁移一体化插件。  由于 z-image-turbo 等高度蒸馏的模型对文本提示词（Prompt）具有极高的服从性，传统的图生图往往无法有效保留参考图的色彩氛围。本插件通过底层 PyTorch 张量计算实现了一种“色彩基因劫持”机制，能够强行将参考图的色调迁移至新生成的图像中，同时保持构图的自由度。
