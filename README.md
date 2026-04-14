# intent-to-twin
intent-to-twin

python -m venv venv

source venv/bin/activate


python -m pipeline.main --config configs/base.yaml


pip install -r requirements.txt

pip install spacy
python -m spacy download en_core_web_sm

pip install transformers accelerate huggingface_hub
hf auth login

pip install diffusers transformers accelerate safetensors opencv-python open3d
pip install open3d --ignore-installed --no-deps
pip install --ignore-installed blinker Flask dash
pip install scikit-learn
pip install pandas