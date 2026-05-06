# NeuTTS

HuggingFace 🤗:

- NeuTTS-Air (English): [Model](https://huggingface.co/neuphonic/neutts-air), [Q8 GGUF](https://huggingface.co/neuphonic/neutts-air-q8-gguf), [Q4 GGUF](https://huggingface.co/neuphonic/neutts-air-q4-gguf), [Space](https://huggingface.co/spaces/neuphonic/neutts-air)

- NeuTTS-Nano Multilingual Collection:
   - NeuTTS-Nano (English): [Model](https://huggingface.co/neuphonic/neutts-nano), [Q8 GGUF](https://huggingface.co/neuphonic/neutts-nano-q8-gguf), [Q4 GGUF](https://huggingface.co/neuphonic/neutts-nano-q4-gguf)
   - NeuTTS-Nano-French: [Model](https://huggingface.co/neuphonic/neutts-nano-french), [Q8 GGUF](https://huggingface.co/neuphonic/neutts-nano-french-q8-gguf), [Q4 GGUF](https://huggingface.co/neuphonic/neutts-nano-french-q4-gguf)
   - NeuTTS-Nano-German: [Model](https://huggingface.co/neuphonic/neutts-nano-german), [Q8 GGUF](https://huggingface.co/neuphonic/neutts-nano-german-q8-gguf), [Q4 GGUF](https://huggingface.co/neuphonic/neutts-nano-german-q4-gguf)
   - NeuTTS-Nano-Spanish: [Model](https://huggingface.co/neuphonic/neutts-nano-spanish), [Q8 GGUF](https://huggingface.co/neuphonic/neutts-nano-spanish-q8-gguf), [Q4 GGUF](https://huggingface.co/neuphonic/neutts-nano-spanish-q4-gguf)
   - [Multilingual Space](https://huggingface.co/spaces/neuphonic/neutts-nano-multilingual-collection)

[NeuTTS-Nano Demo Video](https://github.com/user-attachments/assets/629ec5b2-4818-4fa6-987a-99fcbadc56bc)

_Created by [Neuphonic](http://neuphonic.com/) - building faster, smaller, on-device voice AI_

State-of-the-art Voice AI has been locked behind web APIs for too long. NeuTTS is a collection of open source, on-device, TTS speech language models with instant voice cloning. Built off of LLM backbones, NeuTTS brings natural-sounding speech, real-time performance, built-in security and speaker cloning to your local device - unlocking a new category of embedded voice agents, assistants, toys, and compliance-safe apps.

## Key Features

- 🗣Best-in-class realism for their size - produce natural, ultra-realistic voices that sound human, at the sweet spot between speed, size, and quality for real-world applications
- 📱Optimised for on-device deployment - quantisations provided in GGUF format, ready to run on phones, laptops, or even Raspberry Pis
- 👫Instant voice cloning - create your own speaker with as little as 3 seconds of audio
- 🚄Simple LM + codec architecture - making development and deployment simple

> [!CAUTION]
> Websites like neutts.com are popping up and they're not affliated with Neuphonic, our github or this repo.
>
> We are on neuphonic.com only. Please be careful out there! 🙏

> [!NOTE]
> **Personal fork** — I'm using this primarily with NeuTTS-Nano (English) on a Raspberry Pi 5. My notes and experiments are in the `experiments/` directory.

## Model Details

NeuTTS models are built from small LLM backbones - lightweight yet capable language models optimised for text understanding and generation - as well as a powerful combination of technologies designed for efficiency and quality:

- **Supported Languages**: English, Spanish, German, French (model-dependent)
- **Audio Codec**: [Ne
