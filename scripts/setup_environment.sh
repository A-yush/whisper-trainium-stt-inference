#!/bin/bash
# Environment setup and verification script

set -e

echo "=========================================="
echo "Whisper Trainium Environment Setup"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on Trainium instance
echo "Step 1: Verifying Trainium Hardware..."
if neuron-ls &>/dev/null; then
    echo -e "${GREEN}✓${NC} NeuronCores detected"
    neuron-ls
else
    echo -e "${RED}✗${NC} NeuronCores not found. Are you running on a trn1 instance?"
    exit 1
fi
echo ""

# Check Neuron driver
echo "Step 2: Checking Neuron Driver..."
if lsmod | grep neuron &>/dev/null; then
    echo -e "${GREEN}✓${NC} Neuron kernel module loaded"
else
    echo -e "${RED}✗${NC} Neuron kernel module not loaded"
    exit 1
fi
echo ""

# Check Neuron device
echo "Step 3: Checking Neuron Device..."
if ls /dev/neuron* &>/dev/null; then
    echo -e "${GREEN}✓${NC} Neuron device accessible"
    ls -la /dev/neuron*
else
    echo -e "${RED}✗${NC} Neuron device not accessible"
    exit 1
fi
echo ""

# Check virtual environment
echo "Step 4: Checking Virtual Environment..."
VENV_PATH="/opt/aws_neuronx_venv_pytorch_2_9_nxd_inference"
if [ -d "$VENV_PATH" ]; then
    echo -e "${GREEN}✓${NC} Neuron virtual environment found"
    echo "  Path: $VENV_PATH"

    # Activate and check packages
    source "$VENV_PATH/bin/activate"

    echo ""
    echo "Step 5: Verifying Python Packages..."

    # Check PyTorch
    if python -c "import torch; print('PyTorch:', torch.__version__)" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} PyTorch installed"
    else
        echo -e "${RED}✗${NC} PyTorch not found"
        exit 1
    fi

    # Check torch-neuronx
    if python -c "import torch_neuronx; print('torch-neuronx:', torch_neuronx.__version__)" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} torch-neuronx installed"
    else
        echo -e "${RED}✗${NC} torch-neuronx not found"
        exit 1
    fi

    # Check neuronx-distributed-inference
    if python -c "import neuronx_distributed_inference as nxd; print('NxD Inference:', nxd.__version__)" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} neuronx-distributed-inference installed"
    else
        echo -e "${RED}✗${NC} neuronx-distributed-inference not found"
        exit 1
    fi

else
    echo -e "${RED}✗${NC} Neuron virtual environment not found at $VENV_PATH"
    exit 1
fi
echo ""

# Install additional dependencies
echo "Step 6: Installing Additional Dependencies..."
pip install -q soundfile jiwer openai-whisper 2>/dev/null || {
    echo -e "${YELLOW}⚠${NC} Some packages may already be installed"
}

# Verify additional packages
if python -c "import soundfile; import jiwer; import whisper" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} All dependencies installed"
else
    echo -e "${YELLOW}⚠${NC} Installing missing dependencies..."
    pip install soundfile jiwer openai-whisper
fi
echo ""

# Create necessary directories
echo "Step 7: Creating Directory Structure..."
mkdir -p models logs test_audio
echo -e "${GREEN}✓${NC} Directories created"
echo ""

# Summary
echo "=========================================="
echo "Environment Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Download model:    python src/download_model.py"
echo "  2. Compile model:     python src/compile_model.py"
echo "  3. Test inference:    python benchmarks/test_inference.py test_audio/sample.mp3"
echo ""
echo "For full instructions, see: docs/DEPLOYMENT_GUIDE.md"
echo ""
